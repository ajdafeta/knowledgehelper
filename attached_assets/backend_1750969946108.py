# backend.py - Enhanced for Enterprise Technical Success Manager Demo
import anthropic
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import json
import hashlib
from typing import Dict, List, Tuple
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class EnterpriseKnowledgeBot:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.usage_tracker = UsageTracker()
        self.optimization_engine = OptimizationEngine()
        self.document_index = None
        self.document_chunks = None

    def set_document_store(self, index, chunks):
        """Set the document index and chunks for retrieval"""
        self.document_index = index
        self.document_chunks = chunks

    def retrieve_documents(self, query: str, top_k: int = 3) -> List[str]:
        """Retrieve relevant documents based on query"""
        if self.document_index is None or self.document_chunks is None:
            return ["No documents available. Please ensure the knowledge base is loaded."]

        try:
            # Encode the query
            query_embedding = self.model.encode([query]).astype('float32')

            # Search for similar documents
            scores, indices = self.document_index.search(query_embedding, top_k)

            # Return the relevant document chunks
            relevant_docs = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.document_chunks):
                    relevant_docs.append(self.document_chunks[idx][0])  # Get the text chunk

            return relevant_docs if relevant_docs else ["No relevant documents found."]

        except Exception as e:
            return [f"Error retrieving documents: {str(e)}"]

    def process_query(self, query: str, user_id: str, department: str) -> Dict:
        """Process user query with full tracking and optimization"""
        start_time = datetime.now()

        # Retrieve relevant documents
        relevant_docs = self.retrieve_documents(query)

        # Generate response with Claude
        response = self._generate_response(query, relevant_docs)

        # Track usage metrics
        processing_time = (datetime.now() - start_time).total_seconds()
        self.usage_tracker.log_interaction(
            user_id=user_id,
            department=department,
            query=query,
            response_length=len(response),
            processing_time=processing_time,
            documents_retrieved=len(relevant_docs)
        )

        # Get optimization recommendations
        optimization_tips = self.optimization_engine.get_recommendations(
            query, response, processing_time
        )

        return {
            'response': response,
            'sources': relevant_docs,
            'processing_time': processing_time,
            'optimization_tips': optimization_tips
        }

    def _generate_response(self, query: str, context_docs: List[str]) -> str:
        """Generate response using Claude with enterprise-focused prompting"""
        context = "\n\n".join([f"Document {i + 1}: {doc}" for i, doc in enumerate(context_docs)])

        prompt = f"""You are an internal company assistant helping employees find information quickly and accurately.

Context from company documents:
{context}

Employee question: {query}

Provide a helpful, accurate response based on the company documents. If the information isn't available in the documents, clearly state that and suggest who they might contact instead.

Keep responses concise but complete, and include relevant policy numbers or document references when applicable."""

        try:
            response = self.client.messages.create(
                model="claude-4-sonnet-20250514",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"I apologize, but I encountered an error processing your request. Please try again or contact IT support. Error: {str(e)}"


class UsageTracker:
    """Track usage patterns for optimization and business insights"""

    def __init__(self):
        self.interactions = []

    def log_interaction(self, user_id: str, department: str, query: str,
                        response_length: int, processing_time: float, documents_retrieved: int):
        """Log individual interaction for analysis"""
        interaction = {
            'timestamp': datetime.now(),
            'user_id': hashlib.md5(user_id.encode()).hexdigest()[:8],  # Anonymized
            'department': department,
            'query_hash': hashlib.md5(query.encode()).hexdigest()[:8],
            'query_length': len(query),
            'response_length': response_length,
            'processing_time': processing_time,
            'documents_retrieved': documents_retrieved,
            'query_type': self._classify_query(query)
        }
        self.interactions.append(interaction)

    def _classify_query(self, query: str) -> str:
        """Classify query type for better analytics"""
        query_lower = query.lower()
        if any(word in query_lower for word in ['pto', 'vacation', 'time off']):
            return 'Time Off'
        elif any(word in query_lower for word in ['benefits', 'health', 'insurance']):
            return 'Benefits'
        elif any(word in query_lower for word in ['policy', 'procedure', 'rules']):
            return 'Policy'
        elif any(word in query_lower for word in ['org', 'team', 'manager', 'contact']):
            return 'Organizational'
        else:
            return 'General'

    def get_usage_analytics(self) -> Dict:
        """Generate comprehensive usage analytics"""
        if not self.interactions:
            return {'error': 'No interactions logged yet'}

        df = pd.DataFrame(self.interactions)

        return {
            'total_interactions': len(df),
            'unique_users': df['user_id'].nunique(),
            'avg_processing_time': df['processing_time'].mean(),
            'most_active_department': df['department'].value_counts().index[0],
            'query_type_distribution': df['query_type'].value_counts().to_dict(),
            'daily_usage_trend': df.set_index('timestamp').resample('D').size().tail(7).to_dict(),
            'performance_metrics': {
                'avg_response_length': df['response_length'].mean(),
                'avg_documents_retrieved': df['documents_retrieved'].mean(),
                'queries_per_user': len(df) / df['user_id'].nunique() if df['user_id'].nunique() > 0 else 0
            }
        }


class OptimizationEngine:
    """Provide real-time optimization recommendations"""

    def get_recommendations(self, query: str, response: str, processing_time: float) -> List[str]:
        """Generate optimization recommendations based on interaction"""
        recommendations = []

        # Performance optimization
        if processing_time > 3.0:
            recommendations.append("⚡ Consider caching frequently asked questions to improve response times")

        # Query optimization
        if len(query.split()) < 3:
            recommendations.append("💡 More specific queries often yield better results")

        # Usage pattern optimization
        recommendations.append("📊 This query type could benefit from a dedicated FAQ section")

        return recommendations


# Document processing utilities
class DocumentProcessor:
    """Handle document ingestion and vector store creation"""

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def process_documents(self, document_paths: List[str]) -> faiss.IndexFlatIP:
        """Process documents and create FAISS index"""
        all_chunks = []

        for path in document_paths:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                chunks = self._chunk_document(content)
                all_chunks.extend([(chunk, path) for chunk in chunks])

        # Create embeddings
        texts = [chunk[0] for chunk in all_chunks]
        embeddings = self.model.encode(texts)

        # Create FAISS index
        index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings.astype('float32'))

        return index, all_chunks

    def _chunk_document(self, content: str, chunk_size: int = 500) -> List[str]:
        """Split document into manageable chunks"""
        words = content.split()
        chunks = []

        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)

        return chunks
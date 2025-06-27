# app.py - Enterprise Internal Support Chatbot with Reference Linking
import os
import json
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session
from backend import EnterpriseKnowledgeBot, DocumentProcessor
from document_processor import DynamicDocumentProcessor
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'enterprise-chatbot-secret-key')

# Global variables
bot = None
document_processor = None
dynamic_doc_processor = None
documents_processed = False
document_index = None
document_chunks = None

def initialize_bot():
    """Initialize the chatbot with API key"""
    global bot
    
    # Try to get API key from environment
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key:
        logger.error("ANTHROPIC_API_KEY not found in environment variables")
        return False
    
    try:
        bot = EnterpriseKnowledgeBot(api_key)
        logger.info("Bot initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize bot: {e}")
        return False

def process_documents():
    """Process and index company documents using dynamic processor"""
    global documents_processed, document_index, document_chunks, document_processor, dynamic_doc_processor
    
    if documents_processed:
        return True
    
    try:
        logger.info("Processing company documents...")
        
        # Ensure documents directory exists
        os.makedirs("documents", exist_ok=True)
        create_sample_documents()
        
        # Create document processors
        document_processor = DocumentProcessor()
        dynamic_doc_processor = DynamicDocumentProcessor()
        
        # Get all supported documents from documents folder
        document_files = dynamic_doc_processor.scan_documents_folder()
        
        if document_files:
            # Convert to list of file paths for the processor
            document_paths = list(document_files.values())
            
            # Process documents and create index
            index, chunks = document_processor.process_documents(document_paths)
            document_index = index
            document_chunks = chunks
            documents_processed = True
            
            # Set document store in bot
            if bot:
                bot.set_document_store(index, chunks)
            
            logger.info(f"Successfully processed {len(document_paths)} documents")
            return True
        else:
            logger.error("No documents available for processing")
            return False
        
    except Exception as e:
        logger.error(f"Error processing documents: {e}")
        return False

def create_sample_documents():
    """Create sample company documents"""
    documents = {
        "documents/sample_pto_policy.txt": """PTO Policy - Document #HR-001

Paid Time Off (PTO) Allocation:
- Full-time employees: 20 days annually
- Part-time employees: Pro-rated based on hours worked
- PTO accrues monthly at 1.67 days per month

PTO Request Process:
1. Submit request through HR portal at least 2 weeks in advance
2. Manager approval required for requests over 5 consecutive days
3. Blackout periods apply during Q4 for Finance and Sales teams

Contact Information:
For questions about PTO policies, contact hr@company.com
Phone: (555) 123-4567

Additional Benefits:
- Unused PTO can be carried over up to 5 days
- PTO can be taken in half-day increments
- Emergency PTO requests are considered on case-by-case basis""",

        "documents/sample_health_benefits.txt": """Health Benefits Overview - Document #HR-002

Medical Insurance Plans:
- Premium Plan: 100% company-paid for employee, 80% for family
- Standard Plan: 90% company-paid for employee, 70% for family
- Basic Plan: 80% company-paid for employee, 60% for family

Deductibles and Coverage:
- Premium Plan: $500 deductible, $10 copay
- Standard Plan: $1,500 deductible, $25 copay
- Basic Plan: $2,500 deductible, $40 copay

Additional Benefits:
- Dental and Vision included in all plans
- $1,000 annual wellness reimbursement
- Mental health coverage with $0 copay
- Prescription drug coverage included

Enrollment Information:
- Open enrollment occurs every November
- New employees have 30 days to enroll
- Contact benefits@company.com for assistance
- Benefits hotline: (555) 987-6543""",

        "documents/sample_org_structure.txt": """Organizational Structure - Document #ORG-001

Executive Team:
- Chief Executive Officer: Sarah Johnson (sarah.johnson@company.com)
- Chief Technology Officer: Mike Chen (mike.chen@company.com)
- Vice President of Sales: Lisa Rodriguez (lisa.rodriguez@company.com)
- Chief Financial Officer: Robert Smith (robert.smith@company.com)

Department Heads:
- Engineering Manager: David Kim (david.kim@company.com)
- Human Resources Director: Jennifer Liu (jennifer.liu@company.com)
- Marketing Director: Amanda Brown (amanda.brown@company.com)
- Operations Manager: Carlos Martinez (carlos.martinez@company.com)

Support Contacts:
- IT Support: it-help@company.com
- HR General Inquiries: hr@company.com
- Facilities: facilities@company.com
- Security: security@company.com

Office Locations:
- Headquarters: 123 Business Ave, Suite 500, San Francisco, CA 94105
- Remote employees: See internal directory for contact information""",

        "documents/claude_usage_policy.txt": """Claude AI Usage Policy - Document #IT-003

Approved Use Cases:
- Internal support and documentation queries
- Code review and technical assistance
- Meeting notes and summary generation
- Employee onboarding support

Security Guidelines:
- Do not share confidential customer data
- No proprietary code or trade secrets
- Employee personal information must be anonymized
- All interactions are logged for compliance

Best Practices:
- Be specific in your queries for better results
- Verify important information with human experts
- Use Claude for assistance, not final decision making
- Report any inappropriate responses to IT

Data Handling:
- No sensitive financial data should be processed
- Customer information requires approval from legal team
- All Claude interactions are subject to audit
- Data retention follows company policy

Contact Information:
- IT Support for technical issues: it-help@company.com
- Legal questions: legal@company.com
- Privacy concerns: privacy@company.com"""
    }
    
    for path, content in documents.items():
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

@app.route('/')
def index():
    """Main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests with conversation history support"""
    if not bot:
        return jsonify({'error': 'Bot not initialized. Please check API key configuration.'}), 500
    
    data = request.json
    query = data.get('query', '').strip()
    user_id = data.get('user_id', 'anonymous')
    department = data.get('department', 'General')
    conversation_history = data.get('conversation_history', [])
    
    if not query:
        return jsonify({'error': 'Query cannot be empty'}), 400
    
    try:
        # Process the query with conversation history
        result = bot.process_query(query, user_id, department)
        
        # Add document references with highlighting info
        enhanced_sources = []
        for i, source in enumerate(result['sources']):
            if isinstance(source, str) and not source.startswith('Error') and not source.startswith('No'):
                # Find which document this source came from
                doc_info = find_document_source(source)
                enhanced_sources.append({
                    'text': source,
                    'document': doc_info['document'],
                    'highlight_text': source[:100] + '...' if len(source) > 100 else source
                })
        
        result['sources'] = enhanced_sources
        
        # Store conversation in session for persistence
        if 'chat_history' not in session:
            session['chat_history'] = []
        
        session['chat_history'].append({
            'type': 'user',
            'content': query,
            'timestamp': datetime.now().isoformat(),
            'department': department
        })
        
        session['chat_history'].append({
            'type': 'bot',
            'content': result['response'],
            'timestamp': datetime.now().isoformat(),
            'sources': enhanced_sources
        })
        
        # Keep only last 20 messages
        if len(session['chat_history']) > 20:
            session['chat_history'] = session['chat_history'][-20:]
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing chat query: {e}")
        return jsonify({'error': f'Error processing query: {str(e)}'}), 500

def find_document_source(source_text):
    """Find which document a source text came from"""
    global document_chunks
    
    if not document_chunks:
        return {'document': 'unknown', 'path': None}
    
    # Find the chunk that matches this source
    for chunk_text, doc_path in document_chunks:
        if source_text.strip() in chunk_text:
            doc_name = os.path.basename(doc_path).replace('.txt', '')
            return {'document': doc_name, 'path': doc_path}
    
    return {'document': 'unknown', 'path': None}

@app.route('/api/analytics')
def analytics():
    """Get usage analytics"""
    if not bot:
        return jsonify({'error': 'Bot not initialized'}), 500
    
    try:
        analytics_data = bot.usage_tracker.get_usage_analytics()
        return jsonify(analytics_data)
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        return jsonify({'error': f'Error getting analytics: {str(e)}'}), 500

@app.route('/api/conversation_history')
def get_conversation_history():
    """Get conversation history from session"""
    return jsonify(session.get('chat_history', []))

@app.route('/api/reset_chat', methods=['POST'])
def reset_chat_history():
    """Reset chat history"""
    session['chat_history'] = []
    return jsonify({'success': True, 'message': 'Chat history reset'})

@app.route('/api/documents')
def get_documents():
    """Get list of available documents"""
    global dynamic_doc_processor
    
    if not dynamic_doc_processor:
        dynamic_doc_processor = DynamicDocumentProcessor()
    
    try:
        document_files = dynamic_doc_processor.scan_documents_folder()
        documents_info = []
        
        for doc_name, file_path in document_files.items():
            doc_info = dynamic_doc_processor.get_document_info(file_path)
            documents_info.append({
                'name': doc_name,
                'display_name': doc_name.replace('_', ' ').title(),
                'type': doc_info['type'],
                'size': doc_info['size_kb'],
                'modified': doc_info['modified'],
                'path': file_path
            })
        
        return jsonify(documents_info)
    except Exception as e:
        logger.error(f"Error getting documents: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/document/<document_name>')
def view_document(document_name):
    """View document with highlighting capability using dynamic processor"""
    global dynamic_doc_processor
    
    if not dynamic_doc_processor:
        dynamic_doc_processor = DynamicDocumentProcessor()
    
    try:
        document_files = dynamic_doc_processor.scan_documents_folder()
        
        if document_name not in document_files:
            return "Document not found", 404
        
        file_path = document_files[document_name]
        content = dynamic_doc_processor.extract_text_from_file(file_path)
        doc_info = dynamic_doc_processor.get_document_info(file_path)
        
        highlight_text = request.args.get('highlight', '')
        
        return render_template('document_viewer.html', 
                             document_name=document_name,
                             content=content,
                             highlight_text=highlight_text)
    except Exception as e:
        logger.error(f"Error viewing document: {e}")
        return f"Error loading document: {str(e)}", 500

@app.route('/api/reset-chat', methods=['POST'])
def reset_chat():
    """Reset chat history"""
    if bot:
        # Clear the usage tracker's interactions
        bot.usage_tracker.interactions.clear()
        return jsonify({'success': True, 'message': 'Chat history cleared'})
    return jsonify({'error': 'Bot not initialized'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'bot_initialized': bot is not None,
        'documents_processed': documents_processed,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Initialize the bot and process documents
    if initialize_bot():
        process_documents()
        logger.info("Application starting on port 5000")
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        logger.error("Failed to initialize application")

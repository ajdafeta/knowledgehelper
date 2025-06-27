# Enterprise Support Assistant

## Overview

This is an Enterprise Internal Support Chatbot built with Python, designed to help employees find information about company policies, benefits, procedures, and other internal documentation. The application features both a Flask web interface and a Streamlit interface, with AI-powered document retrieval and response generation using Anthropic's Claude API.

## System Architecture

The application follows a modular architecture with clear separation between the frontend interfaces, backend logic, and document processing components:

### Frontend Architecture
- **HTML Interface**: Professional Bootstrap-based web interface with enterprise styling
- **Responsive Design**: Mobile-friendly design with clean, intuitive layout
- **Real-time Chat Interface**: Interactive chat interface with conversation memory and message history
- **Document Viewer**: Integrated document viewing with highlighting in new browser tabs

### Backend Architecture
- **Simple HTTP Server**: Uses Python's built-in HTTP server - no external web framework dependencies
- **AI-Powered Query Processing**: Uses Anthropic Claude API (claude-sonnet-4-20250514) for natural language understanding
- **Enhanced Document Retrieval**: Intelligent keyword matching with strict relevance filtering for accurate source attribution
- **User Authentication**: File-based authentication system with session management and role-based access control
- **Session Management**: Maintains conversation history and user sessions with secure cookie-based authentication

## Key Components

### Core Classes
1. **EnterpriseKnowledgeBot**: Main bot class handling AI interactions and document retrieval
2. **DocumentProcessor**: Handles document ingestion, chunking, and indexing
3. **UsageTracker**: Monitors API usage, response times, and user interactions
4. **OptimizationEngine**: Provides performance insights and optimization recommendations

### Document Management
- **Knowledge Base**: Text-based document storage in `/documents/` directory - ONLY existing files
- **No Document Generation**: System reads only pre-existing documents, never creates sample content
- **Dynamic Document Processing**: Automatically scans and loads all document formats in documents folder
- **Source Attribution**: Links responses back to source documents with highlighting

### User Interface Components
- **Chat Interface**: Real-time messaging with user/bot message distinction
- **Analytics Dashboard**: Performance metrics and usage statistics
- **Settings Panel**: User profile configuration (Employee ID, Department)
- **Document Viewer**: Integrated document display with search highlighting

## Data Flow

1. **Query Processing**:
   - User submits query through web interface
   - Query is processed and embedded using sentence transformers
   - Similar documents are retrieved using FAISS vector search
   - Retrieved documents are used as context for Claude API

2. **Response Generation**:
   - Claude API generates response based on query and retrieved documents
   - Response includes source attribution and confidence indicators
   - Usage metrics are tracked and stored

3. **Document Processing**:
   - Documents are loaded from `/documents/` directory
   - Text is chunked and embedded using sentence transformers
   - Embeddings are indexed using FAISS for efficient retrieval

## External Dependencies

### Core AI Services
- **Anthropic Claude API**: Primary language model for query understanding and response generation
- **Sentence Transformers**: Local embedding model for document vectorization
- **FAISS**: Vector similarity search library

### Web Framework Dependencies
- **Flask**: Traditional web application framework
- **Streamlit**: Data science web application framework
- **Bootstrap 5**: Frontend CSS framework for responsive design

### Python Libraries
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing for vector operations
- **plotly**: Interactive visualization for analytics dashboard

## Deployment Strategy

### Replit Configuration
- **Python 3.11 Runtime**: Uses modern Python version with enhanced performance
- **Autoscale Deployment**: Configured for automatic scaling based on demand
- **Multi-Port Support**: Supports both Flask (port 5000) and Streamlit interfaces
- **Environment Variables**: Secure API key management through environment configuration

### Development Workflow
- **Parallel Execution**: Supports running both Flask and Streamlit interfaces simultaneously
- **Hot Reload**: Development server with automatic reloading for code changes
- **Asset Management**: Separate directories for templates, static files, and documents

### Security Considerations
- **API Key Protection**: Anthropic API key stored securely in environment variables
- **Data Privacy**: Built-in guidelines for handling sensitive employee information
- **Audit Logging**: All interactions logged for compliance and monitoring

## Changelog

- June 26, 2025: Initial setup with Streamlit interface
- June 26, 2025: Migrated to HTML frontend with Python HTTP server backend
- June 26, 2025: Implemented conversational memory and document highlighting 
- June 26, 2025: Removed all document generation code - system now only uses existing files
- June 27, 2025: Added user authentication system with login/logout and session management
- June 27, 2025: Integrated document relevance intelligence to only show truly relevant sources
- June 27, 2025: Employee ID and department now automatically populated from authenticated user database
- June 27, 2025: Fixed authentication cookie handling - switched to traditional HTML form submission for reliable login flow

## User Preferences

Preferred communication style: Simple, everyday language.
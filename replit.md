# Enterprise Support Assistant

## Overview

This is an Enterprise Internal Support Chatbot built with Python, designed to help employees find information about company policies, benefits, procedures, and other internal documentation. The application features a clean HTML web interface with Python HTTP server backend, providing AI-powered document retrieval and response generation using Anthropic's Claude API.

## System Architecture

The application follows a modular architecture with clear separation between the frontend interfaces, backend logic, and document processing components:

### Current Architecture

**Frontend:**
- Clean HTML interface with Bootstrap 5 styling
- Responsive design optimized for desktop and mobile
- Real-time chat interface with conversation history
- Document viewer with search highlighting in new tabs
- Professional enterprise styling with company branding

**Backend:**
- Python HTTP server (no external web framework dependencies)
- File-based authentication with secure session management
- Role-based access control (admin/employee roles)
- Dynamic document processing from `/documents/` folder
- Intelligent document relevance filtering

**AI Integration:**
- Anthropic Claude API (claude-sonnet-4-20250514) for natural language processing
- Complete document access - Claude receives full content for comprehensive answers
- Conversational memory with context awareness
- Enhanced prompting for enterprise support scenarios

## Current File Structure

**Core Application Files:**
- `web_app.py` - Main HTTP application server and request handling
- `simple_auth.py` - File-based authentication system with session management
- `document_processor.py` - Dynamic document processing for multiple file formats
- `user_data.json` - Employee database with authentication credentials

**Frontend Assets:**
- `templates/index.html` - Main chat interface template
- `templates/document_viewer.html` - Document display template
- `static/css/style.css` - Application styling and responsive design
- `static/js/main.js` - Client-side JavaScript for chat functionality

**Company Documents:**
- `documents/Employee_Handbook.txt` - Company policies and procedures
- `documents/IT_Security_Policy.txt` - IT security guidelines and requirements
- `documents/claude_usage_policy.txt` - AI usage policies and guidelines

**Key Features:**
- **Authentication**: Secure login/logout with session cookies and role-based access
- **Document Processing**: Dynamic scanning and text extraction from documents folder
- **AI Integration**: Complete document content provided to Claude for comprehensive answers
- **Conversation Memory**: Maintains chat history and context across user sessions
- **Admin Dashboard**: Usage analytics and employee management for admin users

## How It Works

1. **User Authentication**:
   - Employee logs in with username/password
   - System validates credentials against `user_data.json`
   - Secure session created with HTTP-only cookies
   - User role determines access level (admin vs employee)

2. **Document Processing**:
   - System scans `/documents/` folder for supported file types
   - Documents are dynamically loaded and text extracted
   - No preprocessing or indexing - documents read on demand

3. **Query Processing**:
   - User submits question through chat interface
   - System intelligently matches query to relevant documents using keyword analysis
   - Complete document content provided to Claude (not excerpts)
   - Claude generates comprehensive response with full document context

4. **Response Generation**:
   - Claude processes query with complete document content
   - Maintains conversation history for context awareness
   - Response includes source attribution and document references
   - Usage analytics logged for admin dashboard

## Dependencies

**Core Python Libraries:**
- `anthropic` - Claude API integration for AI-powered responses
- `hashlib` - Password hashing for secure authentication
- `json` - Data serialization for user database and analytics
- `http.server` - Built-in HTTP server for web application hosting
- `urllib.parse` - URL parsing and query string handling

**Frontend Technologies:**
- **Bootstrap 5** - Responsive CSS framework for professional UI
- **Vanilla JavaScript** - Client-side functionality without additional frameworks
- **HTML5** - Modern semantic markup for accessibility and SEO

**Authentication & Security:**
- File-based user database with SHA-256 password hashing
- HTTP-only secure session cookies
- CSRF protection through session validation
- Role-based access control (admin/employee permissions)

## Deployment

**Replit Configuration:**
- Python 3.11 runtime environment
- Anthropic API key stored securely in environment variables
- Single-port deployment on port 5000 for web interface
- Workflow configured to run `python web_app.py`

**Production Considerations:**
- Stateless design allows horizontal scaling
- File-based authentication suitable for small to medium teams
- Session management through secure HTTP-only cookies
- All user interactions logged for audit and analytics purposes

**Setup Requirements:**
1. Set `ANTHROPIC_API_KEY` environment variable
2. Ensure `/documents/` folder contains company documentation
3. Configure user accounts in `user_data.json`
4. Deploy with `python web_app.py` on port 5000

## Changelog

- June 26, 2025: Initial setup with Streamlit interface
- June 26, 2025: Migrated to HTML frontend with Python HTTP server backend
- June 26, 2025: Implemented conversational memory and document highlighting 
- June 26, 2025: Removed all document generation code - system now only uses existing files
- June 27, 2025: Added user authentication system with login/logout and session management
- June 27, 2025: Integrated document relevance intelligence to only show truly relevant sources
- June 27, 2025: Employee ID and department now automatically populated from authenticated user database
- June 27, 2025: Fixed authentication cookie handling - switched to traditional HTML form submission for reliable login flow
- June 30, 2025: Enhanced document access - Claude now receives complete document content instead of excerpts for comprehensive answers
- June 30, 2025: Cleaned up project structure - removed unused files and updated documentation to reflect current simplified architecture

## User Preferences

Preferred communication style: Simple, everyday language.
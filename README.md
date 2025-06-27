# Enterprise Support Assistant

An intelligent AI-powered internal support chatbot that helps employees quickly find information about company policies, benefits, procedures, and other internal documentation through natural language conversations. Built with Claude Sonnet 4 and Replit.

![Enterprise Support Assistant](https://img.shields.io/badge/AI-Claude%20Sonnet%204-blue) ![Python](https://img.shields.io/badge/Python-3.11+-green) ![License](https://img.shields.io/badge/License-Apache2.0-yellow)

## 🚀 Features

### Core Capabilities
- **Intelligent Document Search**: Automatically processes and searches through company documents with semantic understanding
- **Natural Language Conversations**: Chat interface that understands employee questions in plain English
- **Source Attribution**: Every response includes references to specific company documents with highlighted sections
- **Conversation Memory**: Maintains context throughout chat sessions for follow-up questions
- **Multi-Format Support**: Handles TXT, PDF, DOCX, DOC, and RTF document formats

### User Management
- **Secure Authentication**: File-based user authentication with session management
- **Role-Based Access**: Separate interfaces for employees and administrators
- **Employee Profiles**: Automatic population of user information from employee database
- **Session Security**: Secure cookie-based sessions with proper logout functionality

### Administrative Features
- **Usage Analytics**: Comprehensive dashboard showing query patterns, response times, and user engagement
- **Department Insights**: Analytics broken down by department and query categories
- **Document Access Tracking**: Monitor which documents are most frequently referenced
- **Performance Metrics**: Response time analysis and system optimization recommendations

### Technical Features
- **Responsive Design**: Professional Bootstrap-based interface that works on desktop and mobile
- **Real-time Updates**: Live chat interface with instant responses
- **Document Viewer**: Integrated document viewing with search term highlighting
- **Error Handling**: Comprehensive error management with user-friendly messages

## 🛠️ Technology Stack

- **AI Engine**: Anthropic Claude Sonnet 4 API
- **Backend**: Python 3.11+ with built-in HTTP server
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Authentication**: File-based user management with secure sessions
- **Document Processing**: Dynamic text extraction and processing
- **Analytics**: Real-time usage tracking and visualization

## 📋 Prerequisites

- Python 3.11 or higher
- Anthropic API key
- Company documents in supported formats (TXT, PDF, DOCX, DOC, RTF)

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/enterprise-support-assistant.git
   cd enterprise-support-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install anthropic flask
   ```

3. **Set up environment variables**
   ```bash
   export ANTHROPIC_API_KEY="your_api_key_here"
   ```

4. **Add your company documents**
   ```bash
   mkdir documents
   # Copy your company policy documents into the documents/ folder
   ```

5. **Run the application**
   ```bash
   python web_app.py
   ```

6. **Access the application**
   - Open http://localhost:5000 in your browser
   - Use demo credentials: `john.doe` / `password123`

## 📚 Documentation

- [Setup Guide](docs/SETUP.md) - Detailed installation and configuration
- [User Guide](docs/USER_GUIDE.md) - How to use the chat interface
- [Admin Guide](docs/ADMIN_GUIDE.md) - Managing users and viewing analytics
- [API Reference](docs/API.md) - Technical API documentation
- [Configuration](docs/CONFIGURATION.md) - Customization options

## 👥 Default User Accounts

The system comes with demo user accounts for testing:

| Username | Password | Role | Department |
|----------|----------|------|------------|
| john.doe | password123 | Admin | IT |
| jane.smith | password123 | Employee | HR |
| bob.wilson | password123 | Employee | Marketing |
| alice.brown | password123 | Employee | Finance |

## 🏗️ Architecture

The application follows a modular architecture:

```
├── web_app.py              # Main application server
├── simple_auth.py          # Authentication system
├── document_processor.py   # Document handling and processing
├── documents/              # Company documents directory
├── user_data.json         # User database (file-based)
├── templates/             # HTML templates (if needed)
└── static/               # Static assets (CSS, JS, images)
```

### Key Components

- **EnterpriseHandler**: Main HTTP request handler managing all routes
- **SimpleUserAuth**: File-based authentication with session management
- **DynamicDocumentProcessor**: Automatic document scanning and text extraction
- **Analytics Engine**: Usage tracking and performance monitoring

## 🔧 Configuration

### Environment Variables
- `ANTHROPIC_API_KEY`: Your Anthropic API key (required)

### Application Settings
- Document folder: `documents/` (configurable)
- Server port: `5000` (configurable)
- Session timeout: 24 hours (configurable)

## 📊 Analytics and Monitoring

The admin dashboard provides insights into:

- **Query Analytics**: Most common question types and patterns
- **User Engagement**: Active users, session duration, and usage frequency
- **Document Performance**: Most referenced documents and search patterns
- **System Metrics**: Response times, error rates, and optimisation opportunities
- **Department Insights**: Usage patterns by organizational department

## 🔒 Security Features

- **Session Management**: Secure HTTP-only cookies with automatic expiration
- **Input Validation**: Comprehensive validation of all user inputs
- **Authentication**: File-based user management with password hashing
- **Access Control**: Role-based permissions for admin features
- **Audit Logging**: Complete logging of user interactions for compliance

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.


## 🎯 Use Cases

Perfect for organisations that need to:

- **Reduce HR workload** by automating policy questions
- **Improve employee self-service** for common inquiries
- **Centralize knowledge management** across departments
- **Track information usage patterns** for continuous improvement
- **Provide 24/7 support** for employee questions
- **Maintain compliance** with audit trails and usage analytics

## 🔮 Roadmap

- [ ] Evaluation and Monitoring
- [ ] Integration with external HR systems
- [ ] Multi-language support
- [ ] Slack/Teams integration

---

# Enterprise Support Assistant

An AI-powered internal support chatbot that helps employees quickly find information about company policies, benefits, procedures, and documentation using Anthropic's Claude API.

![Enterprise Support Assistant](https://img.shields.io/badge/AI-Claude%20Sonnet%204-blue) ![Python](https://img.shields.io/badge/Python-3.11+-green) ![License](https://img.shields.io/badge/License-Apache2.0-yellow)

## Features

- **Quick Demo**: [Watch here](https://drive.google.com/file/d/1_CM1lLJZNw4sozQfxh_u7vj-J7bM9ULn/view?usp=sharing)
- **AI-Powered Responses**: Uses Claude 4.0 Sonnet for natural language understanding and comprehensive answers
- **Complete Document Access**: Claude receives full document content for detailed, accurate responses
- **Secure Authentication**: File-based authentication with session management and role-based access
- **Document Management**: Dynamic processing of company documents from the `/documents/` folder
- **Conversation Memory**: Maintains chat history and context across user sessions
- **Admin Dashboard**: Usage analytics and employee management for administrators
- **Responsive Design**: Professional Bootstrap-based interface optimized for desktop and mobile

## Quick Start

### Prerequisites

- Python 3.11+
- Anthropic API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/enterprise-support-assistant.git
cd enterprise-support-assistant
```

2. Install dependencies:
```bash
pip install anthropic
```

3. Set your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

4. Add your company documents to the `/documents/` folder

5. Run the application:
```bash
python web_app.py
```

### Default Login Credentials

- **Admin**: username: `john.doe`, password: `password123`
- **Employee**: username: `jane.smith`, password: `password123`

## Project Structure

```
├── web_app.py              # Main application server
├── simple_auth.py          # Authentication system
├── document_processor.py   # Document processing
├── user_data.json         # Employee database
├── documents/             # Company documentation
├── templates/             # HTML templates
├── static/               # CSS and JavaScript assets
└── README.md             # This file
```

## Configuration

### Adding Users

Edit `user_data.json` to add new employees:

```json
{
  "employees": {
    "username": {
      "employee_id": "EMP001",
      "name": "Full Name",
      "department": "Department",
      "role": "employee",
      "password_hash": "hashed_password"
    }
  }
}
```

### Adding Documents

Simply place your company documents in the `/documents/` folder. Supported formats:
- Plain text (.txt)
- PDF (.pdf) 
- Word documents (.docx)
- Rich Text Format (.rtf)

## Security Features

- SHA-256 password hashing
- HTTP-only secure session cookies
- Role-based access control (admin/employee)
- Session validation and CSRF protection

## API Usage

The application uses the Anthropic Claude API for generating responses. Ensure you have:
- Valid Anthropic API key set in environment variables
- Sufficient API credits for your usage volume

## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.

## Roadmap

- Evaluation and Monitoring
- Improve chat intelligence
- Improve response formatting
- Multi-language support
- Voice integration

# Setup Guide

This guide will walk you through setting up the Enterprise Support Assistant in your organization.

## System Requirements

- **Python**: 3.11 or higher
- **Memory**: Minimum 512MB RAM (2GB recommended)
- **Storage**: 100MB for application + space for your documents
- **Network**: Internet connection for Claude API access

## Installation Steps

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/enterprise-support-assistant.git
cd enterprise-support-assistant

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install anthropic flask
```

### 2. API Configuration

1. **Get Anthropic API Key**
   - Visit https://console.anthropic.com/
   - Create an account or sign in
   - Generate a new API key
   - Keep this key secure and never commit it to version control

2. **Set Environment Variable**
   ```bash
   # Linux/Mac
   export ANTHROPIC_API_KEY="your_api_key_here"
   
   # Windows
   set ANTHROPIC_API_KEY=your_api_key_here
   
   # Or create a .env file (recommended for development)
   echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
   ```

### 3. Document Setup

```bash
# Create documents directory
mkdir documents

# Add your company documents
cp /path/to/your/policies/* documents/
```

**Supported document formats:**
- `.txt` - Plain text files
- `.pdf` - PDF documents
- `.docx` - Microsoft Word (modern format)
- `.doc` - Microsoft Word (legacy format)
- `.rtf` - Rich Text Format

### 4. User Configuration

The system comes with demo users in `user_data.json`. For production:

1. **Edit user_data.json** to add your organization's users
2. **Change default passwords** for security
3. **Set appropriate roles** (admin vs employee)

Example user entry:
```json
{
  "employees": {
    "jane.doe": {
      "employee_id": "EMP001",
      "password_hash": "hashed_password",
      "first_name": "Jane",
      "last_name": "Doe",
      "department": "HR",
      "position": "HR Manager",
      "is_admin": true
    }
  }
}
```

### 5. Launch Application

```bash
python web_app.py
```

The application will start on `http://localhost:5000`

## Production Deployment

### Using Replit (Recommended)

1. **Fork to Replit**
   - Import the GitHub repository to Replit
   - Add `ANTHROPIC_API_KEY` to Secrets
   - Upload your documents to the `documents/` folder
   - Click Run

### Using Docker

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install anthropic flask

EXPOSE 5000
CMD ["python", "web_app.py"]
```

Build and run:
```bash
docker build -t enterprise-support .
docker run -p 5000:5000 -e ANTHROPIC_API_KEY="your_key" enterprise-support
```

### Using Cloud Platforms

**Heroku:**
1. Create `requirements.txt`:
   ```
   anthropic
   flask
   ```

2. Create `Procfile`:
   ```
   web: python web_app.py
   ```

3. Deploy via Heroku CLI or GitHub integration

**AWS/GCP/Azure:**
- Use container services with the Docker approach above
- Configure environment variables through platform settings
- Ensure security groups allow port 5000 access

## Configuration Options

### Server Settings

Edit `web_app.py` to modify:
```python
# Change port
server = HTTPServer(('0.0.0.0', 8080), EnterpriseHandler)

# Change documents directory
DOCUMENTS_FOLDER = "company_docs"
```

### Authentication Settings

Edit `simple_auth.py` for:
- Session timeout duration
- Password hashing method
- User data storage location

### UI Customization

Modify the HTML template in `web_app.py`:
- Company branding colors
- Logo and styling
- Navigation elements

## Troubleshooting

### Common Issues

**"Authentication system not available"**
- Check that `user_data.json` exists and is valid JSON
- Verify file permissions allow reading

**"API key not found"**
- Ensure `ANTHROPIC_API_KEY` environment variable is set
- Check API key is valid and has sufficient credits

**"No documents found"**
- Verify documents exist in the `documents/` folder
- Check file formats are supported
- Ensure proper file permissions

**Login not working**
- Clear browser cookies for the site
- Check credentials match `user_data.json`
- Verify session management is working

### Debug Mode

Enable debug logging by adding to `web_app.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Optimization

**For large document collections:**
- Consider implementing document indexing
- Add caching for frequently accessed documents
- Monitor response times via admin analytics

**For high user load:**
- Use a production WSGI server (gunicorn, uwsgi)
- Implement connection pooling
- Consider load balancing

## Security Considerations

### Production Security

1. **Change default passwords**
2. **Use HTTPS** in production
3. **Secure API keys** with proper secret management
4. **Regular backups** of user data and analytics
5. **Monitor access logs** for unusual activity

### Network Security

- Configure firewall rules appropriately
- Use VPN access for internal tools
- Implement rate limiting if needed
- Consider IP whitelisting for admin features

## Support

If you encounter issues:

1. Check the [troubleshooting section](#troubleshooting) above
2. Review application logs for error details
3. Check GitHub Issues for known problems
4. Contact support with specific error messages and setup details
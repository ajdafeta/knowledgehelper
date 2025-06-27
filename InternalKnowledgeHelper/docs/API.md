# API Reference

This document describes the HTTP API endpoints available in the Enterprise Support Assistant.

## Authentication

All API endpoints (except `/api/login`) require a valid session cookie. The session cookie is automatically set upon successful login and should be included in all subsequent requests.

**Cookie Name**: `session_token`  
**Cookie Attributes**: `HttpOnly; Path=/; Max-Age=86400`

## Endpoints

### Authentication Endpoints

#### POST /api/login
Authenticate user credentials and establish a session.

**Request:**
```http
POST /api/login HTTP/1.1
Content-Type: application/x-www-form-urlencoded

username=john.doe&password=password123
```

**Response (Success):**
```http
HTTP/1.1 302 Found
Location: /
Set-Cookie: session_token=xyz123...; HttpOnly; Path=/; Max-Age=86400
```

**Response (Failure):**
```http
HTTP/1.1 302 Found
Location: /login?error=Invalid%20username%20or%20password
```

#### GET /logout
End the current user session and redirect to login page.

**Response:**
```http
HTTP/1.1 302 Found
Location: /login
Set-Cookie: session_token=; HttpOnly; Path=/; Max-Age=0
```

### User Information

#### GET /api/user
Get current authenticated user information.

**Request:**
```http
GET /api/user HTTP/1.1
Cookie: session_token=xyz123...
```

**Response:**
```json
{
  "employee_id": "EMP001",
  "first_name": "John",
  "last_name": "Doe", 
  "department": "IT",
  "position": "System Administrator",
  "is_admin": true
}
```

### Chat Interface

#### POST /api/chat
Submit a query to the AI assistant and receive a response.

**Request:**
```json
{
  "query": "What is our vacation policy?",
  "user_id": "EMP001",
  "department": "IT",
  "conversation_history": [
    {
      "role": "user",
      "content": "Previous question"
    },
    {
      "role": "assistant", 
      "content": "Previous response"
    }
  ]
}
```

**Response:**
```json
{
  "response": "Our vacation policy allows for...",
  "sources": [
    {
      "document": "Employee_Handbook.txt",
      "relevance": "high",
      "excerpt": "Vacation time accrues..."
    }
  ],
  "processing_time": 1.23,
  "conversation_history": [
    // Updated conversation history
  ]
}
```

#### POST /api/reset_chat
Clear the current user's conversation history.

**Request:**
```http
POST /api/reset_chat HTTP/1.1
Content-Type: application/json
Cookie: session_token=xyz123...
```

**Response:**
```json
{
  "success": true,
  "message": "Chat history cleared"
}
```

### Document Management

#### GET /api/documents
Retrieve list of available company documents.

**Response:**
```json
[
  {
    "name": "Employee_Handbook",
    "display_name": "Employee Handbook",
    "type": "Text Document",
    "size": "45.2 KB",
    "modified": "2025-06-27",
    "path": "documents/Employee_Handbook.txt"
  },
  {
    "name": "IT_Security_Policy", 
    "display_name": "IT Security Policy",
    "type": "Text Document",
    "size": "23.1 KB", 
    "modified": "2025-06-20",
    "path": "documents/IT_Security_Policy.txt"
  }
]
```

#### GET /document/{document_name}
View a specific document with optional query highlighting.

**Parameters:**
- `document_name` (string): Name of the document
- `highlight` (string, optional): Text to highlight in the document

**Example:**
```
GET /document/Employee_Handbook?highlight=vacation%20policy
```

**Response:** HTML document with highlighted search terms

### Analytics (Admin Only)

#### GET /api/analytics
Retrieve usage analytics and system metrics.

**Authorization:** Requires admin privileges

**Response:**
```json
{
  "total_queries": 1247,
  "unique_users": 45,
  "departments": {
    "HR": 324,
    "IT": 298,
    "Finance": 156,
    "Marketing": 234,
    "General": 235
  },
  "documents_accessed": {
    "Employee_Handbook.txt": 89,
    "IT_Security_Policy.txt": 67,
    "Benefits_Guide.pdf": 45
  },
  "query_types": {
    "HR & Benefits": 456,
    "IT & Security": 234,
    "Finance": 167,
    "General Policies": 234,
    "Other": 156
  },
  "daily_usage": {
    "2025-06-27": 23,
    "2025-06-26": 45,
    "2025-06-25": 34
  },
  "avg_response_time": 1.34,
  "error_count": 12,
  "error_rate": 0.96,
  "popular_queries": [
    "vacation policy",
    "health insurance",
    "password requirements"
  ]
}
```

### Static Content

#### GET /
Main application interface (redirects to `/login` if not authenticated).

#### GET /login
Login page interface.

#### GET /admin
Admin dashboard interface (requires admin privileges).

## Error Responses

### 401 Unauthorized
```json
{
  "error": "Authentication required",
  "message": "Please log in to access this resource"
}
```

### 403 Forbidden
```json
{
  "error": "Insufficient privileges", 
  "message": "Admin access required"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found",
  "message": "The requested resource does not exist"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred"
}
```

## Request/Response Headers

### Common Request Headers
```http
Content-Type: application/json
Cookie: session_token=xyz123...
```

### Common Response Headers
```http
Content-Type: application/json
Server: BaseHTTP/0.6 Python/3.11.10
```

## Rate Limiting

Currently no rate limiting is implemented, but consider implementing rate limiting for production deployments to prevent abuse.

**Recommended limits:**
- Chat API: 10 requests per minute per user
- Analytics API: 5 requests per minute per admin user
- Document API: 20 requests per minute per user

## API Usage Examples

### Python Example
```python
import requests

# Login
login_data = {
    'username': 'john.doe',
    'password': 'password123'
}
session = requests.Session()
response = session.post('http://localhost:5000/api/login', data=login_data)

# Ask a question
chat_data = {
    'query': 'What is the PTO policy?',
    'user_id': 'EMP001', 
    'department': 'IT',
    'conversation_history': []
}
response = session.post('http://localhost:5000/api/chat', json=chat_data)
print(response.json())
```

### JavaScript Example
```javascript
// Login
const loginResponse = await fetch('/api/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: 'username=john.doe&password=password123'
});

// Ask a question
const chatResponse = await fetch('/api/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    credentials: 'same-origin',
    body: JSON.stringify({
        query: 'What is the PTO policy?',
        user_id: 'EMP001',
        department: 'IT', 
        conversation_history: []
    })
});

const result = await chatResponse.json();
console.log(result);
```

### curl Example
```bash
# Login and save cookies
curl -c cookies.txt -X POST http://localhost:5000/api/login \
  -d "username=john.doe&password=password123"

# Ask a question
curl -b cookies.txt -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query":"What is the PTO policy?","user_id":"EMP001","department":"IT","conversation_history":[]}'
```

## Security Considerations

1. **HTTPS**: Use HTTPS in production to protect session cookies
2. **Session Management**: Sessions expire after 24 hours
3. **Input Validation**: All inputs are validated and sanitized
4. **Admin Access**: Analytics endpoints require admin privileges
5. **Cookie Security**: Session cookies are HttpOnly to prevent XSS

## Integration Notes

- The API uses standard HTTP methods and JSON formatting
- Session management is handled via HTTP cookies
- All endpoints return appropriate HTTP status codes
- Error responses include descriptive messages for debugging
- The API is designed to be stateless except for session management
import os
import hashlib
import secrets
import json
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class SimpleUserAuth:
    """Simple file-based user authentication system"""
    
    def __init__(self):
        self.data_file = 'user_data.json'
        self.sessions = {}  # In-memory session storage
        self.init_data_storage()
    
    def init_data_storage(self):
        """Initialize user data storage"""
        try:
            if not os.path.exists(self.data_file):
                # Create initial user data with sample employees
                initial_data = {
                    'employees': {
                        'john.doe': {
                            'employee_id': 'EMP001',
                            'username': 'john.doe',
                            'email': 'john.doe@company.com',
                            'password_hash': self.hash_password('password123'),
                            'first_name': 'John',
                            'last_name': 'Doe',
                            'department': 'Engineering',
                            'position': 'Senior Developer',
                            'is_admin': True,
                            'is_active': True,
                            'created_at': datetime.now().isoformat(),
                            'last_login': None
                        },
                        'jane.smith': {
                            'employee_id': 'EMP002',
                            'username': 'jane.smith',
                            'email': 'jane.smith@company.com',
                            'password_hash': self.hash_password('password123'),
                            'first_name': 'Jane',
                            'last_name': 'Smith',
                            'department': 'Human Resources',
                            'position': 'HR Manager',
                            'is_admin': False,
                            'is_active': True,
                            'created_at': datetime.now().isoformat(),
                            'last_login': None
                        },
                        'bob.wilson': {
                            'employee_id': 'EMP003',
                            'username': 'bob.wilson',
                            'email': 'bob.wilson@company.com',
                            'password_hash': self.hash_password('password123'),
                            'first_name': 'Bob',
                            'last_name': 'Wilson',
                            'department': 'Marketing',
                            'position': 'Marketing Specialist',
                            'is_admin': False,
                            'is_active': True,
                            'created_at': datetime.now().isoformat(),
                            'last_login': None
                        },
                        'alice.brown': {
                            'employee_id': 'EMP004',
                            'username': 'alice.brown',
                            'email': 'alice.brown@company.com',
                            'password_hash': self.hash_password('password123'),
                            'first_name': 'Alice',
                            'last_name': 'Brown',
                            'department': 'Finance',
                            'position': 'Financial Analyst',
                            'is_admin': False,
                            'is_active': True,
                            'created_at': datetime.now().isoformat(),
                            'last_login': None
                        }
                    },
                    'sessions': {}
                }
                
                with open(self.data_file, 'w') as f:
                    json.dump(initial_data, f, indent=2)
                
                logger.info("Created initial user data with sample employees")
            
            return True
            
        except Exception as e:
            logger.error(f"Error initializing data storage: {e}")
            return False
    
    def load_data(self):
        """Load user data from file"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading user data: {e}")
            return {'employees': {}, 'sessions': {}}
    
    def save_data(self, data):
        """Save user data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving user data: {e}")
            return False
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_user(self, username: str, password: str):
        """Authenticate user and return user info"""
        try:
            data = self.load_data()
            password_hash = self.hash_password(password)
            
            # Check if user exists and password matches
            if username in data['employees']:
                user = data['employees'][username]
                if user.get('password_hash') == password_hash and user.get('is_active', True):
                    # Update last login
                    user['last_login'] = datetime.now().isoformat()
                    self.save_data(data)
                    
                    # Create session
                    session_token = self.create_session(user['employee_id'])
                    
                    # Return user info with session
                    return {
                        'employee_id': user['employee_id'],
                        'username': user['username'],
                        'email': user['email'],
                        'first_name': user['first_name'],
                        'last_name': user['last_name'],
                        'department': user['department'],
                        'position': user['position'],
                        'is_admin': user['is_admin'],
                        'session_token': session_token
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return None
    
    def create_session(self, employee_id: str) -> str:
        """Create a new session for user"""
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=24)  # 24 hour session
        
        # Store in memory for quick access
        self.sessions[session_token] = {
            'employee_id': employee_id,
            'expires_at': expires_at,
            'created_at': datetime.now()
        }
        
        return session_token
    
    def get_user_from_session(self, session_token: str):
        """Get user information from session token"""
        if not session_token or session_token not in self.sessions:
            return None
        
        try:
            session = self.sessions[session_token]
            
            # Check if session is expired
            if session['expires_at'] < datetime.now():
                del self.sessions[session_token]
                return None
            
            # Get user data
            data = self.load_data()
            employee_id = session['employee_id']
            
            # Find user by employee_id
            for username, user in data['employees'].items():
                if user['employee_id'] == employee_id:
                    return {
                        'employee_id': user['employee_id'],
                        'username': user['username'],
                        'email': user['email'],
                        'first_name': user['first_name'],
                        'last_name': user['last_name'],
                        'department': user['department'],
                        'position': user['position'],
                        'is_admin': user['is_admin']
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Session validation error: {e}")
            return None
    
    def logout_user(self, session_token: str) -> bool:
        """Logout user by invalidating session"""
        try:
            if session_token in self.sessions:
                del self.sessions[session_token]
                return True
            return False
            
        except Exception as e:
            logger.error(f"Logout error: {e}")
            return False
    
    def get_all_employees(self) -> list:
        """Get list of all employees for admin dashboard"""
        try:
            data = self.load_data()
            employees = []
            
            for username, user in data['employees'].items():
                employees.append({
                    'employee_id': user['employee_id'],
                    'username': user['username'],
                    'email': user['email'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'department': user['department'],
                    'position': user['position'],
                    'is_admin': user['is_admin'],
                    'is_active': user['is_active'],
                    'created_at': user['created_at'],
                    'last_login': user.get('last_login')
                })
            
            # Sort by department, then by name
            employees.sort(key=lambda x: (x['department'], x['last_name'], x['first_name']))
            return employees
            
        except Exception as e:
            logger.error(f"Error fetching employees: {e}")
            return []
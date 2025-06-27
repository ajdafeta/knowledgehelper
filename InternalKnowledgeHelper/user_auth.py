import os
import hashlib
import secrets
import json
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class UserAuthManager:
    """Manage user authentication and session handling"""
    
    def __init__(self):
        self.data_file = 'user_data.json'
        self.sessions = {}  # In-memory session storage
        self.init_data_storage()
    
    def get_db_connection(self):
        """Get database connection"""
        try:
            return psycopg2.connect(**self.db_config)
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            return None
    
    def init_database(self):
        """Initialize database tables"""
        try:
            conn = self.get_db_connection()
            if not conn:
                return False
                
            with conn.cursor() as cursor:
                # Create employees table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS employees (
                        id SERIAL PRIMARY KEY,
                        employee_id VARCHAR(50) UNIQUE NOT NULL,
                        username VARCHAR(100) UNIQUE NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        first_name VARCHAR(100) NOT NULL,
                        last_name VARCHAR(100) NOT NULL,
                        department VARCHAR(100) NOT NULL,
                        position VARCHAR(100),
                        is_active BOOLEAN DEFAULT true,
                        is_admin BOOLEAN DEFAULT false,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP
                    )
                """)
                
                # Create sessions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_sessions (
                        id SERIAL PRIMARY KEY,
                        session_token VARCHAR(255) UNIQUE NOT NULL,
                        employee_id VARCHAR(50) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMP NOT NULL,
                        is_active BOOLEAN DEFAULT true,
                        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
                    )
                """)
                
                conn.commit()
                
                # Check if we have sample employees, if not create them
                cursor.execute("SELECT COUNT(*) FROM employees")
                count = cursor.fetchone()[0]
                
                if count == 0:
                    self.create_sample_employees(cursor)
                    conn.commit()
                    
            conn.close()
            logger.info("Database initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            return False
    
    def create_sample_employees(self, cursor):
        """Create sample employees for demo purposes"""
        sample_employees = [
            {
                'employee_id': 'EMP001',
                'username': 'john.doe',
                'email': 'john.doe@company.com',
                'password': 'password123',  # In real app, would be properly hashed
                'first_name': 'John',
                'last_name': 'Doe',
                'department': 'Engineering',
                'position': 'Senior Developer',
                'is_admin': True
            },
            {
                'employee_id': 'EMP002',
                'username': 'jane.smith',
                'email': 'jane.smith@company.com',
                'password': 'password123',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'department': 'Human Resources',
                'position': 'HR Manager',
                'is_admin': False
            },
            {
                'employee_id': 'EMP003',
                'username': 'bob.wilson',
                'email': 'bob.wilson@company.com',
                'password': 'password123',
                'first_name': 'Bob',
                'last_name': 'Wilson',
                'department': 'Marketing',
                'position': 'Marketing Specialist',
                'is_admin': False
            },
            {
                'employee_id': 'EMP004',
                'username': 'alice.brown',
                'email': 'alice.brown@company.com',
                'password': 'password123',
                'first_name': 'Alice',
                'last_name': 'Brown',
                'department': 'Finance',
                'position': 'Financial Analyst',
                'is_admin': False
            }
        ]
        
        for emp in sample_employees:
            password_hash = self.hash_password(emp['password'])
            cursor.execute("""
                INSERT INTO employees (employee_id, username, email, password_hash, 
                                     first_name, last_name, department, position, is_admin)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                emp['employee_id'], emp['username'], emp['email'], password_hash,
                emp['first_name'], emp['last_name'], emp['department'], 
                emp['position'], emp['is_admin']
            ))
        
        logger.info("Sample employees created")
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256 (simplified for demo)"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_user(self, username: str, password: str) -> dict:
        """Authenticate user and return user info"""
        try:
            conn = self.get_db_connection()
            if not conn:
                return None
                
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                password_hash = self.hash_password(password)
                
                cursor.execute("""
                    SELECT employee_id, username, email, first_name, last_name, 
                           department, position, is_admin, is_active
                    FROM employees 
                    WHERE (username = %s OR email = %s) AND password_hash = %s AND is_active = true
                """, (username, username, password_hash))
                
                user = cursor.fetchone()
                
                if user:
                    # Update last login
                    cursor.execute("""
                        UPDATE employees SET last_login = CURRENT_TIMESTAMP 
                        WHERE employee_id = %s
                    """, (user['employee_id'],))
                    conn.commit()
                    
                    # Create session
                    session_token = self.create_session(user['employee_id'])
                    
                    user_dict = dict(user)
                    user_dict['session_token'] = session_token
                    
                    conn.close()
                    return user_dict
                    
            conn.close()
            return None
            
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return None
    
    def create_session(self, employee_id: str) -> str:
        """Create a new session for user"""
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=24)  # 24 hour session
        
        try:
            conn = self.get_db_connection()
            if not conn:
                return None
                
            with conn.cursor() as cursor:
                # Deactivate old sessions
                cursor.execute("""
                    UPDATE user_sessions SET is_active = false 
                    WHERE employee_id = %s AND is_active = true
                """, (employee_id,))
                
                # Create new session
                cursor.execute("""
                    INSERT INTO user_sessions (session_token, employee_id, expires_at)
                    VALUES (%s, %s, %s)
                """, (session_token, employee_id, expires_at))
                
                conn.commit()
                
            # Store in memory for quick access
            self.sessions[session_token] = {
                'employee_id': employee_id,
                'expires_at': expires_at,
                'created_at': datetime.now()
            }
            
            conn.close()
            return session_token
            
        except Exception as e:
            logger.error(f"Session creation error: {e}")
            return None
    
    def get_user_from_session(self, session_token: str) -> dict:
        """Get user information from session token"""
        if not session_token:
            return None
            
        try:
            conn = self.get_db_connection()
            if not conn:
                return None
                
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT e.employee_id, e.username, e.email, e.first_name, e.last_name,
                           e.department, e.position, e.is_admin, s.expires_at
                    FROM employees e
                    JOIN user_sessions s ON e.employee_id = s.employee_id
                    WHERE s.session_token = %s AND s.is_active = true 
                    AND s.expires_at > CURRENT_TIMESTAMP
                """, (session_token,))
                
                user = cursor.fetchone()
                conn.close()
                
                if user:
                    return dict(user)
                    
            return None
            
        except Exception as e:
            logger.error(f"Session validation error: {e}")
            return None
    
    def logout_user(self, session_token: str) -> bool:
        """Logout user by invalidating session"""
        try:
            conn = self.get_db_connection()
            if not conn:
                return False
                
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE user_sessions SET is_active = false 
                    WHERE session_token = %s
                """, (session_token,))
                
                conn.commit()
                
            # Remove from memory
            if session_token in self.sessions:
                del self.sessions[session_token]
                
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Logout error: {e}")
            return False
    
    def get_all_employees(self) -> list:
        """Get list of all employees for admin dashboard"""
        try:
            conn = self.get_db_connection()
            if not conn:
                return []
                
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT employee_id, username, email, first_name, last_name,
                           department, position, is_admin, is_active, created_at, last_login
                    FROM employees
                    ORDER BY department, last_name, first_name
                """)
                
                employees = cursor.fetchall()
                conn.close()
                
                return [dict(emp) for emp in employees]
                
        except Exception as e:
            logger.error(f"Error fetching employees: {e}")
            return []
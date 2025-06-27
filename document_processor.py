# Dynamic Document Processor for Enterprise Support Chatbot
import os
import re
import mimetypes
from typing import Dict, List, Tuple
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime

class DynamicDocumentProcessor:
    """Process various document formats dynamically from documents folder"""
    
    def __init__(self, documents_folder: str = "documents"):
        self.documents_folder = documents_folder
        self.supported_extensions = {'.txt', '.pdf', '.doc', '.docx', '.rtf'}
        
    def scan_documents_folder(self) -> Dict[str, str]:
        """Scan documents folder and return all supported files"""
        documents = {}
        
        if not os.path.exists(self.documents_folder):
            os.makedirs(self.documents_folder, exist_ok=True)
            return documents
        
        # Get all files in documents folder
        for filename in os.listdir(self.documents_folder):
            file_path = os.path.join(self.documents_folder, filename)
            
            # Skip directories
            if os.path.isdir(file_path):
                continue
                
            # Check if file extension is supported
            _, ext = os.path.splitext(filename.lower())
            if ext in self.supported_extensions:
                # Use filename without extension as document key
                doc_key = os.path.splitext(filename)[0].replace(' ', '_').replace('-', '_')
                documents[doc_key] = file_path
                
        return documents
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from various file formats"""
        _, ext = os.path.splitext(file_path.lower())
        
        try:
            if ext == '.txt':
                return self._read_text_file(file_path)
            elif ext == '.pdf':
                return self._read_pdf_file(file_path)
            elif ext == '.docx':
                return self._read_docx_file(file_path)
            elif ext == '.doc':
                return self._read_doc_file(file_path)
            elif ext == '.rtf':
                return self._read_rtf_file(file_path)
            else:
                return f"Unsupported file format: {ext}"
                
        except Exception as e:
            return f"Error reading {file_path}: {str(e)}"
    
    def _read_text_file(self, file_path: str) -> str:
        """Read plain text file"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    def _read_pdf_file(self, file_path: str) -> str:
        """Read PDF file using basic text extraction"""
        try:
            # Try to import PyPDF2 if available
            import PyPDF2
            
            text = ""
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
            
        except ImportError:
            # Fallback: Try to read as text (may not work well)
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                    # Very basic PDF text extraction - look for text between stream objects
                    text_parts = []
                    content_str = content.decode('latin-1', errors='ignore')
                    
                    # Simple regex to find text in PDF
                    text_pattern = r'\((.*?)\)'
                    matches = re.findall(text_pattern, content_str)
                    
                    for match in matches:
                        if len(match) > 5 and match.isprintable():
                            text_parts.append(match)
                    
                    return '\n'.join(text_parts) if text_parts else "PDF content could not be extracted. Please install PyPDF2 for better PDF support."
                    
            except Exception as e:
                return f"PDF reading failed: {str(e)}. Please install PyPDF2 for PDF support."
    
    def _read_docx_file(self, file_path: str) -> str:
        """Read DOCX file using built-in XML parsing"""
        try:
            # Try to import python-docx if available
            from docx import Document
            
            doc = Document(file_path)
            text_parts = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)
                    
            return '\n'.join(text_parts)
            
        except ImportError:
            # Fallback: Manual DOCX extraction using zipfile
            try:
                text_parts = []
                
                with zipfile.ZipFile(file_path, 'r') as docx_zip:
                    # Read the main document content
                    if 'word/document.xml' in docx_zip.namelist():
                        content = docx_zip.read('word/document.xml')
                        
                        # Parse XML to extract text
                        root = ET.fromstring(content)
                        
                        # Find all text elements
                        for elem in root.iter():
                            if elem.text and elem.text.strip():
                                text_parts.append(elem.text.strip())
                
                return '\n'.join(text_parts) if text_parts else "DOCX content could not be extracted."
                
            except Exception as e:
                return f"DOCX reading failed: {str(e)}. Please install python-docx for better DOCX support."
    
    def _read_doc_file(self, file_path: str) -> str:
        """Read DOC file (legacy Word format)"""
        try:
            # Try basic text extraction from DOC file
            with open(file_path, 'rb') as f:
                content = f.read()
                
            # Very basic DOC text extraction
            # DOC files are binary, so this is a rough approximation
            text_parts = []
            content_str = content.decode('latin-1', errors='ignore')
            
            # Look for readable text patterns
            words = re.findall(r'[a-zA-Z0-9\s\.\,\;\:\!\?\-]{10,}', content_str)
            
            for word_group in words:
                if word_group.strip() and len(word_group.strip()) > 15:
                    text_parts.append(word_group.strip())
            
            return '\n'.join(text_parts[:50]) if text_parts else "DOC file content could not be properly extracted. Consider converting to DOCX format."
            
        except Exception as e:
            return f"DOC reading failed: {str(e)}. Consider converting to DOCX format."
    
    def _read_rtf_file(self, file_path: str) -> str:
        """Read RTF file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Basic RTF text extraction - remove RTF control codes
            # RTF uses \commands for formatting
            text = re.sub(r'\\[a-z]+\d*\s?', '', content)  # Remove RTF commands
            text = re.sub(r'[{}]', '', text)  # Remove braces
            text = re.sub(r'\\\*[^;]*;', '', text)  # Remove extended RTF commands
            
            # Clean up whitespace
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            return '\n'.join(lines)
            
        except Exception as e:
            return f"RTF reading failed: {str(e)}"
    
    def get_document_info(self, file_path: str) -> Dict[str, str]:
        """Get metadata about a document"""
        try:
            stat = os.stat(file_path)
            _, ext = os.path.splitext(file_path)
            filename = os.path.basename(file_path)
            
            return {
                'filename': filename,
                'extension': ext,
                'size_kb': f"{stat.st_size / 1024:.2f}",
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
                'type': self._get_file_type_description(ext)
            }
        except Exception as e:
            return {
                'filename': os.path.basename(file_path),
                'extension': 'unknown',
                'size_kb': '0',
                'modified': 'unknown',
                'type': 'unknown',
                'error': str(e)
            }
    
    def _get_file_type_description(self, ext: str) -> str:
        """Get human-readable file type description"""
        type_map = {
            '.txt': 'Plain Text Document',
            '.pdf': 'PDF Document',
            '.docx': 'Microsoft Word Document',
            '.doc': 'Legacy Microsoft Word Document',
            '.rtf': 'Rich Text Format Document'
        }
        return type_map.get(ext.lower(), f'{ext.upper()} Document')
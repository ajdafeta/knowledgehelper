// Enterprise Support Assistant - Main JavaScript

let chatHistory = [];
let conversationHistory = [];
let isProcessing = false;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Enterprise Support Assistant initialized');
    
    // Focus on the input field
    document.getElementById('queryInput').focus();
    
    // Load conversation history and documents
    loadConversationHistory();
    loadDocuments();
    
    // Add welcome message if no history
    if (chatHistory.length === 0) {
        addWelcomeMessage();
    }
});

function addWelcomeMessage() {
    const welcomeMessage = {
        type: 'bot',
        content: 'Hello! I\'m your Enterprise Support Assistant. I can help you find information about company policies, benefits, procedures, and more. What would you like to know?',
        timestamp: new Date(),
        sources: [],
        optimizationTips: ['💡 Try asking specific questions like "How many PTO days do I get?" or "What health benefits are available?"']
    };
    
    displayMessage(welcomeMessage);
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendQuery();
    }
}

async function loadConversationHistory() {
    try {
        const response = await fetch('/api/conversation_history');
        if (response.ok) {
            const history = await response.json();
            chatHistory = history;
            conversationHistory = history.map(msg => ({
                role: msg.type === 'user' ? 'user' : 'assistant',
                content: msg.content
            }));
            
            // Display all messages
            const chatHistoryDiv = document.getElementById('chatHistory');
            chatHistoryDiv.innerHTML = '';
            history.forEach(message => displayMessage(message));
        }
    } catch (error) {
        console.error('Error loading conversation history:', error);
    }
}

async function loadDocuments() {
    try {
        const response = await fetch('/api/documents');
        if (response.ok) {
            const documents = await response.json();
            displayDocumentsList(documents);
        }
    } catch (error) {
        console.error('Error loading documents:', error);
        document.getElementById('documentsList').innerHTML = '<p class="small text-danger">Error loading documents</p>';
    }
}

function displayDocumentsList(documents) {
    const documentsDiv = document.getElementById('documentsList');
    
    if (documents.length === 0) {
        documentsDiv.innerHTML = '<p class="small text-muted">No documents found</p>';
        return;
    }
    
    let html = '<div class="small">';
    documents.forEach(doc => {
        html += `
            <div class="d-flex justify-content-between align-items-center mb-2 p-2 border rounded">
                <div>
                    <strong>${doc.display_name}</strong><br>
                    <small class="text-muted">${doc.type} • ${doc.size} KB</small>
                </div>
                <button class="btn btn-sm btn-outline-primary" onclick="viewDocument('${doc.name}')">
                    <i class="fas fa-eye"></i>
                </button>
            </div>
        `;
    });
    html += '</div>';
    
    documentsDiv.innerHTML = html;
}

function viewDocument(documentName) {
    window.open(`/document/${documentName}`, '_blank');
}

async function sendQuery() {
    const queryInput = document.getElementById('queryInput');
    const query = queryInput.value.trim();
    
    if (!query || isProcessing) return;
    
    // Get user settings
    const userId = document.getElementById('employeeId').value;
    const department = document.getElementById('department').value;
    
    // Clear input and show processing state
    queryInput.value = '';
    setProcessingState(true);
    
    // Add user message to chat
    const userMessage = {
        type: 'user',
        content: query,
        timestamp: new Date(),
        userId: userId,
        department: department
    };
    
    displayMessage(userMessage);
    
    try {
        // Send request to server
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                user_id: userId,
                department: department,
                conversation_history: conversationHistory
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Add bot response to chat
            const botMessage = {
                type: 'bot',
                content: data.response,
                timestamp: new Date(),
                sources: data.sources || [],
                processingTime: data.processing_time,
                optimizationTips: data.optimization_tips || []
            };
            
            displayMessage(botMessage);
            
            // Update conversation history
            conversationHistory.push({role: 'user', content: query});
            conversationHistory.push({role: 'assistant', content: data.response});
        } else {
            // Handle error
            const errorMessage = {
                type: 'error',
                content: data.error || 'An error occurred while processing your request.',
                timestamp: new Date()
            };
            
            displayMessage(errorMessage);
        }
    } catch (error) {
        console.error('Error sending query:', error);
        
        const errorMessage = {
            type: 'error',
            content: 'Network error. Please check your connection and try again.',
            timestamp: new Date()
        };
        
        displayMessage(errorMessage);
    } finally {
        setProcessingState(false);
        queryInput.focus();
    }
}

function displayMessage(message) {
    const chatHistory = document.getElementById('chatHistory');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${message.type}-message new-message`;
    
    let messageHTML = '';
    
    if (message.type === 'user') {
        messageHTML = `
            <div class="message-header">
                <i class="fas fa-user"></i>
                You (${message.department})
            </div>
            <div class="message-content">${escapeHtml(message.content)}</div>
            <div class="message-meta">
                ${formatTimestamp(message.timestamp)}
            </div>
        `;
    } else if (message.type === 'bot') {
        messageHTML = `
            <div class="message-header">
                <i class="fas fa-robot"></i>
                Support Assistant
                <span class="status-indicator status-online"></span>
            </div>
            <div class="message-content">${escapeHtml(message.content)}</div>
        `;
        
        // Add sources if available
        if (message.sources && message.sources.length > 0) {
            messageHTML += '<div class="sources-section"><strong>📄 Sources:</strong><br>';
            message.sources.forEach(source => {
                if (source.document && source.document !== 'unknown') {
                    const highlightText = encodeURIComponent(source.highlight_text || source.text.substring(0, 100));
                    messageHTML += `<a href="/document/${source.document}?highlight=${highlightText}" 
                                   class="source-link" target="_blank" rel="noopener">
                                   ${source.document.replace('_', ' ').toUpperCase()}
                                   </a>`;
                }
            });
            messageHTML += '</div>';
        }
        
        // Add optimization tips
        if (message.optimizationTips && message.optimizationTips.length > 0) {
            messageHTML += '<div class="optimization-tips"><strong>💡 Tips:</strong>';
            message.optimizationTips.forEach(tip => {
                messageHTML += `<div class="optimization-tip">${escapeHtml(tip)}</div>`;
            });
            messageHTML += '</div>';
        }
        
        messageHTML += `
            <div class="message-meta">
                ${formatTimestamp(message.timestamp)}
                ${message.processingTime ? ` • Response time: ${message.processingTime.toFixed(2)}s` : ''}
            </div>
        `;
    } else if (message.type === 'error') {
        messageHTML = `
            <div class="message-header">
                <i class="fas fa-exclamation-triangle"></i>
                Error
            </div>
            <div class="message-content">${escapeHtml(message.content)}</div>
            <div class="message-meta">
                ${formatTimestamp(message.timestamp)}
            </div>
        `;
    }
    
    messageDiv.innerHTML = messageHTML;
    chatHistory.appendChild(messageDiv);
    
    // Scroll to bottom
    chatHistory.scrollTop = chatHistory.scrollHeight;
    
    // Store in history
    chatHistory.push(message);
}

function setProcessingState(processing) {
    isProcessing = processing;
    const loadingOverlay = document.getElementById('loadingOverlay');
    const queryInput = document.getElementById('queryInput');
    
    if (processing) {
        loadingOverlay.style.display = 'flex';
        queryInput.disabled = true;
    } else {
        loadingOverlay.style.display = 'none';
        queryInput.disabled = false;
    }
}

async function showAnalytics() {
    const modal = new bootstrap.Modal(document.getElementById('analyticsModal'));
    const content = document.getElementById('analyticsContent');
    
    // Show loading state
    content.innerHTML = `
        <div class="text-center">
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">Loading analytics...</p>
        </div>
    `;
    
    modal.show();
    
    try {
        const response = await fetch('/api/analytics');
        const data = await response.json();
        
        if (response.ok && !data.error) {
            displayAnalytics(data);
        } else {
            content.innerHTML = `
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i>
                    ${data.error || 'No analytics data available yet. Start asking questions to see usage statistics!'}
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading analytics:', error);
        content.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle"></i>
                Error loading analytics data.
            </div>
        `;
    }
}

function displayAnalytics(data) {
    const content = document.getElementById('analyticsContent');
    
    let analyticsHTML = `
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value">${data.total_interactions}</div>
                    <div class="metric-label">Total Interactions</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value">${data.unique_users}</div>
                    <div class="metric-label">Unique Users</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value">${data.avg_processing_time}s</div>
                    <div class="metric-label">Avg Response Time</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-value">${data.most_active_department}</div>
                    <div class="metric-label">Most Active Dept</div>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <div class="analytics-chart">
                    <h6>Query Types</h6>
                    <div id="queryTypeChart"></div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="analytics-chart">
                    <h6>Performance Metrics</h6>
                    <p><strong>Avg Response Length:</strong> ${data.performance_metrics.avg_response_length} chars</p>
                    <p><strong>Avg Documents Retrieved:</strong> ${data.performance_metrics.avg_documents_retrieved}</p>
                    <p><strong>Queries per User:</strong> ${data.performance_metrics.queries_per_user}</p>
                </div>
            </div>
        </div>
    `;
    
    content.innerHTML = analyticsHTML;
    
    // Simple chart for query types
    if (data.query_type_distribution) {
        const chartDiv = document.getElementById('queryTypeChart');
        let chartHTML = '';
        
        for (const [type, count] of Object.entries(data.query_type_distribution)) {
            const percentage = (count / data.total_interactions * 100).toFixed(1);
            chartHTML += `
                <div class="mb-2">
                    <div class="d-flex justify-content-between">
                        <span>${type}</span>
                        <span>${count} (${percentage}%)</span>
                    </div>
                    <div class="progress" style="height: 8px;">
                        <div class="progress-bar" style="width: ${percentage}%"></div>
                    </div>
                </div>
            `;
        }
        
        chartDiv.innerHTML = chartHTML;
    }
}

async function resetChat() {
    if (confirm('Are you sure you want to reset the chat history? This action cannot be undone.')) {
        try {
            const response = await fetch('/api/reset_chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Clear the chat display and conversation history
                document.getElementById('chatHistory').innerHTML = '';
                chatHistory = [];
                conversationHistory = [];
                
                // Add welcome message back
                addWelcomeMessage();
                
                // Show success message
                const successMessage = {
                    type: 'bot',
                    content: 'Chat history has been reset. How can I help you today?',
                    timestamp: new Date(),
                    sources: [],
                    optimizationTips: []
                };
                
                displayMessage(successMessage);
            } else {
                alert('Error resetting chat history: ' + (data.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error resetting chat:', error);
            alert('Network error while resetting chat history.');
        }
    }
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatTimestamp(timestamp) {
    return new Date(timestamp).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

// Handle window resize
window.addEventListener('resize', function() {
    const chatHistory = document.getElementById('chatHistory');
    if (chatHistory) {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
});

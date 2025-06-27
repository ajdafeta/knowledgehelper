# app.py - Enterprise Internal Support Chatbot
import os

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv

from backend import EnterpriseKnowledgeBot, DocumentProcessor

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Enterprise Support Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enterprise look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .optimization-tip {
        background-color: #e6f3ff;
        padding: 0.8rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'bot' not in st.session_state:
        # Try multiple sources for API key
        api_key = None

        # 1. Try environment variable
        api_key = os.getenv('ANTHROPIC_API_KEY')

        # 2. Try Streamlit secrets (for deployment)
        if not api_key:
            try:
                api_key = st.secrets.get('ANTHROPIC_API_KEY', '')
            except:
                pass

        # 3. Allow manual input as fallback
        if not api_key:
            st.session_state.api_key_needed = True
        else:
            st.session_state.bot = EnterpriseKnowledgeBot(api_key)
            st.session_state.api_key_needed = False

            # Set document store if documents are already processed
            if (hasattr(st.session_state, 'document_index') and
                    hasattr(st.session_state, 'document_chunks')):
                st.session_state.bot.set_document_store(
                    st.session_state.document_index,
                    st.session_state.document_chunks
                )

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'documents_processed' not in st.session_state:
        st.session_state.documents_processed = False


def sidebar_config():
    """Configure sidebar with user settings and admin features"""
    with st.sidebar:
        st.header("🏢 User Settings")

        user_id = st.text_input("Employee ID", value="emp_001", help="Your employee identifier")
        department = st.selectbox("Department", [
            "Engineering", "Sales", "Marketing", "HR", "Finance", "Operations"
        ])

        st.header("📊 Admin Dashboard")

        if st.session_state.bot and st.button("View Usage Analytics"):
            st.session_state.show_analytics = True

        if st.button("Reset Chat History"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")

        # Document management
        st.header("📁 Knowledge Base")
        if st.button("Refresh Documents"):
            process_documents()
            st.success("Documents refreshed!")

        return user_id, department


def process_documents():
    """Process and index company documents"""
    if not st.session_state.documents_processed:
        with st.spinner("Processing company documents..."):
            processor = DocumentProcessor()
            doc_paths = [
                "documents/sample_pto_policy.txt",
                "documents/sample_health_benefits.txt",
                "documents/sample_org_structure.txt",
                "documents/claude_usage_policy.txt"
            ]

            # Create placeholder documents if they don't exist
            os.makedirs("documents", exist_ok=True)
            create_sample_documents()

            try:
                index, chunks = processor.process_documents(doc_paths)
                st.session_state.document_index = index
                st.session_state.document_chunks = chunks
                st.session_state.documents_processed = True

                # Set the document store in the bot if it exists
                if st.session_state.bot:
                    st.session_state.bot.set_document_store(index, chunks)

            except Exception as e:
                st.error(f"Error processing documents: {e}")
                st.session_state.documents_processed = False


def create_sample_documents():
    """Create sample company documents for demo"""
    documents = {
        "documents/sample_pto_policy.txt": """
        PTO Policy - Document #HR-001

        Paid Time Off (PTO) Allocation:
        - Full-time employees: 20 days annually
        - Part-time employees: Pro-rated based on hours worked
        - PTO accrues monthly at 1.67 days per month

        PTO Request Process:
        1. Submit request through HR portal at least 2 weeks in advance
        2. Manager approval required for requests over 5 consecutive days
        3. Blackout periods apply during Q4 for Finance and Sales teams

        Contact: hr@company.com for questions
        """,

        "documents/sample_health_benefits.txt": """
        Health Benefits Overview - Document #HR-002

        Medical Insurance:
        - Premium Plan: 100% company-paid for employee, 80% for family
        - Standard Plan: 90% company-paid for employee, 70% for family
        - Deductibles: Premium $500, Standard $1,500

        Additional Benefits:
        - Dental and Vision included in all plans
        - $1,000 annual wellness reimbursement
        - Mental health coverage with $0 copay

        Enrollment: Open enrollment occurs in November
        Contact: benefits@company.com
        """,

        "documents/sample_org_structure.txt": """
        Organizational Structure - Document #ORG-001

        Executive Team:
        - CEO: Sarah Johnson (sarah.johnson@company.com)
        - CTO: Mike Chen (mike.chen@company.com)
        - VP Sales: Lisa Rodriguez (lisa.rodriguez@company.com)

        Department Heads:
        - Engineering: David Kim (david.kim@company.com)
        - HR: Jennifer Liu (jennifer.liu@company.com)
        - Finance: Robert Smith (robert.smith@company.com)

        IT Support: it-help@company.com
        HR General: hr@company.com
        """
    }

    for path, content in documents.items():
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write(content)


def main_chat_interface(user_id: str, department: str):
    """Main chat interface"""
    st.markdown('<h1 class="main-header">🤖 Enterprise Support Assistant</h1>', unsafe_allow_html=True)

    # Handle API key input if needed
    if st.session_state.get('api_key_needed', False):
        st.warning("⚠️ Claude API key not found. Please enter your API key to continue.")
        api_key_input = st.text_input("Enter your Anthropic API Key:", type="password")
        if st.button("Set API Key") and api_key_input:
            st.session_state.bot = EnterpriseKnowledgeBot(api_key_input)
            st.session_state.api_key_needed = False

            # Set document store if documents are already processed
            if (hasattr(st.session_state, 'document_index') and
                    hasattr(st.session_state, 'document_chunks')):
                st.session_state.bot.set_document_store(
                    st.session_state.document_index,
                    st.session_state.document_chunks
                )

            st.success("API key set successfully!")
            st.rerun()
        return

    if not st.session_state.bot:
        st.error("⚠️ Unable to initialize the chatbot. Please check your API key configuration.")
        return

    # Process documents if needed
    if not st.session_state.documents_processed:
        process_documents()

    # Ensure bot has access to document store
    if (st.session_state.bot and st.session_state.documents_processed and
            hasattr(st.session_state, 'document_index') and
            hasattr(st.session_state, 'document_chunks')):
        st.session_state.bot.set_document_store(
            st.session_state.document_index,
            st.session_state.document_chunks
        )

    # Chat interface
    st.subheader("💬 Ask me anything about company policies and procedures")

    # Display chat history
    for i, (query, response, tips) in enumerate(st.session_state.chat_history):
        with st.expander(f"Query {i + 1}: {query[:50]}..."):
            st.write("**Your Question:**", query)
            st.write("**Response:**", response)
            if tips:
                st.write("**Optimization Tips:**")
                for tip in tips:
                    st.markdown(f'<div class="optimization-tip">{tip}</div>', unsafe_allow_html=True)

    # New query input
    query = st.text_input("Enter your question:", placeholder="e.g., How many PTO days do I get?")

    if st.button("Ask Assistant", type="primary") and query:
        with st.spinner("Processing your question..."):
            try:
                result = st.session_state.bot.process_query(query, user_id, department)

                # Display response
                st.success("**Response:**")
                st.write(result['response'])

                # Show optimization tips
                if result['optimization_tips']:
                    st.info("**Optimization Suggestions:**")
                    for tip in result['optimization_tips']:
                        st.markdown(f'<div class="optimization-tip">{tip}</div>', unsafe_allow_html=True)

                # Show performance metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Response Time", f"{result['processing_time']:.2f}s")
                with col2:
                    st.metric("Sources Used", len(result['sources']))

                # Add to chat history
                st.session_state.chat_history.append((
                    query,
                    result['response'],
                    result['optimization_tips']
                ))

            except Exception as e:
                st.error(f"Error processing query: {e}")


def show_analytics_dashboard():
    """Display usage analytics dashboard"""
    if not st.session_state.bot:
        return

    st.header("📊 Usage Analytics Dashboard")

    analytics = st.session_state.bot.usage_tracker.get_usage_analytics()

    if 'error' in analytics:
        st.info("No usage data available yet. Start asking questions to see analytics!")
        return

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Interactions", analytics['total_interactions'])
    with col2:
        st.metric("Unique Users", analytics['unique_users'])
    with col3:
        st.metric("Avg Response Time", f"{analytics['avg_processing_time']:.2f}s")
    with col4:
        st.metric("Most Active Dept", analytics['most_active_department'])

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        # Query type distribution
        if analytics['query_type_distribution']:
            fig = px.pie(
                values=list(analytics['query_type_distribution'].values()),
                names=list(analytics['query_type_distribution'].keys()),
                title="Query Types Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Daily usage trend
        if analytics['daily_usage_trend']:
            dates = list(analytics['daily_usage_trend'].keys())
            values = list(analytics['daily_usage_trend'].values())

            fig = go.Figure(data=go.Scatter(x=dates, y=values, mode='lines+markers'))
            fig.update_layout(title="Daily Usage Trend", xaxis_title="Date", yaxis_title="Interactions")
            st.plotly_chart(fig, use_container_width=True)

    # Performance insights
    st.subheader("💡 Performance Insights")
    perf = analytics['performance_metrics']

    insights = []
    if perf['avg_response_length'] < 100:
        insights.append("📝 Consider expanding responses for better user satisfaction")
    if perf['queries_per_user'] > 5:
        insights.append("🔄 High repeat usage indicates strong user engagement")
    if analytics['avg_processing_time'] > 2:
        insights.append("⚡ Consider implementing response caching for better performance")

    for insight in insights:
        st.info(insight)


def main():
    """Main application function"""
    initialize_session_state()

    # Sidebar configuration
    user_id, department = sidebar_config()

    # Main content area
    if st.session_state.get('show_analytics', False):
        show_analytics_dashboard()
        if st.button("← Back to Chat"):
            st.session_state.show_analytics = False
            st.rerun()
    else:
        main_chat_interface(user_id, department)


if __name__ == "__main__":
    main()
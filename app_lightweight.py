import streamlit as st
import os

# Basic setup
st.set_page_config(page_title="TX School Psych Chatbot", page_icon=":robot_face", layout="wide")

# Simple CSS
st.markdown("""
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .message {
    color: #fff;
}
</style>
""", unsafe_allow_html=True)

# Check for OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    st.error("❌ OPENAI_API_KEY not configured. Please set it in Streamlit Cloud secrets.")
    st.stop()

# Try to import dependencies
try:
    from PyPDF2 import PdfReader
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    st.error("PyPDF2 not available")

try:
    import openai
    openai.api_key = OPENAI_API_KEY
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    st.error("OpenAI not available")

if not all([PDF_AVAILABLE, OPENAI_AVAILABLE]):
    st.error("Some dependencies are missing. Consider deploying to Hugging Face Spaces instead.")
    st.info("""
    **Alternative Deployment Options:**
    1. **Hugging Face Spaces** - Perfect for AI apps
    2. **Render.com** - Reliable dependency installation
    3. **Railway.app** - Modern platform
    """)
    st.stop()

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "processed_text" not in st.session_state:
    st.session_state.processed_text = ""

def extract_pdf_text(pdf_files):
    """Extract text from PDF files"""
    text = ""
    for pdf_file in pdf_files:
        pdf_reader = PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_ai_response(question, context=""):
    """Get AI response using OpenAI"""
    try:
        prompt = f"""
        You are a licensed school psychologist supervisor in Texas. 
        Answer the following question based on the context provided.
        
        Context: {context}
        
        Question: {question}
        
        Provide a professional, accurate response with citations if applicable.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a licensed school psychologist supervisor in Texas."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting AI response: {str(e)}"

# Main app
st.header("Chat with TX School Psych Chatbot")

# Sidebar
with st.sidebar:
    st.subheader("Upload Documents")
    pdf_files = st.file_uploader("Upload PDFs", type=['pdf'], accept_multiple_files=True)
    
    if st.button("Process Documents"):
        if pdf_files:
            with st.spinner("Processing PDFs..."):
                st.session_state.processed_text = extract_pdf_text(pdf_files)
                st.success(f"Processed {len(pdf_files)} PDF(s)")
        else:
            st.error("Please upload at least one PDF file")

# Chat interface
st.subheader("Ask Questions")

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user">
            <div class="message"><strong>You:</strong> {message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot">
            <div class="message"><strong>Assistant:</strong> {message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

# User input
user_question = st.text_input("Ask a question:")
if st.button("Send"):
    if user_question:
        if not st.session_state.processed_text:
            st.error("Please process documents first")
        else:
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            
            # Get AI response
            with st.spinner("Getting response..."):
                ai_response = get_ai_response(user_question, st.session_state.processed_text)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            
            st.rerun()

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()

# Show processed text length
if st.session_state.processed_text:
    st.info(f"📄 Processed text length: {len(st.session_state.processed_text)} characters") 
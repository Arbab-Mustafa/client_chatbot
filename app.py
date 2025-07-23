import streamlit as st
import os

# Try to import dotenv, but don't fail if it's not available
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    def load_dotenv():
        pass  # No-op function if dotenv is not available

# Load environment variables
if DOTENV_AVAILABLE:
    try:
        load_dotenv()
    except Exception as e:
        st.warning(f"Could not load .env file: {e}")

# Check for required API keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

# Import dependencies with error handling
try:
    from PyPDF2 import PdfReader
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    st.error("PyPDF2 is not installed. Please check requirements.txt")

try:
    from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
    from langchain_community.embeddings import OpenAIEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_community.chat_models import ChatOpenAI
    from langchain_community.callbacks.manager import get_openai_callback
    from langchain.chains import LLMChain
    from langchain.chains.question_answering import load_qa_chain
    from langchain.memory import ConversationBufferMemory
    from langchain.memory.vectorstore import VectorStoreRetrieverMemory
    from langchain.chains import ConversationalRetrievalChain, RetrievalQA
    from langchain_core.prompts import PromptTemplate
    from langchain.prompts.chat import SystemMessagePromptTemplate
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    LANGCHAIN_AVAILABLE = False
    st.error(f"LangChain dependencies not available: {e}")

try:
    from htmlTempletes import css, bot_template, user_template
    from questionmaker import NoOpLLMChain
    from prompts import general_prompt, general_citation, engagedlow_student_prompt, engagedchild_student_prompt
    LOCAL_MODULES_AVAILABLE = True
except ImportError as e:
    LOCAL_MODULES_AVAILABLE = False
    st.error(f"Local modules not available: {e}")

def get_pdf_text(pdf_docs):
    if not PDF_AVAILABLE:
        st.error("PDF processing not available")
        return ""
    
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    if not LANGCHAIN_AVAILABLE:
        st.error("Text processing not available")
        return []
    
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    if not LANGCHAIN_AVAILABLE:
        st.error("Vector store not available")
        return None
    
    # Use OpenAI embeddings instead of HuggingFace for lighter deployment
    if not OPENAI_API_KEY:
        st.error('OpenAI API key not configured for embeddings', icon="🚨")
        return None
    
    try:
        embeddings = OpenAIEmbeddings()
        # Use ChromaDB instead of FAISS for lighter vector storage
        vectorstore = Chroma.from_texts(texts=text_chunks, embedding=embeddings)
        return vectorstore
    except Exception as e:
        st.error(f"Failed to create vector store: {e}")
        return None

def get_conversation_chain(vectorstore, model, student_type):
    if not LANGCHAIN_AVAILABLE or not LOCAL_MODULES_AVAILABLE:
        st.error("Conversation chain not available")
        return None
    
    # Simplified model selection - use only OpenAI for production
    if model == 'OpenAI GPT 3.5': 
        if not OPENAI_API_KEY:
            st.error('OpenAI API key not configured', icon="🚨")
            return None
        llm = ChatOpenAI(temperature=0)
    elif model == 'GPT-4o mini': 
        if not OPENAI_API_KEY:
            st.error('OpenAI API key not configured', icon="🚨")
            return None
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    else:
        st.error('Only OpenAI models are supported in production deployment', icon="🚨")
        return None
    
    try:
        #create memory type
        memory = ConversationBufferMemory(memory_key='chat_history', output_key='answer', return_messages=True)
        #create conversation chain
        conv_rqa = ConversationalRetrievalChain.from_llm(llm=llm,
                                                    chain_type="stuff",
                                                    verbose="False",
                                                    memory = memory,
                                                    retriever=vectorstore.as_retriever(search_type="similarity_score_threshold",search_kwargs={'k': 30, 'score_threshold': 0.42}),
                                                    return_source_documents = True)
        no_op_chain = NoOpLLMChain(llm=llm)
        conv_rqa.question_generator = no_op_chain
        if student_type == 'General':
            modified_template = general_prompt()
        elif student_type == 'General with citation':
            modified_template = general_citation()
        elif student_type == 'Engaged Low':
            modified_template = engagedlow_student_prompt()
        elif student_type == 'Engaged Child':
            modified_template = engagedchild_student_prompt()
        system_message_prompt = SystemMessagePromptTemplate.from_template(modified_template)
        conv_rqa.combine_docs_chain.llm_chain.prompt.messages[0] = system_message_prompt
        # add chat_history as a variable to the llm_chain's ChatPromptTemplate object
        conv_rqa.combine_docs_chain.llm_chain.prompt.input_variables = ['context', 'question', 'chat_history']

        return conv_rqa
    except Exception as e:
        st.error(f"Failed to create conversation chain: {e}")
        return None

def select_model():
    # Simplified model selection for production - only OpenAI models
    if not OPENAI_API_KEY:
        st.error("❌ OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.")
        return None
    
    available_models = ['GPT-4o mini', 'OpenAI GPT 3.5']
    
    model = st.selectbox(
        'Select the model you want to use',
        available_models
    )
    return model

def select_student_type():
    student_type = st.selectbox(
    'Select the type of question you would like to ask',
    ('General', 'General with citation', 'Engaged Low', 'Engaged Child'))
    return student_type

def handle_userinput(user_question):
    if not st.session_state.conversation:
        st.error("No conversation available. Please process documents first.")
        return
    
    try:
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history = response['chat_history']
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error processing question: {e}")

def main():
    # Environment variables are already loaded at module level
    
    st.set_page_config(page_title="Chat with TX School Psych Chatbot",
                      page_icon=":robot_face", layout="wide")
    
    if LOCAL_MODULES_AVAILABLE:
        st.write(css, unsafe_allow_html=True)
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    
    st.header("Chat with TX School Psych Chatbot")
    
    # Check if all dependencies are available
    if not all([PDF_AVAILABLE, LANGCHAIN_AVAILABLE, LOCAL_MODULES_AVAILABLE]):
        st.error("Some dependencies are missing. Please check the installation.")
        st.stop()
    
    user_question = st.text_input("Ask a question as if you were talking to your supervisor:")
    if user_question:
        handle_userinput(user_question)
    
    if st.button("Clear memory"):
        if st.session_state.chat_history:
            st.session_state.chat_history.clear()
    
    with st.sidebar:
        #select model
        model = select_model()
        if model is None:
            st.stop()
        #select student type
        student_type = select_student_type()
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)  
                if raw_text == "":
                    st.error("Please upload at least one PDF")
                    st.stop()
                else:
                    # get the text chunks
                    text_chunks = get_text_chunks(raw_text)
                    if not text_chunks:
                        st.error("Failed to process text chunks")
                        st.stop()
                    # create vector store
                    vectorstore = get_vectorstore(text_chunks)
                    if vectorstore is None:
                        st.error("Failed to create vector store. Please check your OpenAI API key.")
                        st.stop()
                    # create conversation chain
                    conversation = get_conversation_chain(vectorstore, model, student_type)
                    if conversation:
                        st.session_state.conversation = conversation
                        st.success("Documents processed successfully!")
                    else:
                        st.error("Failed to create conversation chain. Please check your API keys and try again.")

if __name__ == '__main__':
    main()
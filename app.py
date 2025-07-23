import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings, HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import HuggingFaceHub
from langchain_community.callbacks.manager import get_openai_callback
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
from langchain.memory.vectorstore import VectorStoreRetrieverMemory
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain.prompts.chat import SystemMessagePromptTemplate
from htmlTempletes import css, bot_template, user_template
from questionmaker import NoOpLLMChain
from prompts import general_prompt, general_citation, engagedlow_student_prompt, engagedchild_student_prompt
import os
import tiktoken

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    #embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device':"cpu"})
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore, model, student_type):
    #create llm
    if model == 'OpenAI GPT 3.5': 
        llm = ChatOpenAI(temperature=0)
    elif model == 'GPT-4o mini': 
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    elif model == 'Google flan-t5-xxl':
        llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
    elif model == 'Facebook LLAMA':
        pass
        #llm = CTransformers(model="llama-2-7b-chat.ggmlv3.q4_0.bin",model_type="llama",config={'max_new_tokens':128,'temperature':0.01})
    else:
        st.error('Model name not valid', icon="🚨")
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

def select_model():
    model = st.selectbox(
    'Select the model you want to use',
    ('GPT-4o mini','OpenAI GPT 3.5', 'Google flan-t5-xxl', 'Facebook LLAMA 7b'))
    return model

def select_student_type():
    student_type = st.selectbox(
    'Select the type of question you would like to ask',
    ('General', 'General with citation', 'Engaged Low', 'Engaged Child'))
    return student_type


def handle_userinput(user_question):
    
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    # Load environment variables - works for both local .env and Streamlit Cloud secrets
    try:
        load_dotenv()
    except Exception as e:
        st.warning(f"Could not load .env file: {e}")
    
    st.set_page_config(page_title="Chat with TX School Psych Chatbot",
                       page_icon=":robot_face", layout="wide")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with TX School Psych Chatbot")
    user_question = st.text_input("Ask a question as if you were talking to your supervisor:")
    if user_question:
        handle_userinput(user_question)
    st.button("Clear memory", on_click=lambda: st.session_state.chat_history.clear())

    #st.button("Clear chat", on_click=lambda: st.stop())
    with st.sidebar:
        #select model
        model = select_model()

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

                    # create vector store
                    vectorstore = get_vectorstore(text_chunks)

                    # create conversation chain
                    st.session_state.conversation = get_conversation_chain(
                        vectorstore, model, student_type)


if __name__ == '__main__':
    main()
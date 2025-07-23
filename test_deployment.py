#!/usr/bin/env python3
"""
Test script to verify deployment dependencies
"""

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        import os
        print("✅ os imported successfully")
    except ImportError as e:
        print(f"❌ os import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    try:
        from PyPDF2 import PdfReader
        print("✅ PyPDF2 imported successfully")
    except ImportError as e:
        print(f"❌ PyPDF2 import failed: {e}")
        return False
    
    try:
        from langchain_community.embeddings import OpenAIEmbeddings
        print("✅ langchain-community.embeddings imported successfully")
    except ImportError as e:
        print(f"❌ langchain-community.embeddings import failed: {e}")
        return False
    
    try:
        from langchain_community.vectorstores import Chroma
        print("✅ langchain-community.vectorstores imported successfully")
    except ImportError as e:
        print(f"❌ langchain-community.vectorstores import failed: {e}")
        return False
    
    try:
        from langchain_community.chat_models import ChatOpenAI
        print("✅ langchain-community.chat_models imported successfully")
    except ImportError as e:
        print(f"❌ langchain-community.chat_models import failed: {e}")
        return False
    
    try:
        from langchain.text_splitter import CharacterTextSplitter
        print("✅ langchain.text_splitter imported successfully")
    except ImportError as e:
        print(f"❌ langchain.text_splitter import failed: {e}")
        return False
    
    try:
        from langchain.chains import ConversationalRetrievalChain
        print("✅ langchain.chains imported successfully")
    except ImportError as e:
        print(f"❌ langchain.chains import failed: {e}")
        return False
    
    try:
        from langchain.memory import ConversationBufferMemory
        print("✅ langchain.memory imported successfully")
    except ImportError as e:
        print(f"❌ langchain.memory import failed: {e}")
        return False
    
    try:
        import chromadb
        print("✅ chromadb imported successfully")
    except ImportError as e:
        print(f"❌ chromadb import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ numpy imported successfully")
    except ImportError as e:
        print(f"❌ numpy import failed: {e}")
        return False
    
    try:
        import scipy
        print("✅ scipy imported successfully")
    except ImportError as e:
        print(f"❌ scipy import failed: {e}")
        return False
    
    try:
        import sklearn
        print("✅ scikit-learn imported successfully")
    except ImportError as e:
        print(f"❌ scikit-learn import failed: {e}")
        return False
    
    return True

def test_local_modules():
    """Test local module imports"""
    print("\nTesting local modules...")
    
    try:
        from htmlTempletes import css, bot_template, user_template
        print("✅ htmlTempletes imported successfully")
    except ImportError as e:
        print(f"❌ htmlTempletes import failed: {e}")
        return False
    
    try:
        from questionmaker import NoOpLLMChain
        print("✅ questionmaker imported successfully")
    except ImportError as e:
        print(f"❌ questionmaker import failed: {e}")
        return False
    
    try:
        from prompts import general_prompt, general_citation
        print("✅ prompts imported successfully")
    except ImportError as e:
        print(f"❌ prompts import failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment variables"""
    print("\nTesting environment...")
    
    import os
    
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        print("✅ OPENAI_API_KEY found")
    else:
        print("⚠️ OPENAI_API_KEY not found (will need to be set in Streamlit Cloud)")
    
    return True

if __name__ == "__main__":
    print("=== Deployment Test ===")
    
    imports_ok = test_imports()
    modules_ok = test_local_modules()
    env_ok = test_environment()
    
    print("\n=== Test Results ===")
    if imports_ok and modules_ok and env_ok:
        print("✅ All tests passed! Ready for deployment.")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        exit(1) 
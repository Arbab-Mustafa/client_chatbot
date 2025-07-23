from setuptools import setup, find_packages

setup(
    name="chatbot-streamlit-client",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0",
        "python-dotenv>=1.0.0",
        "PyPDF2>=3.0.0",
        "langchain>=0.1.0",
        "langchain-community>=0.0.10",
        "langchain-core>=0.1.0",
        "openai>=1.0.0",
        "faiss-cpu>=1.7.0",
        "sentence-transformers>=2.2.0",
        "huggingface_hub>=0.17.0",
        "torch>=2.0.0",
        "transformers>=4.30.0",
    ],
    python_requires=">=3.8",
) 
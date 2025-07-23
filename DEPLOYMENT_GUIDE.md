# Streamlit Cloud Deployment Guide

## Optimized for Production

This guide covers deploying the Texas School Psychology Chatbot to Streamlit Cloud with optimized dependencies.

## Key Optimizations Made

### 1. **Lighter Dependencies**

- **Removed**: `torch`, `transformers`, `sentence-transformers`, `faiss-cpu`, `huggingface_hub`
- **Added**: `chromadb`, `scikit-learn`, `numpy`, `scipy`
- **Result**: ~2GB → ~200MB package size

### 2. **Simplified AI Models**

- **Before**: OpenAI + HuggingFace + Local models
- **After**: OpenAI only (GPT-3.5, GPT-4o-mini)
- **Benefits**: Faster startup, lower memory usage, better reliability

### 3. **Vector Database Change**

- **Before**: FAISS (heavy, requires compilation)
- **After**: ChromaDB (lightweight, Python-native)
- **Benefits**: Easier deployment, better Streamlit Cloud compatibility

### 4. **Robust Error Handling**

- **Added**: Try-catch blocks for all imports
- **Added**: Graceful fallbacks for missing dependencies
- **Added**: Better error messages for debugging

## Deployment Steps

### 1. **Environment Variables Setup**

In Streamlit Cloud dashboard, add these secrets:

```
OPENAI_API_KEY = your_openai_api_key_here
```

### 2. **File Structure**

Ensure your repository has:

```
├── app.py
├── requirements.txt
├── runtime.txt
├── packages.txt
├── .streamlit/config.toml
├── htmlTempletes.py
├── prompts.py
├── questionmaker.py
├── test_deployment.py
└── images/
```

### 3. **Deploy to Streamlit Cloud**

1. Connect your GitHub repository
2. Set main file path: `app.py`
3. Add environment variables
4. Deploy

### 4. **Troubleshooting Deployment**

If you encounter dependency issues:

1. **Check the logs** in Streamlit Cloud dashboard
2. **Run the test script** locally: `python test_deployment.py`
3. **Verify requirements.txt** has all dependencies
4. **Check Python version** compatibility (3.11+)

## Performance Expectations

### **Memory Usage**

- **Before**: ~2GB+ (exceeded limits)
- **After**: ~200-300MB (within limits)

### **Startup Time**

- **Before**: 2-3 minutes (heavy models)
- **After**: 30-60 seconds (lightweight)

### **Functionality**

- ✅ PDF processing
- ✅ AI-powered Q&A
- ✅ Multiple response styles
- ✅ Chat memory
- ✅ Real-time responses
- ✅ Robust error handling

## Common Deployment Issues

### **1. ModuleNotFoundError: No module named 'PyPDF2'**

**Solution**: 
- Ensure `requirements.txt` has `PyPDF2>=3.0.0`
- Check that Streamlit Cloud is installing dependencies
- Try using `>=` instead of `==` for version flexibility

### **2. LangChain Import Errors**

**Solution**:
- Verify `langchain>=0.1.0` and `langchain-community>=0.0.10` in requirements.txt
- Check for version conflicts
- Use the test script to verify imports

### **3. Environment Variable Issues**

**Solution**:
- Set `OPENAI_API_KEY` in Streamlit Cloud secrets
- Verify the key is valid and has credits
- Check for typos in the environment variable name

## Testing Your Deployment

### **Local Testing**

Run the test script before deploying:

```bash
python test_deployment.py
```

This will verify:
- All dependencies can be imported
- Local modules are accessible
- Environment variables are set

### **Streamlit Cloud Testing**

1. Upload a small PDF file
2. Test the processing functionality
3. Verify AI responses work
4. Check error handling

## Performance Tips

1. **Optimize PDFs**: Compress large files before upload
2. **Chunk Size**: Current 1000 chars is optimal for balance
3. **Memory Management**: Clear chat history regularly
4. **API Usage**: Monitor OpenAI usage to avoid rate limits

## Cost Considerations

### **OpenAI API Costs**

- Embeddings: ~$0.0001 per 1K tokens
- GPT-3.5: ~$0.002 per 1K tokens
- GPT-4o-mini: ~$0.00015 per 1K tokens

### **Estimated Monthly Cost**

- Light usage (100 queries/day): ~$5-10/month
- Heavy usage (1000 queries/day): ~$50-100/month

## Security Notes

- No data persistence beyond session
- API keys stored securely in Streamlit Cloud
- No user authentication required
- Temporary file processing only

## Support

For deployment issues:

1. Check Streamlit Cloud logs
2. Verify environment variables
3. Test with smaller PDF files first
4. Monitor OpenAI API usage
5. Run the test script locally
6. Check the error handling in the app

## Recent Fixes Applied

### **Dependency Installation Issues**
- Updated `requirements.txt` to use `>=` instead of `==`
- Added `packages.txt` for system dependencies
- Improved error handling in `app.py`

### **Import Error Handling**
- Added try-catch blocks for all imports
- Graceful fallbacks for missing modules
- Better error messages for debugging

### **Deployment Robustness**
- Added dependency availability checks
- Improved error handling throughout the app
- Added success/error feedback for users

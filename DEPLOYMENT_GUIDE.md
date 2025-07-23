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
├── .streamlit/config.toml
├── htmlTempletes.py
├── prompts.py
├── questionmaker.py
└── images/
```

### 3. **Deploy to Streamlit Cloud**

1. Connect your GitHub repository
2. Set main file path: `app.py`
3. Add environment variables
4. Deploy

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

## Limitations

### **Model Options**

- Only OpenAI models available
- No local/HuggingFace models
- Requires OpenAI API key

### **File Upload**

- Limited to 200MB total
- PDF files only
- Processing time depends on file size

## Troubleshooting

### **Common Issues**

1. **"OpenAI API key not configured"**

   - Check environment variables in Streamlit Cloud
   - Ensure key is valid and has credits

2. **"Failed to create vector store"**

   - Verify OpenAI API key
   - Check internet connectivity

3. **Slow processing**
   - Large PDF files take longer
   - Consider splitting documents

### **Performance Tips**

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

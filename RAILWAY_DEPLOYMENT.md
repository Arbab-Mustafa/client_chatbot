# Railway Deployment Guide for TXPsybot

## Prerequisites
1. GitHub repository with your code
2. Railway account (free tier available)
3. API keys for OpenAI and/or HuggingFace

## Step 1: Prepare Your Repository
✅ All files are ready:
- `app.py` - Main application
- `requirements.txt` - Dependencies
- `Procfile` - Railway deployment config
- `runtime.txt` - Python version
- `env.example` - Environment template

## Step 2: Get API Keys

### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Copy the key (starts with `sk-`)

### HuggingFace API Key
1. Go to https://huggingface.co/settings/tokens
2. Create new token
3. Copy the token

## Step 3: Deploy to Railway

1. **Connect Repository**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

2. **Configure Environment Variables**
   - In Railway dashboard, go to "Variables" tab
   - Add these variables:
     ```
     OPENAI_API_KEY=sk-your-actual-key-here
     HUGGINGFACE_API_KEY=hf-your-actual-token-here
     ```

3. **Deploy**
   - Railway will automatically detect Python app
   - Build process will install dependencies
   - App will be available at Railway URL

## Step 4: Verify Deployment

1. **Check Logs**
   - Monitor build logs for any errors
   - Look for successful startup message

2. **Test Application**
   - Upload a PDF document
   - Try different AI models
   - Test conversation functionality

## Troubleshooting

### Common Issues:

**1. Build Fails**
- Check `requirements.txt` syntax
- Ensure Python 3.11 compatibility

**2. App Won't Start**
- Verify Procfile syntax
- Check environment variables

**3. Model Errors**
- Ensure API keys are set correctly
- Check API key permissions

**4. Memory Issues**
- Railway free tier has 512MB RAM limit
- Consider upgrading for larger models

### Performance Tips:
- Use CPU-only torch (already configured)
- Start with smaller models
- Monitor memory usage

## Environment Variables Reference

| Variable | Required | Purpose |
|----------|----------|---------|
| `OPENAI_API_KEY` | Yes* | For GPT-3.5 and GPT-4o-mini models |
| `HUGGINGFACE_API_KEY` | Yes* | For flan-t5-xxl model |
| `PORT` | No | Railway sets automatically |
| `STREAMLIT_SERVER_PORT` | No | Streamlit configuration |

*At least one API key is required for the app to function.

## Support
If you encounter issues:
1. Check Railway logs
2. Verify environment variables
3. Test locally first
4. Check API key permissions 
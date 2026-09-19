# Render Deployment Guide

## Overview
This guide explains how to deploy the IoT Intrusion Detection demo app to Render.com.

## Prerequisites
- GitHub repository with the project code
- Render.com account (free tier available)
- Git LFS installed and configured (for large model files)

## Deployment Steps

### 1. Prepare Your Repository

Ensure your repository contains all necessary files:
- ✅ `app.py` - Flask backend
- ✅ `index.html` - Frontend interface  
- ✅ `requirements.txt` - Python dependencies
- ✅ `render.yaml` - Render configuration
- ✅ `Procfile` - Process configuration
- ✅ `saved_models/` - Trained models (with Git LFS)
- ✅ `.gitattributes` - Git LFS configuration

### 2. Verify Git LFS Setup

Check that your `.pkl` files are tracked by Git LFS:

```bash
git lfs ls-files
```

Expected output should show all `.pkl` files with LFS pointers.

### 3. Push Updated Code to GitHub

If you haven't already pushed the deployment files:

```bash
git add render.yaml Procfile .env.example requirements.txt app.py
git commit -m "feat: add Render deployment configuration"
git push origin master
```

### 4. Deploy to Render

#### Option A: Using Render Dashboard (Recommended)

1. **Create Render Account**
   - Go to https://render.com
   - Sign up for a free account
   - Connect your GitHub account

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Select your GitHub repository: `Lucid-spacex/Cyber-Threat-Detection`
   - Render will automatically detect the `render.yaml` configuration
   - Click "Create Web Service"

3. **Configure Build Settings**
   - **Runtime**: Python 3.9
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Branch**: `master`

4. **Environment Variables** (Optional)
   - `FLASK_ENV`: `production`
   - `FLASK_DEBUG`: `0`
   - `PORT`: `5000`

5. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy your app
   - Wait for the deployment to complete (usually 2-5 minutes)

#### Option B: Using Render CLI

```bash
# Install Render CLI
npm install -g @render-oss/render-cli

# Login to Render
render login

# Deploy
render deploy
```

### 5. Access Your Deployed App

Once deployment is complete:
- Render will provide a URL like: `https://cyber-threat-detection-demo.onrender.com`
- Open this URL in your browser to access the demo

## Important Notes

### Model File Size Considerations

**Issue**: The demo app includes large model files (~40MB total) which may cause:
- Longer deployment times
- Potential timeout issues on free tier
- Increased cold start times

**Solutions**:
1. **Current Setup**: Using Git LFS for model files
2. **Alternative**: Upload models to cloud storage (S3, Cloud Storage) and load from URL
3. **Optimization**: Further reduce model size if needed

### Dataset Dependency

**Current Behavior**: 
- Local deployment: Loads sample data from `CSV/CSV/` directory
- Render deployment: Uses hardcoded sample data (no CSV files in production)

**Why**: The full CICIoT2023 dataset is 8.33GB and not suitable for cloud deployment

**Result**: Demo still works with 3 hardcoded sample examples for demonstration purposes

### Performance Considerations

**Free Tier Limitations**:
- 512MB RAM limit
- 750 hours/month execution time
- Spin-down after 15 minutes of inactivity
- Cold start time: 30-60 seconds

**Expected Performance**:
- Initial load: 30-60 seconds (model loading)
- Prediction requests: <1 second
- Sample requests: <100ms

## Troubleshooting

### Build Failures

**Issue**: Build fails with dependency errors
```
Solution: 
- Check requirements.txt versions
- Ensure Python version compatibility
- Check Render build logs
```

**Issue**: Model loading fails
```
Solution:
- Verify saved_models/ directory exists
- Check file permissions
- Ensure Git LFS files are properly tracked
```

### Runtime Errors

**Issue**: 502 Bad Gateway / timeouts
```
Solution:
- Check if app is running (Render dashboard)
- Review application logs
- Increase timeout if model loading takes longer
```

**Issue**: Sample data not loading
```
Solution:
- The app will fallback to hardcoded samples
- This is expected behavior for production deployment
```

### Git LFS Issues

**Issue**: Large files not properly tracked
```
Solution:
git lfs install
git lfs track "*.pkl"
git add .gitattributes
git commit -m "Add Git LFS tracking"
git push
```

## Monitoring and Logs

### View Logs in Render Dashboard

1. Go to your Render dashboard
2. Select your web service
3. Click "Logs" tab
4. View real-time logs and deployment history

### Common Log Messages

**Successful Startup**:
```
Loading models and preprocessing components...
Models loaded successfully!
Top features: ['Header_Length', 'Tot sum', ...]
Loading sample data for examples...
CSV directory not found, using hardcoded sample data
Loaded 3 hardcoded sample rows
Starting Flask server...
```

**Error States**:
```
Error loading models: [specific error]
Error loading sample data: [specific error]
```

## Scaling and Production Considerations

### For Production Use

1. **Upgrade to Paid Tier**
   - More RAM and CPU
   - No spin-down
   - Better performance

2. **Use External Storage**
   - Upload models to S3/Cloud Storage
   - Load from URL instead of local files
   - Reduces deployment size

3. **Add Caching**
   - Cache model predictions
   - Use Redis for session management
   - Improve response times

4. **Add Authentication**
   - Protect endpoints with API keys
   - Add user authentication
   - Rate limiting

### Cost Estimates

**Free Tier**:
- $0/month
- Suitable for demos and testing
- Limitations: spin-down, resource constraints

**Starter Tier** ($7/month):
- More resources
- No spin-down
- Better for production demos

## Alternative Deployment Options

If Render doesn't meet your needs:

### Heroku
- Similar setup to Render
- Add `runtime.txt` for Python version
- Use Heroku CLI for deployment

### Railway
- Simple deployment process
- Good free tier
- Automatic SSL

### Vercel/Netlify
- Static hosting for frontend only
- Backend would need separate deployment
- Good for frontend demos

## Maintenance

### Updates and Redeployment

1. Make changes to code
2. Commit and push to GitHub
3. Render automatically detects changes
4. Redeploys automatically

### Monitoring

- Regularly check Render dashboard
- Monitor resource usage
- Review error logs
- Update dependencies as needed

## Support

For Render-specific issues:
- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
- Render Status: https://status.render.com

For project-specific issues:
- Check GitHub Issues
- Review project documentation
- Contact project maintainers

## Security Considerations

### For Academic Demos (Current Setup)
- ✅ No authentication required
- ✅ Public access acceptable
- ✅ No sensitive data exposure

### For Production Use
- ⚠️ Add authentication
- ⚠️ Use HTTPS (automatic on Render)
- ⚠️ Add rate limiting
- ⚠️ Validate inputs
- ⚠️ Add logging and monitoring

## Summary

The Render deployment provides:
- ✅ Easy cloud deployment
- ✅ Automatic HTTPS
- ✅ Git-based deployment
- ✅ Free tier available
- ✅ Suitable for academic demos
- ⚠️ Limited resources on free tier
- ⚠️ Model loading may cause cold starts
- ⚠️ Dataset dependency handled via hardcoded samples

For academic presentations, the free tier should be sufficient. For production use, consider upgrading to a paid tier or exploring alternative deployment options.
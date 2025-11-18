# Deploying INDMoney FAQ Assistant to Vercel (Frontend + Backend)

This guide explains how to deploy both the frontend and backend of the INDMoney FAQ Assistant to Vercel in a single app.

## Prerequisites

1. A Vercel account
2. A GitHub account
3. A Gemini API key (for AI features)

## Deployment Steps

### 1. Prepare Your Repository

Make sure your repository is pushed to GitHub:

```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### 2. Deploy to Vercel

1. Go to [Vercel](https://vercel.com) and sign in
2. Click "New Project"
3. Import your GitHub repository
4. Configure the project with these settings:
   - **Framework**: Other
   - **Root Directory**: Leave empty
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: Leave as default

### 3. Environment Variables

Add these environment variables in your Vercel project settings:

```
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 4. Deployment Configuration

The `vercel.json` file in your project root is already configured to:
- Build the frontend using Vite
- Serve the backend API from the same domain
- Route API requests to the Python backend

### 5. How It Works

- The frontend is built using Vite and served as static files
- The backend API is served by the Python server
- Both are deployed together in the same Vercel app
- API requests from the frontend are made to `/api/` endpoints

### 6. Custom Domain (Optional)

After deployment, you can add a custom domain in your Vercel project settings.

## Troubleshooting

### "Module not found" errors

Make sure all dependencies in `requirements.txt` are compatible with Vercel's Python runtime.

### Size Limit Issues

If you encounter size limit issues:
1. Ensure you're using the minimal `requirements.txt`
2. Remove any unnecessary dependencies
3. Consider using smaller alternatives for heavy libraries

### API Not Working

If the API endpoints aren't working:
1. Check the Vercel logs for errors
2. Ensure your `vercel.json` routes are correctly configured
3. Verify environment variables are set correctly

## Notes

- The current setup uses a minimal version of the Gemini service to reduce dependencies
- Some advanced RAG features may be limited due to dependency constraints on Vercel
- For production use, consider separating frontend and backend deployments for better scalability
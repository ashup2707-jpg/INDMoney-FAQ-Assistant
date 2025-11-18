# 🚀 Deployment Guide - INDMoney FAQ Assistant

## 📋 Prerequisites
- GitHub account
- Git installed locally
- Your Gemini API key

---

## 🔧 Step 1: Prepare Your Repository

### 1.1 Initialize Git (if not already done)
```bash
cd "/Users/sneha/Nextleap- INDMoney FAQ Assistant/INDMoney-FAQ-Assistant"
git init
```

### 1.2 Create .env.example (template for others)
Your `.env` file is already ignored. Create a template:
```bash
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env.example
```

### 1.3 Add all files to Git
```bash
git add .
git commit -m "Initial commit: INDMoney FAQ Assistant with RAG"
```

---

## 🌐 Step 2: Create GitHub Repository

### 2.1 Go to GitHub
1. Visit https://github.com/new
2. Repository name: `indmoney-faq-assistant` (or your choice)
3. Description: "AI-powered FAQ chatbot for HDFC mutual funds with RAG"
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license
6. Click **Create repository**

### 2.2 Link Local to GitHub
GitHub will show you commands. Use these:
```bash
git remote add origin https://github.com/YOUR_USERNAME/indmoney-faq-assistant.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## ☁️ Step 3: Deploy Options

### **Option A: Deploy on Render (Recommended - Free Tier)**

#### Backend (FastAPI)
1. Go to https://render.com
2. Sign up/login with GitHub
3. Click **New +** → **Web Service**
4. Connect your repository
5. Configure:
   - **Name**: `indmoney-faq-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**: Add `GEMINI_API_KEY=your_key`
6. Click **Create Web Service**

#### Frontend (React)
1. In Render, click **New +** → **Static Site**
2. Connect same repository
3. Configure:
   - **Name**: `indmoney-faq-app`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`
4. Update `frontend/vite.config.js`:
   ```js
   proxy: {
     '/api': {
       target: 'https://indmoney-faq-api.onrender.com',  // Your backend URL
       changeOrigin: true,
     }
   }
   ```
5. Click **Create Static Site**

---

### **Option B: Deploy on Railway (Easiest)**

1. Go to https://railway.app
2. Sign in with GitHub
3. Click **New Project** → **Deploy from GitHub repo**
4. Select your repository
5. Railway auto-detects Python + Node.js
6. Add environment variable: `GEMINI_API_KEY`
7. Railway will provide a URL automatically

---

### **Option C: Deploy on Vercel (Frontend) + Render (Backend)**

#### Frontend on Vercel
1. Go to https://vercel.com
2. Import your GitHub repository
3. Configure:
   - **Framework**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Deploy

#### Backend on Render (same as Option A)

---

## 🔑 Step 4: Environment Variables

For any deployment platform, add these environment variables:

```
GEMINI_API_KEY=AIzaSyC7gg3AfshflqtVlitDYAZCWy8Mtp9xHmI
```

⚠️ **IMPORTANT**: In production, use secrets management, not hardcoded keys!

---

## 📊 Step 5: Database Setup

### Option 1: Keep SQLite (Simple)
- SQLite database will be created automatically
- Data will reset on each deployment (ephemeral storage)

### Option 2: Use PostgreSQL (Production)
1. Add to `requirements.txt`:
   ```
   psycopg2-binary==2.9.9
   ```
2. Update `data_storage.py` to use PostgreSQL instead of SQLite
3. Add `DATABASE_URL` environment variable

---

## ✅ Step 6: Verify Deployment

1. Visit your deployed frontend URL
2. Test the chatbot
3. Check source links work
4. Verify RAG is functioning

---

## 📝 Quick Deploy Commands

```bash
# 1. Initialize and commit
cd "/Users/sneha/Nextleap- INDMoney FAQ Assistant/INDMoney-FAQ-Assistant"
git init
git add .
git commit -m "Initial commit: INDMoney FAQ Assistant"

# 2. Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/indmoney-faq-assistant.git
git branch -M main
git push -u origin main

# 3. Go to your deployment platform (Render/Railway/Vercel)
# 4. Connect GitHub repo
# 5. Add GEMINI_API_KEY environment variable
# 6. Deploy!
```

---

## 🛠️ Troubleshooting

### "Module not found" errors
- Ensure `requirements.txt` is in root directory
- Check build command includes `pip install -r requirements.txt`

### Frontend can't connect to backend
- Update API proxy URL in `vite.config.js`
- Check CORS settings in `api.py`

### ChromaDB errors
- ChromaDB needs persistent storage
- Run `python3 index_data.py` after first deployment

---

## 🎉 You're Ready!

Your INDMoney FAQ Assistant will be live at:
- **Frontend**: `https://your-app.vercel.app` (or Render/Railway URL)
- **Backend API**: `https://your-api.onrender.com` (or Railway URL)

Share the link and enjoy your deployed AI chatbot! 🚀

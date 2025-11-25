# 🚀 Quick Start: Streamlit Cloud Deployment (Recommended)

## 5-Minute Deploy

### Step 1: Push to GitHub
```bash
cd /mnt/d/coursesP/Resto
git remote add origin https://github.com/YOUR-USERNAME/restaurant-ai-dashboard.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud
1. Go to https://streamlit.io/cloud
2. Sign up with GitHub
3. Click "New app"
4. Select repo, branch (main), main file (app.py)
5. Click "Deploy"

### Step 3: Add Secrets
1. Click app settings (⚙️)
2. Click "Secrets"
3. Add these environment variables:
```
COLAB_API_URL=https://your-ngrok-url/
OPENROUTER_API_KEY=sk-or-v1-your-key
OPENROUTER_MODEL=openai/gpt-4o-mini
```
4. Save

### Done! 🎉
Your app is live at: `https://your-username-restaurant-ai-dashboard.streamlit.app`

---

## Alternative Platforms

- **Railway**: https://railway.app (Best paid option)
- **Render**: https://render.com (Good free tier)
- **Heroku**: https://heroku.com (Costs money now)
- **AWS/GCP**: Enterprise options

See **DEPLOYMENT.md** for full details on each platform.

---

## Why Not Vercel?
Vercel doesn't support long-running Python servers. Use Streamlit Cloud instead!

---

## Need Help?
See DEPLOYMENT.md for troubleshooting and detailed guides.

# 🚀 Deployment Guide - Restaurant AI Dashboard

## ⚡ Quick Comparison

| Platform | Cost | Setup Time | Difficulty | Best For |
|----------|------|-----------|-----------|----------|
| **Streamlit Cloud** | Free tier available | 2 min | ⭐ Very Easy | ✅ **Recommended** |
| **Heroku** | $7-50/month | 10 min | Easy | Production apps |
| **Railway** | $5+/month | 5 min | Easy | Dev & production |
| **Render** | Free tier available | 5 min | Easy | Side projects |
| **Vercel** | ❌ Not recommended | N/A | Hard | Next.js/React only |
| **AWS/GCP/Azure** | Variable | 30+ min | Hard | Enterprise |

---

## ✅ RECOMMENDED: Streamlit Cloud (FREE & EASIEST)

### Why Streamlit Cloud?
- ✅ Built specifically for Streamlit apps
- ✅ Free tier (no credit card needed)
- ✅ Automatic deploys from GitHub
- ✅ Custom domain support
- ✅ Environment variables management
- ✅ Instant scaling
- ✅ Official support

### Step-by-Step Setup

#### 1. Push to GitHub First
```bash
cd /mnt/d/coursesP/Resto

git remote add origin https://github.com/YOUR-USERNAME/restaurant-ai-dashboard.git
git branch -M main
git push -u origin main
```

#### 2. Go to Streamlit Cloud
1. Visit **https://streamlit.io/cloud**
2. Click **"Sign up with GitHub"**
3. Authorize Streamlit
4. Click **"New app"**

#### 3. Configure Your App
- **Repository**: Select `restaurant-ai-dashboard`
- **Branch**: `main`
- **Main file path**: `app.py`
- Click **"Deploy"** ✨

#### 4. Add Environment Variables
1. Go to your app settings (gear icon)
2. Click **"Secrets"**
3. Paste your `.env` content:
```
COLAB_API_URL=https://your-ngrok-url/
OPENROUTER_API_KEY=sk-or-v1-your-key-here
OPENROUTER_MODEL=openai/gpt-4o-mini
```
4. Save and redeploy

#### 5. Your App is Live! 🎉
URL format: `https://your-username-restaurant-ai-dashboard.streamlit.app`

---

## 🚀 Alternative: Heroku (Still Free Until Nov 2024)

### Setup Steps

#### 1. Install Heroku CLI
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

#### 2. Create Heroku App
```bash
heroku login
heroku create your-app-name
```

#### 3. Create Procfile
```bash
cat > Procfile << EOF
web: sh setup.sh && streamlit run app.py
EOF
```

#### 4. Create setup.sh
```bash
cat > setup.sh << EOF
mkdir -p ~/.streamlit/
echo "[theme]
primaryColor = \"#667eea\"
backgroundColor = \"#ffffff\"
secondaryBackgroundColor = \"#f0f2f6\"
textColor = \"#262730\"
font = \"sans serif\"

[server]
headless = true
port = \$PORT
enableXsrfProtection = false
" > ~/.streamlit/config.toml
EOF

chmod +x setup.sh
```

#### 5. Set Environment Variables
```bash
heroku config:set OPENROUTER_API_KEY=sk-or-v1-your-key-here
heroku config:set COLAB_API_URL=https://your-ngrok-url/
```

#### 6. Deploy
```bash
git push heroku main
```

#### 7. View Your App
```bash
heroku open
```

**Note**: Heroku free tier ended Nov 2024. Paid plans start at $7/month.

---

## 🚢 Alternative: Railway.app (Recommended After Streamlit Cloud)

### Setup Steps

#### 1. Go to Railway
- Visit **https://railway.app**
- Sign up with GitHub
- Click **"New Project"**
- Select **"Deploy from GitHub repo"**

#### 2. Select Your Repository
- Choose `restaurant-ai-dashboard`
- Authorize Railway

#### 3. Add Environment Variables
- Click on your deployment
- Go to **Variables**
- Add:
  - `OPENROUTER_API_KEY`
  - `COLAB_API_URL`
  - `OPENROUTER_MODEL`

#### 4. Add Start Command
In Railway dashboard, set start command:
```
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

#### 5. Deploy
Railway auto-deploys from GitHub pushes!

**Cost**: $5/month per deployment (trial credit available)

---

## 🎨 Alternative: Render.com (Good Free Tier)

### Setup Steps

#### 1. Go to Render
- Visit **https://render.com**
- Sign up with GitHub
- Click **"New +"**
- Select **"Web Service"**

#### 2. Connect Repository
- Authorize GitHub
- Select `restaurant-ai-dashboard`

#### 3. Configure
- **Name**: restaurant-ai-dashboard
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run app.py --server.port=10000`

#### 4. Add Environment Variables
- **OPENROUTER_API_KEY**: your-key
- **COLAB_API_URL**: your-url
- **OPENROUTER_MODEL**: openai/gpt-4o-mini

#### 5. Deploy
Click **"Create Web Service"**

**Cost**: Free tier (auto-sleeps), $7+/month for always-on

---

## ❌ Why NOT Vercel?

Vercel is optimized for:
- Next.js applications
- Static websites
- Serverless functions
- REST APIs

Vercel is **NOT suitable** for:
- ❌ Long-running processes (Streamlit needs persistence)
- ❌ WebSocket connections (Streamlit uses WebSockets)
- ❌ Stateful applications
- ❌ Server-side sessions

**If you really want Vercel**, you'd need to:
1. Convert to Flask/FastAPI
2. Host separately or use different stack
3. Much more complex than alternatives

**Bottom line**: Use Streamlit Cloud for Streamlit apps!

---

## 🔐 Environment Variables Setup

### For All Platforms:

1. **Get your API keys:**
   ```bash
   # OpenRouter API key
   # Get from: https://openrouter.ai/account/api-keys
   
   # Colab API URL (if using Colab backend)
   # From ngrok tunnel: https://your-unique-id.ngrok-free.dev/
   ```

2. **Never commit `.env` file** (it's in .gitignore)

3. **Set in deployment platform:**
   - Streamlit Cloud: Secrets tab
   - Heroku: `heroku config:set KEY=value`
   - Railway: Variables section
   - Render: Environment variables

---

## 📊 Deployment Checklist

Before deploying, verify:

```bash
# ✅ Code is clean
git status
# Should show: "working tree clean"

# ✅ All changes committed
git log --oneline
# Should show your commits

# ✅ requirements.txt is updated
cat requirements.txt
# Should have all dependencies

# ✅ .env is in .gitignore
cat .gitignore | grep .env
# Should show .env

# ✅ App works locally
streamlit run app.py
# Should run without errors
```

---

## 🎯 Recommended Deployment Path

### For Best Results:
1. **Push to GitHub** ✅ (Already done!)
2. **Use Streamlit Cloud** ✨ (Free, 2-minute setup)
3. **Monitor your app** 📊 (Check logs, performance)
4. **Scale when needed** 📈 (Paid tier if required)

### If You Want More Control:
1. **GitHub** (Done)
2. **Railway** or **Render** (Easy, affordable)
3. **Custom domain** (optional)
4. **Monitor & scale** (paid tiers)

---

## 🆘 Troubleshooting

### App won't start: "ModuleNotFoundError"
```bash
# Make sure all imports in app.py are in requirements.txt
pip freeze > requirements.txt
git add requirements.txt && git commit -m "Update requirements" && git push
```

### "No module named spacy"
```bash
# Add to requirements.txt:
spacy>=3.0
# Then download model in deployment

# For Streamlit Cloud, add to app.py at startup:
import subprocess
subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
```

### Environment variables not loading
- Double-check variable names are exact
- Restart the deployment after adding variables
- Check in app: `import os; print(os.getenv('KEY'))`

### App is too slow
- Check requirements.txt (remove unused packages)
- Reduce startup processes
- Cache expensive computations with `@st.cache_resource`

---

## 📈 Scaling Guide

### As Your App Grows:

**Free Tier (Streamlit Cloud):**
- ✅ Up to 1 GB RAM
- ✅ Enough for small datasets
- ✅ Good for demos

**Paid Options ($10-50/month):**
- 📈 More CPU/RAM
- 📈 Custom domains
- 📈 Priority support
- 📈 Higher concurrency

**Enterprise ($100+/month):**
- 🚀 Dedicated infrastructure
- 🚀 Load balancing
- 🚀 99.9% uptime SLA

---

## 🎉 Post-Deployment

After deployment:

1. **Test your app**
   - Click all tabs
   - Test with real data
   - Check error messages

2. **Share with users**
   - Direct link to deployed app
   - Add to portfolio
   - Share on social media

3. **Monitor performance**
   - Check deployment logs
   - Monitor API usage
   - Track errors

4. **Update regularly**
   - Push to GitHub
   - Auto-deploys to Streamlit Cloud
   - No manual redeploy needed

---

## 📚 Additional Resources

- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-cloud
- **Streamlit Deployment Guide**: https://docs.streamlit.io/deploy
- **Railway Docs**: https://docs.railway.app
- **Render Docs**: https://render.com/docs
- **Heroku Docs**: https://devcenter.heroku.com/articles/getting-started-with-python

---

## 🎯 My Recommendation

**Use Streamlit Cloud:**
- ✅ Free tier (no credit card)
- ✅ Designed for Streamlit
- ✅ 2-minute setup
- ✅ Auto-deploys from GitHub
- ✅ Perfect for your use case

**Next step**: Go to https://streamlit.io/cloud and deploy! 🚀

---

*Last updated: November 25, 2025*

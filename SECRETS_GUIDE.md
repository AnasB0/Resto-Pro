# 🔐 How to Add Secrets to Streamlit Cloud

## Step-by-Step Visual Guide

### Step 1: Go to Your Deployed App
1. Visit your Streamlit Cloud app URL: `https://your-username-restaurant-ai-dashboard.streamlit.app`
2. Look for the **Settings icon (⚙️)** in the top-right corner
3. Click it

![Location of settings icon](https://imgur.com/placeholder.png)

---

### Step 2: Click "Secrets" in the Menu

In the dropdown menu, you'll see:
- **Rerun app**
- **Settings** 
- **About**

Click on the **three-dot menu (⋯)** and select **"Settings"**

Or look for **"Secrets"** tab directly (varies by Streamlit version)

---

### Step 3: Open the Secrets Editor

In your app's settings, find the **"Secrets"** section and click **"Edit secrets"**

This opens a text editor where you can add environment variables.

---

### Step 4: Paste Your Secrets

Copy and paste ALL of these into the secrets editor:

```
COLAB_API_URL=https://your-ngrok-url-here.ngrok-free.dev/
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
OPENROUTER_MODEL=openai/gpt-4o-mini
```

**Replace:**
- `https://your-ngrok-url-here.ngrok-free.dev/` with your actual ngrok URL (if using Colab backend)
- `sk-or-v1-your-actual-key-here` with your real OpenRouter API key

---

### Step 5: Save

Click **"Save"** button at the bottom of the secrets editor.

---

### Step 6: App Auto-Restarts ✨

Streamlit automatically restarts your app to load the new secrets. You'll see a message: 
> "App is restarting..."

Wait 10-30 seconds for it to finish.

---

## 📋 What Are These Secrets?

### COLAB_API_URL
- **Purpose**: URL to your Colab/Flask backend server
- **Example**: `https://abc-123-def.ngrok-free.dev/`
- **How to get**: 
  - If running Colab backend, get from ngrok tunnel output
  - If not using Colab backend, you can leave it empty or use a placeholder
- **Optional?** Yes, only needed if you have a Colab server

### OPENROUTER_API_KEY
- **Purpose**: API authentication for GPT-4o-mini model
- **Example**: `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`
- **How to get**:
  1. Go to https://openrouter.ai/account/api-keys
  2. Create new API key
  3. Copy it (it starts with `sk-or-v1-`)
- **Optional?** No, needed for AI summaries

### OPENROUTER_MODEL
- **Purpose**: Which AI model to use for summaries
- **Value**: `openai/gpt-4o-mini`
- **Optional?** No, needed for AI summaries

---

## ✅ Verify Secrets Are Working

After saving and the app restarts:

1. **Go to your app** (refresh the page)
2. **Click the "Dish Analytics" tab**
3. **Upload or load a CSV** with reviews
4. **Generate an AI Summary** using the button

If you see a summary generated, your secrets are working! ✨

If you see an error about "API key" or "environment variable", the secrets didn't load correctly.

---

## 🆘 Troubleshooting

### "NameError: name 'OPENROUTER_API_KEY' is not defined"
- Secrets didn't save properly
- Try again: Settings → Secrets → paste all three → Save
- Wait for app to restart fully

### "401 Unauthorized" or "API key invalid"
- Your API key is wrong or expired
- Get a fresh one from https://openrouter.ai/account/api-keys
- Update the secret
- Save and wait for restart

### "Connection refused" for COLAB_API_URL
- Your ngrok tunnel is not running
- Start ngrok on your machine: `ngrok http 8000`
- Update the URL in secrets
- Save and restart

### App says "Secrets not loaded"
- Wait longer for restart (up to 1 minute)
- Refresh the page (Ctrl+R or Cmd+R)
- Try redeploying the app

---

## 🔒 Security Best Practices

✅ **DO:**
- Store secrets ONLY in Streamlit Cloud secrets
- Use environment variables in your code
- Never commit `.env` file to GitHub
- Rotate API keys regularly

❌ **DON'T:**
- Put secrets in your code
- Commit `.env` to GitHub
- Share your API keys
- Use the same key for multiple projects

---

## 📝 Example: How Your Code Uses These Secrets

In `app.py`, secrets are loaded like this:

```python
import os
from dotenv import load_dotenv

# Load from .env locally, or from Streamlit secrets in cloud
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
colab_url = os.getenv("COLAB_API_URL", "")
model = os.getenv("OPENROUTER_MODEL")
```

Streamlit Cloud automatically makes these available through `os.getenv()` without needing a `.env` file.

---

## 🎯 Quick Checklist

After adding secrets:

- [ ] All three secrets pasted in
- [ ] No typos in variable names
- [ ] Values are correct (API key, URLs)
- [ ] Click "Save"
- [ ] Wait for app to restart
- [ ] Test by generating an AI summary
- [ ] See summary appear = secrets working! ✨

---

## 📚 More Help

- **Streamlit Secrets Docs**: https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app#add-a-secret
- **OpenRouter API Docs**: https://openrouter.ai/docs
- **Can't find secrets button?** Try clicking the three dots (⋯) menu in top-right

---

If you're still stuck, reply with:
1. Screenshot of your Streamlit Cloud app
2. What error message you see
3. Which secret is having trouble (API key, URL, etc.)

I'm here to help! 🚀

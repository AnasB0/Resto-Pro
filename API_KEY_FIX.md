# 🔑 How to Fix: Invalid OpenRouter API Key (401 Error)

## What This Error Means
```
⚠️ API Error 401: {"error":{"message":"User not found.","code":401}}
```

Your API key is **invalid, expired, or incorrectly formatted**. The OpenRouter API can't find your account with that key.

---

## ✅ Solution: Get a New API Key

### Step 1: Go to OpenRouter Website
1. Visit: **https://openrouter.ai/account/api-keys**
2. Sign in with your account (create one if needed - it's free!)

### Step 2: Create a New API Key
1. Click **"Create Key"** button
2. Give it a name like "Resto-Pro"
3. Click **"Create"**
4. **Copy the full key** (starts with `sk-or-v1-`)

### Step 3: Add to Streamlit Cloud Secrets

1. **Go to your Streamlit Cloud app**
2. Click **"Manage app"** (bottom right)
3. Go to **"Settings"** → **"Secrets"**
4. **Edit secrets** and update this line:
   ```
   OPENROUTER_API_KEY=sk-or-v1-YOUR-NEW-KEY-HERE
   ```
   Replace `YOUR-NEW-KEY-HERE` with your actual key

5. **Save** the secrets
6. App will **auto-restart** ✨

### Step 4: Test It Works
1. Go to the **"Reviews"** tab in your app
2. Click **"Generate AI Insights"**
3. Should show summary (not error)

---

## ⚠️ Common Mistakes

### ❌ Mistake 1: Wrong Format
**Wrong:** `openrouter_api_key=sk-or-v1-xxx` (lowercase, with underscore)
**Right:** `OPENROUTER_API_KEY=sk-or-v1-xxx` (uppercase, with underscore)

### ❌ Mistake 2: Incomplete Key
**Wrong:** `OPENROUTER_API_KEY=sk-or-v1-` (incomplete)
**Right:** `OPENROUTER_API_KEY=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` (full key)

### ❌ Mistake 3: Extra Spaces
**Wrong:** `OPENROUTER_API_KEY = sk-or-v1-xxx` (spaces around =)
**Right:** `OPENROUTER_API_KEY=sk-or-v1-xxx` (no spaces)

### ❌ Mistake 4: Old/Revoked Key
- OpenRouter may have revoked your old key
- Always use a newly created key
- Test it works in OpenRouter dashboard first

---

## 🧪 How to Test Your Key (Before Adding to Streamlit)

Run this in your terminal locally:

```bash
curl -X POST "https://openrouter.ai/api/v1/chat/completions" \
  -H "Authorization: Bearer YOUR-KEY-HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-4o-mini",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

**If you see results**: ✅ Key works!
**If you see 401 error**: ❌ Key is invalid

---

## 💰 Do I Need to Pay for OpenRouter?

**Free tier available!**
- ✅ Free: ~$5 credit to try
- ✅ You can use it for testing
- ⚠️ Small restaurant = may use your free credit quickly
- 💳 Optional: Pay for more if needed

**Cost estimate:**
- AI summary per review: ~$0.001-0.005
- 50 reviews = ~$0.05-0.25
- Very affordable!

---

## 🔄 Step-by-Step Recap

1. **Get new key** → https://openrouter.ai/account/api-keys
2. **Copy the key** (full thing starting with sk-or-v1-)
3. **Update Streamlit Cloud secrets** with new key
4. **Wait for app to restart** (1-2 minutes)
5. **Test** → Go to Reviews tab, click "Generate AI Insights"
6. **Should work!** ✨

---

## 🆘 Still Getting 401?

### Checklist:
- [ ] Key is newly created (not old)
- [ ] Key starts with `sk-or-v1-`
- [ ] No extra spaces in secret
- [ ] Secret name is exactly `OPENROUTER_API_KEY`
- [ ] Tested key works locally (curl test above)
- [ ] App has restarted after updating secret
- [ ] Waited 2+ minutes for restart

### If Still Failing:
1. Delete the key from OpenRouter dashboard
2. Create a completely new key
3. Test with curl first
4. Then add to Streamlit Cloud
5. Wait 5 minutes for restart
6. Refresh app

---

## 📚 More Help

- **OpenRouter Docs**: https://openrouter.ai/docs
- **API Key Issues**: https://openrouter.ai/account/api-keys
- **Your App Logs**: Go to "Manage app" → "Logs" to see detailed errors

---

## 🎯 Quick Reference

**File:** `.env` (local) or Streamlit Cloud Secrets (production)
**Name:** `OPENROUTER_API_KEY`
**Value:** `sk-or-v1-...` (your actual key)
**Format:** Exactly as shown, no changes

Copy this exact format:
```
OPENROUTER_API_KEY=sk-or-v1-YOUR-FULL-KEY-HERE
OPENROUTER_MODEL=openai/gpt-4o-mini
```

That's it! Your AI summaries will work! 🚀

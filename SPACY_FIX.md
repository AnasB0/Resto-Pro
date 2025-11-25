# 🔧 Fix for spaCy Model Error on Streamlit Cloud

## The Problem
Streamlit Cloud shows: `OSError: [E050] Can't find model 'en_core_web_sm'`

This happens because the spaCy language model isn't installed by default.

## The Solution: Two Approaches

### ✅ RECOMMENDED: Manual Installation (Most Reliable)

1. **Reboot your Streamlit Cloud app:**
   - Go to your app URL
   - Click **"Manage app"** (bottom right corner)
   - Click **"Reboot app"** button
   - Wait for it to restart

2. **After reboot, the app will:**
   - Show an info message about installing the model
   - Download the spaCy model (takes 1-2 minutes)
   - Work normally after

3. **If it still fails:**
   - Click "Manage app" → "Settings" → "Advanced settings"
   - Click "Rerun app"

---

### Alternative: Deploy with Pre-configured Environment

If the above doesn't work, follow these steps:

1. **In your GitHub repo, add a `.streamlit/startup.sh` file:**
   ```bash
   #!/bin/bash
   python -m spacy download en_core_web_sm
   exit 0
   ```

2. **Redeploy from GitHub:**
   - On Streamlit Cloud, go to "Manage app"
   - Click "Reboot app"
   - Choose "Deploy from GitHub"

---

## 🕐 First Load Takes Time

**First load: 2-5 minutes** ⏳
- Streamlit Cloud downloads the spaCy model
- This is a one-time process
- After that, loading is instant!

**Signs it's working:**
- ✅ You see a blue "info" box about downloading the model
- ✅ You see a spinner/loading indicator
- ✅ After 2-3 minutes, the app loads with all 5 tabs

---

## 🆘 If You Still See Errors

**Error: "CalledProcessError"**
- Solution: Manual reboot (see above)
- Click "Manage app" → "Reboot app"

**Error: "Can't find model en_core_web_sm"**
- Solution: Refresh page (Ctrl+R) and wait
- The model is downloading in the background
- This takes 2-3 minutes, be patient!

**Error: "Permission denied"**
- Solution: Go to "Manage app" settings
- Click "Settings" → "Advanced" → Check disk space
- Sometimes Cloud needs to clear cache

---

## ✅ Verify It's Working

After successful deployment:

1. **Go to your app URL**
2. **Click the "Dish Analytics" tab**
3. **You should see:**
   - ✅ All data loaded
   - ✅ Charts displaying
   - ✅ No error messages

If you see this, the spaCy model loaded successfully! 🎉

---

## 📋 Checklist Before Redeploying

- [ ] All changes committed to GitHub
- [ ] Push all commits to main branch
- [ ] Go to Streamlit Cloud
- [ ] Click "Manage app"
- [ ] Click "Reboot app"
- [ ] Wait 3-5 minutes for first load
- [ ] Test by clicking tabs and loading data

---

## 🚀 Next Steps

1. **Reboot your app** (click "Manage app" → "Reboot app")
2. **Wait 2-3 minutes** for the model to download
3. **Refresh your browser** (Ctrl+R)
4. **Test the app** by clicking tabs

The app should work perfectly after! ✨

---

## 📞 Still Stuck?

If the app still doesn't work after rebooting:

1. Click "Manage app"
2. Scroll down to "Logs"
3. Share the error message
4. Try deploying again from GitHub

99% of the time, a simple reboot fixes this! 🔧

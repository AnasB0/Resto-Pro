import streamlit as st

# Streamlit Cloud deployment - this is the recommended way
# Vercel doesn't directly support Streamlit, so we'll use Streamlit Cloud instead

st.error("""
⚠️ **Important:** Streamlit apps cannot be deployed directly to Vercel.

**Recommended Solution: Use Streamlit Cloud (Free & Easy)**

Streamlit Cloud is the official, easiest way to deploy Streamlit apps:
1. Push your code to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app" and connect your GitHub repo
4. Select app.py
5. Your app goes live in 2 minutes!

**Alternative Options:**

1. **Heroku** - Great for Streamlit apps
2. **Railway** - Modern, simple deployment
3. **Render** - Easy with custom scripts
4. **PythonAnywhere** - Python-focused hosting
5. **AWS/GCP/Azure** - Advanced options

See DEPLOYMENT.md for detailed instructions for each platform.
""")

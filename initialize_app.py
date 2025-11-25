"""
Initialize spaCy model on Streamlit Cloud startup.
This script runs before the main app loads.
"""

import subprocess
import sys
import os

def setup():
    """Download spaCy model if not present"""
    try:
        import spacy
        try:
            spacy.load("en_core_web_sm")
            print("✅ spaCy model already available")
        except OSError:
            print("📥 Downloading spaCy model... (this may take a few minutes)")
            subprocess.run(
                [sys.executable, "-m", "spacy", "download", "en_core_web_sm"],
                check=True,
                timeout=600
            )
            print("✅ spaCy model downloaded successfully")
    except Exception as e:
        print(f"⚠️ Could not download spaCy model: {e}")
        print("The app will attempt to load without it, but NLP features may be limited")

if __name__ == "__main__":
    setup()

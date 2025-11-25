#!/usr/bin/env python3
"""
Pre-installation script for Streamlit Cloud
Installs required spaCy language model
"""

import subprocess
import sys
import os

def install_spacy_model():
    """Install spaCy language model"""
    try:
        import spacy
        try:
            spacy.load("en_core_web_sm")
            print("✅ spaCy model already installed")
            return True
        except OSError:
            print("📥 Installing spaCy language model...")
            result = subprocess.run(
                [sys.executable, "-m", "spacy", "download", "en_core_web_sm"],
                capture_output=True,
                timeout=300,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ spaCy model installed successfully")
                return True
            else:
                print(f"❌ Failed to install model")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
                return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = install_spacy_model()
    sys.exit(0 if success else 1)

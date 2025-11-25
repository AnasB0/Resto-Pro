#!/bin/bash
# Post-installation script for Streamlit Cloud
# Downloads required spaCy language model

echo "🔧 Setting up spaCy language model..."
python -m spacy download en_core_web_sm

if [ $? -eq 0 ]; then
    echo "✅ spaCy model installed successfully"
else
    echo "⚠️ Warning: spaCy model installation may have issues"
    echo "The app will try to download it on first run"
fi

exit 0

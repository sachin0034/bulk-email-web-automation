#!/bin/bash

# Build script for Maven Email Automation
# This script can be used for local testing and deployment preparation

echo "🚀 Building Maven Email Automation..."

# Check if running in server environment
if [ "$RENDER" = "true" ] || [ "$HEROKU" = "true" ] || [ "$DOCKER" = "true" ]; then
    echo "🌐 Detected server environment"
    
    # Install system dependencies
    echo "📦 Installing system dependencies..."
    apt-get update
    apt-get install -y wget gnupg unzip curl
    
    # Install Google Chrome
    echo "🔧 Installing Google Chrome..."
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
    apt-get update
    apt-get install -y google-chrome-stable
    
    # Install ChromeDriver
    echo "📥 Installing ChromeDriver..."
    CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | awk -F'.' '{print $1}')
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}"
    unzip /tmp/chromedriver.zip -d /usr/local/bin/
    chmod +x /usr/local/bin/chromedriver
    rm /tmp/chromedriver.zip
    
    echo "✅ Chrome and ChromeDriver installed successfully"
else
    echo "💻 Running in local environment"
fi

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Build completed successfully!"
echo "🚀 Ready to run: streamlit run main.py"

# 🪟 Windows Local Usage Guide

## 🎯 **What This Fixes**

- ❌ Chrome driver "unexpectedly exited" errors on Windows
- ❌ Linux path errors (`/usr/local/bin/chromedriver` not found)
- ❌ Chrome binary location issues
- ✅ **Now works on Windows locally!**

## 🚀 **Quick Start (Windows)**

### **Step 1: Install Dependencies**

```bash
# Make sure you have Python 3.8+ installed
pip install -r requirements.txt
```

### **Step 2: Install Chrome Browser**

- Download and install [Google Chrome](https://www.google.com/chrome/) if not already installed
- Make sure Chrome is in your system PATH

### **Step 3: Run the Application**

```bash
streamlit run main.py
```

## 🔧 **What Changed**

### **Environment Detection**

- ✅ **Automatically detects Windows vs Linux**
- ✅ **Uses appropriate Chrome options for each platform**
- ✅ **No more Linux path errors on Windows**

### **Windows-Specific Configuration**

- ✅ **Uses `--start-maximized` instead of `--headless`**
- ✅ **Uses Windows temp directories for user data**
- ✅ **Optimized for local Windows development**

### **Chrome Driver Strategy**

- ✅ **webdriver-manager first** (most reliable on Windows)
- ✅ **System ChromeDriver fallback** (for Linux/Render)
- ✅ **Direct initialization** (final fallback)

## 🧪 **Testing on Windows**

### **1. Test Chrome Setup**

1. Open the app in your browser
2. Go to sidebar → "🧪 Chrome Driver Test"
3. Click "Test Chrome Setup"
4. Should show: "✅ Chrome driver is working!"

### **2. Test Email Extraction**

1. Enter your OpenAI API key
2. Upload a CSV file
3. Click "🚀 Extract Emails"
4. Should work immediately

### **3. Test Automation**

1. Extract emails from CSV
2. Enter Maven URL
3. Start automation
4. Watch Chrome browser open and automate

## 🎯 **Expected Results on Windows**

- ✅ **Chrome opens in a new window** (not headless)
- ✅ **Automation runs visibly** (you can see what's happening)
- ✅ **No Linux path errors**
- ✅ **Fast startup** (no Chrome installation needed)

## 🚨 **Troubleshooting Windows Issues**

### **Issue 1: Chrome Not Found**

**Error**: `Chrome browser not found`
**Solution**:

- Install Google Chrome from [google.com/chrome](https://www.google.com/chrome/)
- Make sure it's in your system PATH

### **Issue 2: ChromeDriver Download Fails**

**Error**: `Failed to download ChromeDriver`
**Solution**:

- Check your internet connection
- Try running as administrator
- Check Windows Defender/firewall settings

### **Issue 3: Permission Errors**

**Error**: `Access denied` or `Permission error`
**Solution**:

- Run Command Prompt as Administrator
- Check Windows User Account Control settings

## 🔄 **Deployment Options**

### **Local Windows Development** ✅

- Fast development and testing
- Visible automation (Chrome opens in window)
- Easy debugging
- **Use this guide**

### **Render Deployment** ✅

- Production deployment
- Headless automation
- Chrome installed during build
- **Use DEPLOYMENT_GUIDE.md**

### **Streamlit Cloud** ❌

- No automation features
- Email extraction only
- **Use STREAMLIT_CLOUD_DEPLOYMENT.md**

## 📊 **Performance on Windows**

- **Startup Time**: 5-10 seconds
- **Chrome Launch**: 2-5 seconds
- **Email Processing**: 2-5 seconds per email
- **Memory Usage**: Lower than Linux (no headless overhead)

## 🎉 **Success Checklist for Windows**

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Google Chrome installed
- [ ] App runs (`streamlit run main.py`)
- [ ] Chrome test passes
- [ ] Email extraction works
- [ ] Automation runs successfully

---

**🎯 Goal**: Run Maven automation locally on Windows without Chrome driver errors!

**⏱️ Time**: 5-10 minutes setup

**💡 Pro Tip**: On Windows, you'll see Chrome open and watch the automation happen in real-time!

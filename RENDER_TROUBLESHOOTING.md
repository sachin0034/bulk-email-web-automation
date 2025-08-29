# 🚨 Render Deployment Troubleshooting Guide

## 🎯 **Fix for "Publish directory does not exist" Error**

### **Error Message:**

```
==> Publish directory streamlit run main.py does not exist!
==> Build failed 😞
```

## 🔧 **Solution 1: Use render.yaml (Recommended)**

### **Step 1: Ensure render.yaml is in your repository root**

```bash
your-repo/
├── main.py
├── requirements.txt
├── render.yaml          # ← MUST be in root directory
├── .streamlit/
│   └── config.toml
└── README.md
```

### **Step 2: Push to GitHub**

```bash
git add .
git commit -m "Fixed render.yaml configuration"
git push origin main
```

### **Step 3: Deploy on Render**

1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repository
4. **Render will auto-detect render.yaml**
5. Click "Create Web Service"

## 🔧 **Solution 2: Manual Render Configuration**

If `render.yaml` doesn't work, use manual configuration:

### **Step 1: Create Web Service**

1. Go to Render dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repository

### **Step 2: Configure Service**

- **Name**: `maven-email-automation`
- **Environment**: `Python`
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: Leave **EMPTY** (this is important!)
- **Build Command**: Leave **EMPTY** (render.yaml handles this)
- **Start Command**: Leave **EMPTY** (render.yaml handles this)

### **Step 3: Environment Variables**

Add these manually:

```
RENDER=true
PYTHON_VERSION=3.11
CHROME_BIN=/usr/bin/google-chrome
CHROMEDRIVER_PATH=/usr/local/bin/chromedriver
DISPLAY=:99
```

## 🚨 **Common Causes of "Publish directory" Error**

### **Cause 1: Wrong Build Command**

❌ **Wrong**: `streamlit run main.py`
✅ **Correct**: Leave empty (render.yaml handles it)

### **Cause 2: Wrong Start Command**

❌ **Wrong**: `streamlit run main.py`
✅ **Correct**: Leave empty (render.yaml handles it)

### **Cause 3: Root Directory Set**

❌ **Wrong**: Setting root directory to anything
✅ **Correct**: Leave root directory empty

### **Cause 4: render.yaml Not in Root**

❌ **Wrong**: render.yaml in subdirectory
✅ **Correct**: render.yaml must be in repository root

## 🔍 **Verify Your Repository Structure**

### **✅ Correct Structure:**

```
your-repo/
├── main.py
├── requirements.txt
├── render.yaml          # ← Root level
├── .streamlit/
│   └── config.toml
└── README.md
```

### **❌ Wrong Structure:**

```
your-repo/
├── src/
│   ├── main.py
│   └── render.yaml      # ← Wrong! Not in root
├── requirements.txt
└── README.md
```

## 🧪 **Test Your Configuration**

### **Step 1: Check render.yaml Syntax**

```yaml
services:
  - type: web
    name: maven-email-automation
    env: python
    plan: free
    # ... rest of configuration
```

### **Step 2: Validate YAML**

Use an online YAML validator to check syntax

### **Step 3: Test Locally**

```bash
# Test if your app runs locally
streamlit run main.py
```

## 🚀 **Alternative: Use Render's Auto-Detect**

### **Step 1: Remove render.yaml**

```bash
git rm render.yaml
git commit -m "Remove render.yaml for auto-detect"
git push origin main
```

### **Step 2: Let Render Auto-Detect**

1. Create new Web Service
2. Connect repository
3. Render will auto-detect Python app
4. Set environment variables manually

### **Step 3: Manual Configuration**

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run main.py --server.port $PORT --server.address 0.0.0.0`

## 🔄 **Complete Reset Process**

### **Step 1: Clean Repository**

```bash
# Remove render.yaml if it exists
git rm render.yaml
git commit -m "Clean repository for Render auto-detect"
git push origin main
```

### **Step 2: Delete Render Service**

1. Go to Render dashboard
2. Delete existing service
3. Start fresh

### **Step 3: Create New Service**

1. New Web Service
2. Connect repository
3. Let Render auto-detect
4. Configure manually

## 📊 **Expected Results**

### **After Successful Fix:**

- ✅ **Build starts** (no publish directory error)
- ✅ **Chrome installation** begins
- ✅ **Python dependencies** install
- ✅ **App deploys** successfully

### **Build Time:**

- **First deployment**: 5-10 minutes (Chrome installation)
- **Subsequent deployments**: 2-3 minutes

## 🆘 **Still Having Issues?**

### **Check These:**

1. **Repository structure** - render.yaml in root?
2. **YAML syntax** - valid YAML format?
3. **GitHub connection** - repository accessible?
4. **Branch name** - correct branch selected?
5. **File permissions** - files readable?

### **Get Help:**

- Check [Render documentation](https://render.com/docs)
- Look at build logs for specific errors
- Try the manual configuration approach

---

**🎯 Goal**: Fix the "Publish directory" error and deploy successfully!

**💡 Pro Tip**: The "Publish directory" error usually means Render is confused about your build/start commands. Using render.yaml or leaving them empty usually fixes it!

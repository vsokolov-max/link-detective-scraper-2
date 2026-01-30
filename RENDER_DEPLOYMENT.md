# 🚀 Deploy to Render.com - Step by Step

## Why Render.com?
- ✅ **Works reliably** with Chrome/Selenium
- ✅ **$7/month** only (or FREE with limits)
- ✅ **Easy setup** - 10 minutes
- ✅ **Auto HTTPS**
- ✅ **No Chrome issues** - just works!

---

## 📋 Step-by-Step Guide

### Step 1: Prepare Files

Create a GitHub repository with these files:

1. **`streamlit_app.py`** (use streamlit_app_render.py)
2. **`requirements.txt`**:
```
streamlit>=1.28.0
selenium>=4.15.0
pandas>=2.0.0
```

3. **`render.yaml`**:
```yaml
services:
  - type: web
    name: linkdetective-scraper
    env: python
    region: oregon
    plan: starter
    buildCommand: |
      apt-get update
      apt-get install -y chromium chromium-driver
      pip install -r requirements.txt
    startCommand: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

### Step 2: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/linkdetective-scraper.git
git push -u origin main
```

### Step 3: Deploy to Render

1. Go to: https://render.com/
2. Sign up (free)
3. Click **"New +"** → **"Blueprint"**
4. Connect your GitHub repository
5. Render will detect `render.yaml`
6. Click **"Apply"**
7. Wait 5-10 minutes for build

### Step 4: Done! 🎉

Your app will be live at:
```
https://linkdetective-scraper.onrender.com
```

---

## 💰 Pricing

### FREE Plan:
- ✅ Works but spins down after 15 min of inactivity
- ✅ 750 hours/month free
- ⚠️ Slow cold starts

### Starter Plan ($7/month):
- ✅ Always on
- ✅ Fast performance
- ✅ Custom domain
- ✅ No cold starts

**Recommended:** Starter Plan

---

## 🔧 Configuration

### Environment Variables (Optional)

In Render dashboard → Environment:

```
PYTHON_VERSION=3.11.7
STREAMLIT_SERVER_HEADLESS=true
```

### Custom Domain

1. Render dashboard → Settings → Custom Domain
2. Add your domain
3. Update DNS records

---

## 🐛 Troubleshooting

### Issue: Build fails
**Solution:** Check build command syntax in `render.yaml`

### Issue: App crashes on startup
**Solution:** Check logs in Render dashboard

### Issue: Chrome not found
**Solution:** Verify build command installs chromium and chromium-driver

### Issue: Slow performance
**Solution:** Upgrade to Starter plan ($7/mo)

---

## 📊 Monitoring

### View Logs:
Render Dashboard → Your Service → Logs

### Metrics:
Render Dashboard → Your Service → Metrics

---

## 🔄 Updates

### Auto-deploy from GitHub:
Any push to `main` branch auto-deploys!

### Manual deploy:
Render Dashboard → Your Service → Manual Deploy

---

## 🎯 Complete Example Repository Structure

```
linkdetective-scraper/
├── streamlit_app.py
├── requirements.txt
├── render.yaml
└── README.md
```

---

## ✅ Verification Checklist

Before going live:

- [ ] GitHub repo created
- [ ] All 3 files committed
- [ ] Render account created
- [ ] Blueprint deployed
- [ ] App URL accessible
- [ ] Test scraping works
- [ ] (Optional) Custom domain added
- [ ] (Optional) Upgraded to Starter plan

---

## 🎉 Success!

Your LinkDetective Scraper is now:
- ✅ Online 24/7
- ✅ Accessible from anywhere
- ✅ No installation for users
- ✅ Just share the URL!

Example usage for your team:
1. Open: https://your-app.onrender.com
2. Paste LinkDetective URL
3. Click "Start Scraping"
4. Download CSV
5. Done!

---

## 💡 Pro Tips

### 1. Add Password Protection

Add to top of `streamlit_app.py`:
```python
import streamlit as st

if "authenticated" not in st.session_state:
    password = st.text_input("Password:", type="password")
    if st.button("Login"):
        if password == "your-secret-password":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Wrong password")
    st.stop()
```

### 2. Rate Limiting

Prevent abuse:
```python
import time
from datetime import datetime, timedelta

if 'last_run' not in st.session_state:
    st.session_state.last_run = datetime.now() - timedelta(minutes=10)

if datetime.now() - st.session_state.last_run < timedelta(minutes=5):
    st.error("Wait 5 minutes between requests")
    st.stop()

st.session_state.last_run = datetime.now()
```

### 3. Usage Analytics

Add Google Analytics ID in Streamlit config.

---

## 📞 Support

Need help?
- Render Docs: https://render.com/docs
- Render Community: https://community.render.com/

---

## 🔥 Quick Deploy Commands

```bash
# Clone template
git clone https://github.com/YOUR_USERNAME/linkdetective-scraper.git
cd linkdetective-scraper

# Make changes
# ... edit files ...

# Deploy
git add .
git commit -m "Update"
git push

# Render auto-deploys! 🚀
```

---

## ✨ Summary

**Time to deploy:** 10 minutes
**Cost:** $7/month (or FREE with limits)
**Reliability:** ⭐⭐⭐⭐⭐
**Difficulty:** Easy

**This is the best solution for your case!**

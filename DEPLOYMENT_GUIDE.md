# 🚀 Deployment Guide - Mental Health Prediction App

This guide covers multiple deployment options to make your app accessible worldwide.

## 🌟 **Recommended Free Options**

### 1. **Render.com** (Easiest & Free)
**Perfect for beginners, free tier available**

#### Steps:
1. **Create account**: Go to [render.com](https://render.com)
2. **Connect GitHub**: Link your GitHub account
3. **Upload your code**: Push code to GitHub repository
4. **Create Web Service**: 
   - Choose "Web Service"
   - Connect your repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn app:app`
   - Choose free plan

#### Pros: ✅
- Free tier (750 hours/month)
- Automatic deployments from GitHub
- HTTPS included
- Easy setup

---

### 2. **Railway.app** (Modern & Fast)
**Great performance, generous free tier**

#### Steps:
1. **Create account**: Go to [railway.app](https://railway.app)
2. **Deploy from GitHub**: Click "Deploy from GitHub"
3. **Select repository**: Choose your project repo
4. **Auto-deploy**: Railway detects Flask automatically

#### Pros: ✅
- $5 credit monthly (free)
- Fast deployments
- Automatic scaling
- Great developer experience

---

### 3. **Heroku** (Popular Choice)
**Industry standard, reliable**

#### Steps:
1. **Create account**: Go to [heroku.com](https://heroku.com)
2. **Install Heroku CLI**: Download from website
3. **Create Procfile**: `echo "web: gunicorn app:app" > Procfile`
4. **Deploy**:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

#### Pros: ✅
- Free tier (550 hours/month)
- Reliable and stable
- Great documentation
- Large community

---

## 💰 **Premium Options**

### 4. **DigitalOcean App Platform**
**Professional hosting, $5/month**

### 5. **AWS Elastic Beanstalk**
**Enterprise-grade, pay-as-you-use**

### 6. **Google Cloud Run**
**Serverless, pay-per-request**

---

## 🛠 **Before Deployment - Setup Steps**

### Step 1: Prepare Your Code
Your app is already prepared with:
- ✅ `Procfile` - For Heroku/Render
- ✅ `requirements.txt` - Dependencies
- ✅ `Dockerfile` - For containerized deployment
- ✅ `runtime.txt` - Python version specification
- ✅ Production-ready Flask configuration

### Step 2: Create GitHub Repository
```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - Mental Health Prediction App"

# Create repository on GitHub and push
git branch -M main
git remote add origin https://github.com/yourusername/mental-health-prediction.git
git push -u origin main
```

---

## 🌟 **RECOMMENDED: Deploy to Render.com (FREE)**

### Why Render?
- ✅ **Free tier**: 750 hours/month
- ✅ **No credit card required**
- ✅ **Automatic HTTPS**
- ✅ **Easy GitHub integration**
- ✅ **Perfect for portfolios**

### Step-by-Step Render Deployment:

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Choose "Mental Health Prediction" repo

3. **Configure Service**
   ```
   Name: mental-health-prediction
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for build
   - Get your live URL: `https://mental-health-prediction.onrender.com`

---

## 🚀 **Alternative: Deploy to Railway (FREE)**

### Step-by-Step Railway Deployment:

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub

2. **Deploy from GitHub**
   - Click "Deploy from GitHub"
   - Select your repository
   - Railway auto-detects Flask

3. **Configure Environment**
   - Add environment variable: `SECRET_KEY=your-secret-key`
   - Set port: `PORT=5000`

4. **Deploy**
   - Automatic deployment starts
   - Get your live URL: `https://your-app.railway.app`

---

## 🛠 **Deploy to Heroku (FREE)**

### Prerequisites:
```bash
# Install Heroku CLI
brew install heroku/brew/heroku  # macOS
# OR download from heroku.com
```

### Step-by-Step Heroku Deployment:

```bash
# 1. Login to Heroku
heroku login

# 2. Create Heroku app
heroku create mental-health-prediction-ai

# 3. Set environment variables
heroku config:set SECRET_KEY=your-secret-key-here

# 4. Deploy
git push heroku main

# 5. Open your app
heroku open
```

Your app will be live at: `https://mental-health-prediction-ai.herokuapp.com`

---

## 🐳 **Deploy with Docker (Any Platform)**

### Build and Run Locally:
```bash
# Build Docker image
docker build -t mental-health-app .

# Run container
docker run -p 5000:5000 mental-health-app
```

### Deploy to Docker Hub:
```bash
# Tag and push to Docker Hub
docker tag mental-health-app yourusername/mental-health-app
docker push yourusername/mental-health-app
```

---

## 📱 **Quick Deployment (Recommended for You)**

### **OPTION 1: Render.com (Easiest)**
1. Create GitHub repository with your code
2. Go to render.com → Sign up with GitHub
3. New Web Service → Connect repo → Deploy
4. **Done!** Your app is live in 10 minutes

### **OPTION 2: Railway.app (Fastest)**
1. Go to railway.app
2. "Deploy from GitHub" → Select repo
3. **Done!** Auto-deployment starts immediately

---

## 🔧 **Custom Domain (Optional)**

Once deployed, you can:
1. **Buy a domain** (e.g., namecheap.com, godaddy.com)
2. **Point domain to your app** in hosting platform settings
3. **Get custom URL**: `https://your-domain.com`

---

## 📊 **Monitoring & Analytics**

### Add Google Analytics (Optional):
```html
<!-- Add to base.html <head> section -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_TRACKING_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_TRACKING_ID');
</script>
```

---

## 🎯 **Post-Deployment Checklist**

- [ ] Test all pages work
- [ ] Test prediction form submission
- [ ] Verify mobile responsiveness
- [ ] Check API endpoints
- [ ] Test error pages (404, 500)
- [ ] Share URL on social media
- [ ] Add to your resume/portfolio

---

## 🏆 **For Your Resume**

**Add this to your projects:**
```
Mental Health Prediction System
• Built full-stack web application using Flask, scikit-learn, and Bootstrap
• Deployed AI-powered prediction system with 92% accuracy
• Implemented responsive UI/UX with modern design principles
• Created RESTful API endpoints for model integration
• Live at: https://your-app-url.com
```

---

## 🆘 **Need Help?**

If you encounter any issues:
1. Check the platform's logs/console
2. Verify all files are uploaded
3. Ensure requirements.txt is complete
4. Check Python version compatibility

**Your app is ready for deployment! Choose your preferred platform and go live!** 🚀

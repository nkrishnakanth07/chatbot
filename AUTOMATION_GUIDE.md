# 🤖 Automation Scripts & CI/CD Guide

This project includes several automation scripts to make deployment and development easier.

## 📜 Available Scripts

### 1. deploy.sh / deploy.bat
**Purpose:** Automated Git commit and push to GitHub

**Usage:**
```bash
# Mac/Linux
./deploy.sh

# Windows
deploy.bat
```

**What it does:**
1. Checks for changes in your code
2. Shows you what will be committed
3. Asks for commit message (or uses timestamp)
4. Commits changes locally
5. Asks if you want to push to GitHub
6. Pushes to GitHub (triggers auto-deploy on Vercel/Render)

**When to use:**
- After making changes to your code
- Want quick deployment without typing Git commands
- Perfect for small updates

---

### 2. vercel.json
**Purpose:** Configuration for Vercel deployment

**What it contains:**
- Frontend build commands
- Backend serverless function config
- Environment variable mapping
- Routing rules

**You don't need to run this** - Vercel reads it automatically

**Customization:**
```json
{
  "functions": {
    "api/*.py": {
      "runtime": "python3.9",
      "maxDuration": 60  // Increase for large PDFs
    }
  }
}
```

---

### 3. render.yaml
**Purpose:** Configuration for Render deployment

**What it contains:**
- Backend service configuration
- Frontend static site configuration
- Environment variables
- Auto-deploy settings

**How to use:**
1. Push to GitHub
2. In Render dashboard, select "Blueprint"
3. Point to your repo
4. Render will read `render.yaml` and create services automatically

**Customization:**
```yaml
services:
  - type: web
    name: chatbot-backend
    plan: free  # Change to 'starter' for $7/month (no sleep)
```

---

### 4. GitHub Actions Workflows

Located in `.github/workflows/`

#### deploy-vercel.yml
**Purpose:** Auto-deploy to Vercel on every push

**Triggers:**
- Push to main/master branch
- Pull requests

**What it does:**
1. Runs tests
2. Builds frontend
3. Deploys to Vercel
4. Comments on PRs with preview URL

**Setup Required:**
Add these secrets to GitHub repo settings:
- `VERCEL_TOKEN` - Get from https://vercel.com/account/tokens
- `VERCEL_ORG_ID` - In Vercel project settings
- `VERCEL_PROJECT_ID` - In Vercel project settings

#### deploy-render.yml
**Purpose:** Auto-deploy to Render on every push

**Triggers:**
- Push to main/master branch
- Manual trigger (workflow_dispatch)

**Setup Required:**
Add this secret to GitHub repo settings:
- `RENDER_DEPLOY_HOOK` - Get from Render service settings

#### ci.yml
**Purpose:** Run tests and checks on every push/PR

**What it does:**
1. Lints Python code
2. Checks dependencies
3. Builds frontend
4. Runs security scans

**Triggers:**
- All pushes
- All pull requests

---

## 🚀 Quick Start - Choose Your Path

### Path 1: Manual Deployment (Simplest)

**No automation needed** - just follow the deployment guides:
- Vercel: See `VERCEL_DEPLOY.md`
- Render: See `DEPLOYMENT.md`

### Path 2: Automated Git Pushes

**Use the deploy scripts:**

1. **First time setup:**
   ```bash
   git init
   git remote add origin https://github.com/YOUR_USERNAME/your-repo.git
   ```

2. **Every time you make changes:**
   ```bash
   ./deploy.sh  # Mac/Linux
   # or
   deploy.bat   # Windows
   ```

3. **That's it!** Vercel/Render auto-deploys from GitHub

### Path 3: Full CI/CD with GitHub Actions

**Setup once, deploy automatically forever:**

1. **Set up GitHub secrets:**
   - Go to repo → Settings → Secrets and variables → Actions
   - Add required secrets (see below)

2. **Push to GitHub:**
   ```bash
   git push
   ```

3. **GitHub Actions automatically:**
   - Runs tests
   - Builds project
   - Deploys to Vercel/Render
   - All without you doing anything!

---

## 🔧 GitHub Actions Setup

### For Vercel Auto-Deploy

1. **Get Vercel Token:**
   - Go to https://vercel.com/account/tokens
   - Create new token
   - Copy it

2. **Get Project IDs:**
   - Open your Vercel project
   - Go to Settings
   - Copy `VERCEL_ORG_ID` (in Team settings)
   - Copy `VERCEL_PROJECT_ID` (in General)

3. **Add to GitHub:**
   - Repo → Settings → Secrets → Actions
   - Add these secrets:
     ```
     VERCEL_TOKEN = your_token_here
     VERCEL_ORG_ID = your_org_id
     VERCEL_PROJECT_ID = your_project_id
     ```

### For Render Auto-Deploy

1. **Get Deploy Hook:**
   - Open your Render service
   - Go to Settings
   - Scroll to "Deploy Hook"
   - Copy the webhook URL

2. **Add to GitHub:**
   - Repo → Settings → Secrets → Actions
   - Add secret:
     ```
     RENDER_DEPLOY_HOOK = https://api.render.com/deploy/...
     ```

---

## 📊 Workflow Comparison

| Feature | Manual | Deploy Scripts | GitHub Actions |
|---------|--------|----------------|----------------|
| **Setup Time** | None | 2 min | 15 min |
| **Ease of Use** | Medium | Easy | Automatic |
| **Deploy Speed** | Fast | Fast | Fast |
| **Tests** | Manual | No | Yes |
| **Best For** | Learning | Quick updates | Production |

---

## 🎯 Recommended Setup

**For Learning/Portfolio:**
```
1. Start with manual deployment (learn the process)
2. Add deploy scripts when comfortable
3. Skip GitHub Actions (unnecessary for portfolio)
```

**For Production/Team:**
```
1. Set up GitHub Actions immediately
2. Add automated tests
3. Use deploy scripts for quick fixes
```

---

## 📝 Common Workflows

### Scenario 1: Fix a Bug

```bash
# 1. Make your changes
# 2. Test locally
npm start  # Test frontend
python backend/main.py  # Test backend

# 3. Deploy
./deploy.sh
# Enter commit message: "Fixed bug in upload feature"
# Push to GitHub? y

# 4. Wait 2-3 minutes
# Check Vercel/Render dashboard for deployment status
```

### Scenario 2: Add New Feature

```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Make changes and test

# 3. Commit and push
./deploy.sh

# 4. Create PR on GitHub
# GitHub Actions will:
# - Run tests
# - Create preview deployment
# - Comment with preview URL

# 5. Merge PR
# Automatic production deployment!
```

### Scenario 3: Emergency Hotfix

```bash
# 1. Fix the issue

# 2. Quick deploy
./deploy.sh
# Message: "HOTFIX: Critical bug fix"
# Push? y

# Deployed in 3 minutes!
```

---

## 🐛 Troubleshooting

### Deploy Script Says "Git not initialized"

**Solution:**
```bash
git init
git remote add origin https://github.com/YOUR_USERNAME/your-repo.git
```

### GitHub Actions Failing

**Check:**
1. Secrets are added correctly
2. Workflow file is in `.github/workflows/`
3. Check Actions tab for error logs

**Common fixes:**
```bash
# Update GitHub Actions
git pull origin main
git push
```

### Vercel Deploy Fails

**Check:**
1. Environment variables set correctly
2. `vercel.json` is valid JSON
3. Check Vercel build logs

### Render Deploy Fails

**Check:**
1. `render.yaml` syntax is correct
2. Environment variables set
3. Check Render logs

---

## 💡 Tips & Tricks

### Speed Up Deployments

**Vercel:**
- Use build cache (automatic)
- Only deploy on main branch
- Skip preview deployments if not needed

**Render:**
- Upgrade to paid plan ($7/month) for instant deploys
- Use deploy hooks for faster triggers

### Reduce Costs

**GitHub Actions:**
- Only run on main branch
- Skip tests on documentation changes
- Use caching for dependencies

**Vercel/Render:**
- Stay on free tier
- Deploy only when needed
- Use preview deployments wisely

### Best Practices

1. **Always test locally first**
2. **Write meaningful commit messages**
3. **Use feature branches for big changes**
4. **Keep dependencies updated**
5. **Monitor deployment logs**

---

## 📚 Additional Resources

**Git:**
- Git Basics: https://git-scm.com/book/en/v2
- GitHub Flow: https://guides.github.com/introduction/flow/

**GitHub Actions:**
- Docs: https://docs.github.com/en/actions
- Examples: https://github.com/actions/starter-workflows

**Vercel:**
- Deployment Docs: https://vercel.com/docs/deployments
- Environment Variables: https://vercel.com/docs/environment-variables

**Render:**
- Deploy Docs: https://render.com/docs/deploys
- Blueprint Spec: https://render.com/docs/blueprint-spec

---

## ✅ Quick Checklist

Before using automation:

- [ ] Git initialized
- [ ] GitHub repo created
- [ ] Deploy script tested (`./deploy.sh`)
- [ ] Vercel/Render connected to GitHub
- [ ] GitHub secrets added (if using Actions)
- [ ] Test deployment successful
- [ ] Monitoring set up

---

**You're all set!** Choose the automation level that fits your needs and start deploying! 🚀

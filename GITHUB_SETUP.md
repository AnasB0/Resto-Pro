# 🚀 How to Push to GitHub

## Step-by-Step Instructions

### 1. Create a GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. **Repository name**: `restaurant-ai-dashboard`
3. **Description**: "AI-powered restaurant insights dashboard with sentiment analysis, forecasting, and inventory alerts"
4. Choose **Public** (so others can see it) or **Private** (only you)
5. **DO NOT** initialize with README, .gitignore, or license (we have them already)
6. Click **"Create repository"**

### 2. Connect Local Repository to GitHub

After creating the repo, you'll see commands like:

```bash
git remote add origin https://github.com/YOUR-USERNAME/restaurant-ai-dashboard.git
git branch -M main
git push -u origin main
```

Run these commands in your terminal:

```bash
cd /mnt/d/coursesP/Resto

# Add GitHub remote
git remote add origin https://github.com/YOUR-USERNAME/restaurant-ai-dashboard.git

# Rename branch to main (if needed)
git branch -M main

# Push code to GitHub
git push -u origin main
```

### 3. Verify on GitHub

1. Go to your repository on GitHub
2. You should see all your files and folders
3. The README should display on the main page

## Using SSH (Recommended for Future Pushes)

If you want to use SSH instead of HTTPS:

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add SSH key to GitHub (go to Settings > SSH Keys > New SSH Key)

# Change remote to SSH
git remote set-url origin git@github.com:YOUR-USERNAME/restaurant-ai-dashboard.git

# Push
git push -u origin main
```

## Future Updates

After making changes locally:

```bash
# Stage changes
git add .

# Commit with message
git commit -m "Your commit message here"

# Push to GitHub
git push
```

## .env File Security

**Important**: Your `.env` file is in `.gitignore` and won't be committed. This keeps your API keys safe! 🔐

For others to use the project, they should:
1. Copy `.env.example` to `.env`
2. Add their own API keys

Create a `.env.example` file (without actual keys):

```env
COLAB_API_URL=your-ngrok-url-here
OPENROUTER_API_KEY=your-api-key-here
OPENROUTER_MODEL=openai/gpt-4o-mini
```

## Sharing Your Repository

Once on GitHub, you can share:
- **Clone link**: `https://github.com/YOUR-USERNAME/restaurant-ai-dashboard.git`
- **Direct URL**: `https://github.com/YOUR-USERNAME/restaurant-ai-dashboard`

## Common Git Commands

```bash
# View status
git status

# View commit history
git log --oneline

# View remote connections
git remote -v

# Undo last commit (before push)
git reset --soft HEAD~1

# View changes before committing
git diff
```

## Troubleshooting

**"Repository not found"** error:
- Make sure the repo exists on GitHub
- Check your username is correct
- Use HTTPS if SSH isn't configured

**"Permission denied" error:**
- Verify SSH key is added to GitHub account
- Or use HTTPS token authentication

**Want to change remote URL:**
```bash
git remote set-url origin https://github.com/YOUR-USERNAME/restaurant-ai-dashboard.git
```

---

**That's it!** Your Restaurant AI Dashboard is now on GitHub! 🎉

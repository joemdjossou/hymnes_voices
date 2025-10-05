# GitHub Pages Setup Guide

## The Issue
The GitHub Actions workflow is failing with:
```
Error: Create Pages site failed
Error: HttpError: Resource not accessible by integration
```

This happens because GitHub Pages needs to be manually enabled in the repository settings before the workflow can deploy to it.

## Solution: Manual Setup

### Step 1: Enable GitHub Pages

1. **Go to your repository** on GitHub: `https://github.com/joemdjossou/hymnes_voices`

2. **Click on Settings** tab (in the repository navigation)

3. **Scroll down to Pages** section in the left sidebar

4. **Under Source**, select **"GitHub Actions"**

5. **Save the settings** (no additional configuration needed)

### Step 2: Verify the Workflow

After enabling Pages, the deployment workflow should work automatically. The workflow will:

1. ✅ Checkout the code
2. ✅ Setup Python and install dependencies
3. ✅ Generate hymnes data (`python generate_data.py`)
4. ✅ Configure Pages
5. ✅ Upload the website files
6. ✅ Deploy to GitHub Pages

### Step 3: Check Deployment

1. **Go to Actions tab** in your repository
2. **Look for "Deploy to GitHub Pages"** workflow
3. **Wait for it to complete** (usually 2-5 minutes)
4. **Visit your site**: `https://joemdjossou.github.io/hymnes_voices`

## Alternative: Use the Simple Workflow

If you continue having issues, you can use the simpler workflow:

1. **Rename the workflow files**:
   ```bash
   mv .github/workflows/deploy.yml .github/workflows/deploy-backup.yml
   mv .github/workflows/deploy-simple.yml .github/workflows/deploy.yml
   ```

2. **Commit and push**:
   ```bash
   git add .
   git commit -m "Switch to simple deployment workflow"
   git push
   ```

## Expected Result

Once GitHub Pages is enabled and the workflow runs successfully, you'll have:

- 🌐 **Live website** at: `https://joemdjossou.github.io/hymnes_voices`
- 🎵 **Browse 654 hymnes** with individual channel access
- 🔍 **Search functionality** to find specific hymnes
- 🎮 **Audio player** with volume control and progress tracking
- 📱 **Responsive design** for mobile and desktop

## Troubleshooting

### If the workflow still fails:

1. **Check repository permissions**:
   - Go to Settings → Actions → General
   - Ensure "Allow GitHub Actions to create and approve pull requests" is enabled

2. **Check Pages settings**:
   - Go to Settings → Pages
   - Ensure Source is set to "GitHub Actions"
   - If you see any errors, try disabling and re-enabling Pages

3. **Check workflow permissions**:
   - The workflow now includes all necessary permissions:
     - `contents: read`
     - `pages: write`
     - `id-token: write`
     - `deployments: write`

### If you get 404 errors:

1. **Wait a few minutes** after deployment completes
2. **Clear your browser cache**
3. **Check the Actions tab** to ensure deployment was successful
4. **Verify the URL** is exactly: `https://joemdjossou.github.io/hymnes_voices`

## Manual Deployment (Backup Option)

If GitHub Actions continues to fail, you can deploy manually:

1. **Generate the data**:
   ```bash
   python generate_data.py
   ```

2. **Copy files to a separate branch**:
   ```bash
   git checkout -b gh-pages
   git add index.html styles.css script.js hymnes_data.json output/
   git commit -m "Deploy to GitHub Pages"
   git push origin gh-pages
   ```

3. **Set Pages source** to the `gh-pages` branch in repository settings

The manual setup should resolve the permission issues and get your hymnes player website live!

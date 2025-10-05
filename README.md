# Hymnes Voices - Deployed Files

This directory contains the files ready for GitHub Pages deployment.

## Manual Deployment Steps:

1. **Create a new branch called `gh-pages`**:
   ```bash
   git checkout -b gh-pages
   ```

2. **Copy all files from this `deploy/` directory to the root**

3. **Commit and push**:
   ```bash
   git add .
   git commit -m "Deploy hymnes player to GitHub Pages"
   git push origin gh-pages
   ```

4. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Source: Select "Deploy from a branch"
   - Branch: Select "gh-pages" and "/ (root)"
   - Save

5. **Your site will be live at**: `https://joemdjossou.github.io/hymnes_voices`

## Files included:
- index.html (main website)
- styles.css (styling)
- script.js (functionality)
- hymnes_data.json (hymnes metadata)
- output/ (MP3 files)
- _config.yml (Jekyll config)

# GitHub Pages Deployment Guide

This guide will help you deploy the Hymnes Voices website to GitHub Pages.

## Prerequisites

1. Your repository is on GitHub
2. You have admin access to the repository
3. The output MP3 files are committed to the repository

## Deployment Steps

### 1. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click on **Settings** tab
3. Scroll down to **Pages** section in the left sidebar
4. Under **Source**, select **GitHub Actions**
5. Save the settings

### 2. Push Your Code

The deployment will automatically trigger when you push to the main branch:

```bash
git add .
git commit -m "Add web interface for hymnes player"
git push origin main
```

### 3. Monitor Deployment

1. Go to the **Actions** tab in your repository
2. You'll see a workflow called "Deploy to GitHub Pages" running
3. Wait for it to complete (usually takes 2-5 minutes)
4. Once complete, your site will be available at:
   `https://yourusername.github.io/hymnes_voices`

### 4. Verify Deployment

1. Visit your GitHub Pages URL
2. You should see the Hymnes Voices interface
3. Test the search functionality
4. Try playing some audio files

## File Structure

The deployment includes these key files:

```
hymnes_voices/
├── index.html              # Main website interface
├── styles.css              # Styling and responsive design
├── script.js               # JavaScript functionality
├── hymnes_data.json        # Generated hymnes metadata
├── output/                 # MP3 files directory
│   ├── h1/
│   │   ├── channel_00.mp3
│   │   ├── channel_01.mp3
│   │   └── ...
│   ├── h2/
│   └── ...
├── .github/workflows/deploy.yml  # GitHub Actions workflow
└── _config.yml             # Jekyll configuration
```

## Features

The deployed website includes:

- **Browse 654 hymnes** with individual channel access
- **Search functionality** to find specific hymnes
- **Audio player** with play/pause controls
- **Responsive design** that works on mobile and desktop
- **Modern UI** with smooth animations and transitions
- **Volume control** and progress tracking
- **Keyboard shortcuts** (Space to play/pause, Escape to close modal)

## Troubleshooting

### If deployment fails:

1. Check the Actions tab for error messages
2. Ensure all MP3 files are committed to the repository
3. Verify the `hymnes_data.json` file is generated correctly
4. Check that the workflow file syntax is correct

### If audio doesn't play:

1. Verify MP3 files are accessible via direct URL
2. Check browser console for JavaScript errors
3. Ensure the file paths in `hymnes_data.json` are correct

### If the site doesn't load:

1. Wait a few minutes after deployment completes
2. Clear your browser cache
3. Check the GitHub Pages settings are correct

## Customization

You can customize the website by modifying:

- `styles.css` - Change colors, fonts, and layout
- `script.js` - Add new features or modify functionality
- `index.html` - Update the page structure or content

## Updating the Site

To update the site with new hymnes:

1. Add new MP3 files to the `output/` directory
2. Run `python generate_data.py` to update the metadata
3. Commit and push the changes
4. The deployment will automatically update the site

## Performance Notes

- The site loads metadata for all 654 hymnes (about 441KB)
- MP3 files are loaded on-demand when played
- Consider using a CDN for better performance with large files
- The site is optimized for modern browsers with HTML5 audio support

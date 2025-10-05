#!/usr/bin/env python3
"""
Manual deployment script for GitHub Pages.
This script prepares the website files for manual deployment.
"""

import os
import shutil
from pathlib import Path

def deploy_manually():
    """Prepare files for manual GitHub Pages deployment."""
    
    print("🚀 Preparing files for manual GitHub Pages deployment...")
    
    # Create deployment directory
    deploy_dir = Path("deploy")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    # Copy essential files
    essential_files = [
        "index.html",
        "styles.css", 
        "script.js",
        "hymnes_data.json",
        "_config.yml"
    ]
    
    for file in essential_files:
        if Path(file).exists():
            shutil.copy2(file, deploy_dir)
            print(f"✅ Copied {file}")
    
    # Copy output directory
    if Path("output").exists():
        shutil.copytree("output", deploy_dir / "output")
        print("✅ Copied output directory")
    
    # Create a simple index for the deploy directory
    readme_content = """# Hymnes Voices - Deployed Files

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
"""
    
    with open(deploy_dir / "README.md", "w") as f:
        f.write(readme_content)
    
    print(f"\n🎉 Deployment files ready in '{deploy_dir}/' directory!")
    print("\n📋 Next steps:")
    print("1. Create a 'gh-pages' branch")
    print("2. Copy files from deploy/ to the branch root")
    print("3. Commit and push the branch")
    print("4. Enable Pages in repository settings")
    print("5. Your site will be live!")

if __name__ == "__main__":
    deploy_manually()

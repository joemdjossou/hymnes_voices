#!/usr/bin/env python3
"""
Script to update hymn lyrics from troisanges.org website
"""
import json
import re
import time
import urllib.request
import urllib.error
from urllib.parse import quote

def fetch_hymn_html(hymn_number):
    """Fetch the HTML content for a hymn number"""
    # Format number as 3 digits with leading zeros (e.g., 001, 101)
    formatted_number = f"{int(hymn_number):03d}"
    url = f"https://troisanges.org/Musique/HymnesEtLouanges/H{formatted_number}.html"
    
    try:
        # Add a small delay to be respectful to the server
        time.sleep(0.1)
        
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            # Try windows-1252 first (as per HTML meta tag), fallback to utf-8
            try:
                html = response.read().decode('windows-1252', errors='ignore')
            except:
                html = response.read().decode('utf-8', errors='ignore')
            return html
    except urllib.error.HTTPError as e:
        print(f"  HTTP Error {e.code} for hymn {hymn_number}")
        return None
    except urllib.error.URLError as e:
        print(f"  URL Error for hymn {hymn_number}: {e.reason}")
        return None
    except Exception as e:
        print(f"  Error fetching hymn {hymn_number}: {str(e)}")
        return None

def extract_lyrics_from_html(html):
    """Extract lyrics from the HTML content"""
    if not html:
        return None
    
    # The HTML structure is:
    # <p style="text-align: center; font-family: Arial">
    # <b>
    # <br>
    # 1<br>
    # Verse line 1<br>
    # Verse line 2<br>
    # ...<br>
    # <br>
    # 2<br>
    # ...
    # </b>
    # </p>
    
    # Extract the content within the <b> tag in the centered paragraph
    # Find the bold section that contains the lyrics
    # Try multiple patterns to handle different HTML structures
    bold_match = re.search(r'<p[^>]*text-align:\s*center[^>]*>\s*<b>(.*?)</b>', html, re.DOTALL | re.IGNORECASE)
    if not bold_match:
        # Try without requiring </b> before </p>
        bold_match = re.search(r'<p[^>]*text-align:\s*center[^>]*>\s*<b>(.*?)(?:</b>|(?=</p>))', html, re.DOTALL | re.IGNORECASE)
    if not bold_match:
        return None
    
    bold_content = bold_match.group(1)
    
    # Parse the content line by line
    lines = bold_content.split('\n')
    verses = []
    current_verse_num = None
    current_verse_lines = []
    
    for line in lines:
        # Remove HTML tags but preserve text
        line = re.sub(r'<[^>]+>', '', line)
        # Remove leading tabs and whitespace, but keep trailing content
        line = line.strip()
        
        if not line:
            # Empty line - might be verse separator
            if current_verse_num is not None and current_verse_lines:
                # Save current verse
                verse_text = '\n'.join(current_verse_lines)
                verses.append(f"{current_verse_num}.\n{verse_text}")
                current_verse_lines = []
                current_verse_num = None
            continue
        
        # Check if line is just a verse number (e.g., "1", "2", "5.", "6.")
        verse_num_match = re.match(r'^(\d+)\.?$', line)
        if verse_num_match:
            # Save previous verse if exists
            if current_verse_num is not None and current_verse_lines:
                verse_text = '\n'.join(current_verse_lines)
                verses.append(f"{current_verse_num}.\n{verse_text}")
                current_verse_lines = []
            current_verse_num = verse_num_match.group(1)
            continue
        
        # This is a verse line
        if current_verse_num is not None:
            current_verse_lines.append(line)
    
    # Don't forget the last verse
    if current_verse_num is not None and current_verse_lines:
        verse_text = '\n'.join(current_verse_lines)
        verses.append(f"{current_verse_num}.\n{verse_text}")
    
    if verses:
        return '\n\n'.join(verses)
    
    return None

def clean_lyrics_text(text):
    """Clean up the lyrics text"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    # Remove HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    # Clean up spacing
    text = re.sub(r' +', ' ', text)
    text = text.strip()
    
    return text

def normalize_lyrics(lyrics):
    """Normalize lyrics for comparison"""
    if not lyrics:
        return ""
    # Remove extra whitespace, normalize line breaks
    normalized = re.sub(r'\s+', ' ', lyrics)
    normalized = re.sub(r'\n\s*\n', '\n', normalized)
    return normalized.strip().lower()

def update_hymn_lyrics():
    """Main function to update all hymn lyrics"""
    # Read the JSON file
    json_path = '/Users/joemdjossou/Documents/GitHub/hymnes_voices/json/hymnes.json'
    
    print("Reading JSON file...")
    with open(json_path, 'r', encoding='utf-8') as f:
        hymns = json.load(f)
    
    total_hymns = len(hymns)
    print(f"Found {total_hymns} hymns in JSON")
    
    updated_count = 0
    error_count = 0
    unchanged_count = 0
    
    for idx, hymn in enumerate(hymns, 1):
        hymn_number = hymn['number']
        print(f"[{idx}/{total_hymns}] Processing hymn {hymn_number}...")
        
        # Fetch HTML from website
        html = fetch_hymn_html(hymn_number)
        if not html:
            error_count += 1
            print(f"  ⚠️  Could not fetch hymn {hymn_number}")
            continue
        
        # Extract lyrics from HTML
        website_lyrics = extract_lyrics_from_html(html)
        
        if not website_lyrics:
            error_count += 1
            print(f"  ⚠️  Could not extract lyrics for hymn {hymn_number}")
            continue
        
        website_lyrics = clean_lyrics_text(website_lyrics)
        current_lyrics = hymn.get('lyrics', '')
        
        # Compare normalized versions
        if normalize_lyrics(website_lyrics) != normalize_lyrics(current_lyrics):
            hymn['lyrics'] = website_lyrics
            updated_count += 1
            print(f"  ✓ Updated hymn {hymn_number}")
        else:
            unchanged_count += 1
            print(f"  - No changes needed for hymn {hymn_number}")
    
    # Save the updated JSON
    print(f"\nSaving updated JSON...")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(hymns, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Complete!")
    print(f"  Updated: {updated_count}")
    print(f"  Unchanged: {unchanged_count}")
    print(f"  Errors: {error_count}")

if __name__ == '__main__':
    update_hymn_lyrics()


#!/usr/bin/env python3
"""
Script to check the number of music sheet PDFs available for each hymn
"""
import json
import time
import urllib.error
import urllib.request


def check_pdf_exists(url):
    """Check if a PDF URL exists (returns True if exists, False if 404, None for other errors)"""
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
        req.add_header('Range', 'bytes=0-0')  # Only request first byte to save bandwidth
        
        with urllib.request.urlopen(req, timeout=10) as response:
            # If we get here, the file exists
            return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False  # File doesn't exist
        else:
            return None  # Other HTTP error
    except urllib.error.URLError as e:
        return None  # URL error
    except Exception as e:
        return None  # Other error

def count_music_sheets(hymn_number):
    """Count the number of music sheet PDFs available for a hymn"""
    # Format number as 3 digits with leading zeros (e.g., 001, 101)
    formatted_number = f"{int(hymn_number):03d}"
    
    # Base URL pattern
    base_url = f"https://troisanges.org/Musique/HymnesEtLouanges/PDF/H{formatted_number}"
    
    count = 0
    
    # Check base PDF (H###.pdf)
    base_pdf_url = f"{base_url}.pdf"
    exists = check_pdf_exists(base_pdf_url)
    
    if exists is True:
        count += 1
    elif exists is None:
        # Error checking base PDF, return None to indicate error
        return None
    
    # Check additional PDFs with 's' suffixes (H###s.pdf, H###ss.pdf, etc.)
    s_count = 1
    while True:
        # Add 's' characters (s, ss, sss, etc.)
        s_suffix = 's' * s_count
        pdf_url = f"{base_url}{s_suffix}.pdf"
        
        exists = check_pdf_exists(pdf_url)
        
        if exists is True:
            count += 1
            s_count += 1
        elif exists is False:
            # 404 - no more PDFs
            break
        else:
            # Error - stop checking
            break
    
    return count

def update_music_sheets_count():
    """Main function to update music sheets count for all hymns"""
    # Read the JSON file
    json_path = '/Users/joemdjossou/Documents/GitHub/hymnes_voices/json/hymnes.json'
    
    print("Reading JSON file...")
    with open(json_path, 'r', encoding='utf-8') as f:
        hymns = json.load(f)
    
    total_hymns = len(hymns)
    print(f"Found {total_hymns} hymns in JSON")
    print(f"Starting to check music sheets...\n")
    
    updated_count = 0
    error_count = 0
    
    for idx, hymn in enumerate(hymns, 1):
        hymn_number = hymn['number']
        print(f"[{idx}/{total_hymns}] Checking hymn {hymn_number}...", end=' ')
        
        # Add small delay to be respectful to the server
        time.sleep(0.2)
        
        # Count music sheets
        sheet_count = count_music_sheets(hymn_number)
        
        if sheet_count is not None:
            # Update the hymn with music sheets count
            hymn['musicsheets'] = sheet_count
            updated_count += 1
            print(f"✓ Found {sheet_count} sheet(s)")
        else:
            error_count += 1
            print(f"⚠️  Error checking sheets")
            # Optionally set to 0 or leave as None
            hymn['musicsheets'] = 0
    
    # Save the updated JSON
    print(f"\nSaving updated JSON...")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(hymns, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Complete!")
    print(f"  Updated: {updated_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total music sheets found: {sum(h.get('musicsheets', 0) for h in hymns)}")

if __name__ == '__main__':
    update_music_sheets_count()


import urllib.request
import re
import os
import json
from urllib.parse import urljoin, urlparse

target_url = "https://www.amsinform.com/insurance-claim-investigations/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

print(f"Fetching main page: {target_url}")
raw_html = fetch_url(target_url)

# Save raw HTML
with open("raw_page.html", "w", encoding="utf-8") as f:
    f.write(raw_html)

print(f"Raw HTML saved. Size: {len(raw_html)} bytes")

# Extract all CSS link tags
css_urls = re.findall(r'<link[^>]+rel=[\'"]stylesheet[\'"][^>]+href=[\'"]([^\'"]+)[\'"]', raw_html, re.IGNORECASE)
css_urls += re.findall(r'<link[^>]+href=[\'"]([^\'"]+\.css[^\'"]*)[\'"][^>]+rel=[\'"]stylesheet[\'"]', raw_html, re.IGNORECASE)

print(f"Found {len(css_urls)} stylesheet links.")

# Ensure css folder exists
os.makedirs("css_assets", exist_ok=True)

combined_css = ""
for idx, css_url in enumerate(css_urls):
    full_css_url = urljoin(target_url, css_url)
    print(f"Fetching CSS ({idx+1}/{len(css_urls)}): {full_css_url}")
    css_content = fetch_url(full_css_url)
    if css_content:
        # Save individual CSS file
        css_filename = os.path.basename(urlparse(full_css_url).path) or f"style_{idx}.css"
        with open(os.path.join("css_assets", css_filename), "w", encoding="utf-8") as f:
            f.write(css_content)
        combined_css += f"\n/* --- Source: {full_css_url} --- */\n" + css_content

with open("combined_styles.css", "w", encoding="utf-8") as f:
    f.write(combined_css)

print(f"Combined CSS saved. Total size: {len(combined_css)} bytes")

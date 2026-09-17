import re
import os
from urllib.parse import urljoin

with open("raw_page.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

# Replace relative image URLs, srcset URLs, and stylesheet links to make sure everything loads correctly or points to valid absolute URLs
site_base = "https://www.amsinform.com/insurance-claim-investigations/"

def fix_url(match):
    prefix = match.group(1)
    url = match.group(2)
    if url.startswith("http://") or url.startswith("https://") or url.startswith("//") or url.startswith("data:"):
        return match.group(0)
    fixed = urljoin(site_base, url)
    return f'{prefix}="{fixed}"'

# Fix src, href, action, data-src attributes
fixed_html = re.sub(r'(src|data-src|href|action)="([^"]+)"', fix_url, html)

# Fix srcset attributes
def fix_srcset(match):
    srcset_val = match.group(1)
    parts = srcset_val.split(',')
    fixed_parts = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        subparts = part.split()
        url = subparts[0]
        if not (url.startswith("http://") or url.startswith("https://") or url.startswith("//") or url.startswith("data:")):
            url = urljoin(site_base, url)
        subparts[0] = url
        fixed_parts.append(" ".join(subparts))
    return f'srcset="{", ".join(fixed_parts)}"'

fixed_html = re.sub(r'srcset="([^"]+)"', fix_srcset, fixed_html)

# Also fix CSS background-image url(...) in inline styles or tags
def fix_css_url(match):
    url = match.group(1).strip("'\"")
    if url.startswith("http://") or url.startswith("https://") or url.startswith("//") or url.startswith("data:"):
        return match.group(0)
    fixed = urljoin(site_base, url)
    return f'url("{fixed}")'

fixed_html = re.sub(r'url\(([^)]+)\)', fix_css_url, fixed_html)

# Combine all downloaded CSS into a unified styles file
combined_css_parts = []
css_folder = "css_assets"
if os.path.exists(css_folder):
    for css_file in sorted(os.listdir(css_folder)):
        file_path = os.path.join(css_folder, css_file)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                # Fix relative font and image URLs inside CSS
                def fix_css_internal_url(m):
                    u = m.group(1).strip("'\"")
                    if u.startswith("http") or u.startswith("//") or u.startswith("data:"):
                        return m.group(0)
                    fixed_u = urljoin(site_base, u)
                    return f'url("{fixed_u}")'
                content = re.sub(r'url\(([^)]+)\)', fix_css_internal_url, content)
                combined_css_parts.append(f"/* === {css_file} === */\n" + content)

master_css = "\n\n".join(combined_css_parts)
with open("style.css", "w", encoding="utf-8") as f:
    f.write(master_css)

print("Saved master style.css, size:", len(master_css))

# Write cleaned standalone index.html
# We can link style.css in the header
with open("index.html", "w", encoding="utf-8") as f:
    f.write(fixed_html)

print("Saved cleaned index.html, size:", len(fixed_html))

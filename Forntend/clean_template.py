import re

with open("index.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

print("Original HTML length:", len(html))

# Remove analytics / tracker script tags if any (GTM, HotJar, Facebook Pixel, Google Analytics)
html = re.sub(r'<script[^>]*src="[^"]*(gtm|googletagmanager|google-analytics|facebook|hubspot|hotjar|clarity)[^"]*"[^>]*></script>', '', html, flags=re.IGNORECASE)

# Ensure style.css is linked in the head
if '<link rel="stylesheet" href="style.css">' not in html:
    html = html.replace('</head>', '  <link rel="stylesheet" href="style.css">\n</head>', 1)

# Write to landing_page.html and index.html
with open("landing_page.html", "w", encoding="utf-8") as f:
    f.write(html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Saved cleaned landing_page.html & index.html!")

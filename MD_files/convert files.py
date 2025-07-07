import os
import json
import re
import html2text

# === CONFIGURATION ===
json_path = "KB_V1_ForProcessing.json"
html_dir = "exported_articles_html"
md_dir = "exported_articles_markdown"

# === UTILITIES ===
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name.strip())

# === CREATE FOLDERS ===
os.makedirs(html_dir, exist_ok=True)
os.makedirs(md_dir, exist_ok=True)

# === LOAD JSON ===
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

articles = data.get("data", {}).get("KnowledgeBaseArticles", [])

# === INIT HTML-TO-MARKDOWN CONVERTER ===
converter = html2text.HTML2Text()
converter.ignore_links = False
converter.ignore_images = False
converter.body_width = 0

# === PROCESS ARTICLES ===
count = 0
for article in articles:
    fields = article.get("fields", {})
    title = fields.get("Title", "").strip()
    body = fields.get("Body", "").strip()
    shortcode = fields.get("ShortCode", "").strip()
    uuid = article.get("uuid", "").strip()

    if not title or not body:
        continue

    # Determine filename base: use ShortCode or fallback to uuid
    filename_base = sanitize_filename(shortcode if shortcode else uuid)

    # File paths
    html_filename = filename_base + ".html"
    md_filename = filename_base + ".md"

    # === WRITE HTML FILE ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
{body}
</body>
</html>"""
    with open(os.path.join(html_dir, html_filename), "w", encoding="utf-8") as f:
        f.write(html_content)

    # === CONVERT TO MARKDOWN FILE ===
    markdown = converter.handle(html_content)
    with open(os.path.join(md_dir, md_filename), "w", encoding="utf-8") as f:
        f.write(markdown)

    count += 1

print(f"✅ {count} articles exported using ShortCode or UUID for filenames.")
print(f"📁 HTML files: {html_dir}/")
print(f"📁 Markdown files: {md_dir}/")

import os
import json
import re
import html2text

# === CONFIGURATION ===
json_path = "articles_data.json"
html_dir = "output_html"
md_dir = "output_markdown"

# === CREATE DIRECTORIES ===
os.makedirs(html_dir, exist_ok=True)
os.makedirs(md_dir, exist_ok=True)

# === HELPERS ===
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name.strip())

# === LOAD JSON ===
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

articles = data.get("data", {}).get("KnowledgeBaseArticlesV2", [])

# === CONVERTER SETUP ===
converter = html2text.HTML2Text()
converter.ignore_links = False
converter.ignore_images = False
converter.body_width = 0

# === PROCESS EACH ARTICLE ===
count = 0
for article in articles:
    fields = article.get("fields", {})
    uuid = article.get("uuid", "").strip()
    code = fields.get("Code", "").strip()
    title = fields.get("Title", "").strip()
    body = fields.get("ArticleContent", "").strip()

    if not body:
        continue  # Skip empty content

    # Choose filename base: prefer Code, fallback to UUID
    filename_base = sanitize_filename(code if code else uuid)

    # === Write HTML ===
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
    html_path = os.path.join(html_dir, filename_base + ".html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # === Convert to Markdown ===
    markdown_content = converter.handle(html_content)
    md_path = os.path.join(md_dir, filename_base + ".md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    count += 1

print(f"✅ {count} articles processed and saved to HTML and Markdown.")
print(f"📁 HTML folder: {html_dir}")
print(f"📁 Markdown folder: {md_dir}")

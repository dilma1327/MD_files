import os
import json
import re
import html2text

json_path = "input/KB_V1_ForProcessing.json"
html_dir = "output/html"
md_dir = "output/markdown"

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name.strip())

os.makedirs(html_dir, exist_ok=True)
os.makedirs(md_dir, exist_ok=True)

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

articles = data.get("data", {}).get("KnowledgeBaseArticles", [])

converter = html2text.HTML2Text()
converter.ignore_links = False
converter.ignore_images = False
converter.body_width = 0

count = 0
for article in articles:
    fields = article.get("fields", {}) or {}
    title = (fields.get("Title") or "").strip()
    body = (fields.get("Body") or "").strip()
    shortcode = (fields.get("ShortCode") or "").strip()
    uuid = (article.get("uuid") or "").strip()

    if not title or not body:
        continue

    filename_base = sanitize_filename(shortcode if shortcode else uuid)
    html_filename = filename_base + ".html"
    md_filename = filename_base + ".md"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
<h1>{title}</h1>
{body}
</body>
</html>"""
    with open(os.path.join(html_dir, html_filename), "w", encoding="utf-8") as f:
        f.write(html_content)

    markdown = f"# {title}\n\n" + converter.handle(body)

    with open(os.path.join(md_dir, md_filename), "w", encoding="utf-8") as f:
        f.write(markdown)

    count += 1

print(f"✅ {count} articles exported using ShortCode or UUID.")
print(f"📁 HTML: {html_dir}")
print(f"📁 Markdown: {md_dir}")

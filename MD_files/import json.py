import os
import json
import re
import html2text

# === SETTINGS ===
json_file = "articles_data.json"
html_dir = "html_articles"
md_dir = "markdown_articles"

# === UTILITIES ===
def sanitize_filename(title):
    """Sanitize filename to remove invalid characters."""
    return re.sub(r'[\\/*?:"<>|]', "_", title.strip())

# === CREATE OUTPUT FOLDERS ===
os.makedirs(html_dir, exist_ok=True)
os.makedirs(md_dir, exist_ok=True)

# === LOAD JSON DATA ===
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

articles = data["data"]["KnowledgeBaseArticlesV2"]

# === HTML TO MARKDOWN CONVERTER ===
converter = html2text.HTML2Text()
converter.ignore_links = False
converter.ignore_images = False
converter.body_width = 0

# === PROCESS ARTICLES ===
for article in articles:
    fields = article.get("fields", {})
    title = fields.get("Title", "Untitled")
    content = fields.get("ArticleContent", "")

    filename_base = sanitize_filename(title)
    html_filename = filename_base + ".html"
    md_filename = filename_base + ".md"

    # === Generate HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
{content}
</body>
</html>"""

    html_path = os.path.join(html_dir, html_filename)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # === Convert HTML to Markdown ===
    markdown_content = converter.handle(html_content)
    md_path = os.path.join(md_dir, md_filename)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

print(f"✅ Done! Created {len(articles)} HTML and Markdown files.")
print(f"📁 HTML folder: {html_dir}")
print(f"📁 Markdown folder: {md_dir}")

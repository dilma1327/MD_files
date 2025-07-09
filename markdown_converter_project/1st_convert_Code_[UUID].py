import os
import json
import re
import html2text
from bs4 import BeautifulSoup

json_path = "input/articles_data.json"
html_dir = "output/html"
md_dir = "output/markdown"
html_nocode_dir = "output/html_nocode"
md_nocode_dir = "output/markdown_nocode"

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name.strip())

def remove_h1_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    for h1 in soup.find_all("h1"):
        h1.decompose()
    return str(soup)

def extract_code_from_body(html):
    match = re.search(r"Code:\s*([A-Z0-9_-]+)", html)
    return match.group(1).strip() if match else ""

# Create folders
os.makedirs(html_dir, exist_ok=True)
os.makedirs(md_dir, exist_ok=True)
os.makedirs(html_nocode_dir, exist_ok=True)
os.makedirs(md_nocode_dir, exist_ok=True)

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

articles = data.get("data", {}).get("KnowledgeBaseArticlesV2", [])

converter = html2text.HTML2Text()
converter.ignore_links = False
converter.ignore_images = False
converter.body_width = 0

count = 0
for article in articles:
    fields = article.get("fields", {}) or {}
    title = (fields.get("Title") or "").strip()
    body = (fields.get("ArticleContent") or "").strip()
    code = (fields.get("Code") or "").strip()
    uuid = (article.get("uuid") or "").strip()

    if not title or not body or not uuid:
        continue

    if not code:
        code = extract_code_from_body(body)

    is_nocode = not bool(code)
    filename_base = f"{code}-[{uuid}]" if code else f"NoCode-[{uuid}]"
    filename_base = sanitize_filename(filename_base)

    html_output = html_dir if not is_nocode else html_nocode_dir
    md_output = md_dir if not is_nocode else md_nocode_dir

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
    with open(os.path.join(html_output, html_filename), "w", encoding="utf-8") as f:
        f.write(html_content)

    clean_body = remove_h1_tags(body)
    markdown = f"# {title}\n\n" + converter.handle(clean_body)
    with open(os.path.join(md_output, md_filename), "w", encoding="utf-8") as f:
        f.write(markdown)

    count += 1

print(f"✅ {count} articles exported using Code-[UUID] or NoCode-[UUID].")
print(f"📁 HTML with code: {html_dir}")
print(f"📁 HTML without code: {html_nocode_dir}")
print(f"📁 Markdown with code: {md_dir}")
print(f"📁 Markdown without code: {md_nocode_dir}")

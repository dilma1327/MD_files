import os
import json
import re
import html2text
from bs4 import BeautifulSoup

# === CONFIGURATION ===
json_path = "input/KB_V1_ForProcessing.json"
html_dir = "output/html"
md_dir = "output/markdown"
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

# === CREATE FOLDERS ===
os.makedirs(html_dir, exist_ok=True)
os.makedirs(md_dir, exist_ok=True)
os.makedirs(md_nocode_dir, exist_ok=True)

# === LOAD JSON ===
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

articles = data.get("data", {}).get("KnowledgeBaseArticles", [])

# === INIT MARKDOWN CONVERTER ===
converter = html2text.HTML2Text()
converter.ignore_links = False
converter.ignore_images = False
converter.body_width = 0

count = 0
for article in articles:
    fields = article.get("fields", {}) or {}
    title = (fields.get("Title") or "").strip()
    body = (fields.get("Body") or "").strip()
    code_field = (fields.get("ShortCode") or "").strip()
    uuid = (article.get("uuid") or "").strip()

    if not title or not body or not uuid:
        continue

    # === Code logic ===
    code_body = extract_code_from_body(body)
    final_code = ""
    inject_code_into_body = False

    if code_field and code_body:
        final_code = code_body if code_body != code_field else code_field
    elif code_field:
        final_code = code_field
        inject_code_into_body = True
    elif code_body:
        final_code = code_body
    else:
        final_code = ""

    # === Inject Code tag into body if needed ===
    if inject_code_into_body:
        body += f"<div><strong>Code: {final_code}</strong></div>"

    filename_base = f"{final_code}-[{uuid}]" if final_code else f"NoCode-[{uuid}]"
    filename_base = sanitize_filename(filename_base)
    html_filename = filename_base + ".html"
    md_filename = filename_base + ".md"

    # === WRITE HTML ===
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

    # === CONVERT TO MARKDOWN ===
    clean_body = remove_h1_tags(body)
    markdown = f"# {title}\n\n" + converter.handle(clean_body)
    md_output = md_dir if final_code else md_nocode_dir
    with open(os.path.join(md_output, md_filename), "w", encoding="utf-8") as f:
        f.write(markdown)

    count += 1

print(f"✅ {count} articles exported.")
print(f"📁 HTML: {html_dir}")
print(f"📁 Markdown with code: {md_dir}")
print(f"📁 Markdown without code: {md_nocode_dir}")

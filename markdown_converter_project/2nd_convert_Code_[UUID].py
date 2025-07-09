import os
import json
import re
import html2text
from bs4 import BeautifulSoup

json_path = "input/KB_V1_ForProcessing.json"
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

os.makedirs(html_dir, exist_ok=True)
os.makedirs(md_dir, exist_ok=True)
os.makedirs(html_nocode_dir, exist_ok=True)
os.makedirs(md_nocode_dir, exist_ok=True)

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
    code_field = (fields.get("ShortCode") or "").strip()
    uuid = (article.get("uuid") or "").strip()

    if not title or not body or not uuid:
        continue

    code_body = extract_code_from_body(body)
    final_code = ""
    inject_code_into_body = False

    if code_field and code_body:
        if code_field != code_body:
            final_code = code_body  # Case 2
        else:
            final_code = code_field  # Case 1
    elif not code_body and code_field:
        final_code = code_field  # Case 3
        inject_code_into_body = True
    else:
        final_code = ""  # Case 4

    if inject_code_into_body:
        body += f"<div><strong>Code: {final_code}</strong></div>"

    is_nocode = not bool(final_code)
    filename_base = f"{final_code}-[{uuid}]" if final_code else f"NoCode-[{uuid}]"
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

print(f"✅ {count} articles exported using 4-level code priority logic.")

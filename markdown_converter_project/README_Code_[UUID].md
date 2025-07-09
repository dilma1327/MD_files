# Markdown & HTML Article Converter

This project converts structured knowledge base JSON files into clean, readable Markdown and HTML documents.  
It handles two JSON schemas and names output files based on a unique logic using `Code` (or `ShortCode`) and `uuid`.

---

## 📁 Project Structure

```
markdown_converter_project/
├── input/
│   ├── articles_data.json           # Format V2
│   └── KB_V1_ForProcessing.json     # Format V1
│
├── output/
│   ├── html/                        # Exported HTML files
│   └── markdown/                    # Exported Markdown files
│
├── 1st_convert_Code_[UUID].py       # Script for articles_data.json
├── 2nd_convert_Code_[UUID].py       # Script for KB_V1_ForProcessing.json
└── README.md                        # This file
```

---

## 🧩 File Naming Logic

Each output file is named using:

- `Code-[UUID]` if the `Code` (or `ShortCode`) is available
- `UUID` alone if no code is found

**Example:**

If:
```json
"Code": "SUSEC",
"uuid": "abc-123"
```

Then:
- `SUSEC-[abc-123].html`
- `SUSEC-[abc-123].md`

If `"Code"` is empty and no code is found in the body:
- `abc-123.html`
- `abc-123.md`

---

## 🔄 Input Format Details

### Format 1 — `articles_data.json`
- Structure:
```json
{
  "data": {
    "KnowledgeBaseArticlesV2": [
      {
        "uuid": "...",
        "fields": {
          "Title": "...",
          "ArticleContent": "...",
          "Code": "..."
        }
      }
    ]
  }
}
```

### Format 2 — `KB_V1_ForProcessing.json`
- Structure:
```json
{
  "data": {
    "KnowledgeBaseArticles": [
      {
        "uuid": "...",
        "fields": {
          "Title": "...",
          "Body": "...",
          "ShortCode": "..."
        }
      }
    ]
  }
}
```

---

## ⚙️ Setup Instructions

1. **Install requirements:**
```bash
pip install html2text beautifulsoup4
```

2. **Run scripts from project root:**

```bash
python 1st_convert_Code_[UUID].py
python 2nd_convert_Code_[UUID].py
```

---

## 🧼 Features

- Converts HTML to Markdown with proper formatting
- Adds `<h1>` / `#` title from the `"Title"` field
- Removes any duplicate embedded `<h1>` from the body
- Extracts fallback `Code` from body if missing in field
- Sanitizes filenames automatically

---

## ✅ Output

Converted files are saved to:
- `output/html/`
- `output/markdown/`

---

## 👨‍💻 Author

Built with Python + ChatGPT  
Contact for improvements or customization.

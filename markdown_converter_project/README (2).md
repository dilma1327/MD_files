# Markdown & HTML Article Converter

This project converts structured knowledge base JSON files into Markdown and HTML documents, organizing the output by presence or absence of article codes.

---

## 📁 Project Structure

```
markdown_converter_project/
├── input/
│   ├── articles_data.json
│   └── KB_V1_ForProcessing.json
│
├── output/
│   ├── html/               # Files with valid Code or ShortCode
│   ├── markdown/
│   ├── html_nocode/        # Files without a Code
│   └── markdown_nocode/
│
├── 1st_convert_NoCode_Folders.py     # Script for articles_data.json (V2)
├── 2nd_convert_NoCode_Folders.py     # Script for KB_V1_ForProcessing.json (V1)
└── README.md
```

---

## 📛 File Naming Logic

- `Code-[UUID]` → used when the article has a `Code` (or `ShortCode`)
- `NoCode-[UUID]` → used when no code is available, even after fallback search

**Examples:**
- With code: `SUSEC-[abc-123].md`, `SUSEC-[abc-123].html`
- Without code: `NoCode-[abc-123].md`, `NoCode-[abc-123].html`

---

## 📤 Output Organization

| Condition        | HTML Path           | Markdown Path         |
|------------------|---------------------|------------------------|
| Has Code         | `output/html/`      | `output/markdown/`     |
| No Code found    | `output/html_nocode/` | `output/markdown_nocode/` |

---

## 📥 Input Formats

### Format 1 — `articles_data.json`

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

## ⚙️ Requirements

Install dependencies:

```bash
pip install html2text beautifulsoup4
```

---

## 🚀 How to Use

From the root directory:

### For `articles_data.json` (V2 format):
```bash
python 1st_convert_Code_[UUID].py
```

### For `KB_V1_ForProcessing.json` (V1 format):
```bash
python 2nd_convert_Code_[UUID].py
```

---

## 🧠 Features

- Uses `Title` field as the document heading
- Removes any duplicate `<h1>` from the body
- Fallback to extract `Code:` from body if missing
- Organizes NoCode outputs into separate folders
- Markdown output maintains clean formatting

---

## 🧑‍💻 Author

Created using Python + ChatGPT  
For feedback or extensions, feel free to reach out.

# Markdown Converter Project

This project converts structured knowledge base articles from JSON format into clean, readable Markdown and HTML files.
It supports two different JSON schemas and handles filename formatting, field fallbacks, and basic error handling.

---

## 📁 Project Structure

```
markdown_converter_project/
├── input/
│   ├── articles_data.json           # JSON input for the first format (V2)
│   └── KB_V1_ForProcessing.json     # JSON input for the second format (V1)
│
├── output/
│   ├── html/                        # Generated HTML files
│   └── markdown/                    # Generated Markdown files
│
├── 1st_convert.py                   # Script for processing articles_data.json (V2)
├── 2nd_convert.py                   # Script for processing KB_V1_ForProcessing.json (V1)
└── README.md                        # This file
```

---

## ⚙️ Requirements

### 🐍 Python

- Version: **Python 3.7 or higher**

### 📦 Python Packages

Install dependencies with:

```bash
pip install html2text
pip install beautifulsoup4
```

---

## 🔄 Input Formats

### Format 1: `articles_data.json` (Used by `1st_convert.py`)

Structure:

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

### Format 2: `KB_V1_ForProcessing.json` (Used by `2nd_convert.py`)

Structure:

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

## 🚀 How to Use

### Step 1: Clone the Project or Download

Make sure the project folder looks like this:

```
markdown_converter_project/
├── input/
├── output/
├── 1st_convert.py
├── 2nd_convert.py
└── README.md
```

Place your input `.json` files into the `input/` folder.

### Step 2: Install Python Dependencies

From your terminal or command prompt:

```bash
pip install html2text
```

### Step 3: Run the Script

Navigate to the root of the project folder.

#### ➤ To convert `articles_data.json` (V2 format):

```bash
python 1st_convert.py
```

#### ➤ To convert `KB_V1_ForProcessing.json` (V1 format):

```bash
python 2nd_convert.py
```

---

## 📁 Output Files

After running the script:

- HTML files are created in: `output/html/`
- Markdown files are created in: `output/markdown/`

Each file is named based on the following logic:

- Prefer `Code` or `ShortCode` field (if available)
- Fallback to the `uuid` if `Code`/`ShortCode` is empty or missing
- Filenames are sanitized to avoid illegal characters

---

## 🧼 Example

Given input:

```json
{
  "uuid": "abc-123",
  "fields": {
    "Title": "How to Setup",
    "Body": "<p>Install guide...</p>",
    "ShortCode": "HTS"
  }
}
```

Output files:

- `HTS.html` in `output/html/`
- `HTS.md` in `output/markdown/`

If `ShortCode` is missing or empty, fallback is:

- `abc-123.html`
- `abc-123.md`

---

## 🧠 Error Handling

- Files with missing or empty `Title` or `Body`/`ArticleContent` are skipped.
- All filenames are sanitized to remove characters like `:`, `/`, `*`, etc.
- Scripts use safe fallback access for all optional fields.

---

## 🤝 Contributions & Customization

Feel free to:
- Add front-matter metadata to Markdown files
- Include article tags, dates, or categories
- Extend the script to support other formats

---

## 👨‍💻 Author

Built with help from ChatGPT + Python

If you have questions or feedback, feel free to reach out!

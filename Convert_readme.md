# Markdown Converter Project

This project converts structured knowledge base articles from JSON format into clean, readable Markdown and HTML files. It's ideal for documentation pipelines, static site generators, or knowledge management systems.

---

## 📁 Project Structure

```
markdown_converter_project/
├── input/
│   ├── articles_data.json           # JSON input for the first format
│   └── KB_V1_ForProcessing.json     # JSON input for the second format
│
├── output/
│   ├── html/                        # Generated HTML files
│   └── markdown/                    # Generated Markdown files
│
├── scripts/
│   ├── 1st_convert.py               # Converts articles_data.json
│   └── 2nd_convert.py               # Converts KB_V1_ForProcessing.json
```

---

## ⚙️ Prerequisites

- Python 3.7+
- Required Python package:

```bash
pip install html2text
```

---

## 🚀 How to Use

### 🧠 Convert `articles_data.json` (Format 1)
```bash
cd scripts
python 1st_convert.py
```

### 🧠 Convert `KB_V1_ForProcessing.json` (Format 2)
```bash
cd scripts
python 2nd_convert.py
```

---

## 📝 Output

- HTML files are saved to: `output/html/`
- Markdown files are saved to: `output/markdown/`
- Filenames are based on:
  - The `Code` or `ShortCode` field (if present)
  - Or the fallback `uuid` (if `Code`/`ShortCode` is missing or empty)

---

## 🧼 File Naming

The script automatically:
- Removes illegal characters from filenames
- Falls back to UUIDs if article codes are missing
- Skips entries with empty title or body fields

---

## ✅ Example

If an article has:
```json
"ShortCode": "GSDP",
"uuid": "ccdb9817-ae11-4faa-88e0-00e0f6cc2a2a",
"Title": "Setting Up Deployment",
"Body": "<p>Setup instructions here...</p>"
```

The output will be:
- `GSDP.html`
- `GSDP.md`

If `ShortCode` is empty, fallback is:
- `ccdb9817-ae11-4faa-88e0-00e0f6cc2a2a.html`
- `ccdb9817-ae11-4faa-88e0-00e0f6cc2a2a.md`

---

## 📌 Notes

- Run scripts from the `scripts/` folder or adjust paths if running elsewhere.
- Make sure your input files are in the `input/` directory.

---

## 👨‍💻 Author

Generated with help from ChatGPT.

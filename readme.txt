# 🔍 Pat-INFORMED Patent Date Extractor

This script automates the following:

1. Opens the [Pat-INFORMED WIPO website](https://patinformed.wipo.int/)
2. Searches for **Paracetamol**
3. Accepts terms and selects an INN result
4. Takes a screenshot of the patent details
5. Crops the relevant portion containing **Publication Date** and **Filing Date**
6. Uses OCR (Tesseract) to extract the dates from the image
7. Calculates the number of days between them

---

## 🖥️ Requirements

- Python 3.7+
- Google Chrome browser
- ChromeDriver (auto-managed via `webdriver-manager`)
- Tesseract OCR engine (manual installation below)

---

## 📦 Python Package Installation

```bash
pip install selenium
pip install webdriver-manager
pip install pytesseract
pip install pillow

# HI Result Finder

**HI Result Finder** is a professional Windows desktop application developed to automate the matching and extraction of laboratory results from PDF reports using patient identifiers from Excel spreadsheets.

The project repository is named **LIMS-Result-Matcher**, while the packaged application is distributed as **HI Result Finder**.

---

## Features

- Import patient lists from Excel
- Match patient IDs with laboratory PDF reports
- Extract matching result pages into individual PDF files
- Generate summary reports
- Generate Found, Missing and Unreadable reports
- Drag-and-drop support
- Progress tracking
- Activity logging
- Modern dark-themed interface
- Professional splash screen
- Windows installer

---

## Screenshots

> Screenshots will be added in a future update.

---

## Requirements

- Windows 10 or later
- Python 3.11+ (for development)
- Microsoft Excel (.xlsx input)
- PDF laboratory reports

---

## Installation

### End Users

Download the latest installer from the GitHub Releases page and run:

```
HI_Result_Finder_v3.0_Setup.exe
```

Follow the installation wizard.

---

### Developers

Clone the repository:

```bash
git clone https://github.com/hamzee4tips/LIMS-Result-Matcher.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

---

## Project Structure

```text
LIMS-Result-Matcher/
│
├── assets/
├── config/
├── core/
├── docs/
├── gui/
│
├── app.py
├── version.py
├── requirements.txt
├── HI Result Finder.spec
├── HI_Result_Finder.iss
└── README.md
```

---

## Technologies Used

- Python 3.11
- CustomTkinter
- PyPDF
- Pillow
- PyInstaller
- Inno Setup

---

## Current Version

**Version 3.0**

Production Release

---

## Roadmap

### Version 3.1

- Improved application icon
- Enhanced settings
- PDF preview
- Automatic updates
- Additional reporting enhancements

---

## Developer

**Hamza Isah**

GitHub:

https://github.com/hamzee4tips

---

## License

This project is licensed under the MIT License.
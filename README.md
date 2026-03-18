# Math Worksheet Generator

An automated system designed to generate arithmetic practice worksheets. The tool reads mathematical rules from an Excel configuration file, generates a set of unique problems matching specific distribution percentages, and exports them into a printable 10x10 grid PDF.

## 🚀 Key Features

- **Excel-Driven Logic:** Add or modify problem types (e.g., "Sum < 10", "Contains Zero") via Excel without touching the code.
- **Smart Distribution:** Automatically generates exactly 100 problems following your defined percentage distribution.
- **Print-Ready PDF:** Professional layout including a header (Name, Date, Score) and 100 vertically aligned math problems.
- **Extensible Architecture:** Modular OOP design allows for easy expansion to multi-digit math or different operations.
- **Robust Testing:** 100% logic coverage ensuring mathematical accuracy and system reliability.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jamil2388/Math_Checker.git
   cd Math_Checker
   ```

2. **Set up a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

Run the generator using the default configuration:
```bash
python src/main.py
```

### Advanced Options
Customize the input, output, and worksheet title using CLI flags:
```bash
python src/main.py --config config/problem_types.xlsx --output my_math_sheet.pdf --title "Daily Addition Practice"
```

**CLI Arguments:**
- `--config`: Path to the Excel rule file (default: `config/problem_types.xlsx`).
- `--output`: Path for the generated PDF (default: `math_worksheet.pdf`).
- `--title`: Custom title displayed at the top of the PDF.

## 🧪 Testing

The project uses `pytest` for unit and integration testing. To run all tests:
```bash
pytest
```

## 📝 Documentation

For a deep dive into the system architecture, class documentation, and detailed function specs, please refer to:
- [PROJECT_DESCRIPTION.md](./PROJECT_DESCRIPTION.md)
- [MILESTONES.md](./MILESTONES.md)

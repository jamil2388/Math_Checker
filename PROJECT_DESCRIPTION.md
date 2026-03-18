# Math Worksheet Generator - System Documentation

This document serves as the technical reference for the Math Worksheet Generator project. It details the system architecture, file structure, and exhaustive documentation for every class and function call within the codebase.

## 1. System Overview

The system is designed using **Object-Oriented Programming (OOP)** and **Test-Driven Development (TDD)** principles. It consists of three primary layers:
1.  **Configuration Layer:** Handles external Excel-based rules.
2.  **Logic Engine:** Evaluates rules and generates math problems.
3.  **Presentation Layer:** Renders the final problems into a printable PDF using ReportLab.

---

## 2. Project Directory Tree

Math_Checker/
├── config/
│   └── problem_types.xlsx      # External configuration defining problem rules and percentages.
├── src/
│   ├── __init__.py             # Package initializer.
│   ├── config_loader.py        # logic for reading and parsing Excel configuration.
│   ├── models.py               # Core data structures (ProblemType, MathProblem).
│   ├── problem_generator.py    # The main engine for problem creation and rule evaluation.
│   ├── worksheet_generator.py  # PDF rendering logic using ReportLab.
│   └── main.py                 # CLI entry point and orchestration logic.
├── tests/
│   ├── test_config_loader.py   # Validation suite for configuration parsing.
│   ├── test_problem_generator.py # Validation suite for the generation engine.
│   ├── test_worksheet_generator.py # Validation suite for PDF generation and layout.
│   └── test_integration.py     # End-to-end system validation.
├── PROJECT_DESCRIPTION.md      # This comprehensive documentation file.
├── GEMINI.md                   # Development mandates, coding style, and standards.
├── MILESTONES.md               # Tracking of project completion phases.
└── requirements.txt            # System dependencies.

---

## 3. Detailed Class and Function Documentation

### 3.1 `src/models.py`

#### `class ProblemType`
Represents a mathematical rule and its metadata as defined in the configuration.
- **`__init__(self, type_id: str, description: str, condition: str, percentage: float)`**
    - **Function:** Initializes a rule definition object.
    - **Arguments:**
        - `type_id` (str): Unique identifier for the rule (e.g., 'T1').
        - `description` (str): A human-readable summary of the rule.
        - `condition` (str): A Python-compliant logical string (e.g., 'a + b < 10').
        - `percentage` (float): The portion of the total 100 problems this type should represent.
    - **Returns:** `None`

#### `class MathProblem`
Represents a specific, generated instance of an arithmetic problem.
- **`__init__(self, a: int, b: int, operator: str = '+')`**
    - **Function:** Initializes a concrete math problem with two operands and an operator.
    - **Arguments:**
        - `a` (int): The first number (top operand).
        - `b` (int): The second number (bottom operand).
        - `operator` (str): The mathematical operation (default is '+').
    - **Returns:** `None`

---

### 3.2 `src/config_loader.py`

#### `class ConfigLoader`
Responsible for bridging the gap between the Excel file and the Python system.
- **`__init__(self, file_path: str)`**
    - **Function:** Links the loader to a specific Excel source file.
    - **Arguments:** `file_path` (str): Path to the `.xlsx` config file.
    - **Returns:** `None`
- **`load_config(self) -> list[ProblemType]`**
    - **Function:** Reads the Excel file using `pandas`, iterates through rows, and instantiates `ProblemType` objects.
    - **Arguments:** `None`
    - **Returns:** `list[ProblemType]`: A collection of all parsed rules ready for the generator.

---

### 3.3 `src/problem_generator.py`

#### `class ProblemGenerator`
The core computational engine of the application.
- **`__init__(self, min_val: int = 0, max_val: int = 9)`**
    - **Function:** Configures the generator's operand boundaries.
    - **Arguments:**
        - `min_val` (int): The lowest possible value for an operand (default 0).
        - `max_val` (int): The highest possible value for an operand (default 9).
    - **Returns:** `None`
- **`_evaluate_condition(self, a: int, b: int, condition: str) -> bool`**
    - **Function:** Evaluates a dynamic rule string against two numbers.
    - **Logic:** Uses a restricted `eval()` environment where only variables `a` and `b` are accessible, preventing unauthorized code execution.
    - **Arguments:**
        - `a` (int): First operand.
        - `b` (int): Second operand.
        - `condition` (str): The logical string to test.
    - **Returns:** `bool`: `True` if the numbers satisfy the rule.
- **`generate_problem(self, problem_type: ProblemType) -> MathProblem`**
    - **Function:** Produces a single valid problem for a specific rule.
    - **Logic:** Employs a brute-force randomization strategy, repeatedly picking numbers until the `_evaluate_condition` returns `True`.
    - **Arguments:** `problem_type` (ProblemType): The rule object to satisfy.
    - **Returns:** `MathProblem`: A valid problem instance.
- **`generate_all(self, problem_types: list[ProblemType], total: int = 100) -> list[MathProblem]`**
    - **Function:** Orchestrates the generation of the full worksheet dataset.
    - **Logic:** Calculates exact counts per type based on percentages, handles rounding errors to ensure exactly `total` problems are returned, and shuffles the final list to randomize the layout.
    - **Arguments:**
        - `problem_types` (list[ProblemType]): The list of rules to use.
        - `total` (int): The total number of problems requested (default 100).
    - **Returns:** `list[MathProblem]`: 100 randomized, valid problems.

---

### 3.4 `src/worksheet_generator.py`

#### `class WorksheetGenerator`
The presentation layer responsible for creating a printable PDF document.
- **`__init__(self, output_path: str)`**
    - **Function:** Initializes the generator with a destination file path.
    - **Arguments:** `output_path` (str): Where the `.pdf` file will be written.
    - **Returns:** `None`
- **`_draw_header(self, c: canvas.Canvas, title: str)`**
    - **Function:** Draws the Title, Name/Date/Score fields, and Instructions.
    - **Arguments:**
        - `c` (canvas.Canvas): The reportlab canvas.
        - `title` (str): The main title of the worksheet.
    - **Returns:** `None`
- **`_draw_problem(self, c: canvas.Canvas, x: float, y: float, problem: MathProblem)`**
    - **Function:** Renders a single math problem in a vertical format.
    - **Logic:** Uses a monospaced font (`Courier-Bold`) and right-alignment to ensure operands and the horizontal line are mathematically correct and visually centered.
    - **Arguments:**
        - `c` (canvas.Canvas): The reportlab canvas.
        - `x` (float): Horizontal position.
        - `y` (float): Vertical position.
        - `problem` (MathProblem): Data for the specific problem.
    - **Returns:** `None`
- **`generate_pdf(self, problems: list[MathProblem], title: str = "Arithmetic Practice")`**
    - **Function:** Creates the final 10x10 grid on a US Letter-sized page.
    - **Logic:** Calculates grid coordinates (x, y) for 100 problems and handles the final file saving.
    - **Arguments:**
        - `problems` (list[MathProblem]): Exactly 100 problems to render.
        - `title` (str): Title for the header.
    - **Returns:** `None`

---

### 3.5 `src/main.py`

The command-line interface (CLI) and system orchestrator.
- **`run_system(config_path: str, output_path: str, title: str)`**
    - **Function:** Links the ConfigLoader, ProblemGenerator, and WorksheetGenerator to execute the full generation pipeline.
    - **Arguments:**
        - `config_path` (str): Path to the Excel config.
        - `output_path` (str): Path for the resulting PDF.
        - `title` (str): Custom title for the worksheet.
    - **Returns:** `None`
- **`main()`**
    - **Function:** Handles command-line argument parsing using `argparse`.
    - **Arguments:** Supports `--config`, `--output`, and `--title` flags.
    - **Returns:** `None`

---

## 4. Testing Standards

We maintain 100% logic coverage using `pytest`.
- **Unit Isolation:** Tests use temporary directories (`tmp_path`) and mock data to ensure they don't depend on external file state.
- **Path Integrity:** Every test file dynamically adjusts `sys.path` to ensure the `src` module is discoverable regardless of the execution environment.

# Math Worksheet Generator - System Documentation

This document serves as the technical reference for the Math Worksheet Generator project. It details the system architecture, file structure, and exhaustive documentation for every class and function call within the codebase.

## 1. System Overview

The system is designed using **Object-Oriented Programming (OOP)** and **Test-Driven Development (TDD)** principles. It consists of three primary layers:
1.  **Configuration Layer:** Handles external Excel-based rules.
2.  **Logic Engine:** Evaluates rules and generates math problems.
3.  **Presentation Layer:** (Upcoming) Renders the final problems into a printable PDF.

---

## 2. Project Directory Tree

Math_Checker/
├── config/
│   └── problem_types.xlsx      # External configuration defining problem rules and percentages.
├── src/
│   ├── __init__.py             # Package initializer.
│   ├── config_loader.py        # logic for reading and parsing Excel configuration.
│   ├── models.py               # Core data structures (ProblemType, MathProblem).
│   └── problem_generator.py    # The main engine for problem creation and rule evaluation.
├── tests/
│   ├── test_config_loader.py   # Validation suite for configuration parsing.
│   └── test_problem_generator.py # Validation suite for the generation engine.
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

## 4. Testing Standards

We maintain 100% logic coverage using `pytest`.
- **Unit Isolation:** Tests use temporary directories (`tmp_path`) and mock data to ensure they don't depend on external file state.
- **Path Integrity:** Every test file dynamically adjusts `sys.path` to ensure the `src` module is discoverable regardless of the execution environment.

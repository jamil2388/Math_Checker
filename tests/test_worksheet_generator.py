import pytest
import os
import sys
from unittest.mock import MagicMock

# Ensure the src directory is in the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from src.worksheet_generator import WorksheetGenerator
except ImportError:
    WorksheetGenerator = None

from src.models import MathProblem

def test_worksheet_generator_initialization():
    """
    Test that the WorksheetGenerator can be initialized.
    """
    if WorksheetGenerator is None:
        pytest.fail("WorksheetGenerator class has not been implemented yet.")
    
    generator = WorksheetGenerator("output.pdf")
    assert generator.output_path == "output.pdf"

def test_pdf_generation_creates_file(tmp_path):
    """
    Test that generate_pdf actually creates a file on disk.
    """
    if WorksheetGenerator is None:
        pytest.fail("WorksheetGenerator class has not been implemented yet.")
        
    output_path = os.path.join(tmp_path, "test_worksheet.pdf")
    generator = WorksheetGenerator(output_path)
    
    # Create some dummy problems
    problems = [MathProblem(i, j) for i, j in zip(range(10), range(10))]
    
    generator.generate_pdf(problems, title="Test Worksheet")
    
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0

import pytest
import os
import sys
import pandas as pd

# Ensure the project root is in the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import run_system

def test_full_integration(tmp_path):
    """
    End-to-end test: Config -> Generation -> PDF.
    """
    config_path = os.path.join(tmp_path, "test_config.xlsx")
    output_path = os.path.join(tmp_path, "test_output.pdf")

    # 1. Create temporary config
    df = pd.DataFrame({
        'Type_ID': ['T1'],
        'Description': ['Simple Addition'],
        'Condition': ['a + b < 10'],
        'Percentage': [100]
    })
    df.to_excel(config_path, index=False)

    # 2. Run system
    run_system(config_path, output_path, title="Integration Test")

    # 3. Verify output
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0

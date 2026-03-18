import pytest
import pandas as pd
import os
import sys

# Ensure the src directory is in the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# This import will fail because ConfigLoader doesn't exist yet!
try:
    from src.config_loader import ConfigLoader
except ImportError:
    ConfigLoader = None

def test_config_loader_initialization(tmp_path):
    """
    Test that the ConfigLoader can be initialized with a path.
    
    Arguments:
        tmp_path: Pytest fixture for a temporary directory.
    """
    if ConfigLoader is None:
        pytest.fail("ConfigLoader class has not been implemented yet.")
        
    config_path = os.path.join(tmp_path, "config.xlsx")
    loader = ConfigLoader(config_path)
    assert loader.file_path == config_path

def test_config_loader_load_config(tmp_path):
    """
    Test that ConfigLoader.load_config() returns a list of ProblemType objects.

    Arguments:
        tmp_path: Pytest fixture for a temporary directory.
    """
    if ConfigLoader is None:
        pytest.fail("ConfigLoader class has not been implemented yet.")

    config_path = os.path.join(tmp_path, "problem_types.xlsx")
    
    # Create a sample Excel file for testing
    df = pd.DataFrame({
        'Type_ID': ['T1', 'T2'],
        'Description': ['Sum < 10', 'Sum = 10'],
        'Condition': ['a + b < 10', 'a + b == 10'],
        'Percentage': [40, 20]
    })
    df.to_excel(config_path, index=False)
    
    loader = ConfigLoader(config_path)
    problem_types = loader.load_config()
    
    assert len(problem_types) == 2
    assert problem_types[0].type_id == 'T1'
    assert problem_types[1].percentage == 20

import pytest
import os
import sys

# Ensure the src directory is in the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models import ProblemType, MathProblem
# Placeholder for ProblemGenerator
try:
    from src.problem_generator import ProblemGenerator
except ImportError:
    ProblemGenerator = None

def test_problem_generator_initialization():
    """
    Test that the ProblemGenerator can be initialized.
    """
    if ProblemGenerator is None:
        pytest.fail("ProblemGenerator class has not been implemented yet.")
    
    generator = ProblemGenerator()
    assert generator is not None

def test_rule_evaluator_simple():
    """
    Test that the rule evaluator can correctly evaluate simple addition conditions.
    """
    if ProblemGenerator is None:
        pytest.fail("ProblemGenerator class has not been implemented yet.")
        
    generator = ProblemGenerator()
    # a + b < 10
    assert generator._evaluate_condition(4, 3, "a + b < 10") is True
    assert generator._evaluate_condition(6, 5, "a + b < 10") is False
    
    # a + b == 10
    assert generator._evaluate_condition(5, 5, "a + b == 10") is True
    assert generator._evaluate_condition(5, 4, "a + b == 10") is False

def test_generate_problem_matches_condition():
    """
    Test that generate_problem returns a MathProblem that satisfies the given ProblemType's condition.
    """
    if ProblemGenerator is None:
        pytest.fail("ProblemGenerator class has not been implemented yet.")
        
    generator = ProblemGenerator()
    pt = ProblemType("T1", "Sum < 10", "a + b < 10", 40)
    
    # Generate 10 problems and verify they all match
    for _ in range(10):
        problem = generator.generate_problem(pt)
        assert problem.a + problem.b < 10
        assert 0 <= problem.a <= 9
        assert 0 <= problem.b <= 9

def test_generate_all_distribution():
    """
    Test that generate_all creates exactly the requested number of problems and follows distribution rules.
    """
    if ProblemGenerator is None:
        pytest.fail("ProblemGenerator class has not been implemented yet.")
        
    generator = ProblemGenerator()
    problem_types = [
        ProblemType("T1", "Sum < 10", "a + b < 10", 60),
        ProblemType("T2", "Sum = 10", "a + b == 10", 40)
    ]
    
    total = 100
    problems = generator.generate_all(problem_types, total=total)
    
    assert len(problems) == total
    
    # Count how many match each condition
    count_t1 = 0
    count_t2 = 0
    for p in problems:
        if p.a + p.b < 10:
            count_t1 += 1
        elif p.a + p.b == 10:
            count_t2 += 1
            
    # Check if distribution is exactly as requested (60/40)
    assert count_t1 == 60
    assert count_t2 == 40

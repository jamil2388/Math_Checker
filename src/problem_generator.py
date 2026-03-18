import random
from src.models import ProblemType, MathProblem

class ProblemGenerator:
    """
    A class to generate arithmetic math problems based on specific rules.
    """

    def __init__(self, min_val: int = 0, max_val: int = 9):
        """
        Initializes the ProblemGenerator.

        Arguments:
            min_val (int): Minimum operand value (default 0).
            max_val (int): Maximum operand value (default 9).

        Returns:
            None
        """
        self.min_val = min_val
        self.max_val = max_val

    def _evaluate_condition(self, a: int, b: int, condition: str) -> bool:
        """
        Evaluates a logic condition string for two numbers.

        Arguments:
            a (int): First operand.
            b (int): Second operand.
            condition (str): Logic rule (e.g., 'a + b < 10').

        Returns:
            bool: True if condition matches, False otherwise.
        """
        # Create a safe evaluation environment with operands 'a' and 'b'
        # We restrict access to built-ins for better security
        safe_env = {'a': a, 'b': b}
        try:
            return bool(eval(condition, {"__builtins__": {}}, safe_env))
        except Exception as e:
            # Handle potential evaluation errors (e.g., invalid syntax in condition)
            raise ValueError(f"Failed to evaluate condition '{condition}': {e}")

    def generate_problem(self, problem_type: ProblemType) -> MathProblem:
        """
        Generates a MathProblem that satisfies the given ProblemType's condition.

        Arguments:
            problem_type (ProblemType): The rule to follow.

        Returns:
            MathProblem: A generated problem instance.
        """
        # Attempt to generate a matching problem (brute-force approach for one-digit)
        # We iterate until a valid combination of 'a' and 'b' is found
        max_attempts = 1000
        for _ in range(max_attempts):
            a = random.randint(self.min_val, self.max_val)
            b = random.randint(self.min_val, self.max_val)
            if self._evaluate_condition(a, b, problem_type.condition):
                return MathProblem(a, b)
        
        raise RuntimeError(f"Could not generate a problem matching '{problem_type.condition}' after {max_attempts} attempts.")

    def generate_all(self, problem_types: list[ProblemType], total: int = 100) -> list[MathProblem]:
        """
        Generates a list of MathProblems based on the specified distribution percentages.

        Arguments:
            problem_types (list[ProblemType]): List of available problem types with percentages.
            total (int): Total number of problems to generate (default 100).

        Returns:
            list[MathProblem]: List of all generated problems.
        """
        all_problems = []
        
        # Determine the number of problems for each type based on percentages
        for pt in problem_types:
            count = int((pt.percentage / 100.0) * total)
            for _ in range(count):
                all_problems.append(self.generate_problem(pt))
        
        # Fill remaining slots if any (due to rounding)
        # We use the first problem type as a fallback
        while len(all_problems) < total and problem_types:
            all_problems.append(self.generate_problem(problem_types[0]))
            
        # Shuffle the list to randomize problem order
        random.shuffle(all_problems)
        return all_problems

import random
import re
from src.models import ProblemType, MathProblem

class ProblemGenerator:
    """
    A class to generate arithmetic math problems with dynamic range and operator inference.
    """

    def __init__(self, default_min: int = 0, default_max: int = 9):
        """
        Initializes the ProblemGenerator.

        Arguments:
            default_min (int): Default minimum operand value (default 0).
            default_max (int): Default maximum operand value (default 9).

        Returns:
            None
        """
        self.default_min = default_min
        self.default_max = default_max

    def _infer_range(self, condition: str) -> tuple[int, int]:
        """
        Infers the minimum and maximum range of operands from the condition string.

        Arguments:
            condition (str): Logic rule (e.g., 'a + b < 50').

        Returns:
            tuple[int, int]: (min_val, max_val).
        """
        # Find all numeric constants in the condition string
        numbers = [int(n) for n in re.findall(r'\d+', condition)]
        
        if not numbers:
            return self.default_min, self.default_max
            
        # The range is determined by the highest number mentioned, with a bit of headroom
        # We also check for minimum values if they are explicitly mentioned
        max_val = max(numbers)
        
        # If the highest number is small (e.g. single digit), stick to default max unless overridden
        max_val = max(max_val, self.default_max)
        
        # Add headroom (e.g., 20% or a minimum increment) to ensure we have search space
        max_val = int(max_val * 1.5) if max_val > 9 else 9
        
        return self.default_min, max_val

    def _infer_operator(self, condition: str) -> str:
        """
        Infers the mathematical operator from the condition string.

        Arguments:
            condition (str): Logic rule (e.g., 'a - b > 5').

        Returns:
            str: The inferred operator (+, -, *, /). Defaults to '+' if none found.
        """
        # Priority map for common operators
        operators = {
            '-': '-',
            '*': '*',
            '/': '/',
            '+': '+'
        }
        
        for char, op in operators.items():
            if char in condition:
                return op
        
        return '+'

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
        # Python's '&&' and '||' equivalents are 'and' and 'or'
        # We replace them for compatibility if the user wrote them in Excel
        processed_condition = condition.replace('&&', ' and ').replace('||', ' or ')
        
        safe_env = {'a': a, 'b': b}
        try:
            return bool(eval(processed_condition, {"__builtins__": {}}, safe_env))
        except Exception as e:
            raise ValueError(f"Failed to evaluate condition '{condition}': {e}")

    def generate_problem(self, problem_type: ProblemType) -> MathProblem:
        """
        Generates a MathProblem that satisfies the given ProblemType's condition.

        Arguments:
            problem_type (ProblemType): The rule to follow.

        Returns:
            MathProblem: A generated problem instance.
        """
        min_val, max_val = self._infer_range(problem_type.condition)
        operator = self._infer_operator(problem_type.condition)
        
        max_attempts = 2000 # Increased for larger search spaces
        for _ in range(max_attempts):
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
            if self._evaluate_condition(a, b, problem_type.condition):
                return MathProblem(a, b, operator=operator)
        
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
        
        for pt in problem_types:
            count = int((pt.percentage / 100.0) * total)
            for _ in range(count):
                all_problems.append(self.generate_problem(pt))
        
        while len(all_problems) < total and problem_types:
            all_problems.append(self.generate_problem(problem_types[0]))
            
        random.shuffle(all_problems)
        return all_problems

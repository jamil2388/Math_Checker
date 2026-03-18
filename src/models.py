class ProblemType:
    """
    Represents a type of math problem with its rule and distribution percentage.
    """

    def __init__(self, type_id: str, description: str, condition: str, percentage: float):
        """
        Initializes a ProblemType.

        Arguments:
            type_id (str): Unique identifier (e.g., 'T1').
            description (str): Human-readable description.
            condition (str): Logic rule (e.g., 'a + b < 10').
            percentage (float): Distribution percentage (e.g., 40.0).

        Returns:
            None
        """
        self.type_id = type_id
        self.description = description
        self.condition = condition
        self.percentage = percentage


class MathProblem:
    """
    Represents a specific math problem instance.
    """

    def __init__(self, a: int, b: int, operator: str = '+'):
        """
        Initializes a MathProblem.

        Arguments:
            a (int): First operand.
            b (int): Second operand.
            operator (str): Operation type (default is '+').

        Returns:
            None
        """
        self.a = a
        self.b = b
        self.operator = operator

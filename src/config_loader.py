import pandas as pd
from src.models import ProblemType

class ConfigLoader:
    """
    A class to load math problem configurations from Excel files.
    """

    def __init__(self, file_path: str):
        """
        Initializes the ConfigLoader with the path to the Excel configuration file.

        Arguments:
            file_path (str): The absolute or relative path to the .xlsx file.

        Returns:
            None
        """
        # Set the file path for the configuration file
        self.file_path = file_path

    def load_config(self) -> list[ProblemType]:
        """
        Reads the Excel file and returns a list of ProblemType objects.

        Returns:
            list[ProblemType]: List of parsed problem types.
        """
        # Load the configuration from the Excel file
        df = pd.read_excel(self.file_path)
        problem_types = []
        for _, row in df.iterrows():
            # Create a ProblemType object for each row in the DataFrame
            problem_types.append(ProblemType(
                type_id=str(row['Type_ID']),
                description=str(row['Description']),
                condition=str(row['Condition']),
                percentage=float(row['Percentage'])
            ))
        return problem_types

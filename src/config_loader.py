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

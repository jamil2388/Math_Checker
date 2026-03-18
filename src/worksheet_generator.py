from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from src.models import MathProblem

class WorksheetGenerator:
    """
    Handles the creation of printable PDF math worksheets using reportlab.
    """

    def __init__(self, output_path: str):
        """
        Initializes the WorksheetGenerator with a target file path.

        Arguments:
            output_path (str): The absolute or relative path where the .pdf will be saved.

        Returns:
            None
        """
        self.output_path = output_path

    def _draw_header(self, c: canvas.Canvas, title: str):
        """
        Draws the worksheet header including metadata fields and instructions.

        Arguments:
            c (canvas.Canvas): The reportlab canvas object.
            title (str): The title text to display at the top.

        Returns:
            None
        """
        # Title - Centered at the top
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(300, 750, title)
        
        # Information Fields (Name, Date, Score)
        c.setFont("Helvetica", 11)
        c.drawString(50, 720, "Name: ________________________________")
        c.drawString(350, 720, "Date: ____________________")
        c.drawString(50, 700, "Score: ________ / 100")
        
        # Instructions section
        c.setFont("Helvetica-Oblique", 11)
        c.drawString(50, 670, "Instructions: Calculate each sum.")
        
        # Separator Line
        c.line(50, 660, 550, 660)

    def _draw_problem(self, c: canvas.Canvas, x: float, y: float, problem: MathProblem):
        """
        Renders a single math problem in vertical format with proper alignment.

        Arguments:
            c (canvas.Canvas): The reportlab canvas object.
            x (float): The horizontal starting coordinate.
            y (float): The vertical starting coordinate.
            problem (MathProblem): The problem data to render.

        Returns:
            None
        """
        # Use a monospaced font for predictable alignment of numbers
        font_name = "Courier-Bold"
        font_size = 14
        c.setFont(font_name, font_size)
        
        # Right-aligning the numbers to handle single/multi-digit consistency
        # First operand (top)
        c.drawRightString(x + 25, y + 25, str(problem.a))
        
        # Operator and second operand (bottom)
        c.drawString(x, y + 10, problem.operator)
        c.drawRightString(x + 25, y + 10, str(problem.b))
        
        # Horizontal calculation line
        c.line(x - 5, y + 5, x + 30, y + 5)

    def generate_pdf(self, problems: list[MathProblem], title: str = "Arithmetic Practice"):
        """
        Generates a complete PDF document containing a 10x10 grid of problems.

        Arguments:
            problems (list[MathProblem]): Collection of exactly 100 problems to render.
            title (str): Title displayed in the worksheet header.

        Returns:
            None
        """
        c = canvas.Canvas(self.output_path, pagesize=letter)
        
        # Render the static header elements
        self._draw_header(c, title)
        
        # Define grid layout constants for 100 problems
        start_x = 65
        start_y = 610
        col_width = 52
        row_height = 55
        
        # Iterate through the problems and place them in the grid
        for i, problem in enumerate(problems):
            if i >= 100: 
                break # Enforce the 100-problem limit per page
            
            col = i % 10
            row = i // 10
            
            x = start_x + (col * col_width)
            y = start_y - (row * row_height)
            
            self._draw_problem(c, x, y, problem)
            
        c.showPage()
        c.save()

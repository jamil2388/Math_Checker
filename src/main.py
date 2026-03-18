import argparse
import sys
import os

# Ensure the project root is in the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config_loader import ConfigLoader
from src.problem_generator import ProblemGenerator
from src.worksheet_generator import WorksheetGenerator

def run_system(config_path: str, output_path: str, title: str = "Arithmetic Practice"):
    """
    Orchestrates the full math worksheet generation process.

    Arguments:
        config_path (str): Path to the Excel configuration file.
        output_path (str): Path where the final PDF should be saved.
        title (str): Title for the worksheet.

    Returns:
        None
    """
    print(f"[*] Loading configuration from: {config_path}")
    loader = ConfigLoader(config_path)
    problem_types = loader.load_config()

    print(f"[*] Generating 100 math problems based on distribution...")
    generator = ProblemGenerator()
    problems = generator.generate_all(problem_types, total=100)

    print(f"[*] Creating PDF worksheet at: {output_path}")
    pdf_gen = WorksheetGenerator(output_path)
    pdf_gen.generate_pdf(problems, title=title)
    
    print("[+] Worksheet successfully generated!")

def main():
    """
    Entry point for the Math Worksheet Generator CLI.
    """
    parser = argparse.ArgumentParser(description="Generate 100 arithmetic problems into a PDF worksheet.")
    
    parser.add_argument(
        "--config", 
        type=str, 
        default="config/problem_types.xlsx",
        help="Path to the Excel configuration file (default: config/problem_types.xlsx)"
    )
    
    parser.add_argument(
        "--output", 
        type=str, 
        default="math_worksheet.pdf",
        help="Path for the output PDF file (default: math_worksheet.pdf)"
    )
    
    parser.add_argument(
        "--title", 
        type=str, 
        default="Arithmetic Practice",
        help="Title for the worksheet (default: Arithmetic Practice)"
    )

    args = parser.parse_args()

    # Validate config exists
    if not os.path.exists(args.config):
        print(f"Error: Configuration file '{args.config}' not found.")
        sys.exit(1)

    try:
        run_system(args.config, args.output, args.title)
    except Exception as e:
        print(f"Error: System execution failed - {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

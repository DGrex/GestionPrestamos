import os
from core.colors import Fore, Back, Style


class ConsoleUtils:
    @staticmethod
    def clear_screen():
        """Clear the console screen."""
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def gotoxy(x, y):
        """Move cursor to position (x, y). 1-based."""
        print(f"\033[{y};{x}H", end="")

    @staticmethod
    def print_colored(text, color=Fore.WHITE, style=Style.NORMAL):
        """Print text with specified color and style."""
        print(f"{style}{color}{text}{Style.RESET_ALL}")

    @staticmethod
    def print_header(text, color=Fore.CYAN, style=Style.BRIGHT):
        """Print a header with color."""
        ConsoleUtils.print_colored(f"\n{text}\n", color, style)

    @staticmethod
    def print_error(text):
        """Print error message in red."""
        ConsoleUtils.print_colored(text, Fore.RED)

    @staticmethod
    def print_success(text):
        """Print success message in green."""
        ConsoleUtils.print_colored(text, Fore.GREEN)

    @staticmethod
    def print_info(text):
        """Print info message in yellow."""
        ConsoleUtils.print_colored(text, Fore.YELLOW)

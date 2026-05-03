try:
    from colorama import Fore, Back, Style, init

    init(autoreset=True)
except ImportError:

    class _ColorStub:
        RESET_ALL = ""
        BLACK = ""
        RED = ""
        GREEN = ""
        YELLOW = ""
        BLUE = ""
        MAGENTA = ""
        CYAN = ""
        WHITE = ""
        LIGHTBLACK_EX = ""
        LIGHTRED_EX = ""
        LIGHTGREEN_EX = ""
        LIGHTYELLOW_EX = ""
        LIGHTBLUE_EX = ""
        LIGHTMAGENTA_EX = ""
        LIGHTCYAN_EX = ""
        LIGHTWHITE_EX = ""

    Fore = _ColorStub()
    Back = _ColorStub()
    Style = _ColorStub()

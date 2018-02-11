
import sys


# http://blog.mathieu-leplatre.info/colored-output-in-console-with-python.html
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def __has_colors(stream, allow_piping=False):
    """Check if Console Has Color."""
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():   # not being piped or redirected
        return allow_piping  # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False


# Has Color Init
has_colors = __has_colors(sys.stdout, True)


# Support methods
def colorText(text, color=WHITE):
    """Color Text."""
    if has_colors:
        return "\x1b[1;%dm" % (30 + color) + str(text) + "\x1b[0m"

    return text


def print_color_text(msg, color=WHITE):
    """Print Color Text."""
    print(colorText(msg, color))


def header(msg, overline_char='=', underline_char='='):
    """Print Header."""
    print_color_text(overline_char * 80, CYAN)
    print_color_text(msg, CYAN)
    print_color_text(underline_char * 80, CYAN)


def sub_header(msg, overline_char='-', underline_char='-'):
    """Print Sub-Header."""
    header(msg, overline_char, underline_char)

from config import TRACE


def trace(msg):
    """
    Turning printing of events on and off.

    Params:
    -------
    msg: str
        string to print to screen.
    """
    if TRACE:
        print(msg)

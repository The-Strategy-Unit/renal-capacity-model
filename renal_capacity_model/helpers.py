from config import g


def trace(msg):
    """
    Turning printing of events on and off.

    Params:
    -------
    msg: str
        string to print to screen.
    """
    if g.trace:
        print(msg)

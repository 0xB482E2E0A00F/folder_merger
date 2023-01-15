import sys
import platform

def wait_for_keypress():
    if platform.system() == "Windows":
        import msvcrt

        print("Press any key to exit...")
        msvcrt.getch()

    elif platform.system() == "Linux":
        import termios, atexit

        # Save the terminal settings
        fd = sys.stdin.fileno()
        new_term = termios.tcgetattr(fd)
        old_term = termios.tcgetattr(fd)

        # New terminal setting unbuffered
        new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)

        # Switch to normal terminal
        def set_normal_term():
            termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)

        # Switch to unbuffered terminal
        def set_curses_term():
            termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)

        atexit.register(set_normal_term)
        set_curses_term()

        print("Press any key to exit...")

        while True:
            select([sys.stdin], [], [], None)
            c = sys.stdin.read(1)
            break
    else:
        input("Press Enter to exit...")

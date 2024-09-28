#! /usr/bin/env python3

from gui import Window


def main():
    win = Window(1024, 768)
    win.wait_for_close()


if __name__ == "__main__":
    main()

import sys

from .app import App


def main() -> int:
    app: App = App()
    app.initialize_ui()
    app.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())

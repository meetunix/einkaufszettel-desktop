import tkinter as tk
import argparse
from argparse import Namespace

from einkaufszettel.controller import Controller
from einkaufszettel.entities import Server


class EinkaufszettelDesktop(tk.Tk):
    def __init__(self, args: Namespace, server: Server):
        super(EinkaufszettelDesktop, self).__init__()
        self.title("Einkaufszettel Desktop App")
        self.geometry("1400x768")
        if args.fixed_window:
            self.resizable(False, False)
        self.controller = Controller(server=server)

    def set_server(self, server: Server):
        self.controller.set_server(server)

    def on_closing(self):
        self.destroy()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixed-window", action="store_true", help="Fixed window size")
    args = parser.parse_args()

    server = Server(name="localhost", base_url="http://127.0.0.1", port=18080)

    app = EinkaufszettelDesktop(args, server)
    app.mainloop()


if __name__ == "__main__":
    main()

import tkinter as tk
import argparse
from argparse import Namespace
from pathlib import Path

from einkaufszettel.controller import Controller
from einkaufszettel.entities import Server, SavedEZ, Configuration


class EinkaufszettelDesktop(tk.Tk):
    def __init__(self, args: Namespace):
        super(EinkaufszettelDesktop, self).__init__()
        self.title("Einkaufszettel Desktop App")
        self.geometry("1400x768")
        if args.fixed_window:
            self.resizable(False, False)
        self.controller = Controller(config_path="./config/ezrc.json")

        self.controller.get_ez("76f2c9e4-ea57-4df6-bdbf-cc7a5301df80")
        self.controller.get_ez("76f2c9e4-ea57-4df6-bdbf-cc7a5301df81")

    def on_closing(self):
        self.destroy()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixed-window", action="store_true", help="Fixed window size")
    args = parser.parse_args()

    app = EinkaufszettelDesktop(args)
    # app.mainloop()


if __name__ == "__main__":
    main()

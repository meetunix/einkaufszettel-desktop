import argparse
import tkinter as tk
from argparse import Namespace
from pathlib import Path

from einkaufszettel.controller import Controller
from einkaufszettel.view import ListFrame, MenuFrame, EditFrame


class EinkaufszettelDesktop(tk.Tk):
    def __init__(self, args: Namespace):
        super(EinkaufszettelDesktop, self).__init__()
        self.title("Einkaufszettel Desktop App")
        self.geometry("1400x768")
        if args.fixed_window:
            self.resizable(False, False)
        self.controller = Controller(config_path=args.config_dir / Path("ezrc.json"), cache_path=args.cache_dir)

        self.columnconfigure(0, weight=3)  # ListFrame
        self.columnconfigure(1, weight=9)  # EditFrame
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=100)

        self.menu_frame = MenuFrame(self)
        self.menu_frame.grid(columnspan=1, row=0, sticky="W")

        self.list_frame = ListFrame(self)
        self.list_frame.grid(column=0, row=1, sticky="NSEW")

        self.edit_frame = EditFrame(self)
        self.edit_frame.grid(column=1, row=1, sticky="NSEW")

        # self.controller.get_ez_from_remote("76f2c9e4-ea57-4df6-bdbf-cc7a5301df80", print)
        # self.controller.get_ez_from_remote("76f2c9e4-ea57-4df6-bdbf-cc7a5301df81", print)

    def on_closing(self):
        self.destroy()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixed-window", action="store_true", help="Fixed window size")
    parser.add_argument("--config-dir", type=Path, help="Path to config dir (default: ~/.config/ez-desktop)")
    parser.add_argument("--cache-dir", type=Path, help="Path to cache directory (default: ~/.cache/ez-dir)")
    args = parser.parse_args()

    app = EinkaufszettelDesktop(args)
    app.mainloop()


if __name__ == "__main__":
    main()

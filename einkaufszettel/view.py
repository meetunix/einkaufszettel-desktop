import tkinter
from tkinter import ttk

from einkaufszettel.controller import Controller


class BasicFrame(ttk.Frame):
    """All frames inherit from this class."""

    def __init__(self, container):
        super(BasicFrame, self).__init__(container)
        self["borderwidth"] = 1
        self["relief"] = "flat"
        self.font_heading = ("Helvetica", 12)
        self.font_medium = ("Helvetica", 12, "bold")
        self.font_big = ("Helvetica", 14, "bold")
        self.font_typewriter = ("Monospace", 10)
        self.font_typewriter_big = ("Monospace", 14)
        self.style_overflow_bar = ttk.Style()
        self.options = {"padx": 5, "pady": 5, "sticky": "NSEW"}


class PopUpWindow(tkinter.Toplevel):
    def __init__(self, root_button: ttk.Button = None):
        super(PopUpWindow, self).__init__()
        # self.geometry("680x550")
        self.maxsize(width=1600, height=1000)
        self.resizable(False, False)
        self.padding = {"pady": 10, "padx": 10}


class ChooseEzWindow(PopUpWindow):
    def __init__(self, controller: Controller):
        super().__init__()
        self.columnconfigure(0, weight=20)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0)
        self.ezs = controller.get_all_ez()

        self.frame_listbox = BasicFrame(self)
        self.frame_listbox.columnconfigure(0, weight=1000)
        self.frame_listbox.columnconfigure(1, weight=1)
        self.frame_listbox.rowconfigure(0)
        self.frame_listbox.grid(column=0, row=0, sticky="NSEW")

        self.listbox_ezs = tkinter.Listbox(self.frame_listbox, exportselection=0, selectmode=tkinter.SINGLE)
        self.listbox_ezs.grid(column=0, row=0, sticky="NSEW")
        self.scroller = tkinter.Scrollbar(self.frame_listbox, orient=tkinter.VERTICAL, command=self.listbox_ezs.yview)
        self.scroller.grid(column=1, row=0, sticky="NS")
        self.listbox_ezs["yscrollcommand"] = self.scroller.set
        idx = 0
        for ez in self.ezs:
            self.listbox_ezs.insert(idx, f"{ez.name:16}")
            idx += 1


def dummy_action():
    pass


class MenuFrame(BasicFrame):
    def __init__(self, container):
        super().__init__(container)
        for i in range(3):
            self.columnconfigure(i)
        self.rowconfigure(0)
        self.controller = container.controller

        self.menu_button_ez = tkinter.Menubutton(self, text="Einkaufszettel")
        self.menu_button_ez.grid(column=0, row=0, sticky="W")
        self.menu_ez = tkinter.Menu(self.menu_button_ez, tearoff=0)
        self.menu_button_ez["menu"] = self.menu_ez
        self.menu_ez.add_command(label="Wähle Einkaufszettel", command=lambda: self.choose_ez(self.controller))  # todo
        self.menu_ez.add_command(label="An Server senden (speichern)", command=dummy_action)  # todo
        self.menu_ez.add_command(label="Aktuellen Einkaufszettel aktualisieren", command=dummy_action)  # todo
        self.menu_ez.add_command(label="Neuen Einkaufzettel vom Server laden", command=dummy_action)  # todo
        self.menu_ez.add_command(label="Lokal speichern", command=dummy_action)  # todo
        self.menu_ez.add_command(label="Lokal laden", command=dummy_action)  # todo

        self.menu_button_config = tkinter.Menubutton(self, text="Konfiguration")
        self.menu_button_config.grid(column=1, row=0, sticky="W")
        self.menu_config = tkinter.Menu(self.menu_button_config, tearoff=0)
        self.menu_button_config["menu"] = self.menu_config
        self.menu_config.add_command(label="Server wählen", command=dummy_action)
        self.menu_config.add_command(label="Konfiguration Bearbeiten", command=self.__edit_configuration)

        self.menu_button_help = tkinter.Menubutton(self, text="Hilfe")
        self.menu_button_help.grid(column=2, row=0, sticky="W")
        self.menu_help = tkinter.Menu(self.menu_button_help, tearoff=0)
        self.menu_button_help["menu"] = self.menu_help

    def __edit_configuration(self):
        pass

    def choose_ez(self, controller):
        # todo check controller if ezs are in config otherwise open ez_load_window
        self.window = ChooseEzWindow(controller)
        self.window.mainloop()


class ListFrame(BasicFrame):
    """Frame showed at the right of the app which shows the current items from the current shopping list."""

    def __init__(self, container):
        super().__init__(container)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # subframe which holds the cart list
        self.frame_cart = ttk.LabelFrame(self, text="shopping-list")
        self.frame_cart.columnconfigure(0, weight=1000)
        self.frame_cart.columnconfigure(1, weight=1)
        self.frame_cart.rowconfigure(0, weight=1)
        self.frame_cart.grid(column=0, row=0, **self.options)

        # cart list
        self.listbox_cart = tkinter.Listbox(
            self.frame_cart,
            font=self.font_typewriter,
            exportselection=0,
            selectmode=tkinter.SINGLE,
        )
        self.listbox_cart.grid(column=0, row=0, **self.options)
        self.scroller = tkinter.Scrollbar(self.frame_cart, orient=tkinter.VERTICAL, command=self.listbox_cart.yview)
        self.scroller.grid(column=1, row=0, sticky="NS")
        self.listbox_cart["yscrollcommand"] = self.scroller.set
        for i in range(120):
            self.listbox_cart.insert(i, f"test {i}")

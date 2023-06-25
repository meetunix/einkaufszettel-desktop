import tkinter
from enum import Enum
from tkinter import ttk

from einkaufszettel.controller import Controller
from einkaufszettel.entities import ConfigEZ


class EZConfigSelectLabel(Enum):
    NAME = "Name"
    ID = "ID"
    SERVER_NAME = "Server-Name"
    SERVER_URL = "Server-URL"


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
        self.padding = {"pady": 5, "padx": 5}


class ChooseEzWindow(PopUpWindow):
    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=20)
        self.rowconfigure(0)

        self.frame_listbox = BasicFrame(self)
        self.frame_listbox.columnconfigure(0, weight=1000)
        self.frame_listbox.columnconfigure(1, weight=1)
        self.frame_listbox.rowconfigure(0)
        self.frame_listbox.grid(column=0, row=0, sticky="NSEW")

        self.__refresh()
        self.listbox_ezs = tkinter.Listbox(
            self.frame_listbox, listvariable=self.listvar_ezs, exportselection=0, selectmode=tkinter.SINGLE, height=20
        )
        self.listbox_ezs.grid(column=0, row=0, sticky="NSEW")
        self.scroller = tkinter.Scrollbar(self.frame_listbox, orient=tkinter.VERTICAL, command=self.listbox_ezs.yview)
        self.scroller.grid(column=1, row=0, sticky="NS")
        self.listbox_ezs["yscrollcommand"] = self.scroller.set
        self.listbox_ezs.bind("<<ListboxSelect>>", self.__on_listbox_select)

        self.frame_left = BasicFrame(self)
        self.frame_left.columnconfigure(0, weight=1, minsize=150)  # todo minsize has no effect
        self.frame_left.columnconfigure(1, weight=3, minsize=450)

        rows = list(range(len(EZConfigSelectLabel) + 1))
        for i in rows:
            self.frame_left.rowconfigure(i)
        self.frame_left.grid(column=1, row=0)

        self.button_load = ttk.Button(self.frame_left, text="laden", command=self.__load_ez)
        self.button_load.grid(column=0, row=rows[-1], sticky="W", **self.padding)

        # set static labels
        row = 0
        self.label_map = {}
        for select_label in EZConfigSelectLabel:
            label = ttk.Label(self.frame_left, text=f"{select_label.value}: ")
            label.grid(column=0, row=row, sticky="W", **self.padding)
            label_dynamic = ttk.Label(self.frame_left, text=f"n.a.")
            label_dynamic.grid(column=1, row=row, sticky="W", **self.padding)
            self.label_map[select_label] = label_dynamic
            row += 1

        self.__refresh()

    def __on_listbox_select(self, event):
        selected_idx = self.listbox_ezs.curselection()[0]
        config_ez: ConfigEZ = self.config_ezs[selected_idx]
        server = self.controller.get_configuration().get_server_by_id(config_ez.server_id)
        self.label_map[EZConfigSelectLabel.ID]["text"] = config_ez.eid
        self.label_map[EZConfigSelectLabel.NAME]["text"] = config_ez.name
        self.label_map[EZConfigSelectLabel.SERVER_NAME]["text"] = server.name
        self.label_map[EZConfigSelectLabel.SERVER_URL]["text"] = server.base_url

    def __load_ez(self):
        """Loads the EZ from remote and close the window."""
        # load the ez from lokal cache
        pass  # todo

    def __refresh_listvar_ez(self):
        # todo throw configuration exception
        self.config_ezs = self.controller.get_all_ez_from_config()
        self.listvar_ezs = tkinter.Variable(value=self.config_ezs)

    def __refresh(self):
        self.__refresh_listvar_ez()


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
    """Frame showed at the left of the app which shows the current items from the current shopping list."""

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


class EditFrame(BasicFrame):
    """Frame showed at the right of the app, used for editing the current list item and save and reload the whole ez."""

    def __init__(self, container):
        super().__init__(container)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=4)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(0, weight=100)

        # subframe which holds the cart list
        self.frame_ctrls = ttk.Frame(self)
        self.frame_ctrls.columnconfigure(0, weight=1)
        self.frame_ctrls.columnconfigure(2, weight=1)
        self.frame_ctrls.columnconfigure(3, weight=1)
        self.frame_ctrls.rowconfigure(0, weight=1)
        self.frame_ctrls.grid(column=0, row=0, padx=5, pady=5, sticky="NWE")

        self.button_refresh_state = ttk.Button(
            self.frame_ctrls, text="reload from remote", command=self.__on_click_refresh_state
        )
        self.button_refresh_state.grid(column=0, row=0, sticky="W")
        self.button_load_remote = ttk.Button(
            self.frame_ctrls, text="reload from remote", command=self.__on_click_load_remote
        )
        self.button_load_remote.grid(column=1, row=0, sticky="W")

        self.button_save_remote = ttk.Button(
            self.frame_ctrls, text="save to remote", command=self.__on_click_save_remote
        )
        self.button_save_remote.grid(column=2, row=0, sticky="W")

    def __on_click_refresh_state(self):
        pass

    def __on_click_load_remote(self):
        pass

    def __on_click_save_remote(self):
        pass

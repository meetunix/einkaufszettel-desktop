import tkinter
from enum import Enum
from tkinter import ttk
from typing import Dict, Optional

from einkaufszettel.controller import Controller
from einkaufszettel.entities import ConfigEZ, Einkaufszettel, Item


class EZConfigSelectLabel(Enum):
    NAME = "Name"
    ID = "ID"
    SERVER_NAME = "Server-Name"
    SERVER_URL = "Server-URL"


class EZLabels(Enum):
    NAME = "Name"
    VERSION_LOCAL = "Version server"
    VERSION_SERVER = "Version local"
    SERVER_NAME = "Server-Name"


class ItemLabels(Enum):
    NAME = ("name", tkinter.StringVar)
    ORIDNAL = ("ordinal", tkinter.IntVar)
    AMOUNT = ("amount", tkinter.IntVar)
    SIZE = ("size", tkinter.DoubleVar)
    UNIT = ("unit", tkinter.StringVar)
    CATEGORY_DESCRIPTION = ("category", tkinter.StringVar)


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
    def __init__(self, controller: Controller, list_frame, edit_frame):
        super().__init__()
        self.controller = controller
        self.list: ListFrame = list_frame
        self.editor: EditFrame = edit_frame
        self.current_config_ez: ConfigEZ = self.controller.get_configuration().get_default_ez()

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
        self.frame_left.columnconfigure(0, weight=1, minsize=150)
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
        self.current_config_ez = config_ez

    def __load_ez(self):
        """Load chosen EZ from cache and propagate it to the main frames."""
        ez: Einkaufszettel = self.controller.get_ez_from_cache(self.current_config_ez.eid)
        print(ez)
        self.list.refresh_ez_and_item_list(ez)
        self.list.refresh_item_editor(0)
        self.destroy()

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
        self.editor: Optional[EditFrame] = None
        self.list: Optional[ListFrame] = None

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
        self.window = ChooseEzWindow(controller, self.list, self.editor)
        self.window.mainloop()

    def set_editor_frame(self, editor_frame):
        self.editor = editor_frame

    def set_list_frame(self, list_frame):
        self.list = list_frame


class ListFrame(BasicFrame):
    """Frame showed at the left of the app which shows the current items from the current shopping list."""

    def __init__(self, container):
        super().__init__(container)
        self.controller = container.controller
        self.current_ez = self.controller.get_default_ez_from_cache()
        self.current_item_list = []  # the sorted list of items independent of the item of the ez
        self.editor: Optional[EditFrame] = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # subframe which holds the cart list
        self.frame_cart = ttk.LabelFrame(self, text="shopping-list")
        self.frame_cart.columnconfigure(0, weight=1000)
        self.frame_cart.columnconfigure(1, weight=1)
        self.frame_cart.rowconfigure(0, weight=1)
        self.frame_cart.grid(column=0, row=0, **self.options)

        self.listvar_items = tkinter.Variable(value=[])
        # cart list
        self.listbox_cart = tkinter.Listbox(
            self.frame_cart,
            font=self.font_typewriter,
            listvariable=self.listvar_items,
            selectmode=tkinter.SINGLE,
            exportselection=0,
        )
        self.listbox_cart.bind("<<ListboxSelect>>", self.__on_listbox_select)

        self.listbox_cart.grid(column=0, row=0, **self.options)
        self.scroller = tkinter.Scrollbar(self.frame_cart, orient=tkinter.VERTICAL, command=self.listbox_cart.yview)
        self.scroller.grid(column=1, row=0, sticky="NS")
        self.listbox_cart["yscrollcommand"] = self.scroller.set

    def refresh(self) -> None:
        self.refresh_ez_and_item_list(self.current_ez)
        self.refresh_item_editor(0)

    def set_editor_frame_and_refresh(self, editor_frame) -> None:
        self.editor = editor_frame
        self.refresh()

    def __on_listbox_select(self, event) -> None:
        selected_idx = self.listbox_cart.curselection()[0]
        self.refresh_item_editor(selected_idx)

    def refresh_item_editor(self, idx):
        """Refresh the editor frame with the selected item stored under given index."""
        iid: str = self.current_item_list[idx].iid
        self.editor.refresh_by_iid(iid)

    def refresh_ez_and_item_list(self, ez: Einkaufszettel) -> None:
        """Refresh the own item list and."""
        self.current_ez = ez
        self.editor.current_ez = ez
        self.current_item_list = sorted(ez.items, key=lambda i: i.ordinal)
        self.listvar_items.set(self.current_item_list)


class EditFrame(BasicFrame):
    """Frame showed at the right of the app, used for editing the current list item and save and reload the whole ez."""

    def __init__(self, container):
        super().__init__(container)

        self.controller = container.controller
        self.current_ez = self.controller.get_default_ez_from_cache()
        self.list: Optional[ListFrame] = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=20)

        # subframe on top wich hold the control buttons
        self.frame_ctrls = ttk.Frame(self)
        self.frame_ctrls.columnconfigure(0, weight=1)
        self.frame_ctrls.columnconfigure(1, weight=1)
        self.frame_ctrls.columnconfigure(2, weight=1)
        self.frame_ctrls.rowconfigure(0, weight=1)
        self.frame_ctrls.grid(column=0, row=0, padx=5, pady=5, ipadx=15, ipady=15, sticky="NW")

        self.button_refresh_state = ttk.Button(
            self.frame_ctrls, text="refresh state", command=self.__on_click_refresh_state
        )
        self.button_refresh_state.grid(column=0, row=0, sticky="W")
        self.button_load_remote = ttk.Button(
            self.frame_ctrls, text="load from server", command=self.__on_click_load_remote
        )
        self.button_load_remote.grid(column=1, row=0, sticky="W")
        self.button_save_remote = ttk.Button(
            self.frame_ctrls, text="save to server (publish)", command=self.__on_click_save_remote
        )
        self.button_save_remote.grid(column=2, row=0, sticky="W")

        # subframe which holds the current ez state
        self.frame_ez_state = ttk.LabelFrame(self, text="current shopping list")
        self.frame_ez_state.rowconfigure(0, weight=1)

        # build labels for showing information for the current EZ
        column = 0
        self.ez_labels = {}
        for select_label in EZLabels:
            self.frame_ez_state.columnconfigure(column, weight=1)
            label = ttk.Label(self.frame_ez_state, text=f"{select_label.value}: ")
            label.grid(column=column, row=0, sticky="W", padx=5, pady=5)
            column += 1
            self.frame_ez_state.columnconfigure(column, weight=1)
            label_dynamic = ttk.Label(self.frame_ez_state, text=f"NA")
            label_dynamic.grid(column=column, row=0, sticky="W", padx=5, pady=5)
            self.ez_labels[select_label] = label_dynamic
            column += 1
        self.frame_ez_state.grid(column=0, row=1, padx=5, pady=5, sticky="NWE")

        # subframe wich holds the widgets for editing the selected item
        self.frame_item = ttk.LabelFrame(self, text="ITEM")
        self.frame_item.columnconfigure(0, weight=1)
        self.frame_item.columnconfigure(1, weight=1)
        for i in range(4):
            self.frame_item.rowconfigure(i)

        # build editable entries for an item
        column = 0
        row = 0
        item_entry = 0
        self.item_vars: Dict[ItemLabels, tkinter.Variable] = {}
        for select_label in ItemLabels:
            label = ttk.Label(self.frame_item, text=f"{select_label.value[0]}: ")
            label.grid(column=column, row=row, sticky="W", padx=5, pady=5)
            row += 1
            var = select_label.value[1]()  # create correct type variable
            entry = ttk.Entry(self.frame_item, textvariable=var, name=select_label.value[0])
            entry.grid(column=column, row=row, sticky="W", padx=5, pady=5)
            self.item_vars[select_label] = var
            item_entry += 1
            if item_entry % 2 == 0:
                column = 0
                row += 1
            else:
                column = 1
                row -= 1

        self.frame_item.grid(column=0, row=2, sticky="NSEW")

    def refresh(self):
        pass

    def refresh_by_iid(self, iid: str):
        item: Item = self.current_ez.get_item_by_iid(iid)
        self.item_vars[ItemLabels.NAME].set(item.itemName)
        self.item_vars[ItemLabels.ORIDNAL].set(item.ordinal)
        self.item_vars[ItemLabels.AMOUNT].set(item.amount)
        self.item_vars[ItemLabels.SIZE].set(item.size)
        self.item_vars[ItemLabels.UNIT].set(item.unit)
        self.item_vars[ItemLabels.CATEGORY_DESCRIPTION].set(item.catDescription)

    def set_list_frame_and_refresh(self, list_frame: ListFrame):
        self.list = list_frame
        self.refresh()

    def __on_click_refresh_state(self):
        pass

    def __on_click_load_remote(self):
        pass

    def __on_click_save_remote(self):
        pass

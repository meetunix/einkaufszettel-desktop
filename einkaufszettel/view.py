import tkinter
from tkinter import ttk


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


class ListFrame(BasicFrame):
    """Frame showed at the right of the app which shows the current items from the current shopping list."""

    def __init__(self, container):
        super().__init__(container)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        # subframe which holds the cart list
        self.frame_cart = ttk.LabelFrame(self, text="shopping-list")
        self.frame_cart.columnconfigure(0, weight=1)
        self.frame_cart.columnconfigure(1, weight=1)
        self.frame_cart.rowconfigure(0, weight=1)
        self.frame_cart.grid(column=1, row=1, **self.options)

        # cart list
        self.scroller = tkinter.Scrollbar(self.frame_cart, orient=tkinter.VERTICAL)
        self.scroller.grid(column=1, row=1, sticky="NS")
        self.listbox_cart = tkinter.Listbox(self.frame_cart, font=self.font_typewriter,
                                            xscrollcommand=self.scroller.set)
        self.listbox_cart.grid(column=0, row=1, **self.options)

        # subframe which holds the cart information
        self.frame_shopping = ttk.LabelFrame(self, text="Einkauf")
        self.frame_shopping.columnconfigure(1, weight=1)
        self.frame_shopping.rowconfigure(1, weight=1)
        self.frame_shopping.grid(column=1, row=2, **self.options)

        self.label_price = ttk.Label(self.frame_shopping, font=self.font_typewriter_big)
        self.label_price.grid(column=1, row=1, **self.options)

# @staticmethod
# def ask_payment(shopping_cart: ShoppingCart):
#     prize_cart = shopping_cart.get_all_round_price()
#     return askquestion(title="Bezahlen", message=f"Bezahlung über {prize_cart:<4.2f} € annehmen?")

# def refresh_frame(self, shopping_cart: ShoppingCart):
#     self.listbox_cart.delete(0, self.listbox_cart.size())
#     cart = shopping_cart.cart
#     i = 1
#     price = 0
#     # fill the listbox
#     for product in list(cart):
#         amount = cart[product]
#         self.listbox_cart.insert(i, f"{amount:>3}x {product.name:<26} {product.price * amount:<4.2f} €")
#         i += 1
#         price += product.price * amount
#     # show the price for all products
#     self.label_price["text"] = f"Preis: {price: >8.2f} €"

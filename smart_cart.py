import tkinter as tk
import csv
from tkinter import ttk
import os

# Load products from CSV
def load_products(filename="products.csv"):
    products = {}
    with open(filename, newline="", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            products[row['barcode']] = {'name': row['name'], 'price': float(row['price'])}
    return products

products = load_products()

class SmartCartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Cart Scanner")
        self.root.geometry("480x320")  # Set window size to 320x480 for 3.5-inch display
        self.root.resizable(False, False)  # Disable resizing to maintain layout

        self.cart = {}
        self.total = 0.0

        # Header Styling (Further reduced font size and padding)
        self.header_label = tk.Label(root, text="🛒 Smart Cart 🛒", font=("Arial", 10, "bold"), bg="#28a745", fg="white", pady=3)
        self.header_label.pack(fill=tk.X)

        # Frame for Products List (Reduced padding and height)
        self.frame = tk.Frame(root, bg="#f8f9fa", bd=2, relief="ridge")
        self.frame.pack(pady=3, padx=3, fill=tk.BOTH, expand=True)

        # Treeview (Reduced height to 8 rows, smaller font)
        self.tree = ttk.Treeview(self.frame, columns=("Product", "Quantity", "Price"), show="headings", height=8)
        self.tree.heading("Product", text="Product")
        self.tree.heading("Quantity", text="Qty")
        self.tree.heading("Price", text="Price")
        self.tree.column("Product", width=150)
        self.tree.column("Quantity", width=50, anchor="center")
        self.tree.column("Price", width=70, anchor="center")
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 7))  # Even smaller font for Treeview
        style.configure("Treeview.Heading", font=("Arial", 7, "bold"))
        self.tree.pack(pady=3, padx=3, fill=tk.BOTH, expand=True)

        # Total Price Display (Smaller font, less padding)
        self.total_label = tk.Label(root, text="Total: ₱0", font=("Arial", 9, "bold"), bg="#f8f9fa", fg="#333")
        self.total_label.pack(pady=1)

        # Button Frame (Smaller buttons, less padding)
        self.button_frame = tk.Frame(root, bg="#f8f9fa")
        self.button_frame.pack(fill=tk.X, padx=3, pady=3)

        # Remove Item Button
        self.remove_btn = tk.Button(self.button_frame, text="Remove Item", command=self.remove_item, bg="#F9D3D3", fg="black", font=("Arial", 7, "bold"), padx=5, pady=2, relief="flat", bd=0, activebackground="#e74c3c", activeforeground="white")
        self.remove_btn.pack(side=tk.LEFT, ipadx=3, ipady=1, padx=2, pady=1)
        self.remove_btn.bind("<Enter>", lambda e: self.remove_btn.config(bg="#e74c3c", fg="white"))
        self.remove_btn.bind("<Leave>", lambda e: self.remove_btn.config(bg="#F9D3D3", fg="black"))

        # Remove One Button
        self.remove_one_btn = tk.Button(self.button_frame, text="Remove One", command=self.remove_one, bg="#FFF3D3", fg="black", font=("Arial", 7, "bold"), padx=5, pady=2, relief="flat", bd=0, activebackground="#ff9900", activeforeground="white")
        self.remove_one_btn.pack(side=tk.LEFT, ipadx=3, ipady=1, padx=2, pady=1)
        self.remove_one_btn.bind("<Enter>", lambda e: self.remove_one_btn.config(bg="#ff9900", fg="white"))
        self.remove_one_btn.bind("<Leave>", lambda e: self.remove_one_btn.config(bg="#FFF3D3", fg="black"))

        # Clear Cart Button
        self.clear_btn = tk.Button(self.button_frame, text="Clear Cart", command=self.clear_cart, bg="#D3E5F9", fg="black", font=("Arial", 7, "bold"), padx=5, pady=2, relief="flat", bd=0, activebackground="#3399ff", activeforeground="white")
        self.clear_btn.pack(side=tk.RIGHT, ipadx=3, ipady=1, padx=2, pady=1)
        self.clear_btn.bind("<Enter>", lambda e: self.clear_btn.config(bg="#3399ff", fg="white"))
        self.clear_btn.bind("<Leave>", lambda e: self.clear_btn.config(bg="#D3E5F9", fg="black"))

        # Hidden Entry Box for Barcode Scanning
        self.entry = ttk.Entry(root, font=("Arial", 1))  # Tiny font
        self.entry.place(x=-100, y=-100)  # Position it off-screen
        self.entry.bind("<Return>", self.scan_barcode)
        self.entry.focus_set()

        # Auto-focus the entry field
        self.root.bind("<Button-1>", self.refocus_entry)

    def scan_barcode(self, event=None):
        barcode = self.entry.get().strip()
        if barcode in products:
            if barcode in self.cart:
                self.cart[barcode]['quantity'] += 1
            else:
                self.cart[barcode] = {**products[barcode], 'quantity': 1}
            self.update_cart_display()
        else:
            print("Unknown product.")
        self.entry.delete(0, tk.END)
        self.entry.focus_set()

    def update_cart_display(self):
        self.tree.delete(*self.tree.get_children())
        for barcode, item in self.cart.items():
            self.tree.insert("", tk.END, values=(item['name'], item['quantity'], f"₱{self.format_price(item['price'] * item['quantity'])}"))
        self.update_total()

    def remove_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            for barcode, item in list(self.cart.items()):
                if item['name'] == item_values[0]:
                    del self.cart[barcode]
                    break
            self.update_cart_display()
        else:
            print("No item selected for removal.")

    def remove_one(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            for barcode, item in list(self.cart.items()):
                if item['name'] == item_values[0]:
                    if item['quantity'] > 1:
                        self.cart[barcode]['quantity'] -= 1
                    else:
                        del self.cart[barcode]
                    self.update_cart_display()
                    break
        else:
            print("No item selected to remove one from.")

    def clear_cart(self):
        self.cart.clear()
        self.update_cart_display()

    def update_total(self):
        self.total = sum(item['price'] * item['quantity'] for item in self.cart.values())
        self.total_label.config(text=f"Total: ₱{self.format_price(self.total)}")

    def refocus_entry(self, event):
        self.entry.focus_set()

    def format_price(self, price):
        return f"{price:.2f}".rstrip('0').rstrip('.')

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartCartApp(root)
    root.mainloop()
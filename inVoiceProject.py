import datetime
import json
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *

class Product:
    def __init__(self, name, quantity, unit_price):
        self.name = name
        self.quantity = quantity
        self.unit_price = unit_price

    def get_total_price(self):
        return self.quantity * self.unit_price

class Inventory:
    def __init__(self, filename="inventory.json"):
        self.filename = filename
        self.products = self.load_inventory()

    def load_inventory(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return [Product(item['name'], item['quantity'], item['unit_price']) for item in data]
        except FileNotFoundError:
            return []

    def save_inventory(self):
        data = [{'name': p.name, 'quantity': p.quantity, 'unit_price': p.unit_price} 
               for p in self.products]
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def add_product(self, product):
        existing = next((p for p in self.products if p.name == product.name), None)
        if existing:
            existing.quantity += product.quantity
        else:
            self.products.append(product)
        self.save_inventory()

    def update_stock(self, product_name, quantity_sold):
        product = next((p for p in self.products if p.name == product_name), None)
        if product:
            product.quantity -= quantity_sold
            self.save_inventory()

class Invoice:
    def __init__(self, inventory):
        self.products = []
        self.inventory = inventory

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Expected a Product instance")
        
        inventory_product = next((p for p in self.inventory.products 
                               if p.name == product.name), None)
        if not inventory_product:
            raise ValueError("Product not in inventory")
        if inventory_product.quantity < product.quantity:
            raise ValueError("Insufficient stock")
            
        self.products.append(product)

    def calculate_total(self):
        return sum(p.get_total_price() for p in self.products)

    def generate_invoice_text(self):
        lines = []
        lines.append("========== INVOICE ==========")
        lines.append(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("------------------------------")
        lines.append(f"{'Product':<15}{'Qty':<5}{'Unit Price':<12}{'Total'}")
        lines.append("------------------------------")

        for p in self.products:
            total = p.get_total_price()
            lines.append(f"{p.name:<15}{p.quantity:<5}${p.unit_price:<11.2f}${total:.2f}")

        lines.append("------------------------------")
        lines.append(f"Grand Total: ${self.calculate_total():.2f}")
        lines.append("==============================")
        return "\n".join(lines)

    def save_to_file(self, filename="invoice.txt"):
        try:
            with open(filename, 'a') as f:
                f.write(self.generate_invoice_text() + "\n\n")
            for p in self.products:
                self.inventory.update_stock(p.name, p.quantity)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error saving invoice: {e}")
            return False

class InvoiceApp(tb.Window):
    def __init__(self):
        tb.Style("superhero")  # Apply modern theme
        super().__init__(themename="superhero")
        self.title("Invoice and Inventory Management System")
        self.geometry("1200x800")
        
        self.inventory = Inventory()
        self.current_invoice = Invoice(self.inventory)
        
        self.create_widgets()
        self.load_inventory_table()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.inventory_frame, text="Inventory Management")
        self.create_inventory_tab()

        self.invoice_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.invoice_frame, text="Invoice Generation")
        self.create_invoice_tab()

    def create_inventory_tab(self):
        columns = ("name", "quantity", "price")
        self.inventory_tree = ttk.Treeview(
            self.inventory_frame, columns=columns, show="headings", height=15
        )
        self.inventory_tree.heading("name", text="Product Name")
        self.inventory_tree.heading("quantity", text="Quantity")
        self.inventory_tree.heading("price", text="Unit Price ($)")
        self.inventory_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        control_frame = ttk.Frame(self.inventory_frame)
        control_frame.pack(pady=10)

        tb.Button(control_frame, text="Add Product", command=self.show_add_dialog, 
                bootstyle=SUCCESS).grid(row=0, column=0, padx=5)
        tb.Button(control_frame, text="Edit Product", command=self.show_edit_dialog,
                bootstyle=INFO).grid(row=0, column=1, padx=5)
        tb.Button(control_frame, text="Delete Product", command=self.delete_product,
                bootstyle=DANGER).grid(row=0, column=2, padx=5)

    def create_invoice_tab(self):
        main_frame = ttk.Frame(self.invoice_frame)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True)

        tb.Label(left_frame, text="Select Product:").pack(anchor=W)
        self.product_combo = ttk.Combobox(left_frame, values=[p.name for p in self.inventory.products])
        self.product_combo.pack(fill=X, pady=5)

        tb.Label(left_frame, text="Quantity:").pack(anchor=W)
        self.quantity_entry = tb.Entry(left_frame)
        self.quantity_entry.pack(fill=X, pady=5)

        tb.Button(left_frame, text="Add to Invoice", command=self.add_to_invoice,
                bootstyle=SUCCESS).pack(pady=10)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10)

        columns = ("product", "qty", "price", "total")
        self.invoice_tree = ttk.Treeview(
            right_frame, columns=columns, show="headings", height=10
        )
        self.invoice_tree.heading("product", text="Product")
        self.invoice_tree.heading("qty", text="Qty")
        self.invoice_tree.heading("price", text="Unit Price")
        self.invoice_tree.heading("total", text="Total")
        self.invoice_tree.pack(fill=BOTH, expand=True)

        self.total_label = tb.Label(right_frame, text="Total: $0.00", font=('Helvetica', 14, 'bold'))
        self.total_label.pack(pady=10)

        control_frame = ttk.Frame(right_frame)
        control_frame.pack(pady=10)
        tb.Button(control_frame, text="Generate Invoice", command=self.generate_invoice,
                 bootstyle=PRIMARY).grid(row=0, column=0, padx=5)
        tb.Button(control_frame, text="Clear Invoice", command=self.clear_invoice,
                 bootstyle=WARNING).grid(row=0, column=1, padx=5)

    def load_inventory_table(self):
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        for product in self.inventory.products:
            self.inventory_tree.insert("", END, values=(
                product.name, 
                product.quantity, 
                f"${product.unit_price:.2f}"
            ))

    def show_add_dialog(self):
        AddProductDialog(self, self.inventory, self.load_inventory_table)

    def show_edit_dialog(self):
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to edit")
            return
        values = self.inventory_tree.item(selected[0], 'values')
        product = next(p for p in self.inventory.products if p.name == values[0])
        EditProductDialog(self, product, self.inventory, self.load_inventory_table)

    def delete_product(self):
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to delete")
            return
        product_name = self.inventory_tree.item(selected[0], 'values')[0]
        self.inventory.products = [p for p in self.inventory.products if p.name != product_name]
        self.inventory.save_inventory()
        self.load_inventory_table()

    def add_to_invoice(self):
        product_name = self.product_combo.get()
        quantity = self.quantity_entry.get()

        if not product_name or not quantity:
            messagebox.showwarning("Warning", "Please fill all fields")
            return

        try:
            quantity = int(quantity)
            product = next(p for p in self.inventory.products if p.name == product_name)
            invoice_product = Product(product.name, quantity, product.unit_price)
            self.current_invoice.add_product(invoice_product)

            self.invoice_tree.insert("", END, values=(
                product.name,
                quantity,
                f"${product.unit_price:.2f}",
                f"${invoice_product.get_total_price():.2f}"
            ))
            self.update_total()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_total(self):
        total = self.current_invoice.calculate_total()
        self.total_label.config(text=f"Total: ${total:.2f}")

    def generate_invoice(self):
        if not self.current_invoice.products:
            messagebox.showwarning("Warning", "Invoice is empty")
            return

        if messagebox.askyesno("Confirm", "Generate and save invoice?"):
            if self.current_invoice.save_to_file():
                messagebox.showinfo("Success", "Invoice saved successfully")
                self.clear_invoice()

    def clear_invoice(self):
        self.current_invoice = Invoice(self.inventory)
        self.invoice_tree.delete(*self.invoice_tree.get_children())
        self.update_total()

class AddProductDialog(tb.Toplevel):
    def __init__(self, parent, inventory, callback):
        super().__init__(parent)
        self.title("Add New Product")
        self.inventory = inventory
        self.callback = callback

        self.name_var = tk.StringVar()
        self.qty_var = tk.StringVar()
        self.price_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(padx=20, pady=20)

        tb.Label(frame, text="Product Name:").grid(row=0, column=0, sticky=W, pady=5)
        tb.Entry(frame, textvariable=self.name_var).grid(row=0, column=1, pady=5)

        tb.Label(frame, text="Quantity:").grid(row=1, column=0, sticky=W, pady=5)
        tb.Entry(frame, textvariable=self.qty_var).grid(row=1, column=1, pady=5)

        tb.Label(frame, text="Unit Price:").grid(row=2, column=0, sticky=W, pady=5)
        tb.Entry(frame, textvariable=self.price_var).grid(row=2, column=1, pady=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, columnspan=2, pady=10)
        tb.Button(btn_frame, text="Add", command=self.add_product,
                 bootstyle=SUCCESS).pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="Cancel", command=self.destroy,
                 bootstyle=DANGER).pack(side=LEFT, padx=5)

    def add_product(self):
        try:
            name = self.name_var.get()
            quantity = int(self.qty_var.get())
            price = float(self.price_var.get())

            if quantity <=0 or price <=0:
                raise ValueError("Values must be positive")

            product = Product(name, quantity, price)
            self.inventory.add_product(product)
            self.callback()
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

class EditProductDialog(AddProductDialog):
    def __init__(self, parent, product, inventory, callback):
        super().__init__(parent, inventory, callback)
        self.title("Edit Product")
        self.product = product

        self.name_var.set(product.name)
        self.qty_var.set(str(product.quantity))
        self.price_var.set(str(product.unit_price))

    def add_product(self):
        try:
            self.product.name = self.name_var.get()
            self.product.quantity = int(self.qty_var.get())
            self.product.unit_price = float(self.price_var.get())

            self.inventory.save_inventory()
            self.callback()
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

if __name__ == "__main__":
    app = InvoiceApp()
    app.mainloop()

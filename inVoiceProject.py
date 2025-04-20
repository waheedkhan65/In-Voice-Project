import datetime

class Product:
    def __init__(self, name, quantity, unit_price):
        self.name = name
        self.quantity = quantity
        self.unit_price = unit_price

    def get_total_price(self):
        return self.quantity * self.unit_price


class Invoice:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Expected a Product instance")
        self.products.append(product)

    def calculate_total(self):
        return sum(product.get_total_price() for product in self.products)

    def generate_invoice_text(self):
        lines = []
        lines.append("========== INVOICE ==========")
        lines.append(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("------------------------------")
        lines.append(f"{'Product':<15}{'Qty':<5}{'Unit Price':<12}{'Total'}")
        lines.append("------------------------------")

        for p in self.products:
            total = p.get_total_price()
            lines.append(f"{p.name:<15}{p.quantity:<5}{p.unit_price:<12}{total:.2f}")

        lines.append("------------------------------")
        lines.append(f"Grand Total: {self.calculate_total():.2f}")
        lines.append("==============================")

        return "\n".join(lines)

    def save_to_file(self, filename="invoice.txt"):
        try:
            with open(filename, 'w') as f:
                f.write(self.generate_invoice_text())
            print(f"Invoice saved to {filename}")
        except Exception as e:
            print(f"Error saving invoice: {e}")


# ====== Main Program ======

def get_valid_input(prompt, input_type=float):
    while True:
        try:
            value = input_type(input(prompt))
            if value < 0:
                raise ValueError("Value cannot be negative.")
            return value
        except ValueError as ve:
            print(f"Invalid input: {ve}")

def main():
    invoice = Invoice()

    print("=== Welcome to the Invoice Generator ===")
    while True:
        name = input("Enter product name: ")
        quantity = get_valid_input("Enter quantity: ", int)
        price = get_valid_input("Enter unit price: ")

        product = Product(name, quantity, price)
        invoice.add_product(product)

        another = input("Add another product? (y/n): ").lower()
        if another != 'y':
            break

    print("\nGenerated Invoice:\n")
    print(invoice.generate_invoice_text())
    invoice.save_to_file()

if __name__ == "__main__":
    main()

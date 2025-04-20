# 🧾 Basic Invoice Generator using Python OOP

This is a **console-based invoice generator** built using fundamental **Object-Oriented Programming (OOP)** principles in Python. It allows users to input product details, calculate totals, and export a well-formatted invoice to a `.txt` file.

---

## 🎯 Project Objective

To demonstrate clean OOP design by simulating a real-world invoice system. Users can:

- Add multiple products
- Automatically calculate totals
- Generate a readable invoice
- Export the invoice to a `.txt` file

---

## 🛠️ Features

✅ Add multiple products with name, quantity, and unit price  
✅ Automatic subtotal and grand total calculation  
✅ Export final invoice as a `.txt` file  
✅ Input validation and error handling  
✅ Fully modular code using OOP principles

---

## 🔍 Object-Oriented Concepts Used

| Concept          | Description |
|------------------|-------------|
| **Classes**      | `Product`, `Invoice` classes to represent real-world entities |
| **Encapsulation**| Data and methods grouped logically in classes |
| **Abstraction**  | Details of invoice generation hidden in class methods |
| **Exception Handling** | Input validation and error messaging |
| **File Handling** | Invoice is saved as a `.txt` file |

---

## 💻 Technologies Used

- **Language**: Python 3.x  
- **Libraries**: Python Standard Library (`datetime`)  
- **Output**: `.txt` invoice file (human-readable)

---

## 🧪 How to Run

1. Make sure Python 3 is installed on your system.
2. Download or clone this repository.
3. Run the program using:

```bash
python invoice_generator.py
```

Example Output (invoice.txt)

========== INVOICE ==========
Date: 2025-04-20 14:45:00
------------------------------
Product        Qty  Unit Price Total
------------------------------
Pen            10   20.0        200.00
Notebook       3    120.0       360.00
------------------------------
Grand Total: 560.00
==============================

```
👨‍💻 Author
Waheed ur Rahman
BS Software Engineering Student
GitHub: @waheedkhan65
```

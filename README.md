# BankTransaction

**Author:** Petr Valenta  
**Language:** Python  
**Description:** A simple threaded bank-transaction with deposits and transfers between accounts, using a generator-based interactive workflow.

---

## 🛠 Features

- Console-based interactive input
- `Account` objects, allowing deposits and transfers.  
- Threaded execution: each operation runs in its own thread, allowing multiple concurrent transactions.  
- Generator function to guide the user through steps in a clean sequence.  
- Proper error-handling for invalid inputs (non-integer amounts, negative values, invalid account choice, same account transfers).  
- Locking in `Transaction.execute` to ensure thread-safe movement of funds between accounts.

---

## 🛠️ Absoluteness
- It is just piece of the whole bank transaction system
- Can be useda as part and scaled for bigger projects

---

## ✅ Requirements

- Python 3.x  
- No external dependencies beyond standard library (e.g., `threading`, `time`)  
- Works on Windows, Linux, macOS (console environment)

---

## 🔧 Installation & Running

1. Clone the repository:
   ```bash
   git clone https://github.com/Fudr007/BankTransaction.git
   cd BankTransaction
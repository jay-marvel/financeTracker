# 💰 Personal Finance Tracker

A simple command-line tool to track income and expenses using Python and CSV. It lets you log transactions, view summaries over time, and visualize trends with plots.

---

## 🧩 Features

- Record income and expenses with date, amount, category, and optional description.
- Save data in a CSV file (`finance_data.csv`).
- View transactions between two dates.
- Display summary statistics (total income, expense, net savings).
- Plot income and expense trends over time.
- Generate weekly or monthly summaries.

---

## 📦 Requirements

- Python 3.x
- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)

Install required packages:

```bash
pip install pandas matplotlib
```

---

## 🚀 Getting Started

1. Clone this repository:

```bash
git clone https://github.com/your-username/finance-tracker.git
cd finance-tracker
```

2. Run the main script:

```bash
python main.py
```

---

## 📂 Project Structure

```
.
├── main.py           # Main application logic and user interface
├── data_entry.py     # Input helpers for user interaction
├── finance_data.csv  # Transaction data (auto-created)
```

---

## 📋 How to Use

When you run `main.py`, you'll see a menu:

```
1. Add a new transaction
2. View transactions and summary within a date range
3. View monthly or weekly summary
4. Exit
```

- Dates must be in `dd-mm-yyyy` format.
- Categories: `I` = Income, `E` = Expense.

---

## 📊 Example Output

```
Transactions from 01-06-2025 to 10-06-2025
    date     amount category description
01-06-2025   2000.00   Income  Paycheck
03-06-2025    150.00  Expense  Groceries

Summary:
Total Income: $2000.00
Total Expense: $150.00
Net Savings: $1850.00
```

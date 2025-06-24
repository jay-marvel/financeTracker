import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt
class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
    
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")
    
    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print('\nSummary:')
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")
        return filtered_df   

def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    df.set_index("date", inplace=True)
    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

def view_time_summary(df, period_choice):
    df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
    df["period_month"] = df["date"].dt.to_period("M")
    df["period_week"] = df["date"].dt.to_period("W")

    if period_choice == "1":
        period_col = "period_month"
        period_label = "Monthly"
    elif period_choice == "2":
        period_col = "period_week"
        period_label = "Weekly"
    else:
        print("Invalid choice.")
        return

    # Group and compute summaries
    grouped = df.groupby([period_col, "category"])["amount"].sum().unstack(fill_value=0)

    # Ensure both Income and Expense columns exist
    for col in ["Income", "Expense"]:
        if col not in grouped.columns:
            grouped[col] = 0

    grouped["Net Savings"] = grouped["Income"] - grouped["Expense"]
    grouped = grouped[["Income", "Expense", "Net Savings"]]

    grouped.index.name = None
    print(f"\n{period_label} Summary:")
    print(grouped.to_string(float_format="%.2f"))




def main():
    CSV.initialize_csv()

    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. View monthly or weekly summary")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", allow_default=True)
            amount = get_amount()
            category = get_category()
            description = get_description()
            add(date, amount, category, description)

        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if not df.empty and input("Do you want to see a plot? (y/n): ").lower() == "y":
                plot_transactions(df)

        elif choice == "3":
            df = pd.read_csv(CSV.CSV_FILE)
            if df.empty:
                print("No transactions recorded.")
                continue
            print("\n1. Monthly Summary")
            print("2. Weekly Summary")
            period_choice = input("Enter your choice (1-2): ")
            view_time_summary(df, period_choice)

        elif choice == "4":
            print("Exiting ...")
            break

        else:
            print("Invalid choice. Enter 1 to 4.")



if __name__ == "__main__":
    main()
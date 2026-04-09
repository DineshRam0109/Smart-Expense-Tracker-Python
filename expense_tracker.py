import json
import os
import csv
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt


class ExpenseTracker:

    DATA_FILE = "expenses.json"
    CATEGORIES_FILE = "categories.json"
    DEFAULT_CATEGORIES = ["Food", "Travel", "Bills", "Entertainment", "Shopping", "Health", "Education", "Other"]

    def __init__(self):
        self.expenses = []
        self.categories = []
        self.download_dir = self._resolve_download_dir()
        self.load_categories()
        self.load_data()

    def _resolve_download_dir(self):
        preferred = r"F:\Virtusa Company Assigned mini projects\Python_MiniProject\Downloaded CSV and Images"
        if os.path.isdir(preferred):
            return preferred
        fallback = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Downloads")
        os.makedirs(fallback, exist_ok=True)
        return fallback

    def _download_path(self, filename):
        return os.path.join(self.download_dir, filename)

    def load_categories(self):
        if os.path.exists(self.CATEGORIES_FILE):
            try:
                with open(self.CATEGORIES_FILE, "r") as f:
                    self.categories = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.categories = list(self.DEFAULT_CATEGORIES)
        else:
            self.categories = list(self.DEFAULT_CATEGORIES)
            self.save_categories()

    def save_categories(self):
        with open(self.CATEGORIES_FILE, "w") as f:
            json.dump(self.categories, f, indent=2)

    def display_categories(self):
        print("\nAvailable Categories:")
        print("-" * 30)
        for i, cat in enumerate(self.categories, 1):
            print(f"  {i}. {cat}")
        print("-" * 30)

    def add_category(self, name):
        name = name.strip().title()
        if not name:
            print("Category name cannot be empty.")
            return False
        if name in self.categories:
            print(f"'{name}' already exists.")
            return False
        self.categories.append(name)
        self.save_categories()
        print(f"Category '{name}' added successfully.")
        return True

    def update_category(self, index):
        if not (0 <= index < len(self.categories)):
            print(f"Invalid number. Enter between 1 and {len(self.categories)}.")
            return
        old_name = self.categories[index]
        new_name = input(f"New name for '{old_name}': ").strip().title()
        if not new_name:
            print("Name cannot be empty.")
            return
        if new_name in self.categories:
            print(f"'{new_name}' already exists.")
            return
        for expense in self.expenses:
            if expense["category"] == old_name:
                expense["category"] = new_name
        self.categories[index] = new_name
        self.save_categories()
        self.save_data()
        print(f"Category renamed from '{old_name}' to '{new_name}'. All expenses updated.")

    def delete_category(self, index):
        if not (0 <= index < len(self.categories)):
            print(f"Invalid number. Enter between 1 and {len(self.categories)}.")
            return
        name = self.categories[index]
        linked = [e for e in self.expenses if e["category"] == name]
        if linked:
            print(f"Cannot delete '{name}' — it is used by {len(linked)} expense(s).")
            print("Reassign or delete those expenses first.")
            return
        self.categories.pop(index)
        self.save_categories()
        print(f"Category '{name}' deleted.")


    def load_data(self):
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    self.expenses = json.load(f)
                print("Data loaded successfully. Total records:", len(self.expenses))
            except (json.JSONDecodeError, IOError):
                print("Could not read the file...")
                self.expenses = []
        else:
            print("No previous data found...")

    def save_data(self):
        with open(self.DATA_FILE, "w") as f:
            json.dump(self.expenses, f, indent=2)

    def add_expense(self, date_str, category, amount, description="No description"):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please enter date as YYYY-MM-DD.")
            return False

        if category not in self.categories:
            print("Invalid category. Please choose from:", ", ".join(self.categories))
            return False

        try:
            amount = float(amount)
        except ValueError:
            print("Please enter a valid amount.")
            return False

        if amount <= 0:
            print("Amount should be greater than zero.")
            return False

        expense = {
            "date": date_str,
            "category": category,
            "amount": amount,
            "description": description
        }

        self.expenses.append(expense)
        self.save_data()

        print("Expense added successfully.")
        print("Category:", category, "| Amount: Rs.", amount, "| Date:", date_str)
        return True

    def view_expenses(self, month=None, year=None):
        if not self.expenses:
            print("No expenses to show.")
            return

        data = self.expenses

        if month and year:
            key = f"{year:04d}-{month:02d}"
            data = [item for item in self.expenses if item["date"].startswith(key)]

        if not data:
            print("No records found for this month.")
            return

        data.sort(key=lambda x: x["date"])

        print("\n" + "-" * 60)
        print("No  Date         Category        Amount        Description")
        print("-" * 60)

        total = 0
        for i, item in enumerate(data, 1):
            print(f"{i:<3} {item['date']:<12} {item['category']:<15} Rs.{item['amount']:<10.2f} {item['description']}")
            total += item["amount"]

        print("-" * 68)
        print("Total amount spent: Rs.", round(total, 2))

    def update_expense(self, index):
        if not self._valid_index(index):
            return

        old = self.expenses[index]
        print("Press Enter if you don't want to change the value.\n")

        date_input     = input(f"Date [{old['date']}]: ").strip()
        category_input = input(f"Category [{old['category']}]: ").strip()
        amount_input   = input(f"Amount [{old['amount']}]: ").strip()
        desc_input     = input(f"Description [{old['description']}]: ").strip()

        new_date     = date_input     if date_input     else old["date"]
        new_category = category_input if category_input else old["category"]
        new_amount   = amount_input   if amount_input   else old["amount"]
        new_desc     = desc_input     if desc_input     else old["description"]

        try:
            datetime.strptime(new_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date...")
            return

        if new_category not in self.categories:
            print("Invalid category...")
            return

        try:
            new_amount = float(new_amount)
            if new_amount <= 0:
                raise ValueError
        except ValueError:
            print("Invalid amount...")
            return

        self.expenses[index] = {
            "date": new_date,
            "category": new_category,
            "amount": new_amount,
            "description": new_desc
        }

        self.save_data()
        print("Expense updated.")

    def delete_expense(self, index):
        if not self._valid_index(index):
            return

        item = self.expenses.pop(index)
        self.save_data()

        print("Deleted expense:")
        print("Category:", item["category"], "| Amount: Rs.", item["amount"], "| Date:", item["date"])

    def search_by_category(self, category):
        results = [e for e in self.expenses if e["category"].lower() == category.lower()]
        if not results:
            print(f"No expenses found under '{category}'.")
            return
        print(f"\nFound {len(results)} record(s) under '{category}':")
        for e in results:
            print(f"  {e['date']}  Rs.{e['amount']:.2f}  {e['description']}")

    def search_by_amount(self, min_amt, max_amt):
        results = [e for e in self.expenses if min_amt <= e["amount"] <= max_amt]
        if not results:
            print(f"No expenses found between Rs.{min_amt:.2f} and Rs.{max_amt:.2f}.")
            return
        print(f"\nFound {len(results)} record(s) between Rs.{min_amt:.2f} and Rs.{max_amt:.2f}:")
        for e in results:
            print(f"  {e['date']}  {e['category']:<15} Rs.{e['amount']:.2f}  {e['description']}")

    def monthly_summary(self, month, year):
        key  = f"{year:04d}-{month:02d}"
        data = [item for item in self.expenses if item["date"].startswith(key)]

        if not data:
            print("No data available for this month.")
            return

        total = sum(item["amount"] for item in data)

        category_data = defaultdict(float)
        for item in data:
            category_data[item["category"]] += item["amount"]

        highest = max(category_data.items(), key=lambda x: x[1])
        lowest  = min(category_data.items(), key=lambda x: x[1])

        days = len(set(item["date"] for item in data))
        avg  = total / days if days else 0

        print("\n" + "-" * 65)
        print("Monthly Summary:", f"{month:02d}/{year}")
        print("-" * 65)
        print("Total spent: Rs.", round(total, 2))
        print("Number of transactions:", len(data))
        print("Days with spending:", days)
        print("Average per day: Rs.", round(avg, 2))
        print("Highest spending category:", highest[0], "- Rs.", round(highest[1], 2))
        print("Lowest spending category:", lowest[0], "- Rs.", round(lowest[1], 2))

        print("\nCategory details:")
        for cat in sorted(category_data):
            amount  = category_data[cat]
            percent = (amount / total) * 100
            filled  = int(percent / 5)
            bar     = "[" + "#" * filled + "-" * (20 - filled) + "]"
            print(f"{cat:<15} Rs.{round(amount, 2):<10} ({round(percent, 1):>5}%) {bar}")

        print("\nNote:")
        top_percent = (highest[1] / total) * 100
        if top_percent > 40:
            print("You are spending a large portion on", highest[0])
        else:
            print("Your spending is fairly balanced")

        print("-" * 65)

    def visualize_monthly(self, month, year):
        key  = f"{year:04d}-{month:02d}"
        data = [item for item in self.expenses if item["date"].startswith(key)]

        if not data:
            print("No data to show.")
            return

        category_data = defaultdict(float)
        for item in data:
            category_data[item["category"]] += item["amount"]

        labels = list(category_data.keys())
        values = list(category_data.values())

        fig, (p1, p2) = plt.subplots(1, 2, figsize=(12, 5))

        p1.pie(values, labels=labels, autopct="%1.1f%%")
        p1.set_title("Expense Distribution")

        bars = p2.bar(labels, values)
        p2.set_title("Category wise spending")
        p2.set_xlabel("Category")
        p2.set_ylabel("Amount (Rs.)")

        for bar in bars:
            height = bar.get_height()
            p2.text(bar.get_x() + bar.get_width() / 2, height, f"Rs.{int(height)}",
                    ha="center", va="bottom")

        plt.xticks(rotation=45)
        plt.tight_layout()

        file_name = self._download_path(f"monthly_{year}_{month}.png")
        plt.savefig(file_name)
        print("Chart saved as", file_name)
        plt.show()

    def visualize_daily_trend(self, month, year):
        key  = f"{year:04d}-{month:02d}"
        data = [item for item in self.expenses if item["date"].startswith(key)]

        if not data:
            print("No data to display.")
            return

        daily_data = defaultdict(float)
        for item in data:
            daily_data[item["date"]] += item["amount"]

        dates  = sorted(daily_data.keys())
        values = [daily_data[d] for d in dates]
        x      = range(len(dates))

        plt.figure(figsize=(10, 5))
        plt.plot(x, values, marker="o")
        plt.fill_between(x, values, alpha=0.2)
        plt.xticks(list(x), dates, rotation=45)
        plt.xlabel("Date")
        plt.ylabel("Amount spent (Rs.)")
        plt.title("Daily spending trend")

        for i, val in enumerate(values):
            plt.text(i, val, f"Rs.{int(val)}", ha="center", va="bottom")

        plt.tight_layout()

        file_name = self._download_path(f"daily_{year}_{month}.png")
        plt.savefig(file_name)
        print("Chart saved as", file_name)
        plt.show()

    def export_csv(self):
        fieldnames = ["date", "category", "amount", "description"]
        file_path  = self._download_path("expenses.csv")

        with open(file_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for expense in self.expenses:
                writer.writerow({
                    "date":        expense.get("date", ""),
                    "category":    expense.get("category", ""),
                    "amount":      expense.get("amount", ""),
                    "description": expense.get("description", "No description")
                })
        print("Your expenses have been saved to a CSV file:")
        print(" ", file_path)

    def export_pdf(self):
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
        except ImportError:
            print("PDF feature is not available. Please install reportlab using: pip install reportlab")
            return

        file_path = self._download_path("expenses.pdf")
        document  = SimpleDocTemplate(file_path, pagesize=letter)
        styles    = getSampleStyleSheet()
        content   = []

        content.append(Paragraph("Expense Report", styles["Title"]))
        content.append(Spacer(1, 12))

        table_data   = [["Date", "Category", "Amount", "Description"]]
        total_amount = 0.0

        for expense in sorted(self.expenses, key=lambda x: x["date"]):
            table_data.append([
                expense.get("date", ""),
                expense.get("category", ""),
                f"Rs.{expense.get('amount', 0):.2f}",
                expense.get("description", "No description")
            ])
            total_amount += expense.get("amount", 0)

        table_data.append(["", "Total", f"Rs.{total_amount:.2f}", ""])

        table = Table(table_data, colWidths=[90, 100, 80, 220])
        table.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0),  (-1, 0),  colors.HexColor("#2E86AB")),
            ("TEXTCOLOR",     (0, 0),  (-1, 0),  colors.white),
            ("FONTNAME",      (0, 0),  (-1, 0),  "Helvetica-Bold"),
            ("ROWBACKGROUNDS",(0, 1),  (-1, -2), [colors.white, colors.HexColor("#f0f4f8")]),
            ("FONTNAME",      (0, -1), (-1, -1), "Helvetica-Bold"),
            ("LINEBELOW",     (0, 0),  (-1, 0),  1, colors.black),
            ("BOX",           (0, 0),  (-1, -1), 0.5, colors.grey),
            ("GRID",          (0, 0),  (-1, -1), 0.25, colors.lightgrey),
        ]))

        content.append(table)
        document.build(content)
        print("Your expenses have been saved as a PDF file:")
        print(" ", file_path)

    def _valid_index(self, index):
        if 0 <= index < len(self.expenses):
            return True
        print(f"Invalid number. Please enter a value between 1 and {len(self.expenses)}.")
        return False



def main():
    expense_tracker = ExpenseTracker()

    print("\n" + "=" * 65)
    print("  Dinesh's Smart Expense Tracker - Manage Your Daily Spending Easily")
    print("=" * 65)

    menu_text = """
  Manage Expenses
    1.  Add Expense
    2.  View All Expenses
    3.  View Expenses by Month
    4.  Update an Expense
    5.  Delete an Expense

  Search
    6.  Search by Category
    7.  Search by Amount Range

  Analytics
    8.  Monthly Summary
    9.  View Charts (Pie & Bar)
    10. View Daily Spending Trend

  Export
    11. Save as CSV
    12. Save as PDF

  Manage Categories
    13. View Categories
    14. Add Category
    15. Update Category
    16. Delete Category

    0.  Exit
"""

    while True:
        print(menu_text)
        user_choice = input("What would you like to do?...Enter the Choice :  ").strip()

        if user_choice == "1":
            print("\nAdd a new expense\n")
            expense_tracker.display_categories()
            date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
            if not date_input:
                date_input = datetime.now().strftime("%Y-%m-%d")
            category_input    = input("Enter category: ").strip()
            amount_input      = input("Enter amount (Rs.): ").strip()
            description_input = input("Enter description (optional): ").strip()
            if not description_input:
                description_input = "No description"
            expense_tracker.add_expense(date_input, category_input, amount_input, description_input)

        elif user_choice == "2":
            expense_tracker.view_expenses()

        elif user_choice == "3":
            try:
                month_input = int(input("Enter month (1-12): "))
                year_input  = int(input("Enter year (YYYY): "))
                expense_tracker.view_expenses(month_input, year_input)
            except ValueError:
                print("Please enter valid numbers for month and year.")

        elif user_choice == "4":
            expense_tracker.view_expenses()
            try:
                index_input = int(input("Enter the number of the expense to update: "))
                expense_tracker.update_expense(index_input - 1)
            except ValueError:
                print("Please enter a valid number.")

        elif user_choice == "5":
            expense_tracker.view_expenses()
            try:
                index_input = int(input("Enter the number of the expense to delete: "))
                expense_tracker.delete_expense(index_input - 1)
            except ValueError:
                print("Please enter a valid number.")

        elif user_choice == "6":
            expense_tracker.display_categories()
            category_input = input("Enter category to search: ").strip()
            expense_tracker.search_by_category(category_input)

        elif user_choice == "7":
            try:
                min_amount = float(input("Enter minimum amount (Rs.): "))
                max_amount = float(input("Enter maximum amount (Rs.): "))
                expense_tracker.search_by_amount(min_amount, max_amount)
            except ValueError:
                print("Please enter valid numbers for amount.")

        elif user_choice == "8":
            try:
                month_input = int(input("Enter month (1-12): "))
                year_input  = int(input("Enter year (YYYY): "))
                expense_tracker.monthly_summary(month_input, year_input)
            except ValueError:
                print("Please enter valid numbers.")

        elif user_choice == "9":
            try:
                month_input = int(input("Enter month (1-12): "))
                year_input  = int(input("Enter year (YYYY): "))
                expense_tracker.visualize_monthly(month_input, year_input)
            except ValueError:
                print("Please enter valid numbers.")

        elif user_choice == "10":
            try:
                month_input = int(input("Enter month (1-12): "))
                year_input  = int(input("Enter year (YYYY): "))
                expense_tracker.visualize_daily_trend(month_input, year_input)
            except ValueError:
                print("Please enter valid numbers.")

        elif user_choice == "11":
            expense_tracker.export_csv()

        elif user_choice == "12":
            expense_tracker.export_pdf()

        elif user_choice == "13":
            expense_tracker.display_categories()

        elif user_choice == "14":
            new_cat = input("Enter new category name: ").strip()
            expense_tracker.add_category(new_cat)

        elif user_choice == "15":
            expense_tracker.display_categories()
            try:
                idx = int(input("Enter the number of the category to rename: "))
                expense_tracker.update_category(idx - 1)
            except ValueError:
                print("Please enter a valid number.")

        elif user_choice == "16":
            expense_tracker.display_categories()
            try:
                idx = int(input("Enter the number of the category to delete: "))
                expense_tracker.delete_category(idx - 1)
            except ValueError:
                print("Please enter a valid number.")

        elif user_choice == "0":
            print("\nThank You for using my Expense Tracker...Exited...\n")
            break

        else:
            print("Invalid choice. Please select a number from the menu.")


if __name__ == "__main__":
    main()
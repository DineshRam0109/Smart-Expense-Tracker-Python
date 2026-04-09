# Smart Expense Tracker (Python CLI Project)

## Problem Statement
Many individuals struggle to track daily expenses and understand spending patterns.  
This project provides a simple yet effective solution to log, categorize, analyze, and visualize personal expenses.

---

## Objectives
- Record daily expenses (date, category, amount, description)
- Categorize spending (Food, Travel, Bills, etc.)
- Generate monthly summaries and insights
- Visualize spending patterns
- Export reports for external use

---

## Features

### Expense Management
- Add, update, and delete expenses
- View all expenses or filter by month
- Search by category or amount range

### Analytics and Insights
Monthly summary includes:
- Total spending
- Average daily spending
- Highest and lowest spending categories
- Intelligent insights (alerts when a category exceeds 40% of total spending)

### Data Visualization
- Pie chart for category distribution
- Bar chart for category-wise spending
- Daily spending trend line chart

### Data Storage
- JSON-based local storage (no external database required)

### Export Options
- Export expense data to CSV
- Generate formatted PDF reports

### Category Management
- Add, update, and delete categories dynamically

---

## Tech Stack
- **Language:** Python
- **Libraries:**
  - matplotlib (data visualization)
  - reportlab (PDF generation)
  - json, csv, datetime, collections

---

## Project Structure

```
Python_MiniProject/
│
├── expense_tracker.py
├── expenses.json
├── categories.json
├── Smart_Expense_Tracker_Documentation.pdf
│
├── Downloads/
│ ├── expenses.csv
│ ├── expenses.pdf
│ ├── monthly_YYYY_MM.png
│ └── daily_YYYY_MM.png
│
└── Output Screenshots/
├── screenshot_1
├── screenshot_2
├── screenshot_3

```
---

## Installation and Setup
```bash
# Clone the repository
git clone https://github.com/dineshram0109/smart-expense-tracker.git

# Navigate to project folder
cd smart-expense-tracker

# Install dependencies
pip install matplotlib reportlab

# Run the application
python expense_tracker.py

## Sample Data Format

### expenses.json
```json
{
  "date": "2026-04-01",
  "category": "Food",
  "amount": 250,
  "description": "Lunch"
}

### Categories.json

["Food", "Travel", "Bills", "Entertainment"]

Detailed Documentation

For a complete explanation of the project, including design, implementation, and all functionalities, refer to:

**Smart Expense Tracker Python Documentation.pdf** (available in this repository)
# Expense Manager

This project demonstrates a personal and small business expense management system.  
It includes both the **original buggy version** (`before/`) and the **reworked optimized version** (`after/`).  

The goal was to fix errors, improve performance, and add new features for more practical financial tracking.

---

## Features

- Add and track **expenses** (date, category, description, amount)  
- Add and track **incomes** (date, source, amount)  
- Persistent data storage using **JSON files**  
- Calculate totals for **expenses, incomes, and net profit**  
- Generate **monthly summaries** for insights  
- Breakdown of expenses by **category**  
- Search and filter expenses by category  
- Simple, clean, and user-friendly console interface  


---

## How to Use

1. Navigate to the `after/` folder.  
2. Run the program with:  
   ```bash
   python expenses.py
3. Follow the menu to:
- Add expenses
- Add incomes
- View totals and net profit
- View category breakdowns
- Generate monthly summaries

All data will be saved automatically in the data/ folder.

Example Entries

```bash

   Expense Entry
   Date: 2025-01-05
   Category: Office Supplies
   Description: Printer ink and paper
   Amount: $45.90


   Income Entry
   Date: 2025-01-20
   Source: Consulting Services
   Amount: $800.00
```
Key Improvements

   The after version was reworked with the following fixes and optimizations:

- Input Handling
- Fixed broken input functions that caused crashes.
- Added validation for numbers and dates to prevent bad entries.
- Data Storage
- Introduced JSON-based storage for expenses and incomes.
- Data now persists between program runs (was lost before).
- Performance
- Optimized calculations for totals and summaries.
- Removed duplicate loops that slowed down performance.
- Categories & Summaries
- Improved category handling (no more duplicates or missing entries).
- Added monthly summary reports for clearer financial tracking.
- User Experience
- Cleaner menus and navigation.
- Error messages are clearer and less confusing.

Notes

- The before version shows the original inefficient and buggy implementation.
- The after version demonstrates the improved, optimized solution with added features.
- This project highlights the ability to debug, rework, and optimize real-world business code for practical use.

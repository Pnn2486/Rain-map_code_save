# Rain Tracking System

Welcome to the **Rain-map_code_save** repository. This project contains the Google Sheets Formula Language code used to track, calculate, filter and validate rain events. 

## 1. Repository Structure
* **`README.md`**: This file, explaining the system mechanics and logic.
* **`Formulas.md`**: The raw, copy-pasteable formula scripts used in the spreadsheet.

---

## 2. Core Modules & Mechanisms

### 2.1 Rain Event Counter (`Number of Rains`)
A formula that calculates the total of rain events, completely ignoring formatting spaces and complex occasions, such as midnight crossovers.
* **The Problem:** When a rain event crosses midnight, the cells are vertically merged. Google Sheets treats the bottom half of a merged cell as a completely blank row, which normally causes counting errors or double-counts.
* **The Solution:** The formula uses `MAP` and `LAMBDA` to skim through the entire column. If it detects a blank cell input, it scans at the row directly above it, saving the start and end hours using Regular Expressions (`REGEXEXTRACT`), and checks if the time crossed midnight (`endHr < startHr`). If it did, the system safely ignores the blank row instead of miscounting it.

### 2.2 Project Progress (`Progress`)
Count how many days had passed since the start of the project.
* **Mechanism:** Uses `DATEDIF` functions to calculate the exact years, months, and days elapsed since the project's beginning (June 12, 2023) against the current `TODAY()` date.

### 2.3 Unique ID Generator (`Code Generator`)
Generates unique ID numbers (such as `#745`) for each valid rain event.
* **Mechanism:** It shares the exact same complex logic as the Rain Event Counter. Furthermore, if a rain event has, for example, a `#745` ID, it would be the 745th rain ever captured on the project.

### 2.4 Dynamic Duration Engine (`Duration Generator`)
The “operating system” of the sheet. It calculates the exact duration of rain events based on cell references, handling complex pattern recognition and filters.
* **Hybrid Input Parsing:** The system accepts both standard comma-separated cells (e.g., `B10, B15`) and colon-indicating ranges (e.g., `B20:B25`). You can freely mix these in the same input box (e.g., `B10, B20:B25, B30`).
* **The Range Expander (Pre-Processor):** Before calculating any math, the formula scans the input for colons (`:`). If it detects a range, it extracts the start and end rows, generates a sequence array of every cell in between, and flattens it into a clean, comma-separated list (`B20, B21, B22, B23, B24, B25`). This prevents serious errors when feeding data to the `TEXTJOIN` function.
* **The Midnight Merge Scan:** When calculating durations, if the formula hits the blank bottom-half of a merged cell, it triggers a backwards `FILTER` scan from row 1 down to the target cell's location. It finds the last filled "master" parent cell, safely copies its timestamp, and processes the duplicate duration without breaking the array.

### 2.5 Debug Scanner (`Debug: Incorrect and Incomplete`)
A built-in Quality Assurance tool that acts as a compiler warning system for the spreadsheet.
* **Mechanism:** It maps across the entire dataset and flags two types of errors:
  1. **Incomplete:** Flags cells that are missing a start time, missing an end time, or missing the formatting pipe (`|`).
  2. **Incorrect:** It independently recalculates the time difference between the logged start and end times of every single cell and compares its own math against the manually typed duration string. If the human math doesn't perfectly match the machine math, it outputs the exact cell address so the user can fix the typo.
* **The Ignore Box:** There's an "Ignore Box" (like cell `A1`) for weird edge cases. If you type a list of cells (e.g., `Ignore: B507, B520`), the scanner just skips them so you don't get annoying false alarms.

### 2.6 Debug: Date Chronology
Scans the master list to make sure you didn't accidentally log dates out of order.
* **Mechanism:** It grabs all the dates, turns them into numbers, and scans the whole list from bottom to top using `SCAN` and `MIN`. If it sees a date that is older than the one logged right after it (a chronological spike), it flags the cell address (like `24/10/2026 - A50`) so you can fix the typo.
* **The Ignore Box:** Just like the duration scanner, you can use an ignore box (like cell `A5`) to skip any intentional weird dates using the same trick.

---
*Check `Formulas.md` for the complete source code.*

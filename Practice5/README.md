# Practice 5 — Python Regular Expressions (RegEx)

## Objective
This practice demonstrates the use of Python's `re` module for pattern matching, searching, splitting, and replacing text.  
It also includes a practical receipt parsing task using regular expressions.

---

## Files in This Folder

- `regex_exercises.py` — Solutions for 10 RegEx tasks (search, findall, split, sub, metacharacters, quantifiers, etc.)
- `receipt_parser.py` — Parses receipt data from `raw.txt`
- `raw.txt` — Raw receipt text used for parsing

---

## Topics Covered

- RegEx syntax and metacharacters (`. * + ? ^ $ [] () |`)
- Special sequences (`\d`, `\w`, `\s`)
- Quantifiers (`{n}`, `{n,m}`)
- `re.search()`
- `re.findall()`
- `re.split()`
- `re.sub()`
- Lookahead expressions
- Text parsing using RegEx

---

## Receipt Parser Functionality

The parser extracts:

- Product names
- Item prices
- Total amount
- Date and time
- Payment method
- Structured JSON output

---

## How to Run

Open terminal inside `Practice5` folder:

```bash
python regex_exercises.py
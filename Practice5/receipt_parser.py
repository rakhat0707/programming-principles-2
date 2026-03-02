import re
import json

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

# -------------------------
# 1. Extract date and time
# -------------------------
datetime_match = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})", text)
date_time = None
if datetime_match:
    date_time = {
        "date": datetime_match.group(1),
        "time": datetime_match.group(2)
    }

# -------------------------
# 2. Extract payment method
# -------------------------
payment_match = re.search(r"(Банковская карта|Наличные)", text)
payment_method = payment_match.group(1) if payment_match else None

# -------------------------
# 3. Extract total amount
# -------------------------
total_match = re.search(r"ИТОГО:\s*\n?([\d\s,]+)", text)
total = None
if total_match:
    total = float(total_match.group(1).replace(" ", "").replace(",", "."))

# -------------------------
# 4. Extract items
# Pattern:
# number.
# product name
# quantity x price
# total price
# -------------------------
item_pattern = re.compile(
    r"\d+\.\s*\n"                # item number
    r"(.+?)\n"                   # product name
    r"\d+,\d+\s*x\s*([\d\s,]+)\n" # price per unit
    r"([\d\s,]+)",               # total price
    re.MULTILINE
)

items = []

for match in item_pattern.finditer(text):
    name = match.group(1).strip()
    price = float(match.group(3).replace(" ", "").replace(",", "."))
    items.append({
        "name": name,
        "total_price": price
    })

# -------------------------
# 5. Extract all prices
# -------------------------
prices = re.findall(r"\d[\d\s]*,\d{2}", text)
prices = [float(p.replace(" ", "").replace(",", ".")) for p in prices]

# -------------------------
# Final structured output
# -------------------------
result = {
    "date_time": date_time,
    "payment_method": payment_method,
    "total_from_receipt": total,
    "calculated_total": round(sum(item["total_price"] for item in items), 2),
    "items": items,
    "all_prices_count": len(prices)
}

print(json.dumps(result, ensure_ascii=False, indent=2))
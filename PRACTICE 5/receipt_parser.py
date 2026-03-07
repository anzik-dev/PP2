import re
import json

with open("PRACTICE 5/raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

#prices
price_pattern = r"\$\d+\.\d{2}"
prices = [float(p[1:]) for p in re.findall(price_pattern, text)]

#products
product_pattern = r"\dx\s([A-Za-z]+)"
products = re.findall(product_pattern, text)

#date
date_pattern = r"\d{4}-\d{2}-\d{2}"
date_match = re.search(date_pattern, text)

#time
time_pattern = r"\d{2}:\d{2}"
time_match = re.search(time_pattern, text)

#payment method
payment_pattern = r"Paid via:\s*(\w+)"
payment_match = re.search(payment_pattern, text)

#calculate total
total = sum(prices)

data = {
    "products": products,
    "prices": prices,
    "total": total,
    "date": date_match.group() if date_match else None,
    "time": time_match.group() if time_match else None,
    "payment_method": payment_match.group(1) if payment_match else None
}

print(json.dumps(data, indent=4))
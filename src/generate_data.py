import csv
import random
from datetime import date, timedelta
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

SEED = 20261004
TOTAL_SALES = 20_000
DUPLICATES_PER_COUNTRY = 20

random.seed(SEED)

PRODUCTS = [f"P{i:03d}" for i in range(1, 21)]
CUSTOMERS = [f"C{i:04d}" for i in range(1, 501)]
START_DATE = date(2025, 1, 1)

ITALY_COLUMNS = [
    "data",
    "codice_articolo",
    "cliente",
    "quantita",
    "prezzo_unitario",
]

GERMANY_COLUMNS = [
    "date",
    "article",
    "customer",
    "qty",
    "price",
]

italy_rows = []
germany_rows = []

for sale_id in range(TOTAL_SALES):
    country = random.choices(["IT", "DE"], weights=[55, 45], k=1)[0]

    sale_date = START_DATE + timedelta(days=random.randrange(365))
    product_id = random.choice(PRODUCTS)
    customer_id = random.choice(CUSTOMERS)
    quantity = random.choices(
        [1, 2, 3, 4, 5, 10, 20, 0, -2],
        weights=[25, 22, 16, 12, 10, 6, 2, 1, 1],
        k=1,
    )[0]
    price = random.choice([8.90, 12.50, 19.99, 24.75, 35.00, 49.90, 79.00])

    row = {
        "date": sale_date.isoformat(),
        "product": product_id,
        "customer": customer_id,
        "quantity": quantity,
        "price": f"{price:.2f}",
    }

    if sale_id % 997 == 0:
        row["customer"] = ""

    if sale_id % 613 == 0:
        row["product"] = ""

    if country == "IT":
        italy_rows.append(row)
    else:
        germany_rows.append(row)

italy_rows.extend(italy_rows[:DUPLICATES_PER_COUNTRY])
germany_rows.extend(germany_rows[:DUPLICATES_PER_COUNTRY])

DATA_DIR.mkdir(parents=True, exist_ok=True)

with (DATA_DIR / "sales_italy.csv").open(
    "w", newline="", encoding="utf-8"
) as file:
    writer = csv.writer(file)
    writer.writerow(ITALY_COLUMNS)

    for row in italy_rows:
        writer.writerow([
            row["date"],
            row["product"],
            row["customer"],
            row["quantity"],
            row["price"],
        ])

with (DATA_DIR / "sales_germany.csv").open(
    "w", newline="", encoding="utf-8"
) as file:
    writer = csv.writer(file)
    writer.writerow(GERMANY_COLUMNS)

    for row in germany_rows:
        writer.writerow([
            row["date"],
            row["product"],
            row["customer"],
            row["quantity"],
            row["price"],
        ])

print(f"Vendite Italia: {len(italy_rows)}")
print(f"Vendite Germania: {len(germany_rows)}")
print(f"Totale: {len(italy_rows) + len(germany_rows)}")
print(f"Seed utilizzato: {SEED}")
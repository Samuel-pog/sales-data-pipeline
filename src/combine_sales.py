from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import lit


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

spark = (
    SparkSession.builder
    .appName("ItalyGermanySales")
    .master("local[*]")
    .getOrCreate()
)

italy_raw = (
    spark.read
    .option("header", True)
    .option("inferSchema", False)
    .csv(str(DATA_DIR / "sales_italy.csv"))
)

germany_raw = (
    spark.read
    .option("header", True)
    .option("inferSchema", False)
    .csv(str(DATA_DIR / "sales_germany.csv"))
)

italy = (
    italy_raw
    .selectExpr(
        "data as sale_date",
        "codice_articolo as product_id",
        "cliente as customer_id",
        "quantita as quantity",
        "prezzo_unitario as unit_price",
    )
    .withColumn("country", lit("IT"))
)

germany = (
    germany_raw
    .selectExpr(
        "date as sale_date",
        "article as product_id",
        "customer as customer_id",
        "qty as quantity",
        "price as unit_price",
    )
    .withColumn("country", lit("DE"))
)

sales = italy.unionByName(germany)

sales.show(truncate=False)
print(f"Numero totale di vendite: {sales.count()}")

spark.stop()
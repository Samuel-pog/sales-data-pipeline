from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, date_format, lit, to_date
from pyspark.sql.functions import sum as spark_sum


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"


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


sales_raw = italy.unionByName(germany)

sales_typed = (
    sales_raw
    .withColumn("sale_date", to_date(col("sale_date"), "yyyy-MM-dd"))
    .withColumn("quantity", col("quantity").cast("integer"))
    .withColumn("unit_price", col("unit_price").cast("decimal(10,2)"))
)

sales = (
    sales_typed
    .filter(
        col("sale_date").isNotNull()
        & col("product_id").isNotNull()
        & (col("product_id") != "")
        & col("customer_id").isNotNull()
        & (col("customer_id") != "")
        & col("quantity").isNotNull()
        & (col("quantity") > 0)
        & col("unit_price").isNotNull()
        & (col("unit_price") > 0)
    )
    .dropDuplicates()
)


print(f"Righe dopo l'unione: {sales_raw.count()}")
print(f"Righe valide dopo la pulizia: {sales.count()}")

sales.show(10, truncate=False)
sales.printSchema()


monthly_sales = (
    sales
    .withColumn("month", date_format(col("sale_date"), "yyyy-MM"))
    .withColumn("revenue", col("quantity") * col("unit_price"))
    .groupBy("country", "month")
    .agg(
        count("*").alias("sales_count"),
        spark_sum("quantity").alias("units_sold"),
        spark_sum("revenue").alias("revenue"),
    )
    .orderBy("country", "month")
)

monthly_sales.show(30, truncate=False)

sales.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(str(OUTPUT_DIR / "sales_clean"))

monthly_sales.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(str(OUTPUT_DIR / "monthly_sales"))

print(f"Vendite pulite salvate in: {OUTPUT_DIR / 'sales_clean'}")
print(f"Riepilogo mensile salvato in: {OUTPUT_DIR / 'monthly_sales'}")

spark.stop()
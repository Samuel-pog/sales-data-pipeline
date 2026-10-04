from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("SalesDataPipeline")
    .master("local[*]")
    .getOrCreate()
)

sales = [
    ("IT", "2026-01-10", "P001", 2, 12.50),
    ("IT", "2026-01-11", "P002", 1, 35.00),
    ("FR", "2026-01-12", "P001", 3, 12.50),
]

columns = ["country", "sale_date", "product_id", "quantity", "unit_price"]
df = spark.createDataFrame(sales, columns)

df.show()
print(f"Numero di righe: {df.count()}")

spark.stop()
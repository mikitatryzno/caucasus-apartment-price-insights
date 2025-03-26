import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, regexp_replace, to_date, lit, round, expr, udf, split
from pyspark.sql.types import StringType, FloatType, IntegerType
import uuid

def parse_arguments():
    parser = argparse.ArgumentParser(description='Apartment Data Cleaning')
    parser.add_argument('--data_date', required=True, help='Date of the data in YYYY-MM-DD format')
    parser.add_argument('--input_path', required=True, help='Input path for raw data')
    parser.add_argument('--output_path', required=True, help='Output path for processed data')
    return parser.parse_args()

def create_spark_session():
    return SparkSession.builder \
        .appName("Apartment Data Cleaning") \
        .getOrCreate()

def clean_tbilisi_data(df):
    """Clean and transform Tbilisi apartment data"""
    # Convert GEL to USD (approximate exchange rate: 1 GEL = 0.37 USD)
    exchange_rate = 0.37
    
    # Generate UUID for id column
    generate_uuid = udf(lambda: str(uuid.uuid4()), StringType())
    
    # Extract floor from Floor column
    return df.withColumn("id", generate_uuid()) \
             .withColumn("original_price", col("PRICE (GEL)").cast("float")) \
             .withColumn("original_currency", lit("GEL")) \
             .withColumn("price", col("PRICE (GEL)").cast("float") * exchange_rate) \
             .withColumn("area", col("Area").cast("float")) \
             .withColumn("rooms", col("Rooms").cast("integer")) \
             .withColumn("neighborhood", col("CityPart")) \
             .withColumn("price_per_sqm", round(col("price") / col("area"), 2)) \
             .withColumn("floor", col("Floor").cast("integer")) \
             .withColumn("building_type", when(col("Status").like("%Newly Constructed%"), "New construction")
                                         .when(col("Status").like("%Old%"), "Old construction")
                                         .when(col("Status").like("%Under Construction%"), "Under construction")
                                         .otherwise("Unknown")) \
             .withColumn("city", lit("Tbilisi"))

def clean_yerevan_data(df):
    """Clean and transform Yerevan apartment data"""
    return df.withColumn("id", col("ID").cast("string")) \
             .withColumn("original_price", col("Price (USD)").cast("float")) \
             .withColumn("original_currency", lit("USD")) \
             .withColumn("price", col("Price (USD)").cast("float")) \
             .withColumn("area", col("Area (sq m)").cast("float")) \
             .withColumn("rooms", col("Rooms").cast("integer")) \
             .withColumn("neighborhood", col("District")) \
             .withColumn("price_per_sqm", round(col("price") / col("area"), 2)) \
             .withColumn("floor", col("Floor").cast("integer")) \
             .withColumn("building_type", col("Building Type")) \
             .withColumn("city", lit("Yerevan"))

def clean_baku_data(df):
    """Clean and transform Baku apartment data"""
    # Convert AZM to USD (approximate exchange rate: 1 AZM = 0.59 USD)
    exchange_rate = 0.59
    
    # Extract floor from floor column (format: "5/12")
    return df.withColumn("id", col("Unnamed: 0").cast("string")) \
             .withColumn("original_price", col("price").cast("float")) \
             .withColumn("original_currency", lit("AZM")) \
             .withColumn("price", col("price").cast("float") * exchange_rate) \
             .withColumn("area", col("square").cast("float")) \
             .withColumn("rooms", col("rooms").cast("integer")) \
             .withColumn("neighborhood", col("location")) \
             .withColumn("price_per_sqm", round(col("price") / col("area"), 2)) \
             .withColumn("floor", split(col("floor"), "/").getItem(0).cast("integer")) \
             .withColumn("building_type", when(col("new_building") == 1, "New construction")
                                         .otherwise("Old construction")) \
             .withColumn("city", lit("Baku"))

def main():
    args = parse_arguments()
    spark = create_spark_session()
    
    # Load data
    tbilisi_df = spark.read.csv(f"{args.input_path}tbilisi_apartments_{args.data_date}.csv", 
                               header=True, inferSchema=True)
    yerevan_df = spark.read.csv(f"{args.input_path}yerevan_apartments_{args.data_date}.csv", 
                               header=True, inferSchema=True)
    baku_df = spark.read.csv(f"{args.input_path}baku_apartments_{args.data_date}.csv", 
                            header=True, inferSchema=True)
    
    # Clean data
    tbilisi_clean = clean_tbilisi_data(tbilisi_df)
    yerevan_clean = clean_yerevan_data(yerevan_df)
    baku_clean = clean_baku_data(baku_df)
    
    # Select and reorder columns to match BigQuery schema
    tbilisi_final = tbilisi_clean.select(
        col("id"),
        col("original_price"),
        col("original_currency"),
        col("price"),
        col("area"),
        col("rooms"),
        col("city"),
        col("neighborhood"),
        col("price_per_sqm"),
        col("floor"),
        col("building_type"),
        lit(args.data_date).alias("date")
    )
    
    yerevan_final = yerevan_clean.select(
        col("id"),
        col("original_price"),
        col("original_currency"),
        col("price"),
        col("area"),
        col("rooms"),
        col("city"),
        col("neighborhood"),
        col("price_per_sqm"),
        col("floor"),
        col("building_type"),
        lit(args.data_date).alias("date")
    )
    
    baku_final = baku_clean.select(
        col("id"),
        col("original_price"),
        col("original_currency"),
        col("price"),
        col("area"),
        col("rooms"),
        col("city"),
        col("neighborhood"),
        col("price_per_sqm"),
        col("floor"),
        col("building_type"),
        lit(args.data_date).alias("date")
    )
    
    # Combine datasets
    combined_df = tbilisi_final.union(yerevan_final).union(baku_final)
    
    # Save processed data
    combined_df.write.parquet(args.output_path, mode="overwrite")
    
    print(f"Data processing completed. Output saved to {args.output_path}")
    
if __name__ == "__main__":
    main()
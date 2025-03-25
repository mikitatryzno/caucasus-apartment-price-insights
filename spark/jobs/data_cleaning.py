import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, regexp_replace, to_date, lit, round

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
    # Assuming the Tbilisi dataset structure
    return df.withColumn("price", col("price").cast("float")) \
             .withColumn("area", col("area").cast("float")) \
             .withColumn("rooms", col("rooms").cast("integer")) \
             .withColumn("price_per_sqm", round(col("price") / col("area"), 2)) \
             .withColumn("city", lit("Tbilisi"))

def clean_yerevan_data(df):
    """Clean and transform Yerevan apartment data"""
    # Assuming the Yerevan dataset structure
    return df.withColumn("price", col("price").cast("float")) \
             .withColumn("area", col("area").cast("float")) \
             .withColumn("rooms", col("rooms").cast("integer")) \
             .withColumn("price_per_sqm", round(col("price") / col("area"), 2)) \
             .withColumn("city", lit("Yerevan"))

def clean_baku_data(df):
    """Clean and transform Baku apartment data"""
    # Assuming the Baku dataset structure
    return df.withColumn("price", col("price").cast("float")) \
             .withColumn("area", col("area").cast("float")) \
             .withColumn("rooms", col("rooms").cast("integer")) \
             .withColumn("price_per_sqm", round(col("price") / col("area"), 2)) \
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
    
    # Combine datasets
    combined_df = tbilisi_clean.union(yerevan_clean).union(baku_clean)
    
    # Add date column
    combined_df = combined_df.withColumn("date", lit(args.data_date))
    
    # Select and reorder columns to match BigQuery schema
    final_df = combined_df.select(
        col("id"),
        col("price"),
        col("area"),
        col("rooms"),
        col("city"),
        col("neighborhood"),
        col("date"),
        col("price_per_sqm")
    )
    
    # Save processed data
    final_df.write.parquet(args.output_path, mode="overwrite")
    
    print(f"Data processing completed. Output saved to {args.output_path}")
    
if __name__ == "__main__":
    main()
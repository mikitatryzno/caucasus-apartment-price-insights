import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, sum, min, max, percentile_approx, lit, date_format

def parse_arguments():
    parser = argparse.ArgumentParser(description='Apartment Data Analysis')
    parser.add_argument('--data_date', required=True, help='Date of the data in YYYY-MM-DD format')
    parser.add_argument('--input_path', required=True, help='Input path for processed data')
    parser.add_argument('--output_path', required=True, help='Output path for analysis results')
    return parser.parse_args()

def create_spark_session():
    return SparkSession.builder \
        .appName("Apartment Data Analysis") \
        .getOrCreate()

def main():
    args = parse_arguments()
    spark = create_spark_session()
    
    # Load processed data
    df = spark.read.parquet(args.input_path)
    
    # Register as temp view for SQL queries
    df.createOrReplaceTempView("apartments")
    
    # Analysis 1: Price statistics by city
    city_stats = spark.sql("""
        SELECT
            city,
            COUNT(*) as listing_count,
            AVG(price) as avg_price,
            MIN(price) as min_price,
            MAX(price) as max_price,
            AVG(price_per_sqm) as avg_price_per_sqm,
            AVG(area) as avg_area,
            AVG(rooms) as avg_rooms
        FROM apartments
        GROUP BY city
    """)
    
    # Analysis 2: Price by room count and city
    room_stats = spark.sql("""
        SELECT
            city,
            rooms,
            COUNT(*) as listing_count,
            AVG(price) as avg_price,
            AVG(price_per_sqm) as avg_price_per_sqm,
            AVG(area) as avg_area
        FROM apartments
        WHERE rooms BETWEEN 1 AND 5
        GROUP BY city, rooms
        ORDER BY city, rooms
    """)
    
    # Analysis 3: Top 10 neighborhoods by price per sqm in each city
    top_neighborhoods = spark.sql("""
        WITH ranked_neighborhoods AS (
            SELECT
                city,
                neighborhood,
                AVG(price_per_sqm) as avg_price_per_sqm,
                COUNT(*) as listing_count,
                RANK() OVER (PARTITION BY city ORDER BY AVG(price_per_sqm) DESC) as rank
            FROM apartments
            WHERE neighborhood IS NOT NULL
            GROUP BY city, neighborhood
            HAVING COUNT(*) >= 5
        )
        SELECT
            city,
            neighborhood,
            avg_price_per_sqm,
            listing_count
        FROM ranked_neighborhoods
        WHERE rank <= 10
        ORDER BY city, rank
    """)
    
    # Save analysis results
    city_stats.write.mode("overwrite").parquet(f"{args.output_path}city_stats")
    room_stats.write.mode("overwrite").parquet(f"{args.output_path}room_stats")
    top_neighborhoods.write.mode("overwrite").parquet(f"{args.output_path}top_neighborhoods")
    
    print(f"Data analysis completed. Results saved to {args.output_path}")
    
if __name__ == "__main__":
    main()
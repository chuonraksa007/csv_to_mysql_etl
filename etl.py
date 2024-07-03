import pandas as pd
import mysql.connector

# Extract data from CSV file
def extract_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Transform data
def transform_data(df):
    transformed_df = df[['transaction_id', 'date', 'product_category', 'product_name', 'units_sold', 'unit_price', 'total_revenue', 'region', 'payment_method']].copy()
    transformed_df['date'] = pd.to_datetime(transformed_df['date']).dt.strftime('%y-%m-%d')
    transformed_df = transformed_df.fillna({'transaction_id': '', 'date': '', 'product_category': '', 'product_name': '', 'units_sold': 0.00, 'unit_price': 0.00, 'total_revenue': 0.00, 'region': '', 'payment_method': ''})
    return transformed_df

# Create table if it does not exist
def create_table(cursor, table_name):
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            `transaction_id` VARCHAR(255),
            `date` DATE,
            `product_category` VARCHAR(255),
            `product_name` VARCHAR(255),
            `units_sold` INT,
            `unit_price` DECIMAL(10,2),
            `total_revenue` DECIMAL(10,2),
            `region` VARCHAR(255),
            `payment_method` VARCHAR(255)
        )
    """
    cursor.execute(create_table_query)

# Load data into MySQL
def load_data(df):
    host = "csv_etl_mysql_container"
    database = "db_etl"
    user = "user_etl"
    password = "123456"
    port = "3306"
    
    connection = mysql.connector.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )
    
    table_name = "tbl_test"
    cursor = connection.cursor()
    
    if connection.is_connected():
        print("Successfully connected to the database")
        
        create_table(cursor, table_name)
        
        columns = ', '.join([f'`{col}`' for col in df.columns])
        placeholders = ', '.join(['%s'] * len(df.columns))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        data = [tuple(row) for row in df.values]
        cursor.executemany(insert_query, data)
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("Data loaded successfully")
    else:
        print("Failed to connect to the database")

# Main function to run ETL
def main():
    # Extract
    file_path = 'sale_data.csv'
    df = extract_data(file_path)
    
    # Transform data
    transformed_data = transform_data(df)

    # Load data
    load_data(transformed_data)
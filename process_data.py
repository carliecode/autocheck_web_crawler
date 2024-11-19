import os
import logging
import pandas as pd
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config.db_settings import CONNECTION_STRING  
from utils import DOWNLOADED_FILE, ARCHIVE_FOLDER

# Initialize database connection
engine = create_engine(CONNECTION_STRING)
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()
car_prices = Table('car_prices', metadata, autoload_with=engine, schema='silver')

def read_download_file(file_name):
    """Read the downloaded CSV file and assign column headers."""
    logging.info("Reading downloaded file.")
    data = pd.read_csv(file_name, header=None)
    column_header = [
        'Manufacturer', 'Model', 'Year', 'Transmission', 'Color', 'Type', 'Location', 'Price'
    ]
    data.columns = column_header
    return data

def clean_data(data):
    """Clean the data: split location, convert price to float, and reformat."""
    logging.info("Cleaning data.")
    data.dropna(inplace=True)
    location_split = data['Location'].str.split(',', expand=True)
    data['State'], data['Area'] = location_split[0], location_split[1]
    data['Price'] = data['Price'].str.replace(',', '').str.replace('₦ ', '')
    data = data[['Manufacturer', 'Model', 'Year', 'Transmission', 'Color', 'Type', 'Area', 'State', 'Price']]
    return data

def save_to_db(data):
    """Save data to the database: insert or update records."""
    logging.info("Saving data to database.")
    today_date = datetime.today()

    for index, row in data.iterrows():

        try:
            data.at[index, 'Price'] = float(row['Price']) 
        except ValueError:
            continue
        
        # Check if record exists
        existing_record = session.query(car_prices).filter(
            car_prices.c.Manufacturer == row['Manufacturer'],
            car_prices.c.Model == row['Model'],
            car_prices.c.Year == row['Year'],
            car_prices.c.Transmission == row['Transmission'],
            car_prices.c.Color == row['Color'],
            car_prices.c.Type == row['Type'],
            car_prices.c.Area == row['Area'],
            car_prices.c.State == row['State'],
            car_prices.c.Price == row['Price']
        ).first()

        if existing_record:
            continue
        else:
            insert_data = {
                'Manufacturer': row['Manufacturer'],
                'Model': row['Model'],
                'Year': row['Year'],
                'Transmission': row['Transmission'],
                'Color': row['Color'],
                'Type': row['Type'],
                'Area': row['Area'],
                'State': row['State'],
                'Price': row['Price'],
                'Created_At': today_date,
                'Updated_At': today_date
            }
            session.execute(car_prices.insert(), insert_data)

    session.commit()

def move_to_archive():
    """Move processed file to the archive folder with a new name."""
    logging.info("Moving file to archive.")
    base_new_file_name = f'{datetime.today().strftime("%Y-%m-%d")}_file.txt'
    new_file_path = os.path.join(ARCHIVE_FOLDER, base_new_file_name)
    
    # Check if file exists and append a number if it does
    counter = 1
    while os.path.exists(new_file_path):
        new_file_path = os.path.join(ARCHIVE_FOLDER, f'{datetime.today().strftime("%Y-%m-%d")}_file_{counter}.txt')
        counter += 1
    
    os.rename(DOWNLOADED_FILE, new_file_path)
    print(f"File moved and renamed from {DOWNLOADED_FILE} to {new_file_path}")

def main():
    """Main process to read, clean, save data and move file to archive."""
    logging.info("Starting data processing.")
    data = read_download_file(DOWNLOADED_FILE)
    data = clean_data(data)
    save_to_db(data)
    move_to_archive()
    logging.info("Data processing completed.")

if __name__ == "__main__":
    main()

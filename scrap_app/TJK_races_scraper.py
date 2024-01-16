import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import re
import json
import logging


# Constants
CONFIG_FILE = "data\config.json"
LOG_FILE = "data\scraping.log"

def read_config():
    # Load configuration from a JSON file
    with open(CONFIG_FILE, 'r') as config_file:
        return json.load(config_file)

def init_logging():
    # Initialize logging
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def delete_races_table(cursor):
    # Delete the races table if it exists
    cursor.execute('DROP TABLE IF EXISTS races')

def create_races_table(cursor, column_names):
    # Create a new table for races with "City" and "Race Time" columns at the beginning
    create_table_sql = f'''
    CREATE TABLE IF NOT EXISTS races (
        "City" TEXT COLLATE NOCASE,
        "Race Time" TEXT COLLATE NOCASE,
        {', '.join([f'"{name}" TEXT COLLATE NOCASE' for name in column_names])}
    )
    '''
    cursor.execute(create_table_sql)

def save_to_database(cursor, data_list, column_names):
    # Get the existing column names from the database table
    cursor.execute(f'PRAGMA table_info(races)')
    existing_columns = [row[1] for row in cursor.fetchall()]
    
    # Identify new columns and missing columns
    new_columns = [col for col in column_names if col not in existing_columns]
    missing_columns = [col for col in existing_columns if col not in column_names]

    # Add new columns to the database table
    for new_col in new_columns:
        cursor.execute(f'ALTER TABLE races ADD COLUMN "{new_col}" TEXT COLLATE NOCASE')

    # Remove missing columns from the database table (optional)
    #for missing_col in missing_columns:
    #    cursor.execute(f'ALTER TABLE races DROP COLUMN "{missing_col}"')

    # Update the master_column_names with adjusted column names
    master_column_names = column_names + ["City", "Race Time"]

    # Generate INSERT INTO SQL statement dynamically
    insert_sql = f'''
    INSERT INTO races ({', '.join(['"' + name + '"' for name in column_names + ["City", "Race Time"]])})
    VALUES ({', '.join(['?' for _ in master_column_names])})
    '''

    for data in data_list:
        values = []
        for name in master_column_names:
            values.append(data.get(name, ''))
        
        #print(f"Inserting values: {data_list}")
        cursor.execute(insert_sql, values)


def clean_text(text):
    # Define patterns or conditions to identify unwanted data and clean it
    patterns_to_clean = [
        (r'\s*\n.*', ''),  # Remove text after newline characters
        (r'\s*\\n.*', ''),  # Remove text after '\n' characters
        (r' \d+\.\d+\s*.*\d{4}\s*.*', ''),  # Remove patterns like ' 1.22.53 Bu derece Diyarbakır Hipodromu'nda, 17.06.2023 tarihinde yapılmıştır.'
    ]

    # Apply the cleaning patterns to the text
    for pattern, replacement in patterns_to_clean:
        text = re.sub(pattern, replacement, text)

    # Replace multiple spaces with a single space
    text = ' '.join(text.split())

    return text.strip()  # Remove leading and trailing spaces

def auto_clean_data(data_list):
    cleaned_data = []
    for data in data_list:
        for column_name in data:
            if isinstance(data[column_name], str):
                # Check if the column contains unwanted patterns and clean them
                data[column_name] = clean_text(data[column_name])

        cleaned_data.append(data)

    return cleaned_data

def scrape_page(column_names, data_list, city_link, master_column_names):
    response = requests.get(f"{URL}{city_link}")
    response.raise_for_status()

    soup_data = BeautifulSoup(response.text, 'html.parser')

    # Extract city from city_link
    city_name_match = soup_data.find('div', class_='program')
    city = city_name_match['id']
    

    tables = soup_data.find_all('table', class_='tablesorter')
    
    rn = 0  # Initialize the race number
    race_time_element = soup_data.find_all('ul', class_=re.compile('races-tabs\d+'))
    
    # Iterate through race_time_element to extract race time for each element
    for element in race_time_element:
        race_time_no = element.find_all('li')   
        # Extract the text of li elements and join them
        time_text = (time_element.text.strip() for time_element in race_time_no)
        # Clean the text and append it to the race_time list
        race_t = ','.join(time_text).split(',')
        
    for table in tables:
        # Extract column names from the current table and exclude the "N,forma,idm" column
        header_row = table.find_all('th')
        current_column_names = [header.text.strip() for header in header_row if header.text.strip() not in ['Forma', 'İdm', 'N']]

        # Ensure that the current table's column names match the master list
        for column_name in master_column_names:
            if column_name not in current_column_names:
                current_column_names.insert(master_column_names.index(column_name), column_name)
        
        # Extract race time from the current table
        
        for row in table.find_all('tr'):
            # Extract data for each row
            row_data = row.find_all('td')
            # Check if row_data is not empty
            
            if row_data:
                horse_data = {}
                is_shifted = row_data[0].text.strip() == ''
               # Initialize the index to zero for shifted rows
                idx = 1

                for i in range(len(master_column_names)):
                    if idx < len(row_data):
                        # Get the cell text
                        cell_text = row_data[idx].text.strip()
                        cell_text_2 = row_data[idx + 1].text.strip()
                        if is_shifted:
                            # Handle the shift by moving the data to the left
                            horse_data[master_column_names[i]] = clean_text(cell_text_2)
                        elif not is_shifted:
                            # If it's not a shifted row, assign the data to the corresponding column
                            horse_data[master_column_names[i]] = clean_text(cell_text)

                        # Increment the index
                        idx += 1
                    else:
                        # Missing columns in the current row, add them with empty strings
                        horse_data[master_column_names[i]] = ''
                
                # Append city and race time to the horse_data dictionary
                horse_data["City"] = clean_text(city)
                race_tm = [' '.join([time.strip() for time in item.split('\r\n') if time.strip()]).split('\n') for item in race_t]
                race_tv = race_tm[rn]
                race_time = ' '.join(race_tv).strip()
                
                #print(race_time)
                if race_time:
                    horse_data["Race Time"] = race_time
                else:
                    horse_data["Race Time"] = ''  # Handle the case when there are no more race times
                
                data_list.append(horse_data)
        rn +=1
    return data_list

def race():
    start_time = time.time()

    config = read_config()
    init_logging()

    global URL
    URL = config["base_url"]
    DB_FILE = config["db_file"]

    # Create the database and table
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    delete_races_table(cursor)

    # Initialize column names from headers
    column_names = []

    # Extract city links
    city_links = []

    main_req = requests.get(config["main_url"])
    soup_main = BeautifulSoup(main_req.text, 'html.parser')

    if main_req.status_code == 200:
        cities = soup_main.find('div', class_='race-info')
        if cities:
            city_list = cities.find_all('a', href=True)
            for city in city_list:
                city_links.append(city['href'])
        else:
            logging.error("No city list found on the page.")
            return
    else:
        logging.error(f"Failed to retrieve the page. Status code: {main_req.status_code}")
        return

    # Loop through each page and scrape data for each city
    for city_link in city_links:
        # Extract column names from the first table
        response = requests.get(f"{URL}{city_link}")
        soup_data = BeautifulSoup(response.text, 'html.parser')
        first_table = soup_data.find('table', class_='tablesorter')
        if first_table:
            header_row = first_table.find_all('th')
            master_column_names = [header.text.strip() for header in header_row if header.text.strip() not in ['N','Forma', 'İdm']]
        else:
            logging.error(f"Column names not found in the first table for city: {city_link}. Check the website structure.")
            continue  # Move on to the next city

        # Initialize data list for this city
        data_list = []

        # Scrape data for this city and get the city and race time
        data_list = scrape_page(column_names, data_list, city_link, master_column_names)
        data_list = auto_clean_data(data_list)
        
        # Create the races table and save data
        create_races_table(cursor, master_column_names)
        save_to_database(cursor, data_list, master_column_names)

    conn.commit()
    conn.close()

    elapsed_time = time.time() - start_time
    logging.info(f'All pages parsed and data saved to the database. Elapsed time: {elapsed_time:.2f} seconds')



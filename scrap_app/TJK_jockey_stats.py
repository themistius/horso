import requests
from bs4 import BeautifulSoup
import time
import sqlite3
import math
import re

# Constants
HEADERS_URL = 'https://www.tjk.org/TR/YarisSever/Query/Page/JokeyIstatistikleri'
DATA_URL = 'https://www.tjk.org/TR/YarisSever/Query/DataRows/JokeyIstatistikleri'

# Database settings
DB_FILE = 'data/horse_racing.db'

def create_database(cursor, column_names):
    # Generate CREATE TABLE SQL statement dynamically
    create_table_sql = f'''
    CREATE TABLE IF NOT EXISTS jockeys (
        id INTEGER PRIMARY KEY,
        {', '.join([f'"{name}" TEXT COLLATE NOCASE' for name in column_names])}
    )
    '''
    conn = sqlite3.connect(DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES, isolation_level=None)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute(create_table_sql)
    conn.commit()
    conn.close()

def save_to_database(cursor, data_list, column_names):
    # Generate INSERT INTO SQL statement dynamically
    insert_sql = f'''
    INSERT INTO jockeys ({', '.join(['"' + name + '"' for name in column_names])})
    VALUES ({', '.join(['?' for _ in column_names])})
    '''

    for data in data_list:
        try:
            cursor.execute(insert_sql, [data.get(name, '') for name in column_names])
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            print(f"Columns: {column_names}")
            print(f"Data: {data}")  # Print the problematic row for reference

def scrape_page(page_number, column_names, data_list):
    url = f"{DATA_URL}?PageNumber={page_number}&Sort=derece1+DESC,derece1yuzde+DESC"

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('tbody', class_='ajaxtbody')

        # Extract column names from table headers on the first page
        if not column_names:
            header_row = table.find('th')
            column_names.extend([header.text.strip() for header in header_row])

            if not column_names:
                print("Column names not found. Check the website structure.")
                exit()

        column_data = table.find_all('tr')
        for row in column_data[:-1]:
            row_data = row.find_all('td')
            indiv_row_data = [data.text.strip() for data in row_data]
            data_list.append(dict(zip(column_names, indiv_row_data)))

        print(f'Page {page_number} parsed')

    except requests.exceptions.RequestException as e:
        print(f'Error requesting page {page_number}: {e}')

def jockey():
    start_time = time.time()

    # Initialize column names from headers
    url_th = HEADERS_URL
    r_req = requests.get(url_th)
    s2 = BeautifulSoup(r_req.text, 'html.parser')
    world_titles = s2.find_all('th')
    column_names = [title.text.strip() for title in world_titles]
    print(f'Headers: {column_names}')

    # Data list to store scraped data
    data_list = []

    # Create the database and table
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    create_database(cursor, column_names)
    conn.commit()
    conn.close()

    # Find the div containing the total count text
    total_results_element = s2.find('td', colspan='12')

    if total_results_element:
        total_results_text = total_results_element.find('div').text

        # Extract the total count from within the table structure
        total_count_match = re.search(r'Toplam (\d+) sonuçtan', total_results_text)

        if total_count_match:
            total_count = int(total_count_match.group(1))
        else:
            print("Total count not found. Using a default value of 0.")
            total_count = 0
    else:
        print("Total count element not found.")
        exit()

    # Calculate the total number of pages based on the count and items per page
    items_per_page = 50
    total_pages = math.ceil(total_count / items_per_page)

    for i in range(0, total_pages):
        scrape_page(i, column_names, data_list)

    # Save any remaining data to the database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    save_to_database(cursor, data_list, column_names)
    conn.commit()
    conn.close()

    elapsed_time = time.time() - start_time
    print(f'All pages parsed and data saved to the database. Elapsed time: {elapsed_time:.2f} seconds')

if __name__ == "__main__":
    jockey()
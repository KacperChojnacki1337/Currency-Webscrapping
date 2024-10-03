# Currency Data Extraction and Storage

This project extracts currency data from the PB website and stores it in a PostgreSQL database.

## Prerequisites

- Python 3.x
- `requests` library
- `BeautifulSoup` library
- `pandas` library
- `psycopg2` library
- `sqlalchemy` library
- PostgreSQL database

  ## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/kacperchojnacki1337/Currency-Webscrapping.git
    cd your-repo-name
    ```

2. Install the required Python packages:
    ```bash
    pip install requests beautifulsoup4 pandas psycopg2 sqlalchemy
    ```

3. Set up your PostgreSQL database and update the connection parameters in the `insert_data_to_postgresql` function.


## Usage

1. Run the script to extract currency data and insert it into the PostgreSQL database:
    ```bash
    python currencies_script.py
    ```

## Functions

### `extract_currency_data()`

This function extracts currency data from the PB website and returns it as a pandas DataFrame.

### `insert_data_to_postgresql()`

This function connects to the PostgreSQL database, creates a table if it doesn't exist, and inserts the extracted currency data into the table.

## Author
Kacper Chojnacki


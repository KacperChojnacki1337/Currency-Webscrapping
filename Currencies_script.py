import requests
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT



def extract_currency_data():
    # Download data from PB
    response = requests.get("https://notowania.pb.pl/instrument/PBWALEURPLN/eurpln")
    response.status_code

    # Check
    if response.status_code == 200:
      # Parse HTML data
      soup = BeautifulSoup(response.content, 'html.parser')

      # Find all rows of a table with currency data
      data_rows = soup.find_all('tr')
      currencies = []
      currency_exchange_rate = []
      changes = []
      percent_changes = []
      buy_rates = []
      sell_rates = []
      dates = []

      # Looping through rows and fetching data
      for row in data_rows:
        if row.find('th'):  # Skip header row
          continue  # Go to next loop iteration

        cells = row.find_all('td')
        currencies.append(cells[0].text.strip())  # Get currency name (remove spaces)
        currency_exchange_rate.append(cells[1].text.strip())  # Fetch currency exchange rate
        changes.append(cells[2].text.strip())  # Fetch Changes
        percent_changes.append(cells[3].text.strip())  # Fetch Percent Changes
        buy_rates.append(cells[4].text.strip())  # Fetch Buy Rates 
        sell_rates.append(cells[5].text.strip())  # Fetch Sell Rates
        dates.append(cells[6].text.strip())  # Fetch Date
      currency_exchange_rate_float = []  
      for k in currency_exchange_rate:
        currency_exchange_rate_float.append(float(k.replace(',', '.')))
      # Data Dictionary
      data = {
          "Currency": currencies,
          "Exchange Rate": currency_exchange_rate_float}

      # create DataFrame from Dict
      currency_df = pd.DataFrame(data)
      USD_PLN_rate = currency_df.loc[0, "rate"]
      EUR_USD_rate = currency_df.loc[3, "rate"]
      EUR_PLN_rate = round((USD_PLN_rate * EUR_USD_rate),4)
      new_row = {"currency": "EUR/PLN", "rate": EUR_PLN_rate }
      currency_df.loc[len(currency_df)] = new_row
      currency_df.loc[len(currency_df)] = {"currency": "PLN/PLN", "rate":1}
      today = pd.to_datetime('today')
      currency_df['data'] = today 
      return currency_df



def insert_data_to_postgresql():
    db_host = "localhost"
    db_port = 5432
    db_name = "postgres"
    db_user = "postgres"
    db_password = "###"
    # Database connection parameters (replace with your credentials)
    try:
        conn1 = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
        print("Connected with DataBase")
    except psycopg2.Error as e:
        print("Database connection error:", e)
        return None
    cursor = conn1.cursor()
    conn1.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    currency_df = extract_currency_data()
    cursor.execute('SELECT current_database()')
    cursor.fetchall()
    
    cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'currency_table');")
    table_exists = cursor.fetchone()[0]

    if table_exists:
        # Truncate the table to clear existing data
        cursor.execute("TRUNCATE TABLE currency_table;")
        print("Existing table 'currency_table' was cleared.")
    else:
        # Create the table with column names inferred from DataFrame headers
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS currency_table (
                """ + ', '.join(currency_df.columns) + """)
        """)
        print("Created new table 'currency_table'.")
    engine = create_engine('postgresql+psycopg2://postgres:###@localhost/postgres')
    print(engine)
    #append, fail, replace
    currency_df.to_sql('currency_table',engine,if_exists='append', index=False)
    conn1.close()

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

class Fantasy:
    def addContracts(self, df_raw, df_contracts):
        df_raw
        # for i in range(len(df_contracts)):
        #     for ii in range(len(df_raw)):
                # print(i)
                # if df_raw.loc[ii, "Player"].split()[1] == df_contracts.loc[i, "Player"].split()[1]:
                    # print(df_contracts.loc[i, "Player"].split()[1])
        # for i in range(len(df_raw)):
        #     print(df_raw.loc[i, "Player"], df_raw.loc[i, "Team"])

    def addAdvanced(self, df_raw, df_advanced):
        # new data frame with split value columns
        new = df_advanced["Player"].str.split(" ", n = 1, expand = True)

        # making separate last name column from new data frame
        df_advanced["Last Name"] = new[1]
        raw_name = df_raw["Player"].str.split(" ", n = 1, expand = True)
        
        df_raw["Last Name"] = raw_name[1]
        merged_df = df_raw.merge(df_advanced, how = 'inner', on = ['Last Name'])

        return merged_df
    
    def makeRegularData(self, df):
        QB_data = df[df["Pos"] == "QB"]
        qb_drop_columns = ['Tgt', 'Rec', 'Receiving_Yds', 'Receiving_Td', 'Receiving_1st', 'Return_Yds', 'Return_Td', '2PT',]
        QB_data = QB_data.drop(qb_drop_columns, axis=1)

        RB_data = df[df["Pos"] == "RB"]
        rb_drop_columns = [ 'Comp', 'Inc', 'Passing_Yds', 'Passing_Td', 'Int', 'Pic6', 'Sks', 'Passing_1st']
        RB_data = RB_data.drop(rb_drop_columns, axis=1)

        WR_data = df[df["Pos"] == "WR"]
        wr_drop_columns = ['Comp', 'Inc', 'Passing_Yds', 'Passing_Td', 'Int', 'Pic6', 'Sks', 'Passing_1st']
        WR_data = WR_data.drop(wr_drop_columns, axis=1)

        TE_data = df[df["Pos"] == "TE"]
        te_drop_columns = ['Comp', 'Inc', 'Passing_Yds', 'Passing_Td', 'Int', 'Pic6', 'Sks', 'Passing_1st', 'Return_Yds', 'Return_Td']
        TE_data = TE_data.drop(te_drop_columns, axis=1)

        return QB_data, RB_data, WR_data, TE_data
    
    def getAdvancedStats(self, type, year):
        url_pro_football_reference = 'https://www.pro-football-reference.com/years/' + year + '/' + type + '_advanced.htm'


        if type == "rushing":

            # For the rushing, we need to use selenium to account for the dynamically implemented dataset

            # Set up ChromeDriver
            driver = webdriver.Chrome()
            driver.get(url_pro_football_reference)

            # Wait for the page to load
            driver.implicitly_wait(5)

            # Get the page source
            html = driver.page_source

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Find the table element by id
            table = soup.find('table', {'id': 'advanced_rushing'})

            # Quit the browser
            driver.quit()

            # Get columns and rows
            headers = table.find_all('tr')[1].find_all('th') # Find all headers in HTML
            players = table.find_all('tbody')[0] # Find all players (which will be our rows)


            # Get column headers
            cols = []
            for th in headers:
                cols.append(th.text.strip())
            cols = cols[1:] # Dont want to include the row number

            # Get table rows
            rows = []

            # Loop through each 'tr' tag
            for tr in players.find_all('tr'):
                row = []
                for td in tr.find_all('td'):
                    row.append(td.text.strip())
                if row:
                    rows.append(row)

            # Make pandas df
            table = pd.DataFrame(rows, columns=cols)
            table['Player'] = table['Player'].str.replace('*', '')
            table['Player'] = table['Player'].str.replace('+', '')

        else:

            table = pd.read_html(url_pro_football_reference, header=1)[0]
            table['Player'] = table['Player'].str.replace('*', '')
            table['Player'] = table['Player'].str.replace('+', '')
        
        return table
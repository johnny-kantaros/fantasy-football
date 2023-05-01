import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

class Fantasy:


    def read_data(year):
        year_prior = int(year) - 1
        # Get X matrix (base)
        df = pd.read_excel(year + '-offense.xlsx', sheet_name='Offense_2020', header=3)

        # Drop columns that we don't need
        drop_columns = ['GS', 'Bye', 'Notes', 'Rank', 'Y! Roto', 'Δ', 'Y! Old', 'Std', 'Δ.1', 'Std Old', 'PPR', 'Δ.2', 'PPR Old', '% Own', 'Fan Pts', 'PPG']
        df = df.drop(drop_columns, axis=1)

        # Change names of duplicate columns
        updated_columns = {'Yds': 'Passing_Yds', 'Yds.1': 'Rushing_Yds', 'Yds.2': 'Receiving_Yds', 'Yds.3': 'Return_Yds', 
                        'TD': 'Passing_Td', 'TD.1': 'Rushing_Td', 'TD.2': 'Receiving_Td', 'TD.3': 'Return_Td', 
                        '1st': 'Passing_1st', '1st.1': 'Rushing_1st', '1st.2': 'Receiving_1st', 'Team': 'Tm'}
        df = df.rename(columns=updated_columns)


        # Get y vector

        df2 = pd.read_excel('2022-offense.xlsx', sheet_name='Offense_Prior_Actuals', header=3)
        y = pd.DataFrame()
        y['Player'] = df2['Player']
        y['points'] = df2['Fan Pts']


        return df, y

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
        # print(type(df_advanced))
        # print(df_advanced['Player'])
        df_advanced['Name'] = df_advanced['Player'].apply(self.extract_initial_last_name)
        df_raw['Name'] = df_raw['Player']

        merged_df = df_raw.merge(df_advanced, on=['Name'], how='left').fillna(0)

        return merged_df
    
    def simpleMerge(self, df_1, df_2):
        # new data frame with split value columns
        print(df_2)
        df_2['Name'] = df_2['Player']
        merged_df = df_1.merge(df_2, on=['Name'], how='left').fillna(0)

        return merged_df
    
    def extract_initial_last_name(self, full_name):
        name_parts = full_name.split(' ')
        if len(name_parts) == 1:
            return name_parts[0]
        elif len(name_parts) == 2:
            first_name, last_name = name_parts
            return f"{first_name[0]}. {last_name}"
        else:
            return full_name


    
    def makeRegularData(self, df, position):
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

        if position == "QB": 
            return QB_data
        elif position == "RB":
            return RB_data
        elif position == "WR":
            return WR_data
        elif position == "TE":
            return TE_data

    
    def getAdvancedStats(self, type, year):
        url_pro_football_reference = 'https://www.pro-football-reference.com/years/' + year + '/' + type + '_advanced.htm'


        if type == "rushing":
            return self.get_table(url_pro_football_reference, "rushing")
        
        elif type == "receiving":
            return self.get_table(url_pro_football_reference, "receiving")

        else:

            table = pd.read_html(url_pro_football_reference, header=1)[0]
            table['Player'] = table['Player'].str.replace('*', '')
            table['Player'] = table['Player'].str.replace('+', '')
        
            return table
    

    def get_table(self, link, type):

        # Set up ChromeDriver
            driver = webdriver.Chrome()
            driver.get(link)

            # Wait for the page to load
            driver.implicitly_wait(5)

            # Get the page source
            html = driver.page_source

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Find the table element by id
            table = soup.find('table', {'id': f'advanced_{type}'})

            # Quit the browser
            driver.quit()

            # Get columns and rows

            if type == "receiving":
                headers = table.find_all('tr')[0].find_all('th') # Find all headers in HTML
            else:
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
            return table

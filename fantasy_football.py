import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

class Fantasy:


    """
    
    Function for web-scraping our main player data

    Inputs: year
    Outputs: df (X matrix), y (target vector)
    
    """

    def read_data(year):

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
        y['PPG'] = df2['PPG']
        y['Pos'] = df2['Pos']


        return df, y





    """
    
    Function to properly format player names in anticipation of merging

    Inputs: full name (Pandas column)
    Outputs: Corrected column
    
    """
    

    
    def extract_initial_last_name(self, full_name):
        name_parts = full_name.split(' ')
        if len(name_parts) == 1:
            return name_parts[0]
        elif len(name_parts) == 2:
            first_name, last_name = name_parts
            return f"{first_name[0]}. {last_name}"
        elif len(name_parts) == 3:
            first_name = name_parts[0]
            last_name = name_parts[1]
            rest = name_parts[2]
            return f"{first_name[0]}. {last_name} {rest}"






    """
    
    Function to split the df by position

    Inputs: df, position
    Outputs: sliced df
    
    """
    
    def splitByPos(self, df, position):
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
        




    """
    
    Function to web-scrape advanced stats

    Inputs: type of stat, year
    Outputs: Advanced stats in pandas df
    
    """

    
    def getAdvancedStats(self, type, year):
        url_pro_football_reference = 'https://www.pro-football-reference.com/years/' + year + '/' + type + '_advanced.htm'


        if type == "rushing":

            table = self.get_table(url_pro_football_reference, "rushing")

            # Drop unneeded columns
            drop_cols = ['Age', 'YBC', 'Tm', 'Att', 'G', 'GS', 'Yds', 'Pos', 'TD', '1D', 'YAC', 'BrkTkl']
            table = table.drop(drop_cols, axis=1)

            
            # Format name correctly
            table['Player'] = table['Player'].apply(self.extract_initial_last_name)
            table['Player'] = table['Player'].str.strip()

            
             
        
        elif type == "receiving":
            
            table = self.get_table(url_pro_football_reference, "receiving")

            drop_cols = ['YBC', 'Tm', 'G', 'GS', 'Tgt', 'Rec', 'Yds', 'Pos', 'TD', '1D', 'YBC', 'YAC', 'BrkTkl', 'Drop']
            table = table.drop(drop_cols, axis=1)
            
            # Format name correctly
            table['Player'] = table['Player'].apply(self.extract_initial_last_name)
            table['Player'] = table['Player'].str.strip()
        else:

            table = pd.read_html(url_pro_football_reference, header=1)[0]
            table['Player'] = table['Player'].str.replace('*', '')
            table['Player'] = table['Player'].str.replace('+', '')

            drop_cols = ['Tm', 'G', 'GS', 'Cmp', 'Att', 'Yds', 'IAY', 'CAY', 'YAC', 'Pos']
            table = table.drop(drop_cols, axis=1)

            # Format name correctly
            table['Player'] = table['Player'].apply(self.extract_initial_last_name)
            table['Player'] = table['Player'].str.strip()


        return table
    





    """
    
    Helper function used to bypass dynamically generated JS tables

    Input: link, type
    Output: table (Pandas Df)
    
    """
    

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

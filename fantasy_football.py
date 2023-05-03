import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.preprocessing import StandardScaler


class Fantasy:


    def read_data():

        # Get X matrix (base)
        df = pd.read_excel('2021-offense.xlsx', sheet_name='Offense_2020', header=3)

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
        y = df2['Fan Pts']

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
        df_advanced['Player'] = df_advanced['Player'].apply(self.extract_initial_last_name)

        merged_df = df_raw.merge(df_advanced, on=['Player', 'Tm'], how='left').fillna(0)

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


    def getTeamStats(self, year):
        # Get the raw team stats for all categories from NFL.com
        passing_stats = pd.DataFrame(pd.read_html("https://www.nfl.com/stats/team-stats/offense/passing/"+ str(year) +"/reg/all")[0])
        rushing_stats = pd.DataFrame(pd.read_html("https://www.nfl.com/stats/team-stats/offense/rushing/"+str(year)+"/reg/all")[0])
        receiving_stats = pd.DataFrame(pd.read_html("https://www.nfl.com/stats/team-stats/offense/receiving/"+str(year)+"/reg/all")[0])
        scoring_stats = pd.DataFrame(pd.read_html("https://www.nfl.com/stats/team-stats/offense/scoring/"+str(year)+"/reg/all")[0])
        downs_stats = pd.DataFrame(pd.read_html("https://www.nfl.com/stats/team-stats/offense/downs/"+str(year)+"/reg/all")[0])

        # Sort all of the different df's by team so they are lined up
        passing_stats.sort_values(by="Team", inplace=True)
        rushing_stats.sort_values(by="Team", inplace= True)
        receiving_stats.sort_values(by="Team", inplace=True)
        scoring_stats.sort_values(by="Team", inplace=True)
        downs_stats.sort_values(by="Team", inplace=True)

        # Drop teams from the last categories so team name is not repeated
        rushing_stats.drop(columns=["Team"], axis=1, inplace=True)
        new_cols = {}
        for col in rushing_stats.columns:
            new_cols[col] = 'rushing_' + col
        rushing_stats = rushing_stats.rename(columns=new_cols)

        receiving_stats.drop(columns=["Team"], axis=1, inplace=True)
        new_cols = {}
        for col in receiving_stats.columns:
            new_cols[col] = 'receiving_' + col
        receiving_stats = receiving_stats.rename(columns=new_cols)

        scoring_stats.drop(columns=["Team"], axis=1, inplace=True)
        new_cols = {}
        for col in scoring_stats.columns:
            new_cols[col] = 'scoring_' + col
        scoring_stats = scoring_stats.rename(columns=new_cols)

        downs_stats.drop(columns=["Team"], axis=1, inplace=True)
        new_cols = {}
        for col in downs_stats.columns:
            new_cols[col] = 'downs_' + col
        downs_stats = downs_stats.rename(columns=new_cols)

        # Team name formatting error fix
        passing_stats['Team'] = passing_stats['Team'].apply(lambda x: x[:int(len(x)/2)])
        new_cols = {}
        for col in passing_stats.columns:
            if col != "Team":
                new_cols[col] = 'passing_' + col
        passing_stats = passing_stats.rename(columns=new_cols)

        # Combine df's
        team_stats = pd.concat([passing_stats, rushing_stats, receiving_stats, scoring_stats, downs_stats], axis=1)

        team_stats = team_stats.reset_index(drop=True)

        return team_stats
    

    
    def getDraftData(self, year):

        # Used to map apreviations from SportsReference.com to NFL.com
        nfl_abrv = {"SFO": "49ers", "CHI": "Bears", "CIN": "Bengals", "BUF": "Bills", "DEN": "Broncos", "CLE": "Browns", "TAM": "Buccaneers",
             "ARI": "Cardinals", "LAC": "Chargers", "KAN": "Chiefs", "IND": "Colts", "DAL": "Cowboys", "MIA": "Dolphins", "PHI": "Eagles",
              "ATL": "Falcons", "WAS": "Football Team", "NYG": "Giants", "JAX": "Jaguars", "NYJ": "Jets", "DET": "Lions", "GNB": "Packers",
               "CAR": "Panthers", "NWE": "Patriots", "LVR": "Raiders", "LAR": "Rams", "BAL": "Ravens", "NOR": "Saints", "SEA": "Seahawks",
                "PIT": "Steelers", "HOU": "Texans", "TEN": "Titans", "MIN": "Vikings" }

        raw_draft = pd.DataFrame(pd.read_html("https://www.pro-football-reference.com/years/"+str(year)+"/draft.htm")[0])

        raw_draft.columns = raw_draft.columns.droplevel(0)

        raw_draft = raw_draft[["Pick", "Tm", "Player", "Pos"]]

        raw_draft = raw_draft[raw_draft["Pos"].isin(["QB", "RB", "WR", "TE", "K"])]

        raw_draft["Tm"] = raw_draft["Tm"].map(nfl_abrv)

        raw_draft = raw_draft.rename(columns={"Tm": "Team"})

        return raw_draft

    def getYearlyRookieData(self, year):

        total_data = pd.DataFrame()

        for y in range(year - 15, year + 1):
            draft_data = self.getDraftData(year=str(y))
            team_data = self.getTeamStats(year=str(y - 1))
            rookie_stats = pd.merge(draft_data, team_data, on='Team')

            labels = pd.DataFrame(pd.read_html("https://www.fantasypros.com/nfl/reports/leaders/?year=" + str(y))[0])

            labels = labels[["Player", "AVG"]]

            labels = labels.drop_duplicates(subset="Player")

            full_data = pd.merge(rookie_stats, labels, on='Player')

            total_data = pd.concat([total_data, full_data], axis=0)


        total_data = total_data.reset_index(drop=True)

        return total_data
    

    def getBestFeatures(self, X, y, numFolds= 3, numFeatures = 5):
        

        selector = SelectKBest(score_func=f_regression, k=numFeatures)
        selector.fit(X, y)

        selected_features = X.columns[selector.get_support()]

        print(selected_features)

        X_selected = X[selected_features]

        kf = KFold(n_splits=numFolds)
        model = LinearRegression()

        # Initialize a list to store the mean squared error for each fold
        mse_list = []
        for train_index, test_index in kf.split(X):

            X_train, X_test = X_selected.iloc[train_index], X_selected.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]

            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)

            mse_list.append(mean_squared_error(y_test, y_pred))

        mean_mse = np.mean(mse_list)
        
        return mean_mse
    
    def prepRookieData(self, df, standardize= False):

        labels = df["AVG"]

        raw_feats = df.iloc[: ,[0] + list(range(4, df.shape[1] - 1))]

        def convert_to_int(val):
            if isinstance(val, str) and val.endswith('T'):
                return int(val[:-1])
            else:
                return int(val)

        raw_feats[['passing_Lng', 'rushing_Lng', 'receiving_Lng']] = raw_feats[['passing_Lng', 'rushing_Lng', 'receiving_Lng']].applymap(convert_to_int)

        if standardize:

            scaler = StandardScaler()

            scaler.fit(raw_feats)

            standardized = scaler.transform(raw_feats)

            feats = pd.DataFrame(standardized, columns=df.iloc[: ,[0] + list(range(4, df.shape[1] - 1))].columns)

        else:
            feats = raw_feats

        return feats, labels


    

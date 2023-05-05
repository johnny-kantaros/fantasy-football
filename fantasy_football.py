import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.preprocessing import StandardScaler


class Fantasy:



    """
    
    Function to perform preprocessing steps for WR data

    Input: year
    Output: Merged and cleaned advanced data set
    
    """
    

    def prepare_TE(self, year):

        # First, lets get our normal data
        TE_normal = self.read_new(year, "TE")
        
        # Next, lets clean the dataset:
        TE_cleaned = self.clean_TE(TE_normal)

        # Lets now pull in our advanced dataset
        advanced = self.get_advanced_TE(year)

        # We now need to merge the two frames together
        # We will merge by the columns 'Player' and 'Tm'
        merge_cols = ['Player', 'Tm']
        merged_df = pd.merge(TE_cleaned, advanced, on=merge_cols, how='left')

        # We want to make per-game stats instead of normal aggregate
        # Therefore, lets divide all aggregate columns by total games played
        columns_to_convert = ['REC', 'TGT', 'Receiving_Yds', '20+', 'Receiving_Td', 'ATT', 
                              'Rushing_Yds', 'Rushing_Td',  'YBC', 'AIR', 'YAC', 'YACON', 
                              'BRKTKL', 'CATCHABLE', 'DROP', 'RZ TGT', 'YBC', 'AIR', 'YAC', 
                              'YACON', 'BRKTKL', '10+ YDS', '30+ YDS', '40+ YDS', '50+ YDS', 
                              ]
        
        # Use for loop to iterate through each agg column
        for col in columns_to_convert:
            merged_df[col] = merged_df[col] / merged_df['G']

        # Also, we do not want to include players who only appeared in a few games
        # This could skew our dataset, so lets remove them
        merged_df = merged_df[merged_df['G'] > 12]

        # Finally, lets remove the names of the QB's and their total number of games
        merged_df = merged_df.drop(['Player', 'G', 'Tm'], axis=1)
        
        # Lastly, lets impute the na values as the mean of the columns:

        merged_df['% TM'] = merged_df['% TM'].str.replace('%', '')
        merged_df['% TM'] = merged_df['% TM'].astype(float)

        numeric_cols = merged_df.select_dtypes(include=['float64', 'int64']).columns
        merged_df[numeric_cols] = merged_df[numeric_cols].fillna(merged_df[numeric_cols].mean())
        return merged_df


    """
    
    Function to perform preprocessing steps for QB data

    Input: year
    Output: Merged and cleaned advanced data set
    
    """

    def prepare_QB(self, year):

        # First, lets get our normal data
        QB_normal = self.read_new(year, "QB")
        
        # Next, lets clean the dataset:
        QB_cleaned = self.clean_QB(QB_normal)

        # Lets now pull in our advanced dataset
        advanced = self.get_advanced_QB(year)

        # We now need to merge the two frames together
        # We will merge by the columns 'Player' and 'Tm'
        merge_cols = ['Player', 'Tm']
        merged_df = pd.merge(QB_cleaned, advanced, on=merge_cols, how='left')

        # We want to make per-game stats instead of normal aggregate
        # Therefore, lets divide all aggregate columns by total games played
        columns_to_convert = ['CMP', 'Passing_att', 'Passing_Yds', 'Passing_Td', 'INT', 'SACKS', 
                              'Rushing_att', 'Rushing_Yds', 'Rushing_Td', '10+ YDS', '20+ YDS', 
                              '30+ YDS', '40+ YDS', '50+ YDS', 'KNCK', 'HRRY', 'BLITZ', 'POOR', 
                              'DROP', 'RZ ATT', 'RTG']
        
        # Use for loop to iterate through each agg column
        for col in columns_to_convert:
            merged_df[col] = merged_df[col] / merged_df['G']

        # Also, we do not want to include players who only appeared in a few games
        # This could skew our dataset, so lets remove them
        merged_df = merged_df[merged_df['G'] > 9]

        # Finally, lets remove the names of the QB's and their total number of games
        merged_df = merged_df.drop(['Player', 'G', 'Tm'], axis=1)

        return merged_df
    


    """
    
    Function to perform preprocessing steps for WR data

    Input: year
    Output: Merged and cleaned advanced data set
    
    """
    

    def prepare_WR(self, year):

        # First, lets get our normal data
        WR_normal = self.read_new(year, "WR")
        
        # Next, lets clean the dataset:
        WR_cleaned = self.clean_WR(WR_normal)

        # Lets now pull in our advanced dataset
        advanced = self.get_advanced_WR(year)

        # We now need to merge the two frames together
        # We will merge by the columns 'Player' and 'Tm'
        merge_cols = ['Player', 'Tm']
        merged_df = pd.merge(WR_cleaned, advanced, on=merge_cols, how='left')

        # We want to make per-game stats instead of normal aggregate
        # Therefore, lets divide all aggregate columns by total games played
        columns_to_convert = ['REC', 'TGT', 'Receiving_Yds', '20+', 'Receiving_Td', 'ATT', 
                              'Rushing_Yds', 'Rushing_Td', 'YBC', 'AIR', 'YAC', 
                              'YACON', 'BRKTKL', 'CATCHABLE', 'DROP', 'RZ TGT', '10+ YDS', '30+ YDS', 
                              '40+ YDS', '50+ YDS']
        
        # Use for loop to iterate through each agg column
        for col in columns_to_convert:
            merged_df[col] = merged_df[col] / merged_df['G']

        # Also, we do not want to include players who only appeared in a few games
        # This could skew our dataset, so lets remove them
        merged_df = merged_df[merged_df['G'] > 12]

        # Finally, lets remove the names of the QB's and their total number of games
        merged_df = merged_df.drop(['Player', 'G', 'Tm'], axis=1)
        
        # Lastly, lets impute the na values as the mean of the columns:

        merged_df['% TM'] = merged_df['% TM'].str.replace('%', '')
        merged_df['% TM'] = merged_df['% TM'].astype(float)

        numeric_cols = merged_df.select_dtypes(include=['float64', 'int64']).columns
        merged_df[numeric_cols] = merged_df[numeric_cols].fillna(merged_df[numeric_cols].mean())
        return merged_df
    

    """
    
    Function to perform preprocessing steps for RB data

    Input: year
    Output: Merged and cleaned advanced data set
    
    """
    


    def prepare_RB(self, year):

        # First, lets get our normal data
        RB_normal = self.read_new(year, "RB")
        
        # Next, lets clean the dataset:
        RB_cleaned = self.clean_RB(RB_normal)

        # Lets now pull in our advanced dataset
        advanced = self.get_advanced_RB(year)

        # We now need to merge the two frames together
        # We will merge by the columns 'Player' and 'Tm'
        merge_cols = ['Player', 'Tm']
        merged_df = pd.merge(RB_cleaned, advanced, on=merge_cols, how='left')

        # We want to make per-game stats instead of normal aggregate
        # Therefore, lets divide all aggregate columns by total games played
        columns_to_convert = ['ATT', 'Rushing_Yds', 'Rushing_Td', '20+', 'REC', 'TGT', 
                              'Receiving_Yds', 'Receiving_Td', 'YBCON', 'YACON', 'BRKTKL', 
                              'TK LOSS', 'TK LOSS YDS', '50+ YDS', '10+ YDS', 
                              '30+ YDS', '40+ YDS', 'RZ TGT', 
                              'YACON.1']

        # Use for loop to iterate through each agg column
        for col in columns_to_convert:
            merged_df[col] = merged_df[col] / merged_df['G']

        # Also, we do not want to include players who only appeared in a few games
        # This could skew our dataset, so lets remove them
        merged_df = merged_df[merged_df['G'] > 9]

        # Remove the names of the RB's and their total number of games
        merged_df = merged_df.drop(['Player', 'G', 'Tm'], axis=1)

        # Lastly, lets impute the na values as the mean of the columns:
        numeric_cols = merged_df.select_dtypes(include=['float64', 'int64']).columns
        merged_df[numeric_cols] = merged_df[numeric_cols].fillna(merged_df[numeric_cols].mean())
        
        return merged_df
    

    """
    
    Function to clean tight end data
    
    Input: TE dataset
    Output: Cleaned dataset 
    
    """

    def clean_TE(self, df):

        columns_to_drop = ['ROST', 'FPTS', 'Rank', 'FL']
        # Drop unneeded columns
        df = df.drop(columns_to_drop, axis=1)

        # Rename duplicate columns
        updated_columns = {'YDS.1': 'Rushing_Yds', 'YDS': 'Receiving_Yds', 
                            'TD.1': 'Rushing_Td', 'TD': 'Receiving_Td'}
        
        df = df.rename(columns=updated_columns)
        return df



    """
    
    Function to clean wide receiver data
    
    Input: WR dataset
    Output: Cleaned dataset 
    
    """

    def clean_WR(self, df):

        columns_to_drop = ['ROST', 'FPTS', 'Rank', 'FL']
        # Drop unneeded columns
        df = df.drop(columns_to_drop, axis=1)

        # Rename duplicate columns
        updated_columns = {'YDS': 'Receiving_Yds', 'YDS.1': 'Rushing_Yds', 
                            'TD.1': 'Rushing_Td', 'TD': 'Receiving_Td'}
        
        df = df.rename(columns=updated_columns)
        return df




    """
    
    Function to clean running back data
    
    Input: RB dataset
    Output: Cleaned dataset 
    
    """

    def clean_RB(self, df):

        columns_to_drop = ['ROST', 'FPTS', 'Rank', 'FL']
        # Drop unneeded columns
        df = df.drop(columns_to_drop, axis=1)

        # Rename duplicate columns
        updated_columns = {'YDS': 'Rushing_Yds', 'YDS.1': 'Receiving_Yds', 
                            'TD': 'Rushing_Td', 'TD.1': 'Receiving_Td'}
        
        df = df.rename(columns=updated_columns)
        return df
    


    """
    
    Web scrape new advanced data for TE

    Input: year, pos
    Output: advanced dataset with no duplicates
    
    """

    def get_advanced_TE(self, year):

        url = f"https://www.fantasypros.com/nfl/advanced-stats-te.php?year={year}"

        response = requests.get(url)
        html = response.content

        # Make df
        df = pd.read_html(html, header=1)[0]

        # Clean name and team data
        df.insert(1, 'Tm', df['Player'].str.rsplit(n=1).str[-1].str.slice(1, -1))
        df['Player'] = df['Player'].str.rsplit(n=1).str[0]        
        
        dup_columns = ['LNG', 'YDS', 'Y/R', '20+ YDS' , 'G', 'TGT', 'REC', 'Rank']
        
        df = df.drop(dup_columns, axis=1)
        return df


    """
    
    Web scrape new advanced data for RB

    Input: year, pos
    Output: advanced dataset with no duplicates
    
    """

    def get_advanced_RB(self, year):

        url = f"https://www.fantasypros.com/nfl/advanced-stats-rb.php?year={year}"

        response = requests.get(url)
        html = response.content

        # Make df
        df = pd.read_html(html, header=1)[0]

        # Clean name and team data
        df.insert(1, 'Tm', df['Player'].str.rsplit(n=1).str[-1].str.slice(1, -1))
        df['Player'] = df['Player'].str.rsplit(n=1).str[0]        
        
        dup_columns = ['ATT', 'YDS', '20+ YDS' , 'Y/ATT', 'G', 'TGT', 'LNG', 'REC', 'Rank']
        
        df = df.drop(dup_columns, axis=1)
        return df
    

    """
    
    Web scrape new advanced data for WR

    Input: year, pos
    Output: advanced dataset with no duplicates
    
    """

    def get_advanced_WR(self, year):

        url = f"https://www.fantasypros.com/nfl/advanced-stats-wr.php?year={year}"

        response = requests.get(url)
        html = response.content

        # Make df
        df = pd.read_html(html, header=1)[0]

        # Clean name and team data
        df.insert(1, 'Tm', df['Player'].str.rsplit(n=1).str[-1].str.slice(1, -1))
        df['Player'] = df['Player'].str.rsplit(n=1).str[0]        
        
        dup_columns = ['LNG', 'YDS', 'Y/R', '20+ YDS' , 'G', 'TGT', 'REC', 'Rank']
        
        df = df.drop(dup_columns, axis=1)
        return df




    """

    Function to retrieve new data

    Inputs: year, position
    output: positional dataset with y included

    """

    def read_new(self, year, pos):

        # Link takes lowercase positions
        pos = pos.lower()

        url = f"https://www.fantasypros.com/nfl/stats/{pos}.php?year={year}"

        response = requests.get(url)
        html = response.content

        # Make df
        df = pd.read_html(html, header=1)[0]

        # Clean name and team data

        df.insert(1, 'Tm', df['Player'].str.rsplit(n=1).str[-1].str.slice(1, -1))
        df['Player'] = df['Player'].str.rsplit(n=1).str[0]



        # Get y (following year ppg)
        next_year = str(int(year) + 1)
        url = f"https://www.fantasypros.com/nfl/stats/{pos}.php?year={next_year}"

        response = requests.get(url)
        html = response.content

        # Make df
        y = pd.read_html(html, header=1)[0]

        df['y'] = y['FPTS/G']

        return df




    """
    
    Function to clean quarterback data
    
    Input: QB dataset
    Output: Cleaned dataset 
    
    """


    def clean_QB(self, df):

        columns_to_drop = ['ROST', 'FPTS', 'Rank', 'FL']

        # Drop unneeded columns
        df = df.drop(columns_to_drop, axis=1)

        # Rename duplicate columns
        updated_columns = {'ATT': 'Passing_att', 'YDS': 'Passing_Yds', 
                           'ATT.1': 'Rushing_att', 'YDS.1': 'Rushing_Yds', 
                           'TD': 'Passing_Td', 'TD.1': 'Rushing_Td'}

        df = df.rename(columns=updated_columns)
        return df




    """
    
    Web scrape new advanced data for QB

    Input: year, pos
    Output: advanced dataset with no duplicates
    
    """

    def get_advanced_QB(self, year):


        url = f"https://www.fantasypros.com/nfl/advanced-stats-qb.php?year={year}"

        response = requests.get(url)
        html = response.content

        # Make df
        df = pd.read_html(html, header=1)[0]

        # Clean name and team data

        df.insert(1, 'Tm', df['Player'].str.rsplit(n=1).str[-1].str.slice(1, -1))
        df['Player'] = df['Player'].str.rsplit(n=1).str[0]

        dup_columns = ['ATT', 'YDS', 'SK', 'CMP', 'PCT', 'Y/A', 'G', 'AIR', 'Rank']
        df = df.drop(dup_columns, axis=1)

        return df



    
    




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


    

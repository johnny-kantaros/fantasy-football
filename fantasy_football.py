import pandas

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

        # merged_df.drop("Last Name")

        return merged_df
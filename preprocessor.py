import pandas as pd

def preprocess(df,region_df):
    # filtering for summer olympics
    df = df[df['Season'] == 'Summer']
    # merge with region_df
    df = df.merge(region_df, on='NOC', how='left')
    # dropping duplicates
    df.drop_duplicates(inplace=True)
    # one hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df

























# 1
# def save_to_json(df, filename):
#     df.to_json(filename, orient='records', lines=True)
#
#
#
# def save_to_csv(df, filename):
#     df.to_csv(filename, index=False)
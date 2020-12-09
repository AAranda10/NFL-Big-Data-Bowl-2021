import pandas as pd
import acquire_plays_data
import re

def prep_plays_data():
    '''
    This function retrieves calls the function that acquires 
    the plays csv and prepares it for an mvp
    '''
    # acquire the plays csv and save it as a dataframe
    df = acquire_plays_data.get_plays_data()
    # keep only the useful columns for mvp
    df = df[['playDescription', 'quarter', 'down', 'yardsToGo', 'possessionTeam',
             'offenseFormation', 'personnelO', 'defendersInTheBox', 'numberOfPassRushers', 
             'personnelD', 'typeDropback', 'gameClock', 'absoluteYardlineNumber', 'epa', 'playType']]
    # filter out any data that is not a pass play
    df = df[df.playType == 'play_type_pass']
    # create a new column that extracts 
    # "(number) RB, (number) TE, (number) WR"
    # and saves it as a temporary column
    df['tempO'] = df.personnelO.str.extract(r'(\d RB, \d TE, \d WR)')
    # create a new column that extracts 
    # "(number) DL, (number) LB, (number) DB"
    # and saves it as a temporary column
    df['tempD'] = df.personnelD.str.extract(r'(\d DL, \d LB, \d DB)')
    # keeps the rows that contain only the string in tempO column
    df = df[df.personnelO == df.tempO]
    # keep the rows that contain only the string in tempD column
    df = df[df.personnelD == df.tempD]
    # create a temporary dataframe containing the personnelO 
    # column split by a comma and space
    temp = df.personnelO.str.split(', ', expand = True)
    # create a new column with the number of RB on the field
    df['RB'] = temp[0].str.replace(r' RB', '')
    # create a new column with the number of TE on the field
    df['TE'] = temp[1].str.replace(r' TE', '')
    # create a new column with the number of WR on the field
    df['WR'] = temp[2].str.replace(r' WR', '')
    # create a temporary dataframe containing the personnelD 
    # column split by a comma and space
    temp = df.tempD.str.split(', ', expand = True)
    # create a new column with the number of DL on the field
    df['DL'] = temp[0].str.replace(r' DL', '')
    # create a new column with the number of LB on the field
    df['LB'] = temp[1].str.replace(r' LB', '')
    # create a new column with the number of DB on the field
    df['DB'] = temp[2].str.replace(r' DB', '')
    # drop temporary columns and playType
    df = df.drop(columns = {'personnelO', 'personnelD', 'tempO', 'tempD', 'playType'})
    # reorder the index and drop the old index
    df = df.reset_index(drop=True)
    return df

print("Prep.py Loaded Successfully")
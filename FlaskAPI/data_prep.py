import numpy as np
import pandas as pd

def is_Poacher(row):
    if row['att_work_rate_High'] == 0:
        if (row['heading']>=75)&(row['finishing']>=85):
            return 1
        else:
            return 0
    else:
        return 0

def is_Speedster(row):
    if (row['sprint_speed'] + row['acceleration']) >= 180:
        return 1
    else:
        return 0

def is_Aerial_Threat(row):
    if row['height'] < 188:
        return 0
    elif (row['height'] >=188)&(row['height'] <= 194):
        if (row['heading'] >=90)&((row['strength'] >= 85)|(row['jumping'] >= 85)):
            return 1
        else:
            return 0
    elif row['height'] > 194:
        if row['heading'] >= 75:
            return 1
        else:
            return 0
    else:
        return 0

def is_Dribbler(row):
    if (row['dribbling'] >= 86)&(row['skill_moves'] == 5):
        return 1
    elif (row['dribbling']>=86)&(row['balance']>=75):
        return 1
    else:
        return 0

def is_Playmaker(row):
    if row[['CM','CDM','CAM']].sum() >= 1:
        if (row['vision'] >= 86)&(row['short_pass'] >= 86)&(row['long_pass'] >= 73):
            return 1
        else:
            return 0
    else:
        return 0

def is_Engine(row):
    if (row['att_work_rate_High'] == 1)&(row['def_work_rate_High'] == 1)&(row['stamina'] >= 86):
        return 1
    else:
        return 0

def is_Distance_Shooter(row):
    if (row['long_shot'] + row['shot_power']) >= 174:
        return 1
    else:
        return 0

def is_Crosser(row):
    if (row['crossing'] >= 86)&(row['curve'] >= 80):
        return 1
    else:
        return 0

def is_FK_Specialist(row):
    if (row['fk_acc'] >=86)&((row['curve'] >= 85)|(row['shot_power'] >= 85)):
        return 1
    else:
        return 0

def is_Tackling(row):
    if (row['stand_tackle'] >= 86)&(row['side_tackle'] >= 85):
        return 1
    else:
        return 0

def is_Tactician(row):
    if (row['interceptions'] >= 86)&(row['reactions'] >= 80):
        return 1
    else:
        return 0

def is_Acrobat(row):
    if (row['agility'] >= 90):
        return 1
    elif (row['agility'] >= 86)&(row['reactions'] >= 80):
        return 1
    else:
        return 0

def is_Strength(row):
    if (row['weight'] <= 82)&(row['strength'] >= 90):
        return 1
    elif (row['weight'] > 82)&(row['strength'] >= 86):
        return 1
    else:
        return 0

def is_Clinical_Finisher(row):
    if (row['finishing'] >= 86)&(row['long_shot'] >= 80):
        return 1
    else:
        return 0

def is_Complete_Defender(row):
    if (row['Tactician'] == 1)&(row['Tackling'] == 1):
        if row[['Strength','Acrobat','Aerial_Threat']].sum() >= 1:
            return 1
        else:
            return 0
    else:
        return 0

def is_Complete_Midfielder(row):
    if (row['Playmaker'] == 1):
        if row[['Distance_Shooter', 'Engine', 'Dribbler', 'FK_Specialist', 'Tackling', 'Crosser', 'Clinical_Finisher']].sum() >= 2:
            return 1
        else:
            return 0
    else:
        return 0

def is_Complete_Forward(row):
    important = ['Clinical_Finisher','Poacher']
    standard = ['Aerial_Threat', 'Speedster', 'Dribbler', 'Strength']
    if row[important].sum() >= 1:
        if row[standard].sum() >= 2:
            return 1
    elif row[important].sum() >= 2:
        if row[standard].sum() >= 1:
            return 1

    return 0

def prepare_data_for_prediction(input_list):
    ball_skills = ['ball_control','dribbling']
    defence = ['marking','side_tackle','stand_tackle']
    mental = ['aggression','reactions','att_position','interceptions','vision','composure']
    passing = ['crossing', 'short_pass', 'long_pass']
    physical = ['acceleration', 'stamina', 'strength', 'balance', 'sprint_speed', 'agility', 'jumping']
    shooting = ['heading', 'shot_power', 'finishing', 'long_shot', 'curve', 'fk_acc', 'penalties', 'volleys']
    goalkeeper = ['gk_positioning', 'gk_diving', 'gk_handling', 'gk_kicking', 'gk_reflexes']

    attributes = ball_skills + defence + mental + passing + physical + shooting + goalkeeper

    input_columns = ['overall', 'height', 'weight', 'age', 'weak_foot', 'skill_moves',\
                  'preferred_foot_Left', 'preferred_foot_Right', 'att_work_rate_High', 'att_work_rate_Low',\
                  'att_work_rate_Medium', 'def_work_rate_High', 'def_work_rate_Low', 'def_work_rate_Medium',\
                 'RW', 'ST', 'CF', 'LW', 'CAM', 'CB', 'GK', 'CM', 'CDM', 'LM', 'RB', 'RM', 'LB', 'LWB', 'RWB'] + attributes

    X = np.array(input_list).reshape(1,-1)
    X_df = pd.DataFrame(data=X,columns=input_columns)

    # Features given by the mean of each block of attributes
    X_df['ball_skills'] = X_df[ball_skills].mean(axis=1)
    X_df['defence'] = X_df[defence].mean(axis=1)
    X_df['mental'] =X_df[mental].mean(axis=1)
    X_df['passing'] = X_df[passing].mean(axis=1)
    X_df['physical'] = X_df[physical].mean(axis=1)
    X_df['shooting'] = X_df[shooting].mean(axis=1)
    X_df['goalkeeper'] = X_df[goalkeeper].mean(axis=1)

    specialities = ['Dribbler','Distance_Shooter','Crosser','FK_Specialist','Acrobat','Clinical_Finisher','Speedster','Playmaker','Strength',\
               'Complete_Midfielder','Complete_Forward','Complete_Defender','Tackling','Tactician','Poacher','Aerial_Threat','Engine']

    X_df['Dribbler'] = X_df.apply(is_Dribbler,axis=1)
    X_df['Distance_Shooter'] = X_df.apply(is_Distance_Shooter,axis=1)
    X_df['Crosser'] = X_df.apply(is_Crosser,axis=1)
    X_df['FK_Specialist'] = X_df.apply(is_FK_Specialist,axis=1)
    X_df['Acrobat'] = X_df.apply(is_Acrobat,axis=1)
    X_df['Clinical_Finisher'] = X_df.apply(is_Clinical_Finisher,axis=1)
    X_df['Speedster'] = X_df.apply(is_Speedster,axis=1)
    X_df['Playmaker'] = X_df.apply(is_Playmaker,axis=1)
    X_df['Strength'] = X_df.apply(is_Strength,axis=1)
    X_df['Tackling'] = X_df.apply(is_Tackling,axis=1)
    X_df['Tactician'] = X_df.apply(is_Tactician,axis=1)
    X_df['Poacher'] = X_df.apply(is_Poacher,axis=1)
    X_df['Aerial_Threat'] = X_df.apply(is_Aerial_Threat,axis=1)
    X_df['Engine'] = X_df.apply(is_Engine,axis=1)
    X_df['Complete_Defender'] = X_df.apply(is_Complete_Defender,axis=1)
    X_df['Complete_Midfielder'] = X_df.apply(is_Complete_Midfielder,axis=1)
    X_df['Complete_Forward'] = X_df.apply(is_Complete_Forward,axis=1)

    # Body mass index of players
    X_df['bmi'] = X_df['weight']/(X_df['height']/100)**2

    # Number of specialities
    X_df['number_specialities'] = X_df[specialities].sum(axis=1)

    # Number of positions that the player can play
    positions = ['RW', 'ST', 'CF', 'LW', 'CAM', 'CB', 'CM', 'CDM', 'LM', 'RB', 'RM', 'LB', 'LWB', 'RWB']
    X_df['number_preferred_positions'] = X_df[positions].sum(axis=1)

    # Number of attributes above a certain threshold
    X_df['number_attributes_greater_95'] = (X_df[attributes]>=95).sum(axis=1)
    X_df['number_attributes_greater_90'] = (X_df[attributes]>=90).sum(axis=1)
    X_df['number_attributes_greater_85'] = (X_df[attributes]>=85).sum(axis=1)
    X_df['number_attributes_greater_80'] = (X_df[attributes]>=80).sum(axis=1)
    X_df['number_attributes_greater_75'] = (X_df[attributes]>=75).sum(axis=1)
    X_df['number_attributes_greater_70'] = (X_df[attributes]>=70).sum(axis=1)

    # Number of attributes within a certain range
    X_df['number_attributes_greater_90_less_95'] = X_df['number_attributes_greater_90'] - X_df['number_attributes_greater_95']
    X_df['number_attributes_greater_85_less_90'] = X_df['number_attributes_greater_85'] - X_df['number_attributes_greater_90']
    X_df['number_attributes_greater_80_less_85'] = X_df['number_attributes_greater_80'] - X_df['number_attributes_greater_85']
    X_df['number_attributes_greater_75_less_80'] = X_df['number_attributes_greater_75'] - X_df['number_attributes_greater_80']
    X_df['number_attributes_greater_70_less_75'] = X_df['number_attributes_greater_70'] - X_df['number_attributes_greater_75']

    return X_df

def get_features_predictions_positions(X_df):
    gk_cols = ['GK','gk_positioning', 'gk_diving', 'gk_handling', 'gk_kicking', 'gk_reflexes', 'goalkeeper']
    positions_cols = ['RW', 'ST', 'CF', 'LW', 'CAM', 'CB', 'CM', 'CDM', 'LM', 'RB', 'RM', 'LB', 'LWB', 'RWB']
    cols_to_drop = ['age','number_preferred_positions'] + gk_cols + positions_cols

    X_df = X_df.drop(columns=cols_to_drop)

    # Feature engineering - subtracting overall from attribute values
    ball_skills = ['ball_control','dribbling']
    defence = ['marking','side_tackle','stand_tackle']
    mental = ['aggression','reactions','att_position','interceptions','vision','composure']
    passing = ['crossing', 'short_pass', 'long_pass']
    physical = ['acceleration', 'stamina', 'strength', 'balance', 'sprint_speed', 'agility', 'jumping']
    shooting = ['heading', 'shot_power', 'finishing', 'long_shot', 'curve', 'fk_acc', 'penalties', 'volleys']
    goalkeeper = ['gk_positioning', 'gk_diving', 'gk_handling', 'gk_kicking', 'gk_reflexes']

    attributes = ball_skills + defence + mental + passing + physical + shooting

    for attribute in attributes:
        X_df[attribute+'_minus_ovr'] = X_df[attribute] - X_df['overall']

    X_df['ball_skills_minus_ovr'] = X_df['ball_skills'] - X_df['overall']
    X_df['defence_minus_ovr'] = X_df['defence'] - X_df['overall']
    X_df['mental_minus_ovr'] = X_df['mental'] - X_df['overall']
    X_df['passing_minus_ovr'] = X_df['passing'] - X_df['overall']
    X_df['physical_minus_ovr'] = X_df['physical'] - X_df['overall']
    X_df['shooting_minus_ovr'] = X_df['shooting'] - X_df['overall']

    return X_df

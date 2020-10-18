import streamlit as st
import numpy as np
import pandas as pd
import pickle
from data_prep_and_models import *

st.title('FIFA career mode app')
st.write('This app was built to help FIFA career mode players negotiate wages, and know what positions they can use their players besides the ones suggested by the game. Just give us your player features and click the buttom on the bottom of the page to get your answer immediately.')

prediction_options = ('A wage for contract negotiations','His best positions')
prediction_option = st.sidebar.selectbox('What do you want to know about your player?', prediction_options)

st.sidebar.markdown('#### Inform your player\'s main features below')

overall = st.sidebar.slider('Overall',1,99,50)
preferred_foot = st.sidebar.selectbox("Preferred foot", ('Right', 'Left'))

col1, col2, col3 = st.sidebar.beta_columns(3)
def att_work_rate_encoder(x):
    if x == (1,0,0):
        name = 'Low'
    elif x == (0,1,0):
        name = 'Medium'
    else:
        name = 'High'
    return name
with col1:
    age = st.slider('Age',15,40,25)
    att_work_rate_Low, att_work_rate_Medium, att_work_rate_High = st.radio("Att. work rate", ((1,0,0), (0,1,0), (0,0,1)),format_func=att_work_rate_encoder)
with col2:
    height = st.slider('Height (cm)',140,220,170)
    st.markdown('      /       ')
with col3:
    weight = st.slider('Weight (kg)',40,100,70)
    def_work_rate_Low, def_work_rate_Medium, def_work_rate_High = st.radio("Def. work rate", ((1,0,0), (0,1,0), (0,0,1)),format_func=att_work_rate_encoder)

col1, col2 = st.sidebar.beta_columns(2)
with col1:
    weak_foot = st.slider('Weak foot (# of stars)',1,5,3)
with col2:
    skill_moves = st.slider('Skill moves (# of stars)',1,5,3)

if prediction_option == prediction_options[0]:
    st.sidebar.write('Preferred positions')
    col1, col2, col3 = st.sidebar.beta_columns(3)

    with col1:
        GK = int(st.checkbox('GK'))
        CB = int(st.checkbox('CB'))
        CDM = int(st.checkbox('CDM'))
        CM = int(st.checkbox('CM'))
        CAM = int(st.checkbox('CAM'))
    with col2:
        LB = int(st.checkbox('LB'))
        LWB = int(st.checkbox('LWB'))
        LM = int(st.checkbox('LM'))
        LW = int(st.checkbox('LW'))
        CF = int(st.checkbox('CF'))
    with col3:
        RB = int(st.checkbox('RB'))
        RWB = int(st.checkbox('RWB'))
        RM = int(st.checkbox('RM'))
        RW = int(st.checkbox('RW'))
        ST = int(st.checkbox('ST'))

st.markdown('### Adjust your player\'s attributes below')

with st.beta_expander('Physical'):
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        acceleration = st.slider('Acceleration',1,99,50)
        stamina = st.slider('Stamina',1,99,50)
        strength = st.slider('Strength',1,99,50)
    with col2:
        balance = st.slider('Balance',1,99,50)
        sprint_speed = st.slider('Sprint speed',1,99,50)
    with col3:
        agility = st.slider('Agility',1,99,50)
        jumping = st.slider('Jumping',1,99,50)

with st.beta_expander('Ball skills'):
    col1, col2 = st.beta_columns(2)
    with col1:
        ball_control = st.slider('Ball control',1,99,50)
    with col2:
        dribbling = st.slider('Dribbling',1,99,50)

with st.beta_expander('Passing'):
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        crossing = st.slider('Crossing',1,99,50)
    with col2:
        short_pass = st.slider('Short Pass',1,99,50)
    with col3:
        long_pass = st.slider('Long pass',1,99,50)

with st.beta_expander('Shooting'):
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        heading = st.slider('Heading',1,99,50)
        shot_power = st.slider('Shot power',1,99,50)
        finishing = st.slider('Finishing',1,99,50)
    with col2:
        long_shot = st.slider('Long shots',1,99,50)
        curve = st.slider('Curve',1,99,50)
        fk_acc = st.slider('Free kick accuracy',1,99,50)
    with col3:
        penalties = st.slider('Penalties',1,99,50)
        volleys = st.slider('Volleys',1,99,50)

with st.beta_expander('Defence'):
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        marking = st.slider('Marking',1,99,50)
    with col2:
        side_tackle = st.slider('Slide tackle',1,99,50)
    with col3:
        stand_tackle = st.slider('Stand tackle',1,99,50)

with st.beta_expander('Mental'):
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        aggression = st.slider('Aggression',1,99,50)
        reactions = st.slider('Reactions',1,99,50)
    with col2:
        att_position = st.slider('Att. positioning',1,99,50)
        interceptions = st.slider('Interceptions',1,99,50)
    with col3:
        vision = st.slider('Vision',1,99,50)
        composure = st.slider('Composure',1,99,50)

if prediction_option == prediction_options[0]:
    with st.beta_expander('Goalkeeper'):
        col1, col2, col3 = st.beta_columns(3)
        with col1:
            gk_positioning = st.slider('Positioning',1,99,50)
            gk_diving = st.slider('Diving',1,99,50)
        with col2:
            gk_handling = st.slider('Handling',1,99,50)
            gk_kicking = st.slider('Kicking',1,99,50)
        with col3:
            gk_reflexes = st.slider('Reflexes',1,99,50)

st.write("")
if prediction_option == prediction_options[0]:
    button_name = 'Get wage'
else:
    button_name = 'Get positions'

if st.button(button_name):

    if preferred_foot == 'Right':
        preferred_foot_Left = 0
        preferred_foot_Right = 1
    else:
        preferred_foot_Left = 1
        preferred_foot_Right = 0

    ball_skills = [ball_control,dribbling]
    defence = [marking,side_tackle,stand_tackle]
    mental = [aggression,reactions,att_position,interceptions,vision,composure]
    passing = [crossing, short_pass, long_pass]
    physical = [acceleration, stamina, strength, balance, sprint_speed, agility, jumping]
    shooting = [heading, shot_power, finishing, long_shot, curve, fk_acc, penalties, volleys]

    if prediction_option == prediction_options[0]:
        goalkeeper = [gk_positioning, gk_diving, gk_handling, gk_kicking, gk_reflexes]
        attributes = ball_skills + defence + mental + passing + physical + shooting + goalkeeper

        input_list = [overall, height, weight, age, weak_foot, skill_moves,\
                     preferred_foot_Left, preferred_foot_Right, att_work_rate_High, att_work_rate_Low,\
                     att_work_rate_Medium, def_work_rate_High, def_work_rate_Low, def_work_rate_Medium,\
                     RW, ST, CF, LW, CAM, CB, GK, CM, CDM, LM, RB, RM, LB, LWB, RWB] + attributes

        X_df = prepare_data_wage(input_list)
        # load model
        model = load_model_logwage()
        columns = model.get_booster().feature_names
        X_df = X_df[columns]
        wage_prediction = np.expm1(model.predict(X_df))[0]
        # Just giving a more round value to the user
        wage_prediction = int(round(wage_prediction,2 - len(str(int(wage_prediction)))))
        st.markdown('#### A reasonable wage for this player is: '+str(wage_prediction)+' €')

    if prediction_option == prediction_options[1]:
        attributes = ball_skills + defence + mental + passing + physical + shooting

        input_list = [overall, height, weight, weak_foot, skill_moves,preferred_foot_Left,\
                     preferred_foot_Right, att_work_rate_High, att_work_rate_Low, att_work_rate_Medium,\
                     def_work_rate_High, def_work_rate_Low, def_work_rate_Medium] + attributes

        X_df = prepare_data_positions(input_list)
        # load model
        model = load_model_positions()
        probas = model.predict_proba(X_df)
        predicted_probas = []
        for i in range(14):
            predicted_probas = predicted_probas + [int(round(probas[i][0,1],2)*100)]

        positions = ['RW', 'ST', 'CF', 'LW', 'CAM', 'CB', 'CM', 'CDM', 'LM', 'RB', 'RM', 'LB', 'LWB', 'RWB']
        pos_preds_series = pd.Series(data=predicted_probas,index=positions).sort_values(ascending=False)
        indexes = pos_preds_series[pos_preds_series>25].index
        positions_prediction = ''

        for i in range(len(indexes)):
            positions_prediction = positions_prediction + indexes[i] +', '

        positions_prediction = positions_prediction[:-2]
        st.markdown('#### The best positions to use this player are, in order: ' +positions_prediction)

st.write("")
st.write("")
st.markdown('<center style="font-size:16px">The source code for this app (and some players data analysis) can be found on <a href= "https://github.com/yurimuniz7/FIFA-20-players-analysis-and-predictions">Github</a></center>',True)

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

from sklearn.metrics import accuracy_score, auc, f1_score, precision_score, recall_score
st.set_option('deprecation.showfileUploaderEncoding', False)

st.title("Leaderboard")

username = st.text_input("Username", value = "guest", max_chars= 20,)
username = username.replace(",","")
st.text(f"Hi {username} !!!")

# Check if master data has been registered:
master_files = os.listdir('master')
if ("df_master.csv" not in master_files) | ("cfg_master.json" not in master_files):
    st.text("Admin please insert master data")
elif (os.stat("master/df_master.csv").st_size == 0) | (os.stat("master/cfg_master.json").st_size == 0):
    st.text("Master data should not empty")
else:
    # Load Master
    df_master = pd.read_csv('master/df_master.csv')
    with open('master/cfg_master.json') as json_file:
        cfg_master = json.load(json_file)

    competition_type, metric_type= cfg_master['competition_type'], cfg_master['metric_type']
    index_col, target_col = cfg_master['index_col'], cfg_master['target_col']

    st.text(f"Competition Type: {competition_type}")
    st.text(f"Metric: {metric_type}")
    st.text(f"index  column name : {index_col}")
    st.text(f"target column name: {target_col}")

    # set scorer as metric type
    scorer_dict = {"Accuracy": accuracy_score, "Precision": precision_score, "Recall" : recall_score, "Auc" : auc, 
                    "F1": f1_score}
    scorer = scorer_dict[metric_type]

    uploaded_file = st.file_uploader("Upload Submission CSV File",type='csv')
    if st.button("SUBMIT"):
        if uploaded_file is None:
            st.text("UPLOAD FIRST")
        else:
            # save submission
            df_submission = pd.read_csv(uploaded_file)
            datetime_now = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_submission = f"submission/sub_{username}__{datetime_now}.csv"
            df_submission.to_csv(filename_submission, index = False)
            # calculate score
            df = df_master.merge(df_submission, how = 'left', on = index_col)
            true_label = df[target_col + "_x"]
            pred_label = df[target_col + "_y"]
            score = scorer(true_label, pred_label)
            score = round(score,5)
            st.text(f"YOUR {metric_type}: {score}")
            # save score
            with open("leaderboard.csv", "a+") as leaderboard_csv:
                leaderboard_csv.write(f"{username},{score},{datetime_now}\n")

# Showing Leaderboard 
if os.stat("leaderboard.csv").st_size == 0:
    st.text("NO SUBMISSION YET")
else:
    df_leaderboard = pd.read_csv('leaderboard.csv', header = None)
    df_leaderboard
    df_leaderboard.columns = ['Username', 'Score', 'Submission Time']
    df_leaderboard['counter'] = 1
    df_leaderboard = df_leaderboard.groupby('Username').agg({"Score": "max",
                                                            "Submission Time": "max", 
                                                            "counter": "count"})
    df_leaderboard = df_leaderboard.reset_index()                                                    
    df_leaderboard.columns = ['Username','Score', 'Last Submission', 'Total submission']
    df_leaderboard

# To register master data
if username == 'admin': # CHANGE HERE AS YOU WANT
    change_master_key = st.checkbox('Change Master Key')

    if change_master_key:
        competition_type = ["Binary Classification", "Multi Class Classification", "Regression",]
        choosen_competition_type = st.selectbox("Select Competition Type",competition_type)

        metric_type_dict = {"Binary Classification": ["Accuracy", "Precision", "Recall", "Auc", "F1"], 
                            "Multi Class Classification" : ["Accuracy"], 
                            "Regression" : ["MAE", "MSE", "RMSE"]}
        metric_type = metric_type_dict[choosen_competition_type]

        choosen_metric_type = st.selectbox("Select Metric Type",metric_type)

        uploaded_file_master = st.file_uploader("Upload Master CSV File",type='csv')
        if uploaded_file_master is not None:
            df_master_register = pd.read_csv(uploaded_file_master)
            columns_master = list(df_master_register.columns)

            choosen_col_index  = st.selectbox("Select Index Column",columns_master)
            choosen_col_target = st.selectbox("Select Target Column",[col for col in columns_master if col != choosen_col_index])

            if st.checkbox('Show Master Data'):
                st.text(f"TOTAL ROW: {len(df_master_register)}")
                
                df_master_register.loc[:99, [choosen_col_index, choosen_col_target]]

            if st.button("CHANGE"):
                if df_master_register[choosen_col_index].value_counts().max() == 1:
                    filename_master = "master/df_master.csv"
                    filename_master_cfg = "master/cfg_master.json"

                    df_master_register[[choosen_col_index, choosen_col_target]].to_csv(filename_master, index = False)
                    st.text(f"Master data saved into {filename_master}")

                    cfg_master_register = {
                        "competition_type" : choosen_competition_type,
                        "metric_type" : choosen_metric_type,
                        "index_col" : choosen_col_index,
                        "target_col" : choosen_col_target,
                    }
                    with open(filename_master_cfg, 'w') as outfile:
                        json.dump(cfg_master_register, outfile)
                    st.text(f"Master config saved into {filename_master_cfg}")

                    # Change current master
                    cfg_master = cfg_master_register.copy()
                    df_master = df_master_register.copy()
                    
                else:
                    st.text("Index columns is not unique, cannot process")
    
# streamlit-leaderboard
Make simple and competition leaderboard using streamlit in one file of code!

# Why this is "simple" ?
1. Insert name, upload file, see the result
2. For admin of competition do not need to change the code
3. Does not use a database, just store data inside the text file
4. No password what so ever, even for submit the result, just put username

# How to Use as User
1. Go to the website (usually http://localhost:8501/)
2. insert username
3. Upload and submit
4. See your score and position in leaderboard

# How to Use as Admin
1. Install required packages
2. Run `streamlit run leaderboard.py` 

# Setting Master Data
1. Change username into `admin` (or what ever you desire, can change it inside `leaderboard`)
2. Check the "checkbox" `Change Master Key`
3. Select competition type and metric type
4. Upload `csv` file for master data
5. Select index column and target column name
6. click `CHANGE` button

# TODO: 
* Seperate public and private leaderboard
* Make `last submission` columns become relative to current time
* `Multiclass Classification` case
* `Regression` case

# Udates
* 2020-08-20 : already viable with binary competition data

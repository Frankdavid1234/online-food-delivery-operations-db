To use the food delivery operations DB, we must first enter the w11 file 
Step 1: Set up 
At the beginning of every page, there will be a setup section where credentials must be changed to the owner's database and the Instant Client directory 
Step 2: Run the preprocess.py
Preprocess.py will take the .xlsx file and arrange all the data into its respective CSV files.
Step 3: run_schema.py
This file uses create_db.sql to set up all the necessary tables, keys, and constraints for our database.
Step 4: Bulkload.py
This file will take all the information from the CSV files and put it into the database.
Step 5: App.py 
The final file is App.py; unlike the others, this one can not be run normally since it uses Streamlit. The command to run it is the following 
python -m streamlit run app.py

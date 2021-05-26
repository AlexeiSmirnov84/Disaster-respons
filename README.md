# Disaster Response Pipeline Project

### Introduction
This project includes a web app where an emergency worker can input a new message and get classification results in several categories. The web app also displays visualizations of the data. It can be very useful in emergency.

<img src="https://github.com/AlexeiSmirnov84/Disaster-respons/web_interface.JPG">

### Motivations
In this day and age, disasters appear around the world. Likely new technologies allow alleviating people suffering. I proud to have in my portfolio application that can automatically identify people needs and recommend proper responds. 

Maybe someday it will help to somebody.

### Instructions
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python app/run.py`

3. Go to http://0.0.0.0:3001/

4. Type any message and enter, as output the message will be classified.

### Acknowledgments
This application is free for use. Thanks to Udacity team, who helped me with that.

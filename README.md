**Overview** <br></br>
The Fantasy Football Stat Predictor is an application designed to predict player performance in fantasy football using ML algorithms. The project consists of a PostgreSQL database, 
Backend Flask application, and a React App that work together to provide accurate predictions and a user-friendly interface for fantasy football enthusiasts. Users can search for players
on their team and add them to a team on the app to see their entire team's projected predicted score. This model has a 90.9% overall accuracy score using Mean Squared Error, R^2 Score, and Mean Absolute Error.

<img width="1112" alt="image" src="https://github.com/user-attachments/assets/08aad8af-1a0c-4ea4-9872-82c9d289f4f1">
<img width="1091" alt="image" src="https://github.com/user-attachments/assets/8e2d34f4-d42f-428f-bde3-a9b3881da72c">



**Features** <br></br>
Data Scraping: The application scrapes game logs and box score data from Pro-Football-Reference to gather up-to-date player statistics.  <br></br>
Data Extraction: Extracted statistics are saved into a CSV file to be used with ML algorithms.  <br></br>
Machine Learning: Utilizes scikit-learn to apply ML algorithms, training a model to predict player statistics for their upcoming games.  <br></br>
Database Integration: The predicted statistics are stored in a PostgreSQL database and fantasy PPR and NonPPR scores are calculated.  <br></br>
Backend API: A Flask-based backend server is used to get player statistics from the database.  <br></br>
Frontend Application: A React-based web application displays the player statistics, allows users to add players to their fantasy teams, and calculates the projected total score for the selected players.

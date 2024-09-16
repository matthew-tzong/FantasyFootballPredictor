# FantasyFootballPredictor <br></br>
## Overview <br></br>
The Fantasy Football Stat Predictor is an application designed to scrape game logs for over 1000 games, manipulate the data, and predict player performance in fantasy football using ML algorithms. This is accomplished through a Frontend React App, Backend Flask application, and a PostgreSQL database. This model uses ML algorithms and has a 90.9% overall accuracy score using Mean Squared Error, R^2 Score, and Mean Absolute Error.

<img width="1112" alt="image" src="https://github.com/user-attachments/assets/08aad8af-1a0c-4ea4-9872-82c9d289f4f1">
<img width="1091" alt="image" src="https://github.com/user-attachments/assets/8e2d34f4-d42f-428f-bde3-a9b3881da72c">
In this application, fantasy football enthusiasts are able to find fantasy football predictions for every player through a user-friendly interface. Users can search for players
on their team and add them to a team on the app to see their entire team's predicted total.



### Features <br></br>
- **Data Scraping**: Engineered a comprehensive data scraping of box scores for 1000+ games using Python and BeautifulSoup. The application scrapes game logs and box score data from Pro-Football-Reference to gather up-to-date player statistics
- **Machine Learning**: Created a model to predict player statistics by integrating data scraping with scikit-learn to apply ML algorithms
- **Database Integration**: The predicted statistics are stored in a PostgreSQL database with fantasy PPR and NonPPR scores being calculated
- **Backend**: Dynamic manipulation and presentation of player statistics in the database through a Flask application
- **Frontend**: A user-friendly ReactJS interface that displays the predicted player statistics/scores, allows users to add players to their fantasy teams, and calculates the projected total score for the selected players

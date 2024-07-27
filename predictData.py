import pandas as pd
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from scipy.stats import randint
from sklearn.preprocessing import StandardScaler
import psycopg2
from sqlalchemy import create_engine

# Establish connection to PostgreSQL database
conn = psycopg2.connect(
    dbname="playerpredictions",  
    user="postgres",          
    host="localhost",    
    port="5432"          
)
cur = conn.cursor()

# Load dataframe from csv file
df = pd.read_csv("nfl_games.csv", index_col=0)
# Sort by player and date before resetting index
df = df.sort_values(by=['Player', 'Date'])
df = df.reset_index(drop=True)


# Remove columns that aren't are not features or targets
df= df.drop(['Team', 'Season', 'Date'], axis=1)

#Created lagged columns for each target statistic by shifting values for each player, used to track how prev stats can affect/predict future stats
for col in df.columns:
    if col not in ['Player']:
        df[f'Prev_{col}'] = df.groupby('Player')[col].shift(1)

#Drop rows with missing values due to shifting values
df = df.dropna()

# Split data into features (X) that will be used to predict data and targets (Y) that will be what we try to predict
x = df.drop(['Player', 'PassYds', 'PassTD', 'Ints', 'RushYds', 'RushTDs', 'Catches', 'RecYds', 'RecTDs', 'Fumbles'], axis=1)
y = df[['PassYds', 'PassTD', 'Ints', 'RushYds', 'RushTDs', 'Catches', 'RecYds', 'RecTDs', 'Fumbles']]

# Standardize the feature values to have zero mean and unit variance
scaler = StandardScaler()
X_scaled = scaler.fit_transform(x)

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Define the hyperparameter search space for the RandomForestRegressor
param_distributions = {
    'estimator__n_estimators': randint(50, 150),  # Number of Trees in Forest
    'estimator__max_depth': [None, 10, 20],       # Maximum depth of the trees
    'estimator__min_samples_split': randint(2, 6),  # Minimum samples required to split an internal node
    'estimator__min_samples_leaf': randint(1, 6)    # Minimum samples required to be at a leaf node
}

# Initialize MultiOutputRegressor with RandomForestRegressor
model = MultiOutputRegressor(RandomForestRegressor())

# Setup RandomizedSearchCV to find the best hyperparameters
random_search = RandomizedSearchCV(
    model, 
    param_distributions, 
    n_iter=20,  # Number of parameter settings sampled
    cv=3,       # Number of cross-validation folds
    scoring='neg_mean_squared_error', 
    n_jobs=-1,  # Use all available CPU cores
    random_state=42
)

#Train model with training data
random_search.fit(X_train, y_train)

#Predict target variables using testing data
y_pred = random_search.predict(X_test)

# Calculate performance metrics for each target
mse = mean_squared_error(y_test, y_pred, multioutput='raw_values')
r2 = r2_score(y_test, y_pred, multioutput='raw_values')
mae = mean_absolute_error(y_test, y_pred, multioutput='raw_values')

# Print individual metrics
print(f"Mean Squared Error for each target: {mse}")
print(f"R^2 Score for each target: {r2}")
print(f"Mean Absolute Error for each target: {mae}")

# Normalize metrics to be in a common range for combination
mse_norm = 1 / (1 + mse)
mae_norm = 1 / (1 + mae)
r2_norm = (r2 + 1) / 2  

# Combine metrics into a single score using a weighted average
weights = {'mse': 0.45, 'mae': 0.35, 'r2': 0.2}
combined_score = (weights['mse'] * mse_norm.prod()) ** (1 / len(mse_norm)) + \
                  (weights['mae'] * mae_norm.prod()) ** (1 / len(mae_norm)) + \
                  (weights['r2'] * r2_norm.prod()) ** (1 / len(r2_norm))

#Print the overall accuracy score -> ~90.9%
print(f"Combined Accuracy Score: {combined_score}")

# Make predictions for each player and compile the results
results = pd.DataFrame(columns=['Player', 'PassYds', 'PassTD', 'Ints', 'RushYds', 'RushTDs', 'Catches', 'RecYds', 'RecTDs', 'Fumbles'])
for player in df['Player'].unique():
    player_data = df[df['Player'] == player].tail(1)  # Get the most recent data for the player
    if player_data.empty:
        continue
    player_features = player_data.drop(['Player', 'PassYds', 'PassTD', 'Ints', 'RushYds', 'RushTDs', 'Catches', 'RecYds', 'RecTDs', 'Fumbles'], axis=1)
    player_features_scaled = scaler.transform(player_features)          # Scale the features for prediction
    player_prediction = random_search.predict(player_features_scaled)       # Predict values for the player
    player_prediction_df = pd.DataFrame(player_prediction, columns=y.columns)   # Convert prediction to DataFrame
    player_prediction_df['Player'] = player
    results = pd.concat([results, player_prediction_df])        # Append to results DataFrame

# Reset the index of results DataFrame
results = results.reset_index(drop=True)
results.columns = ['player', 'passyds', 'passtd', 'ints', 'rushyds', 'rushtds', 'catches', 'recyds', 'rectds', 'fumbles']

# Add to database
DATABASE_URL = "postgresql://postgres@localhost:5432/playerpredictions"
engine = create_engine(DATABASE_URL)
connection = engine.connect()
print("inserting data now")
try:
    results.to_sql('player_stats', engine, if_exists='append', index=False)
    print("Data inserted successfully!")
except Exception as e:
    print(f"An error occurred: {e}")


# Display results
# print(results.head(10))

cur.close()
conn.close()
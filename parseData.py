import os
import pandas as pd
from bs4 import BeautifulSoup


#Extracts NFL box score statistics from HTML files and saves aggregated data into a CSV file for further analysis



#Define the directory where the box score table HTML files are located
scoresDirectory = "data/scores"
# List all files in that directory
boxScores = os.listdir(scoresDirectory)

def parseHTML(boxScore):
    """
    Parses HTML file and removes unnecessary table headers.
    
    Args:
        boxScore (str): The filename of the box score HTML file.
        
    Returns:
        BeautifulSoup: Parsed BeautifulSoup object of the HTML content without unnecessary table headers
    """
    # Construct the full path to the box score HTML file
    boxScorePath = os.path.join(scoresDirectory, boxScore)
    with open(boxScorePath) as f:  #Read contents of HTML file
        html = f.read()
    soup = BeautifulSoup(html, 'lxml')  #Use Beautiful Soup to parse HTML file
    #Remove unnecessary table rows
    [s.decompose() for s in soup.select("tr.over_header")]
    [s.decompose() for s in soup.select("tr.thead")]
    return soup

def getSeason(date):
    """
    Determines which NFL season a certain game date is from
    
    Args:
        date (str): The date string in 'YYYYMM' format
        
    Returns:
        str: The NFL season corresponding to the date
    """
    # Extract the last two digits of the date string to determine the month
    if int(date[-2:]) < 2:
        season = str(int(date[:4]) - 1)   # If it is month of january, it is the previous year's season
    else:
        season = date[:4]   #Else it is current year's season
    return season


def readBoxScore(soup, season):
    """
    Converts parsed HTML content into a DataFrame, standardizes columns, and adds season information.
    
    Args:
        soup (BeautifulSoup): Parsed BeautifulSoup object of HTML content.
        season (str): The NFL season corresponding to the given game's box score
        
    Returns:
        pd.DataFrame: DataFrame containing processed box score data.
    """
    tbody = soup.find('tbody')           #Finds table's body element
    table_tag = soup.new_tag('table')     #Create new table tag
    body_content = tbody.extract()        #Extract table's body content
    table_tag.append(body_content)         #Append content to new table tag
    soup.body.append(table_tag)            #Append new table tag to content body
    #Convert HTML table to dataframe
    df = pd.read_html(str(soup), index_col=0)[0]
    #Drop unnecessary columns from the dataframe such as attempts, averages, etc.
    df = df.drop(df.columns[[1, 2, 6, 7, 8, 9, 10, 13, 14, 18, 19 ]], axis=1)
    df.reset_index(inplace=True)   #Reset Index
    headers = ["Player", "Team","PassYds","PassTD","Ints","RushYds","RushTDs","Catches","RecYds","RecTDs","Fumbles"]
    df.columns = headers   #Add renamed columns
    df["Season"] = season   #Add season column
    return df

games = []   #Stores dataframe for each box score
print("starting")
for boxScore in boxScores:      #For each box score HTML, parse it, extract and determine the season for given date, convert HTML to dataframe
    soup = parseHTML(boxScore)
    date = str(boxScore[0:6])
    season = getSeason(date)
    df = readBoxScore(soup, season)
    df["Date"] = os.path.basename(boxScore)[:8]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y%m%d")       #Add date & season
    games.append(df)  #Add to list
#Concatenate all dataframes into a single data frame
games_df = pd.concat(games, ignore_index=True)
#Save combined dataframe into a csv file
games_df.to_csv("nfl_games.csv")





from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_cors import CORS

#Initialize flask application, enable CORS
app = Flask(__name__)
CORS(app)

#Define URL to connect to database, use SQL Alchemy with DB URL
DATABASE_URL = "postgresql://postgres@localhost:5432/playerpredictions"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initialize/Create SQL Alchemy Engine for DB, Create Session
db = SQLAlchemy(app)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

#Create Model for Player_Stats Table
class PlayerStats(db.Model):
    __tablename__ = 'player_stats'
    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.String(100), nullable=False)
    passyds = db.Column(db.Float, nullable=True)
    passtd = db.Column(db.Float, nullable=True)
    ints = db.Column(db.Float, nullable=True)
    rushyds = db.Column(db.Float, nullable=True)
    rushtds = db.Column(db.Float, nullable=True)
    catches = db.Column(db.Float, nullable=True)
    recyds = db.Column(db.Float, nullable=True)
    rectds = db.Column(db.Float, nullable=True)
    fumbles = db.Column(db.Float, nullable=True)
    fantasyppr = db.Column(db.Float, nullable=True)
    fantasynonppr = db.Column(db.Float, nullable=True)

#Define URL route to fetch player statistics from database
@app.route('/api/statistics', methods=['GET'])
def get_stats():
    try:
        #Query all records, process and format data from all records
        results = db.session.query(PlayerStats).all()
        stats = []
        for result in results:
            stats.append({
                'Player': result.player,
                'Passing Yards': result.passyds,
                'Passing TDs': result.passtd,
                'Interceptions': result.ints,
                'Rushing Yards': result.rushyds,
                'Rushing TDs': result.rushtds,
                'Receptions': result.catches,
                'Receiving Yards': result.recyds,
                'Receiving TDs': result.rectds,
                'Fumbles': result.fumbles,
                'Fantasy PPR Points' : result.fantasyppr,
                'Fantasy Non-PPR Points' : result.fantasynonppr
            })
        return jsonify(stats)
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
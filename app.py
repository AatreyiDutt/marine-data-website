from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, UniqueConstraint
import psycopg2

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://aatreyi:8f70565c@10.2.95.122/aatreyi'

db = SQLAlchemy(app)

def get_query(filename):
    filename = "queries/" + filename + ".sql"
    with open(filename) as fh:
        return fh.read()

# tables ---------------------------------------------

class behaviour (db.Model):
    __tablename__='behaviour'
    code = db.Column(db.String(1), primary_key=True)
    behaviour = db.Column(db.String(60))

class name (db.Model):
    __tablename__='name'
    code = db.Column(db.String(30), primary_key=True)
    species = db.Column(db.String(30))
    type = db.Column(db.String(10))

class observations (db.Model):
    __tablename__='observations'
    gis_key = db.Column(db.String(30), primary_key=True) # links to transect_log.gis_key
    species_code = db.Column(db.String(30), primary_key=True) # links to name.code
    behaviour_code = db.Column(db.String(1), primary_key=True) # links to behaviour.code
    count = db.Column(db.Integer)
    __table_args__ = (
        UniqueConstraint('gis_key','species_code','behaviour_code'),
    )
        
class transect_log (db.Model):
    __tablename='transect_log'
    gis_key = db.Column(db.String(30), primary_key=True) # links to observations.gis_key
    cruise = db.Column(db.String(30))
    transect_num = db.Column(db.Integer)
    bin_num = db.Column(db.Integer)
    date = db.Column(db.Date)
    time = db.Column(db.Float)
    latitude_start = db.Column(db.Float)
    longitude_start = db.Column(db.Float)
    latitude_mid = db.Column(db.Float)
    longitude_mid = db.Column(db.Float)
    latitude_stop = db.Column(db.Float)
    longitude_stop = db.Column(db.Float)
    length = db.Column(db.Float)
    width = db.Column(db.Float)
    area = db.Column(db.Float)
    season = db.Column(db.String(20))

# main page ------------------------------

@app.route('/')
def index():
    return render_template('index.html')

# queries -----------------------------------

@app.route('/sightings')
def sightings_by_species():
    query = get_query("sightings")
    with db.engine.connect() as connection:
        result = connection.execute(text(query))
    data = [{'species': row.species, 'sightings': row.sightings} for row in result]
    return render_template('sightings.html', data=data)

@app.route('/by-behaviour')
def behaviour_by_species():
    return render_template('by-behaviour.html')

@app.route('/by-behaviour/<bcode>')
def behaviour_specific(bcode):
    query = text(get_query("behaviour_specific"))
    with db.engine.connect() as connection:
        result = connection.execute(query, {"bcode":bcode})
    data = [{'species': row.species, 'occurences': row.occurences} for row in result]
    return render_template('behaviour-specific.html', data=data)

@app.route('/by-date', methods=['GET','POST'])
def bydate():
    data = None
    if request.method == 'POST':
        udate = request.form['user_input']
        query = text(get_query("bdaylist_specific"))
        with db.engine.connect() as connection:
            result = connection.execute(query, {"udate":udate})
        data = [{'year': row.year, 'species': row.species, 'behaviour': row.behaviour}
                for row in result]
    return render_template('by-date.html', data=data)

@app.route('/species')
def image_grid():
    query = text(get_query("species_view"))
    with db.engine.connect() as connection:
        result = connection.execute(query)
    image_data = [{"filename": row.species_code, "name": row.species} for row in result]
    return render_template('species.html', image_data=image_data)

@app.route('/species/<image_name>')
def image_route(image_name):
    query = text(get_query("species_specific"))
    with db.engine.connect() as connection:
        result = connection.execute(query,{"image_name":image_name})
    data = [{"behaviour": row.behaviour, "date": row.date, "time": row.time,
             "latitude": row.latitude_mid, "longitude": row.longitude_mid,
             "season": row.season} for row in result]
    return render_template('species-specific.html', data=data)

# run app.py -------------------

if __name__=='__main__':
    app.run(debug=True)

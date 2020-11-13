"""OpenAQ Air Quality Dashboard with Flask.""" 
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__) 


APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3' 
DB = SQLAlchemy(APP)


@APP.route('/') 
def root(): 
    """Base view.""" 
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    results = getDatesValues(body)
    # Part 4 Stretch Goal
    return render_template("base.html", records=Record.query.filter(Record.value>=10).all())
    return str(Record.query.filter(Record.value>=10).all())
    return str(results)


def getDatesValues(body):
    results = []
    for dictionary in body['results']:
        results.append((dictionary['date']['utc'],dictionary['value']))
    return results


class Record(DB.Model): 
    id = DB.Column(DB.Integer, primary_key=True) 
    datetime = DB.Column(DB.String(25)) 
    value = DB.Column(DB.Float, nullable=False) 
    def __repr__(self): 
        dictionary = {"id" : self.id,
                      "date" : self.datetime,
                      "value" : self.value}
        return str(dictionary)
        

@APP.route('/refresh') 
def refresh(): 
    """Pull fresh data from Open AQ and replace existing data.""" 
    DB.drop_all() 
    DB.create_all()
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')

    results = getDatesValues(body)
    i = 1
    for tup in results:
        rec = Record()
        rec.id = i
        rec.datetime = str(tup[0])
        rec.value = tup[1]
        DB.session.add(rec)
        i += 1
    DB.session.commit() 
    return 'Data refreshed!'


###### STRETCH GOALS ######
# Part 2
# List all cities covered by OpenAQ
@APP.route('/cities')
def cities():
    api = openaq.OpenAQ()
    status, body = api.cities()
    
    results = getCities(body)
    output = "Cities that OpenAQ covers:\n"
    for city in results:
        output += city + "\n"
    return output

def getCities(body):
    results = []
    for dictionary in body['results']:
        results.append(dictionary['city'] + ", " + dictionary['country'])
    return results


# Part 4

from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/hello')
def HelloWorld():
    restaurants = session.query(Restaurant).all()
    #items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    output = ""
    for i in restaurants:
        output += "<ul> %s" % i.name
        items = session.query(MenuItem).filter_by(restaurant_id = i.id)
        for j in items:
            output += "<li> %s </li>" % j.name
        output += "</ul>"
    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)

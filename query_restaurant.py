from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#myFirstRestaurant = Restaurant(name = "Pizza Palace")
#session.add(myFirstRestaurant)
#session.commit()

for line in session.query(Restaurant):
    print line.id, line.name

#cheesepizza = MenuItem(name="Cheese Pizza", description = "Made with all natural ingredients and fresh mozzarella", course="Entree", price="$8.99",
#  restaurant=myFirstRestaurant)
#session.add(cheesepizza)
#session.commit()

r = session.query(Restaurant).filter_by(name = "Boneheads").one()
i = MenuItem(name="Mushroom Burger", restaurant = r)
#session.add(i)
#session.commit()

for line in session.query(MenuItem):
    print line.id, line.name

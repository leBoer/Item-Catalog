from flask import (Flask, render_template, flash, request,
                   redirect, url_for, jsonify)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)
app.secret_key = '9JF(=r2[/Q3n3&.N'

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bin = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Making an API Endpoint (GET Request)
@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurants])


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(
        id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    # return "This page will show all my restaurants"
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new/',
           methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash("New Restaurant Created")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')
    # return "This page will be for making a new restaurant"


@app.route('/restaurant/<int:restaurant_id>/edit/',
           methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    editRestaurant = session.query(Restaurant).filter_by(
            id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editRestaurant.name = request.form['name']
            session.add(editRestaurant)
            session.commit()
            flash("Restaurant Successfully Edited")
            return redirect(url_for('showRestaurants'))
    else:
        return render_template('editrestaurant.html',
                               editRestaurant_id=editRestaurant.id,
                               editRestaurant_name=editRestaurant.name)
    # return "This page will be for editing restaurant %s" % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/delete/',
           methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    deleteRestaurant = session.query(Restaurant).filter_by(
        id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(deleteRestaurant)
        session.commit()
        flash("Restaurant Successfully Deleted")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleterestaurant.html',
                               deleteRestaurant_id=deleteRestaurant.id,
                               deleteRestaurant_name=deleteRestaurant.name)
    # return "This page will be for deleting restaurant %s" % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    menuItems = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    restaurant = session.query(Restaurant).filter_by(
        id=restaurant_id).one()
    # return "This page is the menu for restaurant %s" % restaurant_id
    return render_template('menu.html',
                           restaurant=restaurant,
                           menuItems=menuItems)


@app.route('/restaurant/<int:restaurant_id>/menu/new/',
           methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        if request.form['name']:
            newMenuItem = MenuItem(name=request.form['name'],
                                   course=request.form['course'],
                                   description=request.form['description'],
                                   price=request.form['price'],
                                   restaurant_id=restaurant_id)
            session.add(newMenuItem)
            session.commit()
            flash("Menu Item Created")
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html',
                               restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editMenuItem = session.query(MenuItem).filter_by(
        id=menu_id,
        restaurant_id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editMenuItem.name = request.form['name']
            editMenuItem.course = request.form['course']
            editMenuItem.description = request.form['description']
            editMenuItem.price = request.form['price']
            session.add(editMenuItem)
            session.commit()
            flash("Menu Item Successfully Edited")
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', item=editMenuItem)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deleteMenuItem = session.query(MenuItem).filter_by(
        id=menu_id,
        restaurant_id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(deleteMenuItem)
        session.commit()
        flash("Menu Item Successfully Deleted")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html',
                               restaurant_id=restaurant_id,
                               item=deleteMenuItem)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

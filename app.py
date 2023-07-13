import os

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import uuid
from bson import ObjectId
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

# Configure MongoDB connection
app.config['MONGO_URI'] = 'mongodb+srv://ashish:ashish@cluster0.dsmyzjx.mongodb.net/zesty_zomato?retryWrites=true&w=majority'
mongo = PyMongo(app)

# Default routes
@app.route('/')
def default_routes():
    return '<h1 style="color:blue;text-align:center">Welcome to Zomato Backend!</h1>'

@app.route('/dishes', methods=['GET'])
def get_dishes():
    # Retrieve all dishes from the MongoDB collection
    dishes = list(mongo.db.dishes.find())

    for dish in dishes:
        dish['_id'] = str(dish['_id'])
    # Return the dishes as JSON response
    return jsonify(dishes)


@app.route('/dishes/<dish_id>', methods=['GET'])
def get_dish(dish_id):
    # Retrieve a specific dish by dish_id from the MongoDB collection
    dish = mongo.db.dishes.find_one({'_id': ObjectId(dish_id)}, {'_id': False})

    if dish:
        # Return the dish as JSON response
        return jsonify(dish)
    else:
        # Return a 404 error if the dish is not found
        return jsonify({'error': 'Dish not found'}), 404
    

@app.route('/dishes', methods=['POST'])
def add_dish():
    # Get the dish data from the request body
    dish_data = request.json

    # Insert the new dish into the MongoDB collection
    mongo.db.dishes.insert_one(dish_data)

    # Return a success message
    return jsonify({'message': 'Dish added successfully'}), 201


@app.route('/dishes/<dish_id>', methods=['PUT'])
def update_dish(dish_id):
    # Get the dish data from the request body
    dish_data = request.json

    # Update the dish in the MongoDB collection
    mongo.db.dishes.update_one({'_id': ObjectId(dish_id)}, {'$set': dish_data})
    # mongo.db.dishes.update_one({'disk_id': dish_id}, {'$set': dish_data})
    # Return a success message
    return jsonify({'message': 'Dish updated successfully'})

@app.route('/dishes/<dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
    # Delete the dish from the MongoDB collection
    mongo.db.dishes.delete_one({'_id': ObjectId(dish_id)})

    # Return a success message
    return jsonify({'message': 'Dish deleted successfully'})

@app.route('/orders', methods=['GET'])
def get_orders():
    # Retrieve all orders from the MongoDB collection
    orders = list(mongo.db.orders.find())

    for dish in orders:
        dish['_id'] = str(dish['_id'])
    # Return the orders as JSON response
    return jsonify(orders)


@app.route('/orders', methods=['POST'])
def place_order():
    # Get the order data from the request body
    order_data = request.json

    # Retrieve the dishes corresponding to the dish IDs in the order
    dish_ids = order_data['dish_id']
    dishes = list(mongo.db.dishes.find({'dish_id': {'$in': dish_ids}}, {'_id': False}))

    if len(dishes) != len(dish_ids):
        return jsonify({'error': 'Invalid dish ID(s) in the order'}), 400

    # Calculate the total order price
    total_price = sum(dish['price'] for dish in dishes)

    # Generate a unique order ID
    order_id = str(uuid.uuid4())

    # Prepare the order document
    order = {
        'order_id': order_id,
        'customer_name': order_data['customer_name'],
        'dishes': dishes,
        'total_price': total_price,
        'status': 'received'
    }

    # Insert the order into the orders collection
    mongo.db.orders.insert_one(order)

    # Return the order ID as a response
    return jsonify({'order_id': order_id}), 201

@app.route('/orders/<order_id>', methods=['PUT'])
def update_order_status(order_id):
    # Get the updated status from the request body
    status = request.json.get('status')

    # Validate the status value
    valid_statuses = ['preparing', 'ready for pickup', 'delivered']
    if status not in valid_statuses:
        return jsonify({'error': 'Invalid status value'}), 400

    # Update the status of the order in the orders collection
    result = mongo.db.orders.update_one({'order_id': order_id}, {'$set': {'status': status}})

    if result.matched_count == 0:
        return jsonify({'error': 'Order not found'}), 404

    # Return a success message
    return jsonify({'message': 'Order status updated successfully'})



# if __name__ == '__main__':
#     app.run()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
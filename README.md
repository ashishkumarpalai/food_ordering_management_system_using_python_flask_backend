# Zesty Zomato Web Application

The Zesty Zomato web application is a robust and dynamic platform designed to assist the Zesty Zomato restaurant in delivering gastronomic pleasures to their enthusiastic patrons. The application leverages Flask, a Python web framework, and MongoDB as the chosen database for effective data management.

## API Endpoints

### Dishes

- **GET /dishes**: Retrieve all dishes.
- **GET /dishes/{dish_id}**: Retrieve a specific dish by ID.
- **POST /dishes**: Add a new dish to the menu.
- **PUT /dishes/{dish_id}**: Update a specific dish by ID.
- **DELETE /dishes/{dish_id}**: Delete a specific dish by ID.

### Orders

- **GET /orders**: Retrieve all orders.
- **GET /orders/{order_id}**: Retrieve a specific order by ID.
- **POST /orders**: Place a new order.
- **PUT /orders/{order_id}**: Update the status of a specific order by ID.
- **DELETE /orders/{order_id}**: Delete a specific order by ID.

## Installation and Setup

1. Clone the repository: `git clone <repository_url>`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Configure the MongoDB connection in `config.py`.
4. Run the application: `python app.py`
5. Access the application in your browser at `http://localhost:5000`.

## Technologies Used

- Flask: Python web framework for building the backend.
- MongoDB: NoSQL database for efficient data storage and retrieval.
- HTML, CSS, JavaScript: Frontend technologies for creating the user interface.


## Contact

For any questions or inquiries, please contact us at [ashishkumarpalai2000@gmail.com].

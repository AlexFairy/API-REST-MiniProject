from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

project_app = Flask(__name__)
project_app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/commerce_react'
db = SQLAlchemy(project_app)

class customeraccount(db.Model):
    __tablename__ = 'CustomerAccount'
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(15), nullable=False)

class productcatalog(db.Model):
    __tablename__ = 'ProductCatalog'
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Numeric(5, 2), nullable=False)
    stock_level = db.Column(db.Integer, nullable=False)
    restock_items = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('CustomerAccount.customer_id'), nullable=False)

class ordermanagement(db.Model):
    __tablename__ = 'OrderManagement'
    order_id = db.Column(db.Integer, primary_key=True)
    place_order_date = db.Column(db.Date, nullable=False)
    retrieve_order = db.Column(db.Integer, nullable=True)
    track_order = db.Column(db.String(50), nullable=True)
    manage_order_history = db.Column(db.String(50), nullable=True)
    cancel_order = db.Column(db.Boolean, default=False)
    cal_total_price = db.Column(db.Numeric(10, 2), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customeraccount.customer_id'), nullable=False)


with project_app.app_context():
    db.create_all()

#Routes for CustomerAccount ---------------------------------------------------------------------------------------------
def get_customer_by_id(customer_id):
    customer = customeraccount.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'CustomerAccount not found'}), 404
    return jsonify({
                    'customer_id': customer.customer_id,
                    'name': customer.name,
                    'email': customer.email,
                    'phone_number': customer.phone_number,
                    'username': customer.username,
                    'password': customer.password})

@project_app.route('/customeraccount/all', methods=['GET'])
def get_all_customers():
    customers = customeraccount.query.all()
    return jsonify([{
                    'customer_id': c.customer_id,
                    'name': c.name,
                    'email': c.email,
                    'phone_number': c.phone_number,
                    'username': c.username,
                    'password': c.password} for c in customers])

@project_app.route('/customeraccount', methods=['POST'])
def customerAccountPOST():
    data = request.get_json()
    if not data or 'customer_id' not in data or 'name' not in data or 'email' not in data or 'phone_number' not in data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid'}), 400
    try:
        new_customer = customeraccount(customer_id=data['customer_id'], name=data['name'], email=data['email'], phone_number=data['phone_number'], username=data['username'], password=data['password'])
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'message': 'customeraccount added successfully!', 'customer_id': new_customer.customer_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@project_app.route('/customeraccount/<int:customer_id>', methods=['PUT'])
def customerAccountPUT(customer_id):
    customeraccount = customeraccount.query.get(customer_id)
    if not customeraccount:
        return jsonify({'error': 'customeraccount not found'}), 404
    data = request.get_json()
    try:
        customeraccount.name = data.get('name', customeraccount.name)
        customeraccount.email = data.get('email', customeraccount.email)
        customeraccount.phone_number = data.get('phone_number', customeraccount.phone_number)
        customeraccount.username = data.get('username', customeraccount.username)
        customeraccount.password = data.get('password', customeraccount.password)
        db.session.commit()
        return jsonify({'message': 'Updated successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@project_app.route('/customeraccount/<int:customer_id>', methods=['DELETE'])
def customerAccountDELETE(customer_id):
    customeraccount = customeraccount.query.get(customer_id)
    if not customeraccount:
        return jsonify({'error': 'customeraccount not found'}), 404
    try:
        db.session.delete(customeraccount)
        db.session.commit()
        return jsonify({'message': 'Deleted successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
# ------------------------------------------------------------------------------------------------------------------
#Routes for ProductCatalog
@project_app.route('/productcatalog/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = productcatalog.query.get(product_id)
    if not product:
        return jsonify({'error': 'ProductCatalog not found'}), 404
    return jsonify({
                    'product_id': product.product_id,
                    'product_name': product.product_name,
                    'price': product.price,
                    'stock_level': product.stock_level,
                    'restock_items': product.restock_items,
                    'customer_id': product.customer_id})

@project_app.route('/productcatalog/all', methods=['GET'])
def get_all_products():
    products = productcatalog.query.all()
    return jsonify([{
                    'product_id': p.product_id,
                    'product_name': p.product_name,
                    'price': p.price,
                    'stock_level': p.stock_level,
                    'restock_items': p.restock_items,
                    'customer_id': p.customer_id} for p in products])

@project_app.route('/productcatalog', methods=['POST'])
def productCatalogPOST():
    data = request.get_json()
    if not data or 'product_id' not in data or 'product_name' not in data or 'price' not in data or 'stock_level' not in data or 'restock_items' not in data or 'customer_id' not in data:
        return jsonify({'error': 'Invalid'}), 400
    try:
        new_customer = productcatalog(product_id=data['product_id'], product_name=data['product_name'], price=data['price'], stock_level=data['stock_level'], restock_items=data['restock_items'], customer_id=data['customer_id'] )
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'message': 'productcatalog added successfully!', 'product_id': new_customer.product_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@project_app.route('/productcatalog/<int:product_id>', methods=['PUT'])
def productCatalogPUT(product_id):
    productcatalog = productcatalog.query.get(product_id)
    if not productcatalog:
        return jsonify({'error': 'productcatalog not found'}), 404
    data = request.get_json()
    try:
        productcatalog.product_name = data.get('product_name', productcatalog.product_name)
        productcatalog.price = data.get('price', productcatalog.price)
        productcatalog.stock_level = data.get('stock_level', productcatalog.stock_level)
        productcatalog.restock_items = data.get('restock_items', productcatalog.restock_items)
        productcatalog.customer_id = data.get('customer_id', productcatalog.customer_id)
        db.session.commit()
        return jsonify({'message': 'Updated successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@project_app.route('/productcatalog/<int:product_id>', methods=['DELETE'])
def productCatalogDELETE(product_id):
    productcatalog = productcatalog.query.get(product_id)
    if not productcatalog:
        return jsonify({'error': 'productcatalog not found'}), 404
    try:
        db.session.delete(productcatalog)
        db.session.commit()
        return jsonify({'message': 'Deleted successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ------------------------------------------------------------------------------------------------------------------
#Routes for OrderManagement

@project_app.route('/ordermanagement/<int:order_id>', methods=['GET'])
def orderManagementGet(order_id):
    order = ordermanagement.query.get(order_id)
    if not order:
        return jsonify({'error': 'OrderManagement not found'}), 404
    return jsonify({
                    'order_id': order.order_id, 
                    'place_order_date': order.place_order_date, 
                    'retrieve_order': order.retrieve_order,
                    'track_order': order.track_order,
                    'manage_order_history': order.manage_order_history,
                    'cancel_order': order.cancel_order,
                    'cal_total_price': order.cal_total_price,
                    'customer_id': order.customer_id})

@project_app.route('/ordermanagement', methods=['GET'])
def orderManagementGetAll():
    orders = ordermanagement.query.all()
    return jsonify([{
                    'order_id': x.order_id, 
                    'place_order_date': x.place_order_date, 
                    'retrieve_order': x.retrieve_order,
                    'track_order': x.track_order,
                    'manage_order_history': x.manage_order_history,
                    'cancel_order': x.cancel_order,
                    'cal_total_price': x.cal_total_price,
                    'customer_id': x.customer_id} for x in orders])

@project_app.route('/ordermanagement', methods=['POST'])
def orderManagementPOST():
    data = request.get_json()
    if not data or 'place_order_date' not in data or 'retrieve_order' not in data or 'track_order' not in data or 'manage_order_history' not in data or 'cancel_order' not in data or 'cal_total_price' not in data or 'customer_id' not in data:
        return jsonify({'error': 'Invalid'}), 400
    try:
        new_order = ordermanagement(
                    place_order_date=data['place_order_date'], 
                    retrieve_order=data['retrieve_order'], 
                    track_order=data['track_order'], 
                    manage_order_history=data['manage_order_history'], 
                    cancel_order=data['cancel_order'], 
                    cal_total_price=data['cal_total_price'], 
                    customer_id=data['customer_id'])
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message': 'OrderManagement added successfully!', 'order_id': new_order.order_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@project_app.route('/ordermanagement/<int:order_id>', methods=['PUT'])
def orderManagementPUT(order_id):
    order = ordermanagement.query.get(order_id)
    if not order:
        return jsonify({'error': 'OrderManagement not found'}), 404
    data = request.get_json()
    try:
        order.place_order_date = data.get('place_order_date', order.place_order_date)
        order.retrieve_order = data.get('retrieve_order', order.retrieve_order)
        order.track_order = data.get('track_order', order.track_order)
        order.manage_order_history = data.get('manage_order_history', order.manage_order_history)
        order.cancel_order = data.get('cancel_order', order.cancel_order)
        order.cal_total_price = data.get('cal_total_price', order.cal_total_price)
        order.customer_id = data.get('customer_id', order.customer_id)
        db.session.commit()
        return jsonify({'message': 'Updated successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@project_app.route('/ordermanagement/<int:order_id>', methods=['DELETE'])
def orderManagementDELETE(order_id):
    order = ordermanagement.query.get(order_id)
    if not order:
        return jsonify({'error': 'OrderManagement not found'}), 404
    try:
        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': 'Deleted successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

#-----------------------------------------------------------------------------------------------------------
#CLI w/ Functions

def userinput_CLI():
    while True:
        print("\nWelcome to the CLI!")
        print("1. Manage Customers")
        print("2. Product Management")
        print("3. Order Management")
        print("4. Product Catalog")
        print("5. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            while True:
                print("\nCustomer Management")
                print("1. Log in as Existing Customer")
                print("2. Create a New Customer Account")
                print("3. View Account Holders")
                print("4. Return to Main Screen")
                customer_choice = input("Enter your choice: ")

                if customer_choice == "1":
                    username = input("Enter your username: ")
                    password = input("Enter your password: ")
                    
                    try:
                        customer = customeraccount.query.filter_by(username=username).first()
                        if customer and customer.password == password:
                            print(f"Welcome back, {customer.name}!")
                            while True:
                                print("\nWhat would you like to do?")
                                print("1. Update Account Information")
                                print("2. View All Account Members")
                                print("3. Find an Account Holder by Username")
                                print("4. Return to Previous Menu")
                                sub_choice = input("Enter your choice: ")

                                if sub_choice == "1": 
                                    print("\nUpdate Account Information")
                                    print("1. Change Password")
                                    print("2. Change Email")
                                    print("3. Return to Previous Menu")
                                    update_choice = input("Enter your choice: ")

                                    if update_choice == "1":
                                        new_password = input("Enter new password: ")
                                        customer.password = new_password
                                        db.session.commit()
                                        print("Password updated successfully!")
                                    elif update_choice == "2":
                                        new_email = input("Enter new email: ")
                                        customer.email = new_email
                                        db.session.commit()
                                        print("Email updated successfully!")
                                    elif update_choice == "3":
                                        print("Returning to previous menu...")
                                        continue
                                    else:
                                        print("Invalid choice. Please try again.")

                                elif sub_choice == "2":
                                    customers = customeraccount.query.all()
                                    print("\nAll Account Members:")
                                    for member in customers:
                                        print(f"Name: {member.name}")

                                elif sub_choice == "3":
                                    search_username = input("Enter the username to find: ")
                                    found_customer = customeraccount.query.filter_by(username=search_username).first()
                                    if found_customer:
                                        print(f"Found Account: {found_customer.name}, Email: {found_customer.email}")
                                    else:
                                        print("No account found with that username.")

                                elif sub_choice == "4":
                                    print("Returning to Customer Management menu...")
                                    break

                                else:
                                    print("Invalid choice. Please try again.")
                        else:
                            print("Invalid username or password.")
                    except Exception as e:
                        print(f"Error: {e}")

                elif customer_choice == "2":
                    name = input("Enter your name: ")
                    email = input("Enter your email: ")
                    phone = input("Enter your phone number: ")
                    username = input("Create a username: ")
                    password = input("Create a password: ")

                    try:
                        new_customer = customeraccount(name=name, email=email, phone_number=phone, username=username, password=password)
                        db.session.add(new_customer)
                        db.session.commit()
                        print("Customer account created successfully!")
                    except Exception as e:
                        print(f"Error creating customer: {e}")

                elif customer_choice == "3":
                    print("\nView Account Holders")
                    print("1. View All Account Holders")
                    print("2. View Account Holder by Username")
                    print("3. Return to Previous Menu")
                    view_choice = input("Enter your choice: ")

                    if view_choice == "1":
                        customers = customeraccount.query.all()
                        print("\nAll Account Holders:")
                        for customer in customers:
                            print(f"Name: {customer.name}")

                    elif view_choice == "2":
                        search_username = input("Enter the username to find: ")
                        found_customer = customeraccount.query.filter_by(username=search_username).first()
                        if found_customer:
                            print(f"Found Account: {found_customer.name}, Email: {found_customer.email}")
                        else:
                            print("No account found with that username.")

                    elif view_choice == "3":
                        print("Returning to Customer Management menu...")
                        continue

                    else:
                        print("Invalid choice. Please try again.")

                elif customer_choice == "4":
                    print("returning...")
                    break

                else:
                    print("Invalid choice. Please try again.")

        elif choice == "2":
            while True:
                print("\nProduct Management")
                print("1. Add Product")
                print("2. Update Product")
                print("3. List Products")
                print("4. Return to Main Screen")
                product_choice = input("Enter your choice: ")

                if product_choice == "1":
                    name = input("Enter product name: ")
                    price = float(input("Enter product price: "))
                    stock = int(input("Enter stock level: "))
                    try:
                        new_product = productcatalog(product_name=name, price=price, stock_level=stock)
                        db.session.add(new_product)
                        db.session.commit()
                        print("Product added successfully!")
                    except Exception as e:
                        print(f"Error adding product: {e}")

                elif product_choice == "2": 
                    product_id = int(input("Enter product ID to update: "))
                    product = productcatalog.query.get(product_id)
                    if product:
                        update_name = input("Do you want to update the name? (yes/no): ").lower()
                        if update_name == "yes":
                            product.product_name = input(f"Update name [{product.product_name}]: ") or product.product_name

                        update_quantity = input("Do you want to change the quantity? (no/decrease/restock): ").lower()
                        if update_quantity == "decrease":
                            decrease_amount = int(input("Enter amount to decrease: "))
                            if decrease_amount > product.stock_level:
                                print("Error: Decrease amount exceeds current stock level!")
                            else:
                                product.stock_level -= decrease_amount
                                print(f"Stock decreased. Current stock level: {product.stock_level}")
                        elif update_quantity == "restock":
                            restock_amount = int(input("Enter amount to restock: "))
                            product.stock_level += restock_amount
                            print(f"Stock restocked. Current stock level: {product.stock_level}")

                        update_price = input("Do you want to update the price? (yes/no): ").lower()
                        if update_price == "yes":
                            product.price = float(input(f"Update price [{product.price}]: ") or product.price)

                        db.session.commit()
                        print("Product updated successfully!")
                    else:
                        print("Product not found.")

                elif product_choice == "3":
                    products = productcatalog.query.all()
                    print("\nAvailable Products:")
                    for product in products:
                        print(f"ID: {product.product_id}, Name: {product.product_name}, Price: ${product.price}, Stock: {product.stock_level}")

                elif product_choice == "4":
                    print("Returning to Main Screen...")
                    break

                else:
                    print("Invalid choice. Please try again.")

        elif choice == "3":
            print("\nOrder Management")
            print("1. Retrieve Order by Customer ID")
            print("2. Track Order")
            print("3. Calculate Total Price")
            print("4. Restock Items")
            print("5. Exit Program")
            order_choice = input("Enter your choice: ")

            if order_choice == "1":
                customer_id = int(input("Enter Customer ID: "))
                orders = ordermanagement.query.filter_by(customer_id=customer_id).all()
                print("\nOrders:")
                for order in orders:
                    print(f"Order ID: {order.order_id}, Total Price: ${order.cal_total_price}, Status: {order.manage_order_history}")
            elif order_choice == "2":
                order_id = int(input("Enter Order ID: "))
                order = ordermanagement.query.get(order_id)
                if order:
                    print(f"Tracking Number: {order.track_order}, Status: {order.manage_order_history}")
                else:
                    print("Order not found.")
            elif order_choice == "3":
                customer_id = int(input("Enter Customer ID: "))
                orders = ordermanagement.query.filter_by(customer_id=customer_id).all()
                total_price = sum(order.cal_total_price for order in orders)
                print(f"Total Spent by Customer {customer_id}: ${total_price}")
            elif order_choice == "4":
                product_id = int(input("Enter Product ID to Restock: "))
                product = productcatalog.query.get(product_id)
                if product:
                    restock = int(input("Enter Quantity to Add to Stock: "))
                    if restock > 0:
                        product.stock_level += restock
                        db.session.commit()
                        print("Stock updated successfully!")
                    else:
                        print("Invalid restock quantity. Must be greater than 0.")
                else:
                    print("Product not found.")
            elif order_choice == "5":
                print("Returning to Main Menu...")
                break

            else:
                print("Invalid choice. Please try again.")

        elif choice == "4":
            print("\nProduct Catalog")
            print("1. Find Product by ID")
            print("2. Find Product by Name")
            catalog_choice = input("Enter your choice: ")
            if catalog_choice == "1":
                product_id = int(input("Enter Product ID: "))
                product = productcatalog.query.get(product_id)
                if product:
                    print(f"Name: {product.product_name}, Price: ${product.price}, Stock: {product.stock_level}")
                else:
                    print("Product not found.")
            elif catalog_choice == "2":
                name = input("Enter Product Name: ")
                products = productcatalog.query.filter(productcatalog.product_name.ilike(f"%{name}%")).all()
                for product in products:
                    print(f"ID: {product.product_id}, Name: {product.product_name}, Price: ${product.price}, Stock: {product.stock_level}")

        elif choice == "5":
            print("Goodbye!")
            break

if __name__ == '__main__':
    mode = input("Enter mode ('server' or 'cli'): ").strip().lower()
    if mode == 'server':
        project_app.run(debug=True)
    elif mode == 'cli':
        with project_app.app_context():
            userinput_CLI()

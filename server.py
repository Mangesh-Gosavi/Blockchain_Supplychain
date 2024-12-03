from flask import Flask, render_template, request, redirect, url_for ,jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import hashlib
import datetime
import os

app = Flask(__name__)
CORS(app, origins="https://blockchain-supplychain.onrender.com")

mongo_uri = os.getenv("MONGO_URI")
# MongoDB connection
client = MongoClient(mongo_uri)  # Update with your MongoDB URI
db = client.supplychain
emplogin_collection = db.emplogin
admin_collection = db.admin
product_collection = db.products
mined_collection = db.mined_products
tracker_collection = db.tracker
report_collection = db.reports

def get_previous_hash(collection):
    last_block = collection.find_one(sort=[("blockid", -1)])
    return last_block['hash'] if last_block else '0000000000000000'

@app.route('/')
def home():
    return render_template("supply.html")

@app.route('/rawmat', methods=['GET'])
def rawmat():
        return render_template("rawmat.html")

@app.route('/manufac', methods=['GET'])
def manufac():
        return render_template("manufac.html")

@app.route('/supplier', methods=['GET'])
def supplier():
        return render_template("supplier.html")

@app.route('/retailer', methods=['GET'])
def retailer():
        return render_template("retailer.html")

@app.route('/employeePage')
def employeepage():
    return render_template("employee.html")

@app.route('/employee', methods=['POST'])
def cust():
    data = request.get_json()  
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"status": "error", "message": "All fields must be filled."})

    user = emplogin_collection.find_one({"email": email, "password": password})

    if user:
        return jsonify({"status": "success", "message": "Login successful"})
    else:
        return jsonify({"status": "error", "message": "Login failed. Please check your email and password."})


@app.route('/adminlogin')
def adminlogin():
    return render_template("adminlogin.html")

@app.route('/admin', methods=['POST'])
def admin():
    email = request.form.get('email')
    password = request.form.get('password')
    if not all([email, password]):
        return "All fields must be filled."

    # Check if credentials exist in MongoDB
    admin = admin_collection.find_one({"email": email, "password": password})
    if admin:
        return render_template('admin.html')
    else:
        return "Admin login failed. Please check your email and password."

@app.route('/addemp')
def addemp():
    return render_template("addemp.html")

@app.route('/reg', methods=['POST'])
def register():
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    re_password = request.form.get('repassword')

    if not all([email, mobile, password, re_password]):
        return "All fields must be filled."
    if password != re_password:
        return "Passwords do not match."
    if len(mobile) != 10:
        return "Enter a valid number."

    timestamp = str(datetime.datetime.now())
    previous_hash = get_previous_hash(emplogin_collection)

    block_data = {
        'blockid': emplogin_collection.count_documents({}) + 1,
        'email': email,
        'mobile': mobile,
        'password': password,
        'timestamp': timestamp,
        'prevhash': previous_hash
    }
    block_data['hash'] = hashlib.sha256(str(block_data).encode()).hexdigest()

    try:
        emplogin_collection.insert_one(block_data)
        return "Registered successfully"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/viewemp', methods=['GET'])
def viewemp():
    employees = list(emplogin_collection.find({}, {"_id": 0}))
    return render_template("data.html", cust=employees)

@app.route('/addprod')
def addprod():
    return render_template("addprod.html")

@app.route('/add_prod', methods=['POST'])
def add_prod():
    name = request.form.get('name')
    temperature = request.form.get('temprature')
    price = request.form.get('price')
    brand = request.form.get('brand')
    addby = request.form.get('addby')

    if not all([name, temperature, price, brand]):
        return "All fields must be filled."

    block_data = {
        'blockid': product_collection.count_documents({}) + 1,
        'name': name,
        'temperature': temperature,
        'price': price,
        'brand': brand,
        'addby': addby,
        'status': 'Not Mined'
    }

    try:
        product_collection.insert_one(block_data)
        return "Product added successfully"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/globalprodpage')
def globalprodpage():
    return render_template("empaddprod.html")
    
@app.route('/globalprod', methods=['GET'])
def globalprod():
    products = list(mined_collection.find({}, {"_id": 0}))
    return jsonify(products)  

@app.route('/viewprod', methods=['GET'])
def viewprod():
    products = list(product_collection.find({}, {"_id": 0}))
    return jsonify(products)  

@app.route('/viewprodpage')
def viewprodpage():
    return render_template("product.html")

@app.route('/mineprod', methods=['GET'])
def mine_block():
    last_mined_hash = get_previous_hash(mined_collection)

    not_mined_products = list(product_collection.find({"status": "Not Mined"}))
    for product in not_mined_products:
        product['prevhash'] = last_mined_hash
        product['status'] = 'Mined'
        product['hash'] = hashlib.sha256(str(product).encode()).hexdigest()

        try:
            mined_collection.insert_one(product)
            product_collection.update_one(
                {"blockid": product['blockid']},  # Find the product by its blockid
                {"$set": {
                    "prevhash": product['prevhash'],
                    "status": product['status'],
                    "hash": product['hash']
                }}
            )
            last_mined_hash = product['hash']
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return 'All products are mined'

@app.route('/trackerpage')
def trackerpage():
    return render_template("tracker.html")

@app.route('/trackeddata', methods=['GET'])
def trackeddata():
    trackeddata = list(tracker_collection.find({}, {"_id": 0}))
    return jsonify(trackeddata) 

@app.route('/tracker', methods=['POST'])
def tracker():
    name = request.form.get('name')
    role = request.form.get('role')
    status = request.form.get('status')
    temperature = request.form.get('temperature')
    location = request.form.get('location')
    timestamp = str(datetime.datetime.now())
    data = {
        'name':name,
        'role': role,
        'status': status,
        'temperature': temperature,
        'location': location,
        'timestamp': timestamp
    }

    try:
        tracker_collection.insert_one(data)
        return "Data tracked successfully"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/report_page')
def report_page():
    return render_template("viewrep.html")

@app.route('/report', methods=['POST'])
def report():
    prodname = request.form.get('name')
    report_text = request.form.get('report')
    report_data = {
        'srno': report_collection.count_documents({}) + 1,
        'reportby': 'Retailer',
        'prodname': prodname,
        'report': report_text
    }

    try:
        report_collection.insert_one(report_data)
        return "Report saved successfully"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/viewreport', methods=['GET'])
def viewreport():
    reports = list(report_collection.find({}, {"_id": 0}))
    return jsonify(reports) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



import shutil
from flask import Flask, render_template, request, redirect, url_for
import os
import json
import hashlib 
import datetime

app = Flask(__name__)

def get_previous_hash():
    folder_path = 'emplogin'
    folder_len = len(os.listdir(folder_path))
    if folder_len == 0:
        return '0000000000000000'

    prev_block_filename = f"{folder_len}.json"
    prev_block_path = os.path.join('emplogin', prev_block_filename)

    # Read the previous block's data and return its hash
    with open(prev_block_path, 'r') as file:
        prev_block_data = json.load(file)
        return prev_block_data.get('hash', '0')

@app.route('/')
def home():
    return render_template("supply.html")

@app.route('/employee', methods=['POST'])
def cust():
    #Taking form data
    email = request.form.get('email')
    password = request.form.get('password')

    #Checking if any field is empty
    if not all([email, password]):
        return "All fields must be filled."

    #Checking if the provided email and password match the data in the folder
    folder_path = 'emplogin'
    found = False

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            data = json.load(file)
            if data['email'] == email and data['password'] == password:
                found = True
                break

    if found:
        # If email and password matches, take the user to the next page
        return render_template('employee.html')
    else:
        return "Login failed. Please check your email and password."
    
@app.route('/adminlogin')
def adminlogin():
    return render_template("adminlogin.html")

@app.route('/admin', methods=['POST'])
def admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([email, password]):
            return "All fields must be filled."

        # Check if the provided email and password match the data in the "admin" folder
        folder_path = 'admin'
        found = False

        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                data = json.load(file)
                if data['email'] == email and data['password'] == password:
                    found = True
                    break

        if found:
            # If email and password matches, take the admin to the next page
            return render_template('admin.html')
        else:
            return "Admin login failed. Please check your email and password."


@app.route('/addemp')
def addemp():
    return render_template("addemp.html")


@app.route('/reg', methods=['POST'])
def register():
    #Taking form data
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    re_password = request.form.get('repassword')

    #Checking if any field is empty
    if not all([email, mobile, password, re_password]):
        return "All fields must be filled."

    #If passwords are not same 
    elif password != re_password:
        return "Passwords do not match."
    
    elif len(mobile) != 10:
        return "Enter valid number"

    else:
        #Register and save data to a file
        timestamp = str(datetime.datetime.now())
        folder_path = 'emplogin'
        folder_len = len(os.listdir(folder_path)) + 1

        previous_hash = get_previous_hash()

        block_data = {
            'blockid': folder_len,
            'email': email,
            'mobile': mobile,
            'password': password,
            'timestamp': timestamp,
            'prevhash': previous_hash  
        }

        block_hash = hashlib.sha256(json.dumps(block_data, sort_keys=True).encode()).hexdigest()
        block_data['hash'] = block_hash

        #Saving data with email as file name
        file_name = f"{folder_len}.json"
        file_path = os.path.join('emplogin', file_name)

        #Saving data to a file
        try:
            with open(file_path, 'w') as file:
                json.dump(block_data, file, indent=4)
            return "Registered successfully"
        except Exception as e:
            return f"An error occurred while saving the data: {str(e)}"
        
@app.route('/viewemp', methods=['GET'])
def viewemp():
    if request.method == 'GET':
        folder_path = 'emplogin'
        customer_data = []
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                data = json.load(file)
                customer_data.append({
                    'blockid': data['blockid'],
                    'email': data['email'],
                    'mobile': data['mobile'],
                    'password': data['password']
                })
              

        return render_template("data.html",cust = customer_data)


@app.route('/addprod')
def addprod():
    return render_template("addprod.html")

@app.route('/add_prod', methods=['POST'])
def add_prod():
    if request.method == 'POST':
        name = request.form.get('name')
        temprature = request.form.get('temprature')
        price = request.form.get('price')
        brand = request.form.get('brand')
        addby = request.form.get('addby')
    
    if not all([name, temprature, price, brand]):
        return "All fields must be filled."
    
    else:
        #Registration successful, save data to a file
        timestamp = str(datetime.datetime.now())
        folder_path = 'Add_Product'
        folder_len = len(os.listdir(folder_path)) + 1

        # Hash the current block's data
        block_data = {
            'blockid': folder_len,
            'name': name,
            'temprature': temprature,
            'price': price,
            'brand': brand,
            'addby': addby,
            'status':'Not Mined'
        }

        #Creates a unique file name based on the block ID
        file_name = f"{folder_len}.json"
        file_path = os.path.join('Add_Product', file_name)

        #Saving block data to a file
        try:
            with open(file_path, 'w') as file:
                json.dump(block_data, file, indent=4)
            return "Product Added successfully"
        except Exception as e:
            return f"An error occurred while saving the data: {str(e)}"

@app.route('/viewprod', methods=['GET'])
def viewprod():
    if request.method == 'GET':
        folder_path = 'Add_Product'
        product_data = []
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                data = json.load(file)
                product_data.append({
                    'blockid': data['blockid'],
                    'name': data['name'],
                    'temprature': data['temprature'],
                    'price': data['price'],
                    'brand': data['brand'],
                    'addby': data['addby'],
                    'status': data['status']
                })
              

        return render_template("product.html",prod = product_data)  

@app.route('/mineprod', methods=['GET'])
def mine_block():
    folder_path = 'Add_Product'
    mined_folder_path = 'mined_product'

    #Creates a 'mined_product' folder if it doesn't exist
    if not os.path.exists(mined_folder_path):
        os.makedirs(mined_folder_path)

    last_mined_hash = get_last_mined_hash()

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r+') as file:
            data = json.load(file)

            # Only mine products with status 'Not Mined'
            if data.get('status') == 'Not Mined':
                # Calculate block hash
                block_data = {
                    'blockid': data['blockid'],
                    'name': data['name'],
                    'temprature': data['temprature'],
                    'price': data['price'],
                    'brand': data['brand'],
                    'addby': data['addby'],
                    'status': 'Mined'
                }

                block_data['prevhash'] = last_mined_hash  

                block_hash = hashlib.sha256(json.dumps(block_data, sort_keys=True).encode()).hexdigest()
                block_data['hash'] = block_hash

                # Update file content with block hash, previous hash, and status
                file.seek(0)
                json.dump(block_data, file, indent=4)
                file.truncate()

                #copy the updated file to the 'mined_product' folder
                shutil.copy(file_path, os.path.join(mined_folder_path, file_name))

                #Update the last mined hash for the next block
                last_mined_hash = block_hash

    return redirect(url_for('viewprod'))

def get_last_mined_hash():
    folder_path = 'mined_product'
    files = os.listdir(folder_path)
    if files:
        last_file_path = os.path.join(folder_path, sorted(files)[-1])
        with open(last_file_path, 'r') as file:
            last_block_data = json.load(file)
            return last_block_data['hash'] if 'hash' in last_block_data else '0'
    else:
        return '0000000000000000'
    


@app.route('/globalprod', methods=['GET'])
def globalprod():
    if request.method == 'GET':
        folder_path = 'mined_product'
        product_data = []
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                data = json.load(file)
                product_data.append({
                    'blockid': data['blockid'],
                    'name': data['name'],
                    'temprature': data['temprature'],
                    'price': data['price'],
                    'brand': data['brand'],
                    'addby': data['addby']
                })
              

        return render_template("empaddprod.html",prod = product_data)  

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

#Tracker
def save_data(role, data,prodname):
    #Getting the list of files in the "tracker" folder
    files = os.listdir('tracker')

    #Checking if there are any files in the "tracker" folder
    if not files or role == 'raw supplier':
        # If no files or role is raw supplier, create a new file with the name as the length of files
        file_index = len(files) + 1
        file_name = f'tracker_data_{file_index}.json'
    else:
        # Get the last file in the "tracker" folder
        sorted_files = sorted(files)
        last_file = sorted_files[-1]
        file_name = last_file

    # Defining the file path
    file_path = os.path.join('tracker', file_name)

    #Saving the data to the file
    with open(file_path, 'a') as file:
        file.write(json.dumps(data, indent=4))
        file.write('\n')  

    return f"Data saved to {file_name}."

@app.route('/tracker', methods=['POST'])
def tracker():
    role = request.form.get('role')
    if role == 'raw supplier':
        prodname = request.form.get('name') 
    
    else:
        prodname = None
        
    role = request.form.get('role')  
    status = request.form.get('status')
    temperature = request.form.get('temperature')
    location = request.form.get('location')  
    timestamp = str(datetime.datetime.now())  

    #Creating a dictionary of received data

    if role == 'raw supplier':
        data = {
        'prodname':prodname,
        'role': role,
        'status': status,
        'temperature': temperature,
        'location': location,
        'timestamp': timestamp
    }
    
    else:
        data = {
        'role': role,
        'status': status,
        'temperature': temperature,
        'location': location,
        'timestamp': timestamp
    }

    #Saving data to a file
    result = save_data(role, data,prodname)

    return result

#Reports
@app.route('/report_page')
def report_page():
    return render_template("report.html")


def save_report(report):
    #Creates a "reports" if not exist.
    if not os.path.exists('reports'):
        os.makedirs('reports')

    #Getting the list of files in the "reports" folder
    files = os.listdir('reports')

    #file index based on the length of existing files
    file_index = len(files) + 1

    #file name for the new report file
    file_name = f'reports_data_{file_index}.json'
    file_path = os.path.join('reports', file_name)

    #Saving the report data to the file
    with open(file_path, 'w') as file:
        file.write(json.dumps(report, indent=4))

    return f"Report saved to {file_name}."


@app.route('/report', methods=['POST'])
def report():
    if request.method == 'POST':
        files = os.listdir('reports')
        file_index = len(files) + 1
        prodname = request.form.get('name')
        report_text = request.form.get('report')

        data = {
            'srno': file_index,
            'reportby': 'Retailer',
            'prodname': prodname,
            'report': report_text
        }
        #Saving the report to a file
        result = save_report(data)

        return result

@app.route('/viewreport', methods=['GET'])
def viewreport():
    if request.method == 'GET':
        folder_path = 'reports'
        report_data = []
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                data = json.load(file)
                report_data.append({
                    'srno': data['srno'],
                    'reportby': data['reportby'],
                    'prodname': data['prodname'],
                    'report': data['report']
                })

        return render_template("viewrep.html", rep_data=report_data)
    
@app.route('/find_file')
def freport():
    return render_template('findfile.html')

@app.route('/findfile', methods=['POST'])
def findfile():
    product_name = request.form.get('name')
    matching_filenames = []

    if product_name and request.method == 'POST':
        folder_path = 'mined_product'

        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                data = json.load(file)
                if data['name'] == product_name:
                    matching_filenames.append(file_name)
    
    return matching_filenames


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

from flask import Flask, request, jsonify
from config.database import db, Base
from controllers.customer_controller import CustomerController
from controllers.payment_controller import PaymentController
from controllers.adeona_controller import AdeonaController

from controllers.mobile_controllers import process_csv_upload
from controllers.message_controller import process_message_csv_upload

with db.engine.begin() as conn:
    Base.metadata.create_all(conn)

app = Flask(__name__)
app.json.sort_keys = False

customer_controller = CustomerController()
payment_controller = PaymentController()
adeona_controller = AdeonaController()

@app.route('/api/customers', methods=['GET'])
def get_customers():
    """Fetch all customers"""
    result = customer_controller.get_all_customers()

    status_code = result.pop("status")
    return jsonify(result), status_code

@app.route('/api/customers', methods=['POST'])
def create_customer():
    """add new customer"""
    payload = request.get_json()

    result = customer_controller.add_new_customer(payload)

    status_code = result.pop("status")
    return jsonify(result), status_code

@app.route('/api/customers/<int:cid>', methods=['PUT'])
def update_customer(cid):
    """Update existing customer"""
    payload = request.get_json()

    payload["cid"] = cid

    result = customer_controller.update_customer(payload)

    status_code = result.pop("status")
    return jsonify(result), status_code

@app.route('/api/customers/<int:cid>', methods=['DELETE'])
def delete_customer(cid):
    """Route to delete a customer by CID"""
    result = customer_controller.delete_customer(cid)

    status_code = result.pop("status")
    return jsonify(result), status_code
    
@app.route('/api/customers/search', methods=['GET'])
def search_customers():
    """Search customers with pagination"""
    search_term = request.args.get('term', '')
    limit = request.args.get('limit', 5)
    offset = request.args.get('offset', 0)

    result = customer_controller.get_paginated_customers(search_term, limit, offset)

    status_code = result.pop("status")
    return jsonify(result), status_code

@app.route('/api/payments', methods=['GET'])
def get_payments():
    result = payment_controller.get_all_payments()

    status_code = result.pop("status")
    return jsonify(result), status_code

@app.route('/api/payments', methods=['POST'])
def create_payments():
    payload = request.get_json()

    result = payment_controller.add_new_payment(payload)

    status_code = result.pop("status")
    return jsonify(result), status_code

@app.route('/api/payments/<int:pid>', methods=['PUT'])
def update_payment(pid):
    payload = request.get_json()

    payload["pid"] = pid

    result = customer_controller.update_customer(payload)

    status_code = result.pop("status")
    return jsonify(result), status_code

@app.route('/api/payments/<int:pid>', methods=['DELETE'])
def delete_payments(pid):
    """Route to delete a payment by PID"""
    result = payment_controller.delete_payment(pid)

    status_code = result.pop("status")
    return jsonify(result), status_code

@app.route('/api/salary', methods=['GET'])
def get_salary():
    result = adeona_controller.get_all_salary()

    status_code = result.pop("status")
    return jsonify(result), status_code

@app.route('/api/salary', methods=['POST'])
def create_salary():
    payload = request.get_json()

    result = adeona_controller.add_new_salary(payload)

    status_code = result.pop("status")
    return jsonify(result), status_code

@app.route('/api/number/upload', methods=['POST'])
def upload_numbers_csv():
    if 'fileSelect' not in request.files:
        return jsonify({"ststus": "error", "message": "No file attached!"}), 400
    
    file = request.files['fileSelect']

    if file.filename == '':
        return jsonify({"status": "error", "message": "File is empty!"}), 400
    
    wipe_instruction = request.form.get('wipe_data', 'false')
    
    result = process_csv_upload(file, wipe_instruction)

    return jsonify(result), 200

@app.route('/api/message/upload_csv', methods=['POST'])
def upload_messages_csv():
    if 'fileSelect' not in request.files:
        return jsonify({"status": "error", "message": "No file attached!"}), 400
    
    file = request.files['fileSelect']

    if file.filename == '':
        return jsonify({"status": "error", "message": "File is empty!"}), 400

    if not file.filename.endswith('.csv'):
         return jsonify({"status": "error", "message": "Invalid file type! Please upload a .csv file."}), 400

    wipe_instruction = request.form.get('wipe_data', 'false')

    result = process_message_csv_upload(file, wipe_instruction)                

    status_code = 200 if result["status"] == "success" else 400
    return jsonify(result), status_code

if __name__ == '__main__':
    app.run(debug=True, threaded=False)
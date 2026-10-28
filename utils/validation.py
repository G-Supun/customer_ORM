import re

def validate_customer_data(data):
    if "name" not in data:
        return {"status": 400, "error": "Bad Request", "message": "Missing Key: 'name'"}
    if "mobile" not in data:
        return {"status": 400, "error": "Bad Request", "message": "Missing Key: 'mobile'"}
    if "address" not in data:
        return {"status": 400, "error": "Bad Request", "message": "Missing Key: 'address'"}
    
    if not isinstance(data["name"], str) or len(data["name"].strip()) == 0:
        return {"status": 400, "error": "Bad Request", "message": "Name must be a non empty string."}
    if len(data["name"]) > 100:
        return {"status": 400, "error": "Bad Request", "message": "Name exceeds 100 characters long."}
    
    mobile = data.get("mobile")
    if not (10 <= len(mobile) <= 13):
        return {"status": 400, "error": "Bad Request", "message": "Mobile number must be between 10 and 13 characters long."}
    
    clean_mobile = mobile.replace("+", "")
    if not clean_mobile.isdigit():
        return {"status": 400, "error": "Bad Request", "message": "Mobile number must contain only digits and '+'."} 

    if not isinstance(data["address"], str) or not data["address"].strip():
        return {"status": 400, "error": "Bad Request", "message": "Address must be a non empty string."}
    if len(data["address"]) > 255:
        return {"status": 400, "error": "Bad Request", "message": "Address exceeds 255 characters long."}
    
    return {"status": 200, "error": None, "message": "Success: valid data"}

def validate_pagination_params(limit, offset):
    errors = []

    try:
        limit_val = int(limit)
        if limit_val < 1:
            errors.append("Limit must be 1 or higher.")
    except ValueError:
        errors.append("Limit must be a valid number.")

    try:
        offset_val = int(offset)
        if offset_val < 0:
            errors.append("Offset cannot be negative.")
    except ValueError:
        errors.append("Offset must be a valid number.")

    if len(errors) > 0:
        return False, errors
    
    return True, []

def validate_payment_data(data, is_update=False):
    if not is_update and "cid" not in data:
        return{"status": 400, "error": "Bad Request", "message": "Missing Key: 'cid'"}
    
    if "amount" not in data:
        return {"status": 400, "error": "Bad Request", "message": "Missing key: 'amount'"}
    if "payment_type" not in data:
        return {"status": 400, "error": "Bad Request", "message": "Missing key: 'payment_type'"}
    
    try:
        amount_val = float(data["amount"])
        if amount_val <= 0:
            return {"status": 400, "error": "Bad Request", "message": "Amount must be positive number."}
    except (ValueError, TypeError):
        return {"status": 400, "error": "Bad Request", "message": "Amont must be a valid number."}
    
    p_type = data.get("payment_type", "")
    if not isinstance(p_type, str) or len(p_type.strip()) == 0:
        return {"status": 400, "error": "Bad Request", "message": "Invalied payment type."}
    if len(p_type) > 20:
        return {"status": 400, "error": "Bad Request", "message": "Payment type too long."}
    
    return {"status": 200, "error": None, "message": "Success: payment data is valid"}

def validate_adeona_tables(data, is_update=False):
    if not is_update and "cid" not in data:
        return{"status": 400, "error": "Bad Request", "message": "Missing Key: 'cid'"}
    
    if "salary" not in data:
        return {"status": 400, "error": "Bad Request", "message": "Missing key: 'salary'"}
        
    try:
        salary_val = float(data["salary"])
        if salary_val <= 0:
            return {"status": 400, "error": "Bad Request", "message": "Salary must be positive number."}
    except (ValueError, TypeError):
        return {"status": 400, "error": "Bad Request", "message": "Salary must be a valid number."}
    
    
    return {"status": 200, "error": None, "message": "Success: payment data is valid"}   

def is_valid_mobile(mobile_number):
    "format accepts: '0', '+94'" 

    pattern = re.compile(r"^(0[0-9]{9}|\+94[0-9]{9})$")  

    return bool(pattern.match(mobile_number)) 

def has_required_headers(actual_headers, required_headers):
    """Check contains all required headers"""
    if not actual_headers:
        return False
    
    return all(header in actual_headers for header in required_headers)

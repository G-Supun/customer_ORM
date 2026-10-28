from utils.validation import validate_customer_data, validate_pagination_params
from models.customer_model import Customer
from config.database import db

class CustomerController:

    def add_new_customer(self, payload):
        """
        Coordinates validating data and saving it to the database.
        """
        validation_result = validate_customer_data(payload)

        if validation_result["status"] != 200:
            return validation_result
        
        session = db.get_session()
        try:
            new_customer = Customer(
                name=payload["name"],
                mobile=payload["mobile"],
                address=payload["address"]
            )

            session.add(new_customer)
            session.commit()
            return {"status": 201, "message": "Created: Customer saved successfully."}
        
        except Exception as e:
            print(f"Database Error: {e}")
            session.rollback()
            return {"status": 500, "message": "Error: Database Failed to save customer."}
        
        finally:
            session.close()

    def get_all_customers(self):
        """
        Coordinates fetching all customers using the ORM
        """
        session = db.get_session()
        try:
            total = session.query(Customer).count()

            customers = session.query(Customer).order_by(Customer.cid.asc()).all()

            data = [
                {
                    "cid": c.cid,
                    "name": c.name,
                    "mobile": c.mobile,
                    "address": c.address
                } for c in customers
            ]
            return {"status": 200, "total_count": total, "data": data}
        except Exception as e:
            print(f"Database Error: {e}")
            return {"status": 500, "data": []}
        
        finally:
            session.close()

    def update_customer(self, payload):
        """
        Coordinates updating exsting customer
        """
        validation_result = validate_customer_data(payload)

        if validation_result["status"] != 200:
            return validation_result
        
        session = db.get_session()
        try:
            customer = session.query(Customer).filter(Customer.cid == payload["cid"]).first()

            if not customer:
                return {"status": 404, "message": "404 Not Found: Customer ID does not exist."}
            
            customer.name = payload["name"]
            customer.mobile = payload["mobile"]
            customer.address = payload["address"]

            session.commit()
            return {"status": 200, "message": "200 OK: Customer updated successfully."}

        except Exception as e:
            print(f"Update Error: {e}")
            session.rollback()
            return {"status": 500, "message": "500 Internal Server Error: Failed to update customer."}
        
        finally:
            session.close()

    def delete_customer(self, cid):
        """
        Coordinates deleting a customer
        """
        session = db.get_session()
        try:
            customer = session.query(Customer).filter(Customer.cid == cid).first()

            if not customer:
                return {"status": 409, "message": "409 Conflict: Could not delete."}
            
            session.delete(customer)
            session.commit()
            return {"status": 200, "message": "200 OK: Customer deleted successfully."}
        
        except Exception as e:
            print(f"Delete Error: {e}")
            session.rollback()
            return {"status": 500, "message": "500 Internal Server Error: Failed to delete."}
        
        finally:
            session.close()

    def get_paginated_customers(self, search_term="", limit=5, offset=0):
        """
        Fetches customers with a name filter and pagination
        """
        is_valid, errors = validate_pagination_params(limit, offset)

        if not is_valid:
            return {"status": 400, "message": "Validation Failed", "errors": errors}
        
        if search_term is None:
            search_term = ""

        safe_limit = int(limit)
        safe_offset = int(offset)

        session = db.get_session()
        try:
            base_query = session.query(Customer).filter(
                Customer.name.ilike(f"%{search_term.strip()}%")
            )

            total_count = base_query.count()

            customers = base_query.order_by(Customer.cid.asc()).limit(safe_limit).offset(safe_offset).all()

            data = [
                {
                    "cid": c.cid,
                    "name": c.name,
                    "mobile": c.mobile,
                    "address": c.address
                } for c in customers
            ]

            return {
                "status": 200,
                "total_count": total_count,
                "data": data
            }
        
        except Exception as e:
            print(f"Pagination Error: {e}")
            return {"status": 500, "data": []}
        
        finally:
            session.close()

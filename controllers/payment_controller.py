from utils.validation import validate_payment_data
from models.payment_model import CustomerPayment
from models.customer_model import Customer
from config.database import db

class PaymentController:

    def add_new_payment(self, payload):
        validation_result = validate_payment_data(payload)
        if validation_result["status"] != 200:
            return validation_result
        
        session = db.get_session()
        try:
            customer_exists = session.query(Customer).filter(Customer.cid == payload["cid"]).first()
            if not customer_exists:
                return {"status": 404, "message": "404 Not Found: Cannot add payment. Customer CID not exist."}
            
            new_payment = CustomerPayment(
                cid=payload["cid"],
                amount=payload["amount"],
                payment_type=payload["payment_type"]
            )
            session.add(new_payment)
            session.commit()
            return {"status": 201, "message": "Created: Payment saved successfully."}
        
        except Exception as e:
            print(f"Database Error: {e}")
            session.rollback()
            return {"status": 500, "message": "Error: Database Faild to save payment."}
        finally:
            session.close()

    def get_all_payments(self):
        session = db.get_session()
        try:
            total = session.query(CustomerPayment).count()
            payments = session.query(CustomerPayment).order_by(CustomerPayment.pid.asc()).all()

            data = [
                {
                    "pid": p.pid,
                    "cid": p.cid,
                    "amount": float(p.amount),
                    "payment_type": p.payment_type
                } for p in payments
            ]
            return {"status": 200, "total_count": total, "data": data}
        except Exception as e:
            print(f"Database Error: {e}")
            return {"status": 500, "data": []}
        
        finally:
            session.close()

    def update_payment(self, payload):
        
        validation_result = validate_payment_data(payload, is_update=True)

        if validation_result["status"] != 200:
            return validation_result
        
        session = db.get_session()
        try:
            payment = session.query(CustomerPayment).filter(CustomerPayment.pid == payload["pid"]).first()

            if not payment:
                return {"status": 404, "message": "404 Not Found: Payment ID does not exist."}
            
            payment.amount = payload["amount"]
            payment.payment_type = payload["payment_type"]

            session.commit()
            return {"status": 200, "message": "200 OK: Payment updated successfully."}

        except Exception as e:
            print(f"Update Error: {e}")
            session.rollback()
            return {"status": 500, "message": "500 Internal Server Error: Failed to update."}
        
        finally:
            session.close()

    
    def delete_payment(self, pid):
        session = db.get_session()
        try:
            payment = session.query(CustomerPayment).filter(CustomerPayment.pid == pid).first()

            if not payment:
                return {"status": 409, "message": "409 Conflict: Could not delete."}
            
            session.delete(payment)
            session.commit()
            return {"status": 200, "message": "200 OK: Payment deleted successfully."}
        
        except Exception as e:
            print(f"Delete Error: {e}")
            session.commit()
            return {"status": 500, "message": "500 Internal Server Error: Failed to delete."}
        
        finally:
            session.close()
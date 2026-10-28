from utils.validation import validate_adeona_tables
from models.adeona_tables_model import AdeonaTables
from models.customer_model import Customer
from config.database import db

class AdeonaController:

    def add_new_salary(self, payload):
        validation_result = validate_adeona_tables(payload)
        if validation_result["status"] != 200:
            return validation_result
        
        session = db.get_session()
        try:
            customer_exists = session.query(Customer).filter(Customer.cid == payload["cid"]).first()
            if not customer_exists:
                return {"status": 404, "message": "404 Not Found: Cannot add salary. Customer CID not exist."}
            
            new_salary = AdeonaTables(
                cid=payload["cid"],
                salary=payload["salary"],                
            )
            session.add(new_salary)
            session.commit()
            return {"status": 201, "message": "Created: Salary saved successfully."}
        
        except Exception as e:
            print(f"Database Error: {e}")
            session.rollback()
            return {"status": 500, "message": "Error: Database Faild to save salary."}
        finally:
            session.close()

    def get_all_salary(self):
        session = db.get_session()
        try:
            total = session.query(AdeonaTables).count()
            Asalary = session.query(AdeonaTables).order_by(AdeonaTables.sid.asc()).all()

            data = [
                {
                    "sid": s.sid,
                    "cid": s.cid,
                    "salary": float(s.salary),                
                } for s in Asalary
            ]
            return {"status": 200, "total_count": total, "data": data}
        except Exception as e:
            print(f"Database Error: {e}")
            return {"status": 500, "data": []}
        
        finally:
            session.close()

    def update_salary(self, payload):
        
        validation_result = validate_adeona_tables(payload, is_update=True)

        if validation_result["status"] != 200:
            return validation_result
        
        session = db.get_session()
        try:
            Asalary = session.query(AdeonaTables).filter(AdeonaTables.sid == payload["sid"]).first()

            if not Asalary:
                return {"status": 404, "message": "404 Not Found: Salary ID does not exist."}
            
            Asalary.amount = payload["amount"]
            Asalary.payment_type = payload["payment_type"]

            session.commit()
            return {"status": 200, "message": "200 OK: Payment updated successfully."}

        except Exception as e:
            print(f"Update Error: {e}")
            session.rollback()
            return {"status": 500, "message": "500 Internal Server Error: Failed to update."}
        
        finally:
            session.close()

    
    def delete_salary(self, sid):
        session = db.get_session()
        try:
            Asalary = session.query(AdeonaTables).filter(AdeonaTables.sid == sid).first()

            if not Asalary:
                return {"status": 409, "message": "409 Conflict: Could not delete."}
            
            session.delete(Asalary)
            session.commit()
            return {"status": 200, "message": "200 OK: Salary deleted successfully."}
        
        except Exception as e:
            print(f"Delete Error: {e}")
            session.commit()
            return {"status": 500, "message": "500 Internal Server Error: Failed to delete."}
        
        finally:
            session.close()
import codecs
from sqlalchemy import text
from models.mobile_model import MobileNumber
from config.database import db
from utils.validation import is_valid_mobile

def process_csv_upload(file, wipe_old_data):
    session = db.get_session()

    try:

        if wipe_old_data == "true":
            session.execute(text("TRUNCATE TABLE mobile_numbers RESTART IDENTITY CASCADE;"))
            session.commit()

        stream = codecs.iterdecode(file.stream,'utf-8')

        success_count = 0
        failed_count = 0

        BATCH_SIZE = 10000
        batch = []

        for line in stream:
            mobile_number = line.strip()

            if mobile_number:
                if is_valid_mobile(mobile_number):
                    batch.append({"mobile": mobile_number})
                    success_count += 1
                else:
                    failed_count += 1

            if len(batch) >= BATCH_SIZE:
                session.bulk_insert_mappings(MobileNumber, batch)
                session.commit()
                batch.clear()

        if batch:
            session.bulk_insert_mappings(MobileNumber,batch)
            session.commit()
            
        action = "Replaced" if wipe_old_data == "true" else "Appended"
        return {"status": "success", "message": f"Successfully {action} {success_count} numbers! Skipped {failed_count} invalid rows."}
    
    except Exception as e:
        session.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        session.close()
import csv
import codecs
from sqlalchemy import text
from models.message_models import Message
from config.database import db
from utils.validation import is_valid_mobile, has_required_headers
from utils.ml_manager import ml_model_instance

def process_message_csv_upload(file, wipe_old_data):
    session = db.get_session()

    try:
        if wipe_old_data == "true":
            session.execute(text("TRUNCATE TABLE classified_messages RESTART IDENTITY CASCADE;"))
            session.commit()

        stream = codecs.iterdecode(file.stream, 'utf-8-sig', errors='replace')
        csv_reader = csv.DictReader(stream)

        if not has_required_headers(csv_reader.fieldnames, ['mobile', 'message']):
             return {"status": "error", "message": "CSV must contain 'mobile' and 'message' headers."}    

        success_count = 0
        failed_count = 0
        
        BATCH_SIZE = 100
        batch = []

        for row in csv_reader:
            mobile_number = str(row.get('mobile', '')).strip()
            message_text = str(row.get('message', '')).strip()

            if mobile_number and message_text and is_valid_mobile(mobile_number):

                predicted_category = ml_model_instance.predict_category(message_text)

                clean_prediction = str(predicted_category).strip().lower()

                if clean_prediction in ['transactional', 'label_0', '0']:
                    is_trans = True
                else:
                    is_trans = False

                batch.append({
                    "mobile": mobile_number,
                    "message": message_text,
                    "is_transactional": is_trans
                })
                success_count += 1
            else:
                failed_count += 1
            
            if len(batch) >= BATCH_SIZE:
                session.bulk_insert_mappings(Message, batch)
                session.commit()
                batch.clear()
            
        if batch:
            session.bulk_insert_mappings(Message, batch)
            session.commit()

        action = "Replaced" if wipe_old_data == "true" else "Appended"
        return {"status": "success", "message": f"Successfully {action} and classified {success_count} messages! Skipped {failed_count} invalid rows."}
    
    except Exception as e:
        session.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        session.close()

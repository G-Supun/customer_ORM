from config.database import db 
from sqlalchemy import text

print("Connection Successful!" if db.get_session().execute(text("SELECT 1")).scalar() else "Failed!")

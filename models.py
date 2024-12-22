from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import datetime
# create an object of sqlalchemy, it should be initialized when flask application is created
# and this object should be passed as db variable in app.py
db = SQLAlchemy()

class LanguageStats(db.Model):
    __tablename__ = 'language_stats'

    language_code = db.Column(db.String(10), primary_key=True, index=True)  # language_code is primary key
    main_aps = db.Column(db.Integer)
    main_pages = db.Column(db.Integer)
    main_with_out_scan = db.Column(db.Integer)
    main_with_scan = db.Column(db.Integer)
    not_proofread = db.Column(db.Integer)
    num_of_pages = db.Column(db.Integer)
    page_aps = db.Column(db.Integer)
    problematic = db.Column(db.Integer)
    proofread = db.Column(db.Integer)
    validated = db.Column(db.Integer)
    without_text = db.Column(db.Integer)
    timestamp = db.Column(db.String(100))  # Store timestamp as string
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
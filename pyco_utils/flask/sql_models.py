from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy


class Event():
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    level = db.Column(db.Enum('A', 'B', 'C', 'D'), default='C')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def to_dict(self):
        data = vars(self).copy()
        for k, v in data.items():
            if k.startswith('_'):
                data.pop(k)
        return data

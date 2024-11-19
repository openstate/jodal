from app.extensions import db
from app.models import Column

def delete_user_data(user_id):
    columns = Column.query.filter(Column.user_id==user_id)
    for c in columns:
        db.session.delete(c)
    db.session.commit()

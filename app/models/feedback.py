from sqlalchemy import Column, Integer, String, orm, DATETIME, TEXT

from app.models.base import Base, db

class Feedback(Base):
    id = Column(Integer, primary_key=True)
    uid = Column(Integer)
    create_time = Column(DATETIME)
    title = Column(String(50))
    text = Column(TEXT)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'uid', 'create_time', 'title', 'text']

    @staticmethod
    def feedback(uid, create_time, title, text):
        with db.auto_commit():
            feedback = Feedback()
            feedback.uid = uid
            feedback.create_time = create_time
            feedback.title = title
            feedback.text = text
            db.session.add(feedback)

from sqlalchemy import Column, Integer, String, orm

from app.models.base import Base

# book模型
class Book(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    author = Column(String(30))
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15))
    summary = Column(String(1000))
    image = Column(String(50))

    # 默认的输出字段
    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'title', 'author', 'binding', 'publisher', 'price', 'pages', 'pubdate', 'isbn', 'summary', 'image']
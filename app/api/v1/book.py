from flask import jsonify
from sqlalchemy import or_

from app.libs.redprint import Redprint
#从ginger文件中导入app对象会造成循环导入
from app.libs.token_auth import auth
from app.validators.forms import BookSearchForm
from app.models.book import Book

api = Redprint('book')

@api.route('/search')
def search():
    # url:/v1/book/search?q={}
    form = BookSearchForm().validate_for_api()
    q = '%' + form.q.data + '%'
    # 元类 ORM
    books = Book.query.filter(
        or_(Book.title.like(q), Book.publisher.like(q))).all()
    # 查询中的条件为or_(条件1或条件2);like()模糊查询
    books = [book.hide('summary') for book in books]
    # 隐藏部分字段
    return jsonify(books)

@api.route('/<isbn>/detail')
def detail(isbn):
    # 进入书籍详情页
    book = Book.query.filter_by(isbn=isbn).first_or_404()
    return jsonify(book)
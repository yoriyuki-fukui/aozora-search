import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from typing import List

app = Flask(__name__)

# app.pyファイルがある場所を基準にする
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'library.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- 新しい図書館の設計図を船に教える ---

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    作品名 = db.Column(db.String)
    著者姓 = db.Column(db.String)
    著者名 = db.Column(db.String)
    アクセス数合計 = db.Column(db.Integer)
    著者生年 = db.Column(db.Integer)
    著者没年 = db.Column(db.Integer)
    html_url = db.Column(db.String)

with app.app_context():
    db.create_all()

# 検索画面を見せるための歌
@app.route('/')
def index():
    # 検索画面へ案内する
    return render_template('search.html')

# 検索結果を見せるための、新しい賢い歌
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # フォームから、お客さんの叫び声を受け取る
        title = request.form.get('title_query')
        author_family_name = request.form.get('author_family_name_query')
        author_first_name = request.form.get('author_first_name_query')
        birth = request.form.get('birth_query')
        death = request.form.get('death_query')

        # 賢い倉庫番（SQLAlchemy）に、宝探しを命令する
        query = db.session.query(Book)

        if title:
            query = query.filter(Book.作品名.like(f'%{title}%'))
        if author_family_name:
            query = query.filter(Book.著者姓.like(f'%{author_family_name}%'))
        if author_first_name:
            query = query.filter(Book.著者名.like(f'%{author_first_name}%'))
        if birth:
            query = query.filter(Book.著者生年 >= int(birth))
        if death:
            query = query.filter(Book.著者没年 <= int(death))

        results = query.order_by(Book.アクセス数合計.desc()).all()
        
        return render_template('results.html', results=results)
    
    # GETリクエストの場合は、ただ検索画面を見せる
    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)
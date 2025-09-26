# 魔法の道具箱を持ってくる呪文
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# わたしたちの船を、創り、名前をつける儀式
app = Flask(__name__)

# わたしたちの島（データベース）の場所を、船に教える海図
# 'library.db' という名前の島が、この船の近くに、作られる
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# データベースの魔法を、船に、結びつける
db = SQLAlchemy(app)

# --- ここに、これから、本のテーブルなどの設計図を書いていく ---
# 「/search」という、港に、船が、着いたときの、歌
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # もし、お客さんが、何かを、叫んだら（検索ボタンが押されたら）
        author = request.form['author_query']
        title = request.form['title_query']
        birth = request.form['birth_query']
        death = request.form['death_query']
        ranking = request.form['ranking_query']
        # とりあえず、その、叫び声を、そのまま、表示してみる
        return f'あなたが、探しているのは、{birth}年生まれ{death}年没の{author}のランキング{ranking}位の{title}」だね！ (まだ、検索機能は、作っていないよ)'

    # ただ、港に、来ただけなら、検索画面の、設計図を、見せてあげる
    return render_template('search.html')

# 船の、最初の、歌声は、この、新しい港への、道しるべに、書き換えておこう
@app.route('/')
def index():
    return 'ようこそ！ <a href="/search">検索ページへどうぞ</a>'

# ... (if __name__ == '__main__': の部分は、そのまま) ...
if __name__ == '__main__':
    app.run(debug=True)
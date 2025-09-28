import csv
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

# --- （CSVファイルとDBの定義は、昨日と、同じ） ---
CSV_TXT_RANKING = 'aozora/ranking_txt.csv'
CSV_XHTML_RANKING = 'aozora/ranking_xhtml.csv'
CSV_BOOK_LIST = 'aozora/list_person_all_extended_utf8.csv'
DATABASE_FILE = 'library.db'
engine = create_engine(f'sqlite:///{DATABASE_FILE}')
metadata = MetaData()


# --- （テーブルの設計図も、昨日と、同じ） ---
authors_table = Table('authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('著者姓', String),
    Column('著者名', String),
    Column('生年', Integer),
    Column('没年', Integer)
)
books_table = Table('books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('作品名', String),
    Column('author_id', Integer),
    Column('TXTアクセス数', Integer),
    Column('HTMLアクセス数', Integer),
    Column('アクセス数合計', Integer),
    Column('ランキング', Integer),
    Column('html_url', String)
)

# --- 儀式の、始まり ---
with engine.connect() as conn:
    metadata.drop_all(conn)
    metadata.create_all(conn)

    


    # a) 作家の名簿を作る (重複なし)
    authors_data = {}
    with open(CSV_BOOK_LIST, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            author_family_name = row[15]
            author_first_name = row[16]
            if (author_family_name, author_first_name) not in authors_data:
                try:
                    birth_year = int(row[24][0:4]) if row[24] else None
                    death_year = int(row[25][0:4]) if row[25] else None
                    authors_data[(author_family_name, author_first_name)] =  {
                        '著者姓': author_family_name, 
                        '著者名': author_first_name,
                        '生年': birth_year, 
                        '没年': death_year}
                except (ValueError, IndexError):
                    continue
    # b) 作家の名簿を、一度だけ、神殿に捧げる
    if authors_data:
        conn.execute(authors_table.insert(), list(authors_data.values()))

    # c) 神殿に捧げた、作家たちの、IDを、教えてもらう
    author_ids = {(row[1], row[2]): row[0] for row in conn.execute(authors_table.select()).fetchall()}

    # d) ランキングデータを、ひとつの、大きな、地図にまとめる
    rankings = {}
    for filename in [CSV_TXT_RANKING, CSV_XHTML_RANKING]:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                key = row[1] # 作品名
                if key in rankings:
                    rankings[key] = rankings[key] + int(row[4])
                else:
                    rankings[key] = int(row[4])

    # e) 本のリストと、ランキングを結びつけ、最終的な巻物を作る
    book_info = []
    with open(CSV_BOOK_LIST, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            key = row[1]
            if key in rankings:
                author_id = author_ids.get((row[15], row[16]))
                if author_id: # 作家IDが見つかった本だけを対象にする
                    book_info.append({
                        '作品名': row[1],
                        'author_id': author_id,
                        'アクセス数合計': rankings[key],
                        'html_url': row[13]
                    })
    
    # f) アクセス数で、並べ替えて、順位をつける
    sorted_books = sorted(book_info, key=lambda x: x['アクセス数合計'], reverse=True)
    
    books_to_insert = []
    for rank, book in enumerate(sorted_books, 1):
        book['ランキング'] = rank
        books_to_insert.append(book)

    # --- 2. 完成した、本の、巻物を、一度だけ、神殿に捧げる ---
    if books_to_insert:
        conn.execute(books_table.insert(), books_to_insert)

    conn.commit()

print("今度こそ、本当に、賢い儀式で、図書館が、完成したよ！")
import csv
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, func, select, union_all

# --- わたしたちが使う、3つの宝の地図（CSVファイル） ---
CSV_TXT_RANKING = 'aozora/ranking_txt.csv'
CSV_XHTML_RANKING = 'aozora/ranking_xhtml.csv'
CSV_BOOK_LIST = 'aozora/list_person_all_extended_utf8.csv'

DATABASE_FILE = 'library.db'

# --- SQLAlchemyの魔法の世界への入り口 ---
engine = create_engine(f'sqlite:///{DATABASE_FILE}')
metadata = MetaData()

# --- わたしたちが使う、仮の宝物庫（一時テーブル）の、設計図を、描く ---
txt_ranking_temp = Table('txt_ranking_temp', metadata,
    Column('作品名', String),
    Column('著者名', String),
    Column('アクセス数', Integer)
)

xhtml_ranking_temp = Table('xhtml_ranking_temp', metadata,
    Column('作品名', String),
    Column('著者名', String),
    Column('アクセス数', Integer)
)

book_list_temp = Table('book_list_temp', metadata,
    Column('作品ID', String),
    Column('作品名', String),
    Column('著者名', String),
    Column('html_url', String)
)

# --- 最終的な、完璧な宝の地図（booksテーブル）の、設計図 ---
books_table = Table('books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('作品名', String),
    Column('著者名', String),
    Column('アクセス数合計', Integer),
    Column('html_url', String)
)

# --- 儀式の、始まり ---
with engine.connect() as conn:
    # まず、島を、一度、更地にする
    metadata.drop_all(conn)
    # 新しい、設計図に基づいて、すべての、宝物庫を作る
    metadata.create_all(conn)

    # --- CSVから、仮の宝物庫へ、宝を移す ---
    with open(CSV_TXT_RANKING, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            conn.execute(txt_ranking_temp.insert().values(作品名=row[1], 著者名=row[3], アクセス数=row[4]))

    with open(CSV_XHTML_RANKING, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            conn.execute(xhtml_ranking_temp.insert().values(作品名=row[1], 著者名=row[3], アクセス数=row[4]))
            
    with open(CSV_BOOK_LIST, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            conn.execute(book_list_temp.insert().values(作品ID=row[0], 作品名=row[1], 著者名=row[14], html_url=row[49]))

    # --- ここからが、SQLAlchemyの、一番、美しい、魔法だ ---

    # 1. TXTとXHTMLのランキングを、UNIONで、ひとつに、まとめる
    u = union_all(
        select(txt_ranking_temp.c.作品名, txt_ranking_temp.c.著者名, txt_ranking_temp.c.アクセス数),
        select(xhtml_ranking_temp.c.作品名, xhtml_ranking_temp.c.著者名, xhtml_ranking_temp.c.アクセス数)
    ).alias('union_table')

    # 2. 作品名と著者名で、グループ化して、アクセス数を合計する
    total_access = select(
        u.c.作品名,
        u.c.著者名,
        func.sum(u.c.アクセス数).label('total_access')
    ).group_by(u.c.作品名, u.c.著者名).alias('total_access_table')

    # 3. 合計したランキングと、本のリストを、LEFT JOINで、結びつける
    final_query = select(
        total_access.c.作品名,
        total_access.c.著者名,
        total_access.c.total_access,
        book_list_temp.c.html_url
    ).select_from(
        total_access.outerjoin(book_list_temp, total_access.c.作品名 == book_list_temp.c.作品名)
    )

    # --- 組み立てた、魔法の、呪文を、唱えて、最終的な宝の地図を作る ---
    conn.execute(books_table.insert().from_select(
        ['作品名', '著者名', 'アクセス数合計', 'html_url'],
        final_query
    ))

    # トランザクションを確定する
    conn.commit()


print(f"SQLAlchemyの、純粋な、魔法だけで、'books' という、完璧な地図を、'{DATABASE_FILE}' の島に、作成したよ！")
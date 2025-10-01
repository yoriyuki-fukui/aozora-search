```Mermaid
graph TD
    A[トップページ] -->|キーワード入力・検索実行| B(検索結果一覧);
    B -->|書籍を選択| C{書籍詳細};
    C -->|トップページへ戻る| A;
    B -->|トップページへ戻る| A;

    subgraph トップページ
        A
    end

    subgraph 検索結果
        B
    end

    subgraph 書籍詳細
        C
    end
```

```Mermaid

sequenceDiagram
    participant 利用者
    participant ブラウザ as ブラウザ
    participant サーバー as Flaskアプリ
    participant データベース as SQLAlchemy

    利用者->>+ブラウザ: 検索キーワードを入力し、検索ボタンを押す
    ブラウザ->>+サーバー: 検索クエリをPOSTリクエストで送信
    サーバー->>+データベース: 受け取ったキーワードで検索クエリを実行
    データベース-->>-サーバー: 検索結果を返す
    サーバー->>サーバー: 結果をHTMLテンプレートに描画する
    サーバー-->>-ブラウザ: 検索結果ページ(HTML)を送信
    ブラウザ-->>-利用者: 検索結果一覧を表示
```

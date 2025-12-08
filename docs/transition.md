
```Mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#ffffff',
    'primaryTextColor': '#000000',
    'primaryBorderColor': '#000000',
    'lineColor': '#000000',
    'secondaryColor': '#ffffff',
    'tertiaryColor': '#ffffff',
    'mainBkg': '#ffffff',
    'nodeBorder': '#000000',
    'clusterBkg': '#ffffff',
    'clusterBorder': '#000000',
    'edgeLabelBackground':'#ffffff'
  }
}}%%
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
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'actorBkg': '#ffffff',
    'actorBorder': '#000000',
    'actorTextColor': '#000000',
    'signalColor': '#000000',
    'signalTextColor': '#000000',
    'labelBoxBkgColor': '#ffffff',
    'labelBoxBorderColor': '#000000',
    'noteBkgColor': '#ffffff',
    'noteBorderColor': '#000000',
    'loopTextColor': '#000000',
    'activationBorderColor': '#000000',
    'activationBkgColor': '#ffffff',
    'sequenceNumberColor': '#000000',
    'mainBkg': '#ffffff'
  }
}}%%
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
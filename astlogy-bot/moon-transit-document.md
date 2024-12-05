# トランジット月星座BOTについて
トランジット月星座の位置を把握・計算して、Mastodonに投稿するプログラム。

## 作った理由・目的
Mastodon上でトランジット月星座を確認したかったため。

## ファイル構成
- .env（.gitignore）
  - Mastodonアカウント APIを保管
- astrology_data.py
  - 星座・惑星データを保管しているファイル
- common_calc.py
  - ライブラリ「swisseph」を使って処理するプログラム
  - トランジット10惑星を投稿するプログラムと共通
- moon-transit-document.md
  - このファイル。プログラムの説明ドキュメント
- moon-transit.py
  - プログラム本体

ファイル内の関数・変数については、内部に記載しています。

## どうやって使用・管理するのか
1．.envを作成・MasotodonのAPIを.envに記入する
2. サーバーにswisseph・envライブラリをインストール
3. .envと3つのPythonプログラムを同ディレクトリーにアップロード
4. 3でアップロードしたPythonプログラムのパーミッションを755に変更
5. cronを設定する
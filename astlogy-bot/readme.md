# 西洋占星術BOTについて
- 月星座判定
- トランジット惑星判定
- 今日のアストロダイス運勢判定

上記3つのプログラムを保管している。

## 作った理由・目的
Mastodon上で西洋占星術関連の情報を確認したかったため。

## ファイル構成
- .env（.gitignore）
  - Mastodon API
  - OpenAI API
- astrology_data.py
  - 星座（三区分・四元素）・惑星データを保管しているファイル
- common_calc.py
  - ライブラリ「swisseph」を使って処理するプログラム
  - 各判定プログラムと共通
- readme.md
  - このファイル。プログラムの説明ドキュメント
- moon_transit.py
  - 月星座判定プログラム
- planet_transit.py
  - トランジットの惑星を投稿するプログラム
- today_astrodice.py
  - 今日のアストロダイス運勢を投稿するプログラム
  - OpenAI APIを使用

ファイル内の関数・変数については、内部に記載しています。

## どうやって使用・管理するのか
1. `.env`を作成・MasotodonのAPIを`.env`に記入する
2. サーバーにswisseph・envライブラリをインストール
3. `.env`と3つのPythonプログラムを同ディレクトリーにアップロード
4. 3でアップロードしたPythonプログラムのパーミッションを755に変更
5. cronを設定する
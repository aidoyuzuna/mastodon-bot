# Mastodon Bot
相戸ゆづなが使用するMastodon BOT集です。基本的に1～数ファイルの小さいプログラムなため、プログラムをまとめて管理しています。

## 作ったBOT一覧
- 西洋占星術・月星座BOT（`astrology-bot/moon_transit.py`）
- 西洋占星術・惑星トランジットBOT（`astrology-bot/planet_transit.py`）
- 今日のアストロダイス運勢BOT（`astrology-bot/today_astrodice.py`）
- 飲水リマインダーBOT（`drink_water.py`）

## 依存関係
- 共通: Mastodon.py, python-dotenv
- 占星術系のみ: swisseph
- アストロダイスのみ: openai

## 実行例
```
python astrology-bot/moon_transit.py
python astrology-bot/planet_transit.py
python astrology-bot/today_astrodice.py
python drink_water.py
```

## コメント絵文字一覧
```
👍 ファイル追加  
✨ ファイル更新  
🧹 ファイル削除  
🚚 ファイル移動・ファイル名変更 
🎨 スタイル追加・変更　
🛠️ 設定追加・変更
```

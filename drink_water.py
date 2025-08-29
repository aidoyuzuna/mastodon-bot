import datetime
from dotenv import load_dotenv
import os
import sys
from mastodon import Mastodon, MastodonUnauthorizedError


# 各種APIの読み込み
def initialize_mastodon() -> Mastodon:
    if not all(
        [
            os.environ.get("DRINK_ID"),
            os.environ.get("DRINK_SECRET"),
            os.environ.get("DRINK_TOKEN"),
            os.environ.get("API_URL"),
        ]
    ):
        raise KeyError("Mastodonの必要な環境変数が設定されていません")

    mastodon_api = Mastodon(
        client_id=os.environ.get("DRINK_ID"),
        client_secret=os.environ.get("DRINK_SECRET"),
        access_token=os.environ.get("DRINK_TOKEN"),
        api_base_url=os.environ.get("API_URL"),
    )

    # 認証チェック
    try:
        mastodon_api.me()
    except MastodonUnauthorizedError as e:
        raise MastodonUnauthorizedError(
            "認証エラー: アクセストークンが無効・もしくは読み込み権限がありません。"
        ) from e

    return mastodon_api


def post_water_reminder(mastodon_api: Mastodon, time: datetime.time):
    """MastodonにPostを行う

    Args:
        mastodon_api (Mastodon): MastodonのAPIデータ
        time (datetime.time): 現在の時刻（投稿に使用）
    """
    toot_text = f"{time :%H時%M分}だよ！お水飲んで！ぐびー :ablobcat_drinkwater:"
    print(toot_text)
    mastodon_api.status_post(status=toot_text, visibility="public")


def main():
    # 設定ファイル読み込み
    load_dotenv()
    mastodon = initialize_mastodon()

    now = datetime.datetime.now().time()
    post_water_reminder(mastodon, now)


if __name__ == "__main__":
    main()

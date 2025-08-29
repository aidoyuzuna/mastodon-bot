import datetime
from dotenv import load_dotenv
import os
from mastodon import Mastodon, MastodonUnauthorizedError
from typing import Optional


def initialize_mastodon() -> Mastodon:
    """Mastodon APIを初期化する
    
    環境変数から認証情報を読み取り、Mastodonインスタンスを作成。
    認証チェックも実行する。
    
    Returns:
        Mastodon: 認証済みのMastodonインスタンス
        
    Raises:
        KeyError: 必要な環境変数が設定されていない場合
        MastodonUnauthorizedError: 認証に失敗した場合
    """
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


def create_water_reminder_message(time: datetime.time) -> str:
    """水飲みリマインダーメッセージを作成する（純粋関数）

    Args:
        time (datetime.time): 時刻

    Returns:
        str: 投稿用メッセージ
    """
    return f"{time :%H時%M分}だよ！お水飲んで！ぐびー :ablobcat_drinkwater:"


def post_water_reminder_at_time(
    mastodon_api: Mastodon, current_time: Optional[datetime.time] = None
):
    """指定時刻で水飲みリマインダーを投稿する

    Args:
        mastodon_api (Mastodon): MastodonのAPIデータ
        current_time (datetime.time, optional): 投稿時刻. Noneの場合は現在時刻を使用
    """
    if current_time is None:
        current_time = datetime.datetime.now().time()

    toot_text = create_water_reminder_message(current_time)
    print(toot_text)
    mastodon_api.status_post(status=toot_text, visibility="public")


def run_water_reminder():
    """水飲みリマインダーを実行する（テスト可能な形）"""
    load_dotenv()
    mastodon = initialize_mastodon()
    post_water_reminder_at_time(mastodon)


def main():
    """エントリーポイント"""
    run_water_reminder()


if __name__ == "__main__":
    main()

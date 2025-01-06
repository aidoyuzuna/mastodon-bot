import datetime
from dotenv import load_dotenv
import os
from mastodon import Mastodon


def toot(mastodon_api: Mastodon, time: datetime):
    toot_text = f"{time :%H時%M分}だよ！お水飲んで！ぐびー :ablobcat_drinkwater:"
    print(toot_text)
    mastodon_api.status_post(status=toot_text, visibility="public")


def main():
    # 各種APIの読み込み
    load_dotenv()
    mastodon = Mastodon(
        client_id=os.environ.get("DRINK_ID"),
        client_secret=os.environ.get("DRINK_SECRET"),
        access_token=os.environ.get("DRINK_TOKEN"),
        api_base_url=os.environ.get("API_URL"),
    )

    now = datetime.datetime.now().time()
    toot(mastodon, now)


if __name__ == "__main__":
    main()

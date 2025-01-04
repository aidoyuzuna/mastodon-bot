import datetime
from dotenv import load_dotenv
import os
from mastodon import Mastodon

mastodon = Mastodon(
    client_id=os.environ.get("DRINK_ID"),
    client_secret=os.environ.get("DRINK_SECRET"),
    access_token=os.environ.get("DRINK_TOKEN"),
    api_base_url=os.environ.get("API_URL"),
)


def toot(time):
    toot_text = f"{time}だよ！\nお水飲んで！ぐびー :ablobcat_drinkwater:"
    print(toot_text)
    mastodon.status_post(status=toot_text, visibility="public")


def main():
    now = datetime.datetime.now().time()
    now_format = now.strftime("%H時%M分")
    toot(now_format)


if __name__ == "__main__":
    main()

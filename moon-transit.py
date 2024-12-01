import common_calc
import datetime
from dotenv import load_dotenv
import locale
import os
from mastodon import Mastodon

# 各種APIの読み込み
load_dotenv()
mastodon = Mastodon(
    client_id=os.environ.get("MOON_ID"),
    client_secret=os.environ.get("MOON_SECRET"),
    access_token=os.environ.get("MOON_TOKEN"),
    api_base_url=os.environ.get("API_URL"),
)


def determine_end_time(now: datetime.time) -> datetime:
    """月星座の判定終了時刻を返す
    Args:
        now (datetime.time): 現在の時刻
    Returns:
        datetime: 判定が終わる時刻 (11:59または23:59)
    """

    if now.hour < 12:
        return datetime.datetime(now.year, now.month, now.day, 11, 59, 0)

    else:
        return datetime.datetime(now.year, now.month, now.day, 23, 59, 0)


def create_post_message(start: str, end: str, today: datetime.date) -> str:
    """月星座をMastodonに出力

    Args:
        start (str): 現在の月星座
        end (str): 11:59もしくは23:59時点での月星座
        today (datetime.date): 現在の日時

    Returns:
        str: Mastodonに投稿する内容
    """

    date: str = datetime.datetime.strftime(today, "%Y年%m月%d日（%a）%H時%M分")
    text: str = ""

    if start == end:
        text = f"{date}の月星座ニュースです。\n当面、月星座が{start}のままになります。"

    else:
        text = f"{date}の月星座ニュースです。\n今から12時間以内に、月星座が{start}から{end}に変わります。"

    return text


def main():
    # 日付・タイムゾーン入力
    locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
    today_datetime: datetime = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=9))
    )
    end_datetime: datetime = determine_end_time(today_datetime)

    # 月星座計算
    start_moon: str = common_calc.calculate_planet_position(
        common_calc.convert_to_julian_date(today_datetime), 1
    )

    end_moon: str = common_calc.calculate_planet_position(
        common_calc.convert_to_julian_date(end_datetime), 1
    )

    # 出力
    posttext: str = create_post_message(
        common_calc.determine_sign(start_moon),
        common_calc.determine_sign(end_moon),
        today_datetime,
    )

    print(posttext)

    # mastodon.status_post(
    #    status=posttext,
    #    visibility="public",
    # )


if __name__ == "__main__":
    main()

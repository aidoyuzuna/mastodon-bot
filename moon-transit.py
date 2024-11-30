import common_calc
import datetime
from dotenv import load_dotenv
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


def time_word_calc(now: datetime.time):
    """今の時刻が午前か午後か調べる

    Args:
        now (datetime.time): 今の時刻

    Returns:
        datetime: 11:59もしくは23:59を返す
        str: 午前もしくは午後
    """
    if now < datetime.time(12, 0, 0):
        time = datetime.time(11, 59, 0)
        word = "午前"

    else:
        time = datetime.time(23, 59, 0)
        word = "午後"
    return time, word


def export_mastodon(start: str, end: str, today: datetime.date, time: str):
    """月星座をMastodonに出力

    Args:
        start (str): 現在の月星座
        end (str): 11:59もしくは23:59時点での月星座
        today (datetime.date): 現在の日付
        time (str): 現在の時刻
    """
    date = datetime.datetime.strftime(today, "%Y年%m月%d日")
    posttext = ""

    if start == end:
        posttext = (
            f"{date}{time}の月星座ニュースです。\n今後12時間、{start}になります。"
        )
    else:
        posttext = f"{date}{time}の月星座ニュースです。\n今後12時間以内に{start}から{end}に変わります。"

    print(posttext)

    # mastodon.status_post(
    #    status=posttext,
    #    visibility="public",
    # )


def main():
    # 日付・タイムゾーン入力
    today_date = datetime.date.today()
    now_time = datetime.datetime.now().time()
    timezone_offset = 9

    end_time, time_word = time_word_calc(now_time)

    # 月星座計算
    start_moon = common_calc.calculate_planet_position(
        common_calc.convert_to_julian_date(today_date, now_time, timezone_offset), 1
    )

    end_moon = common_calc.calculate_planet_position(
        common_calc.convert_to_julian_date(today_date, end_time, timezone_offset), 1
    )

    # 出力
    export_mastodon(
        common_calc.determine_sign(start_moon),
        common_calc.determine_sign(end_moon),
        today_date,
        time_word,
    )


if __name__ == "__main__":
    main()

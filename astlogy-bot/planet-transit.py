import astrology_data
import datetime
import common_calc
from dotenv import load_dotenv
import locale
import os
from mastodon import Mastodon

# アカウント設定
load_dotenv()
mastodon = Mastodon(
    client_id=os.environ.get("PLANET_ID"),
    client_secret=os.environ.get("PLANET_SECRET"),
    access_token=os.environ.get("PLANET_TOKEN"),
    api_base_url=os.environ.get("API_URL"),
)


# プリントデバッグ
def print_debug(msg):
    """気になる変数をprint

    Args:
        msg (_type_):デバッグしたい変数
    """
    print(msg)
    print(type(msg))


# ここから下は別のプログラムで使うので今は無視でOK
def retrograde_planet(today: float, yesterday: float):
    """今日と昨日の惑星位置を計算

    Args:
        today (float): 今日の惑星の位置
        yesterday (float): 昨日の惑星の位置

    Returns:
        Boolean: 逆行フラグを返す
    """
    if today > yesterday + 180:
        return True
    elif yesterday > today + 180:
        print(f"elifで計算：今日{today}・昨日{yesterday}→{today + 180}")
        return False
    else:
        return today < yesterday


def export_mastodon_text(today: float, yesterday: float) -> str:
    """Mastodonへのテキストを生成

    Args:
        today (float): 今日のユリウス暦
        yesterday (float): 昨日のユリウス暦

    Returns:
        str: Mastodonへのテキスト
    """
    text: str = ""

    for i in range(10):
        today_transit: float = common_calc.calculate_planet_position(today, i)
        yesterday_transit: float = common_calc.calculate_planet_position(yesterday, i)

        # テキストの追加（逆行があるか否かで文章が変わる）
        if retrograde_planet(today_transit, yesterday_transit):
            text += f"{astrology_data.planet[i]}（逆）：{common_calc.determine_sign(today_transit)}{int(today_transit % 30)}度\n"
        else:
            text += f"{astrology_data.planet[i]}（巡）：{common_calc.determine_sign(today_transit)}{int(today_transit % 30)}度\n"
    return text


def main():
    # 日付とタイムゾーン指定
    locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
    today_datetime: datetime = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=9))
    )
    yesterday_datetime: datetime = today_datetime - datetime.timedelta(days=1)

    # テキストの初期化
    post_text = f"【{today_datetime:%Y年%m月%d日（%a）%H時%M分} 現在のトランジット】\n "

    post_text += export_mastodon_text(
        common_calc.convert_to_julian_date(today_datetime),
        common_calc.convert_to_julian_date(yesterday_datetime),
    )

    # 結果を出力
    # mastodon.status_post(status=post_text, visibility="public")
    print_debug(post_text)


if __name__ == "__main__":
    main()

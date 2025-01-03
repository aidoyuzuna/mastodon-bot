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
def retrograde_planet(today: float, yesterday: float) -> bool:
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


def generate_text_for_mastodon(today: float, yesterday: float) -> str:
    """Mastodonへのテキストを生成

    Args:
        today (float): 今日のユリウス暦
        yesterday (float): 昨日のユリウス暦

    Returns:
        str: Mastodonへのテキスト
    """
    text: str = ""

    # 三区分・四元素のカウント初期化
    cardinal_quality: int = 0
    fixed_quality: int = 0
    mutable_quality: int = 0
    fire_element: int = 0
    earth_element: int = 0
    air_element: int = 0
    water_element: int = 0

    quality = {
        astrology_data.Quality.CARDINAL: 0,
        astrology_data.Quality.FIXED: 0,
        astrology_data.Quality.MUTABLE: 0,
    }

    element = {
        astrology_data.Element.FIRE: 0,
        astrology_data.Element.EARTH: 0,
        astrology_data.Element.AIR: 0,
        astrology_data.Element.WATER: 0,
    }

    for planet in astrology_data.Planet:
        today_transit: float = common_calc.calculate_planet_position(
            today, astrology_data.Planet(planet).index
        )
        yesterday_transit: float = common_calc.calculate_planet_position(
            yesterday, astrology_data.Planet(planet).index
        )

        planet_quarity: float = common_calc.determine_quality(today_transit)
        planet_element: float = common_calc.determine_element(today_transit)

        # 要素のカウントを更新
        quality[planet_quarity] += 1
        element[planet_element] += 1

        # 各要素のカウントを変数に代入
        cardinal_quality = quality[astrology_data.Quality.CARDINAL]
        fixed_quality = quality[astrology_data.Quality.FIXED]
        mutable_quality = quality[astrology_data.Quality.MUTABLE]

        fire_element = element[astrology_data.Element.FIRE]
        earth_element = element[astrology_data.Element.EARTH]
        air_element = element[astrology_data.Element.AIR]
        water_element = element[astrology_data.Element.WATER]

        # テキストの追加（逆行があるか否かで文章が変わる）
        if retrograde_planet(today_transit, yesterday_transit):
            text += f"{astrology_data.Planet(planet).planet_name}：{common_calc.determine_sign(today_transit)}{int(today_transit % 30)}度（逆行）\n"
        else:
            text += f"{astrology_data.Planet(planet).planet_name}：{common_calc.determine_sign(today_transit)}{int(today_transit % 30)}度\n"

    # 三区分・四元素の合計追加
    text += "\n"
    text += f"活動宮：{cardinal_quality} 不動宮：{fixed_quality} 柔軟宮：{mutable_quality}\n"
    text += f"火：{fire_element} 土：{earth_element} 風：{air_element} 水：{water_element}\n"
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

    post_text += generate_text_for_mastodon(
        common_calc.convert_to_julian_date(today_datetime),
        common_calc.convert_to_julian_date(yesterday_datetime),
    )

    # 結果を出力
    # mastodon.status_post(status=post_text, visibility="public")
    print_debug(post_text)


if __name__ == "__main__":
    main()

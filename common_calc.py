import astrology_data
import datetime
import swisseph as swe


def convert_to_julian_date(date: datetime.date, time: datetime.time, timezone: int):
    """日付をユリウス暦に変換する

    Args:
        date (datetime.date): 日付
        time (datetime.time): 時刻
        timezone (int): タイムゾーン

    Returns:
        tuple: ユリウス暦の日付
    """
    utc_time = swe.utc_time_zone(
        date.year, date.month, date.day, time.hour, time.minute, time.second, timezone
    )
    julian_date = swe.utc_to_jd(*utc_time)
    return julian_date


def calculate_planet_position(jul_datetime: tuple, planet_number: int):
    """惑星の位置を計算する

    Args:
        jul_datetime (tuple): ユリウス暦の日付
        planet_number (int): 惑星番号

    Returns:
        tuple: 惑星位置の計算結果
    """

    planet_calc = swe.calc(jul_datetime[0], planet_number)
    return planet_calc


def determine_sign(angle: float):
    """角度から星座を求める

    Args:
        angle (float): 計算した惑星位置の角度

    Raises:
        ValueError: angleが360以下の整数になるか確認

    Returns:
        str: 星座のサイン
    """

    # 360度の円を12等分している。1つの星座につき30度
    idx = int(angle // 30)
    if idx < 0 or idx > 11:
        raise ValueError(
            f"angle は360以下の整数である必要がある: {angle}"
        )  # エラーで原因が分かるようにする

    return astrology_data.zodiac_sign[idx]


# ここから下は別のプログラムで使うので今は無視でOK
def retrograde_planet(today: float, yesterday: float):
    if today > yesterday + 180:
        return True
    else:
        return today < yesterday

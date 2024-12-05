import astrology_data
import datetime
import swisseph as swe


def convert_to_julian_date(import_datetime: datetime.time) -> float:
    """日付をユリウス暦に変換する

    Args:
        date (datetime.date): 日時（タイムゾーンあり）

    Returns:
        float: ユリウス暦の日付
    """

    utc_time = import_datetime.astimezone(datetime.timezone.utc)

    # utc_time: tuple = swe.utc_time_zone(
    #    import_datetime.year,
    #    import_datetime.month,
    #    import_datetime.day,
    #    import_datetime.hour,
    #    import_datetime.minute,
    #    import_datetime.second,
    #    timezone,
    # )

    julian_date: tuple = swe.utc_to_jd(
        utc_time.year,
        utc_time.month,
        utc_time.day,
        utc_time.hour,
        utc_time.minute,
        utc_time.second,
    )
    return julian_date[0]


def calculate_planet_position(jul_datetime: float, planet_number: int) -> float:
    """惑星の位置を計算する

    Args:
        jul_datetime (float): ユリウス暦の日付
        planet_number (int): 惑星番号

    Returns:
        tuple: 惑星位置の計算結果
    """

    planet_calc: tuple = swe.calc(jul_datetime, planet_number)
    return planet_calc[0][0]


def determine_sign(angle: float) -> str:
    """角度から星座を求める

    Args:
        angle (float): 計算した惑星位置の角度

    Raises:
        ValueError: angleが360以下の整数になるか確認

    Returns:
        str: 星座のサイン
    """

    # 360度の円を12等分している。1つの星座につき30度
    idx: int = int(angle // 30)
    if idx < 0 or idx > 11:
        raise ValueError(
            f"angle は360以下の整数である必要がある: {angle}"
        )  # エラーで原因が分かるようにする

    return astrology_data.ZodiacSign(idx).sign_name

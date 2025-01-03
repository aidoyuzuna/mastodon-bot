import astrology_data
import random
import datetime
import locale


def get_current_date():
    """日付を取得する

    Returns:
        date: datetimeで取得した日付
    """

    date = datetime.date.today()
    return date


def generate_seed(current_date: datetime):
    """日付を元にシードを設定する

    Args:
        current_date (datetime): 取得した今日の日付
    """
    seed_num: int = int(current_date.month) * 32 * int(current_date.day)
    random.seed(seed_num)


def roll_dice():
    """さいころを振る

    Returns:
        sign_roll (str): サインのさいころ結果
        house_roll (int): ハウスのさいころ結果
        planet_roll (str): 惑星のさいころ結果
    """
    sign_roll: str = select_sign(random.randint(0, 11))
    house_roll: int = random.randint(1, 12)
    planet_roll: str = select_planet(random.randint(0, 9))

    return (
        sign_roll,
        house_roll,
        planet_roll,
    )


def select_sign(select: int) -> str:
    """ランダムの数値からサインを判定

    Args:
        select (int): ランダムの数値

    Raises:
        ValueError: selectが11以下の整数か確認
        ValueError: selectの数値が星座番号と一致していないか確認

    Returns:
        str: 星座の名前
    """
    if select < 0 or select > 11:
        raise ValueError(
            f"select は11以下の整数である必要がある: {select}"
        )  # エラーで原因が分かるようにする

    for sign in astrology_data.ZodiacSign:
        if sign.index == select:
            return sign.sign_name
    raise ValueError(f"{select} is not a valid ZodiacSign index")


def select_planet(select: int) -> str:
    """ランダムの数値から惑星を判定

    Args:
        select (int): ランダムの数値
    Raises:
        ValueError: selectが9以下の整数か確認
        ValueError: selectの数値が星座番号と一致していないか確認

    Returns:
        str: 惑星の名前
    """
    if select < 0 or select > 9:
        raise ValueError(
            f"select は9以下の整数である必要がある: {select}"
        )  # エラーで原因が分かるようにする

    for sign in astrology_data.Planet:
        if sign.index == select:
            return sign.planet_name
    raise ValueError(f"{select} is not a valid ZodiacSign index")


def main():
    # 日付設定・ランダム生成
    locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
    today = get_current_date()
    generate_seed(today)

    # さいころを振る
    sign_choice, house_choice, planet_choice = roll_dice()

    # 結果を表示・コピー
    result_message = f"{today:%Y年%m月%d日（%a）}の運勢だよ！\n\nサイン：{sign_choice}\nハウス：{house_choice}\n惑星：{planet_choice}\n"
    print(result_message)


if __name__ == "__main__":
    main()

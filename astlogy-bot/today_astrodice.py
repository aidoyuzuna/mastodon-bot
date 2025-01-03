import random
import datetime
import pyperclip

# 星座
sign: tuple[str] = (
    "牡羊座",
    "牡牛座",
    "双子座",
    "蟹座",
    "獅子座",
    "乙女座",
    "天秤座",
    "蠍座",
    "射手座",
    "山羊座",
    "水瓶座",
    "魚座",
)

# 惑星
planet: tuple[str] = (
    "太陽",
    "月",
    "水星",
    "金星",
    "火星",
    "木星",
    "土星",
    "天王星",
    "海王星",
    "冥王星",
)


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
    sign_roll: str = random.choice(sign)
    house_roll: int = random.randint(1, 12)
    planet_roll: str = random.choice(planet)
    return (
        sign_roll,
        house_roll,
        planet_roll,
    )


def main():
    # ランダム生成
    generate_seed(get_current_date())

    # さいころを振る
    sign_choice, house_choice, planet_choice = roll_dice()

    # 結果を表示・コピー
    result_message = f"おはよ～！\n\nサイン：{sign_choice}\nハウス：{house_choice}\n惑星：{planet_choice}\n"
    print(result_message)
    pyperclip.copy(result_message)


if __name__ == "__main__":
    main()

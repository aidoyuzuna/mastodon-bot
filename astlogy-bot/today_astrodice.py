import astrology_data
import datetime
from dotenv import load_dotenv
import locale
from openai import OpenAI
import os
import random
import sys

# 各種APIの読み込み
load_dotenv()
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
chatgpt = OpenAI(api_key=os.environ.get("OPENAI_KEY"))


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


def get_openai_response(sign: str, house: int, planet: str) -> str:
    """openaiに運勢結果を出力させる

    Args:
        sign (str): ランダムで出した星座
        house (int): ランダムで出したハウス
        planet (str): ランダムで出した惑星

    Returns:
        str: chatGPTの出力結果
    """
    question = f"アストロダイスを振った結果「{planet}・{house}ハウス・{sign}」になりました。結果を基に今日の運勢を150文字で読んでください。改行は含めないでください"
    chatgpt_response_message = chatgpt.chat.completions.create(
        model="chatgpt-4o-latest",
        max_tokens=300,
        temperature=0.0,
        messages=[{"role": "user", "content": question}],
    )
    return chatgpt_response_message.choices[0].message.content


def main():
    # 日付設定・ランダム生成
    locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
    today = get_current_date()
    generate_seed(today)

    # さいころを振る
    sign_choice, house_choice, planet_choice = roll_dice()

    # ChatGPTに送る
    chatgpt_result = get_openai_response(sign_choice, house_choice, planet_choice)

    # 結果を表示・コピー
    result_message = f"{today:%Y年%m月%d日（%a）}の運勢です！\n\nサイン：{sign_choice}\nハウス：{house_choice}\n惑星：{planet_choice}\n\n{chatgpt_result}"
    print(result_message)


if __name__ == "__main__":
    main()

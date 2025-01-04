import astrology_data
import datetime
from dotenv import load_dotenv
import locale
from mastodon import Mastodon
from openai import OpenAI
import os
import random
import sys

# 各種APIの読み込み
load_dotenv()
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
chatgpt = OpenAI(api_key=os.environ.get("OPENAI_KEY"))

mastodon = Mastodon(
    client_id=os.environ.get("TODAY_ASTRO_DICE_ID"),
    client_secret=os.environ.get("TODAY_ASTRO_DICE_SECRET"),
    access_token=os.environ.get("TODAY_ASTRO_DICE_TOKEN"),
    api_base_url=os.environ.get("API_URL"),
)


def get_current_date():
    """日付を取得する

    Returns:
        date: datetimeで取得した日付
    """

    date = datetime.date.today()
    return date


def set_seed_by_date(current_date: datetime):
    """日付を元にシードを設定する

    Args:
        current_date (datetime): 取得した今日の日付
    """
    seed_num = current_date.year * 32 * 13 + current_date.month * 32 + current_date.day
    random.seed(seed_num)


def roll_dice():
    """さいころを振る

    Returns:
        sign_roll (str): サインのさいころ結果
        house_roll (int): ハウスのさいころ結果
        planet_roll (str): 惑星のさいころ結果
    """
    sign_roll: str = identify_sign(random.randint(0, 11))
    house_roll: int = random.randint(1, 12)
    planet_roll: str = identify_planet(random.randint(0, 9))

    return (
        sign_roll,
        house_roll,
        planet_roll,
    )


def identify_sign(planet_idx: int) -> str:
    """与えられたインデックスに対応するサインを特定する

    Args:
        planet_idx (int): ランダムの数値

    Raises:
        ValueError: sign_idxが11以下の整数か確認
        ValueError: sign_idxの数値が星座番号と一致していないか確認

    Returns:
        str: 星座の名前
    """
    if planet_idx < 0 or planet_idx > 11:
        raise ValueError(
            f"planet_idx は11以下の整数である必要がある: {planet_idx}"
        )  # エラーで原因が分かるようにする

    for sign in astrology_data.ZodiacSign:
        if sign.index == planet_idx:
            return sign.sign_name
    raise ValueError(f"{planet_idx} is not a valid Planet index")


def identify_planet(planet_idx: int) -> str:
    """与えられたインデックスに対応する惑星を特定する

    Args:
        planet_idx (int): ランダムの数値
    Raises:
        ValueError: planet_idxが9以下の整数か確認
        ValueError: planet_idxの数値が星座番号と一致していないか確認

    Returns:
        str: 惑星の名前
    """
    if planet_idx < 0 or planet_idx > 9:
        raise ValueError(
            f"planet_idx は9以下の整数である必要がある: {planet_idx}"
        )  # エラーで原因が分かるようにする

    for sign in astrology_data.Planet:
        if sign.index == planet_idx:
            return sign.planet_name
    raise ValueError(f"{planet_idx} is not a valid ZodiacSign index")


def get_openai_response(sign: str, house: int, planet: str) -> str:
    """openaiに運勢結果を出力させる

    Args:
        sign (str): ランダムで出した星座
        house (int): ランダムで出したハウス
        planet (str): ランダムで出した惑星

    Returns:
        str: chatGPTの出力結果
    """
    question = f"アストロダイスを振った結果「{planet}・{house}ハウス・{sign}」になりました。結果を基に今日の運勢を120文字で読んでください。改行とハウス・サイン・惑星は出力しないこと。"
    chatgpt_response_message = chatgpt.chat.completions.create(
        model="chatgpt-4o-latest",
        max_tokens=250,
        temperature=0.0,
        messages=[{"role": "user", "content": question}],
    )
    return chatgpt_response_message.choices[0].message.content


def main():
    # 日付設定・ランダム生成
    locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
    today = get_current_date()
    set_seed_by_date(today)

    # さいころを振る
    sign_choice, house_choice, planet_choice = roll_dice()

    # ChatGPTに送る
    chatgpt_result = get_openai_response(sign_choice, house_choice, planet_choice)

    # 結果を表示・コピー
    result_message = f"【{today:%Y年%m月%d日（%a）}の運勢】\n{planet_choice}・{sign_choice}・{house_choice}ハウス\n\n{chatgpt_result}"
    print(result_message)

    # mastodon.status_post(
    #    status=result_message,
    #    visibility="unlisted",
    # )


if __name__ == "__main__":
    main()

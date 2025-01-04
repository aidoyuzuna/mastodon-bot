import astrology_data
import datetime
from dotenv import load_dotenv
import locale
from mastodon import Mastodon, MastodonUnauthorizedError
from openai import OpenAI, OpenAIError
import os
import random
import sys
from typing import Optional


def initialize_mastodon() -> Optional[Mastodon]:
    """Mastodon APIクライアントを初期化し、認証を行います。

    Returns:
        Optional[Mastodon]: 認証済みのMastodon APIクライアントオブジェクト。

    Raises:
        KeyError: 必要な環境変数が設定されていない場合
        MastodonUnauthorizedError: アクセストークンが無効または読み込み権限がない
    """

    if not all(
        [
            os.environ.get("TODAY_ASTRO_DICE_ID"),
            os.environ.get("TODAY_ASTRO_DICE_SECRET"),
            os.environ.get("TODAY_ASTRO_DICE_TOKEN"),
            os.environ.get("API_URL"),
        ]
    ):
        raise KeyError("Mastodonの必要な環境変数が設定されていません")

    mastodon_api = Mastodon(
        client_id=os.environ["TODAY_ASTRO_DICE_ID"],
        client_secret=os.environ["TODAY_ASTRO_DICE_SECRET"],
        access_token=os.environ["TODAY_ASTRO_DICE_TOKEN"],
        api_base_url=os.environ["API_URL"],
    )

    # 認証チェック
    try:
        mastodon_api.me()
    except MastodonUnauthorizedError as e:
        raise MastodonUnauthorizedError(
            "認証エラー: アクセストークンが無効・もしくは読み込み権限がありません。"
        ) from e

    return mastodon_api


def initialize_openai() -> Optional[OpenAI]:
    """OpenAI APIのenv読み込み判定

    Returns:
        Optional[OpenAI]: Open AI APIの環境変数
    """
    if not all([os.environ.get("OPENAI_KEY")]):
        raise KeyError("OpenAi APIの必要な環境変数が設定されていません")

    return OpenAI(api_key=os.environ.get("OPENAI_KEY"))


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
        raise ValueError(f"planet_idx は11以下の整数である必要がある: {planet_idx}")

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
    raise ValueError(f"{planet_idx} is not a valid Planet index")


def get_openai_response(sign: str, house: int, planet: str, openai_key: OpenAI) -> str:
    """openaiに運勢結果を出力させる

    Args:
        sign (str): ランダムで出した星座
        house (int): ランダムで出したハウス
        planet (str): ランダムで出した惑星

    Returns:
        str: chatGPTの出力結果
    """
    question = f"アストロダイスを振った結果「{planet}・{house}ハウス・{sign}」になりました。結果を基に今日の運勢を120文字で読んでください。改行とハウス・サイン・惑星は出力しないこと。"
    try:
        chatgpt_response_message = openai_key.chat.completions.create(
            model="chatgpt-4o-latest",
            max_tokens=150,
            temperature=0.0,
            messages=[{"role": "user", "content": question}],
        )
    except OpenAIError as e:
        raise OpenAIError("OpenAI APIのAPI残高をチェックしてください。") from e
    return chatgpt_response_message.choices[0].message.content


def main():
    # 各種APIの読み込み
    load_dotenv()
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

    mastodon = initialize_mastodon()
    openai = initialize_openai()

    # 日付設定・ランダム生成
    locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
    today = datetime.date.today()
    set_seed_by_date(today)

    # さいころを振る
    sign_choice, house_choice, planet_choice = roll_dice()

    # ChatGPTに送る
    chatgpt_result = get_openai_response(
        sign_choice, house_choice, planet_choice, openai
    )

    # 結果を表示・コピー
    result_message = f"【{today:%Y年%m月%d日（%a）}の運勢】\n{planet_choice}・{sign_choice}・{house_choice}ハウス\n\n{chatgpt_result}"
    print(result_message)

    mastodon.status_post(
        status=result_message,
        visibility="unlisted",
    )


if __name__ == "__main__":
    main()

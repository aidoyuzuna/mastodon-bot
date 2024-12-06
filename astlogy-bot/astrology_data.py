from enum import Enum


class ZodiacSign(Enum):
    ARIES = 0, "牡羊座"
    TAURUS = 1, "牡牛座"
    GEMINI = 2, "双子座"
    CANCER = 3, "蟹座"
    LEO = 4, "獅子座"
    VIRGO = 5, "乙女座"
    LIBRA = 6, "天秤座"
    SCORPIO = 7, "蠍座"
    SAGITTARIUS = 8, "射手座"
    CAPRICORN = 9, "山羊座"
    AQUARIUS = 10, "水瓶座"
    PISCES = 11, "魚座"

    def __init__(self, index: int, name: str):
        self.index: int = index
        self.sign_name: str = name


class Planet(Enum):
    SUN = 0, "太陽"
    MOON = 1, "月"
    MERCURY = 2, "水星"
    VENUS = 3, "金星"
    MARS = 4, "火星"
    JUPITER = 5, "木星"
    SATURN = 6, "土星"
    URANUS = 7, "天王星"
    NEPTUNE = 8, "海王星"
    PLUTO = 9, "冥王星"

    def __init__(self, index: int, name: str):
        self.index: int = index
        self.planet_name: str = name

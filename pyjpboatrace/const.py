from datetime import time

# TODO make them constant

# URL
# TODO format
BOATRACEJP_MAIN_URL = 'https://www.boatrace.jp/'
BOATRACEJP_LOGIN_URL = f'{BOATRACEJP_MAIN_URL}owpc/pc/login?authAfterUrl=/'
BOATRACEJP_LOGOUT_URL = f'{BOATRACEJP_MAIN_URL}owpc/logout'
BOATRACEJP_BASE_URL = f"{BOATRACEJP_MAIN_URL}owpc/pc/race"


IBMBRACEORJP = ''.join([
    f'{BOATRACEJP_MAIN_URL}',
    'owpc/VoteBridgeNew.jsp?',
    'param=H0JS00000stContens'
    '&kbn=1'
    '&voteActionUrl=/owpc/pc/site/index.html'
])

# TIME
BOATRACE_START = time(hour=8, minute=30)  # 8:30
BOATRACE_END = time(hour=20, minute=45)  # 20:45

# RACE
# # races
NUM_RACES = 12  # # of races in a stadium on a day
# # boats
NUM_BOATS = 6
BOATS_GEN = range(1, NUM_BOATS+1)
# # stadiums
STADIUMS_MAP = tuple((i+1, stadium) for i, stadium in enumerate([
    "桐生",
    "戸田",
    "江戸川",
    "平和島",
    "多摩川",
    "浜名湖",
    "蒲郡",
    "常滑",
    "津",
    "三国",
    "びわこ",
    "住之江",
    "尼崎",
    "鳴門",
    "丸亀",
    "児島",
    "宮島",
    "徳山",
    "下関",
    "若松",
    "芦屋",
    "福岡",
    "唐津",
    "大村",
]))
NUM_STADIUMS = len(STADIUMS_MAP)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OKX 멀티 타임프레임(15분/30분/1시간) 3연속 캔들 패턴 감지 → HTML 출력
======================================================================
워치리스트에 등록된 종목들의 OKX 무기한선물(SWAP) 캔들을 여러 타임프레임
(기본: 15분봉, 30분봉, 1시간봉)에서 각각 "최근 3개"(진행 중인 캔들 포함)를
읽어서 다음 두 패턴 중 하나가 나오면 감지합니다.

    양봉 → 음봉 → 음봉   (양음음)
    음봉 → 양봉 → 양봉   (음양양)

타임프레임별로 감지된 종목만, 캔들차트(20MA/200MA 표시)를 HTML에
타임프레임 섹션으로 구분해서 출력합니다. (15분봉 결과 → 30분봉 결과 →
1시간봉 결과 순으로 세로 섹션 배치. 차트를 탭 뒤에 숨기면 Lightweight
Charts가 컨테이너 width=0 상태에서 초기화되어 깨지기 때문에, 탭 대신
섹션을 위아래로 쌓는 방식을 씁니다.)

차트는 OKX에서 받아온 실제 캔들 데이터를 HTML 파일 안에 그대로 넣고
Lightweight Charts(오픈소스, 캔버스 렌더링)로 그리는 방식이라 파일을 더블
클릭해서 file:// 로 열어도(=인터넷 위젯 iframe 없이도) 항상 정상적으로
보입니다. Windows 작업 스케줄러로 15분마다 실행하는 걸 전제로 만들었습니다
(매 실행마다 같은 파일을 덮어씁니다).

── 사전 준비 ──────────────────────────────────────────
1) 설치:
    pip install requests python-dotenv

2) 워치리스트 설정 (둘 중 편한 방식 사용, 우선순위는 .env가 위):

   방법 A) .env 파일 (스크립트와 같은 폴더에 .env 생성):
       WATCHLIST=BTCUSDT.P,ETHUSDT.P,SOLUSDT.P,TSLAUSDT.P
       # (선택) OUTPUT_DIR=D:\\GPTBITCOIN\\BULLKING\\crypto_charts_web
       # (선택) SECOND_OUTPUT_DIR=E:\\Trader_KIM   ← 결과 HTML을 추가로 저장할 경로
       # (선택) TIMEFRAMES=15m,30m,1H     ← 감지할 타임프레임 목록 (콤마 구분)
       # (선택) REQUEST_DELAY_SEC=0.15
       # (선택) CHART_VISIBLE_CANDLES=50   ← 차트 화면에 보이는 캔들 개수 (기본 50)

   방법 B) pattern_watchlist.txt (스크립트를 한 번 실행하면 자동 생성됨):
       한 줄에 하나씩 TradingView 심볼 형태(예: BTCUSDT.P)로 적으면 됨.
       # 로 시작하는 줄은 주석 처리됨.

   .env에 WATCHLIST가 있으면 그게 항상 우선이고, 없을 때만
   pattern_watchlist.txt를 읽습니다.

3) 타임프레임 커스터마이즈:
   기본값은 15분봉/30분봉/1시간봉 3종입니다. .env에
       TIMEFRAMES=15m,1H,4H
   처럼 지정하면 원하는 조합으로 바꿀 수 있습니다.
   OKX bar 코드 표기: 1m,3m,5m,15m,30m,1H,2H,4H,6H,12H,1D,1W,1M 등
   (시간 단위 이상은 대문자 H/D/W/M, 분 단위는 소문자 m — OKX API 규칙)

4) Windows 작업 스케줄러 등록 (예시):
    프로그램/스크립트: C:\\Python313\\python.exe
    인수 추가:        "D:\\GPTBITCOIN\\BULLKING\\okx_3candle_pattern_multi_tf.py"
    트리거:            15분마다 반복
    (여러 타임프레임을 한 번에 스캔하지만, 실제 신호 발생 주기가 가장 짧은
     타임프레임인 15분봉에 맞춰 실행하면 됩니다. 30분/1시간봉은 같은 캔들이
     계속 반복 감지될 수 있는데, 이는 정상 동작입니다 — 진행 중인 캔들
     기준이라 그렇습니다.)

5) 결과 파일:
    D:\\GPTBITCOIN\\BULLKING\\crypto_charts_web\\okx_3candle_pattern.html
    E:\\Trader_KIM\\okx_3candle_pattern.html   ← 동일 내용이 여기에도 저장됩니다
    (매번 덮어쓰므로 브라우저에서 새로고침만 하면 최신 결과가 보입니다)
"""

import os
import time
import json
from datetime import datetime, timezone, timedelta

import requests
from dotenv import load_dotenv

# ══════════════════════════════════════════════════════════
# .env 로드
# ══════════════════════════════════════════════════════════
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
for _p in [os.path.join(_SCRIPT_DIR, ".env"), os.path.join(os.getcwd(), ".env")]:
    if os.path.isfile(_p):
        load_dotenv(_p, override=True)
        print(f"  [.env] 로드: {_p}")
        break

# ══════════════════════════════════════════════════════════
# 설정
# ══════════════════════════════════════════════════════════
OUTPUT_DIR  = os.getenv("OUTPUT_DIR", r"D:\GPTBITCOIN\BULLKING\crypto_charts_web")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "okx_3candle_pattern.html")
LOG_FILE = os.path.join(OUTPUT_DIR, "okx_3candle_pattern_log.csv")

# ── 두 번째 저장 경로 (결과 HTML을 한 군데 더 저장) ─────────
# .env에 SECOND_OUTPUT_DIR=... 로 덮어쓸 수 있음. 기본값은 E:\Trader_KIM.
# 빈 문자열("")로 설정하면 두 번째 저장을 건너뜁니다.
SECOND_OUTPUT_DIR = os.getenv("SECOND_OUTPUT_DIR", r"E:\Trader_KIM")
SECOND_OUTPUT_FILE = (
    os.path.join(SECOND_OUTPUT_DIR, "okx_3candle_pattern.html")
    if SECOND_OUTPUT_DIR else None
)

WATCHLIST_ENV   = os.getenv("WATCHLIST", "").strip()
WATCHLIST_FILE  = os.path.join(_SCRIPT_DIR, "pattern_watchlist.txt")

# ── 멀티 타임프레임 설정 ──────────────────────────────────
# .env의 TIMEFRAMES=15m,30m,1H 형태로 덮어쓸 수 있음 (OKX bar 코드 그대로 사용)
_TIMEFRAMES_ENV = os.getenv("TIMEFRAMES", "").strip()
if _TIMEFRAMES_ENV:
    BARS = [b.strip() for b in _TIMEFRAMES_ENV.split(",") if b.strip()]
else:
    BARS = ["15m", "30m", "1H"]

# 화면/로그에 보여줄 한글 라벨 (없는 bar 코드는 코드 그대로 표시)
BAR_LABEL = {
    "1m": "1분봉", "3m": "3분봉", "5m": "5분봉", "15m": "15분봉", "30m": "30분봉",
    "1H": "1시간봉", "2H": "2시간봉", "4H": "4시간봉", "6H": "6시간봉", "12H": "12시간봉",
    "1D": "일봉", "1W": "주봉", "1M": "월봉",
}

CANDLE_COUNT = int(os.getenv("CANDLE_COUNT", "3") or "3")       # 패턴 판별에 쓸 캔들 개수 (진행 중 캔들 포함)
REQUEST_DELAY_SEC = float(os.getenv("REQUEST_DELAY_SEC", "0.15") or "0.15")  # API 호출 간 딜레이
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10") or "10")

# 차트에 그릴 히스토리 캔들 개수 (200MA를 제대로 그리려면 최소 200개 이상 필요.
# OKX candles 엔드포인트 1회 호출 한도가 300이라 기본값을 300으로 둠)
CHART_HISTORY_COUNT = int(os.getenv("CHART_HISTORY_COUNT", "300") or "300")

# 차트에 "보이는" 캔들 개수 (MA200 계산용 데이터는 CHART_HISTORY_COUNT만큼
# 그대로 유지하고, 화면 초기 확대 범위만 최근 이 개수만큼으로 좁힘)
CHART_VISIBLE_CANDLES = int(os.getenv("CHART_VISIBLE_CANDLES", "50") or "50")

KST = timezone(timedelta(hours=9))

# 스크린샷에서 확인된 종목 (TradingView 심볼 표기, OKX 기준)
# → pattern_watchlist.txt 가 없을 때만 이 기본값으로 파일을 새로 만듭니다.
DEFAULT_WATCHLIST = [
    "ETHUSDT.P",
    "BTCUSDT.P",
    "ONDOUSDT.P",
    "SOLUSDT.P",
    "SNDKUSDT.P",
    "CRCLUSDT.P",
    "SKHYUSDT.P",
    "TSLAUSDT.P",
    "AAPLUSDT.P",
    "SPYUSDT.P",
    "MSTRUSDT.P",
    "GOOGLUSDT.P",
    "SOXLUSDT.P",
    "NVDAUSDT.P",
    "QQQUSDT.P",
    "XAUUSDT.P",
    "MUUSDT.P",
    "AMDUSDT.P",
    "PLTRUSDT.P",
    "EWYUSDT.P",
]

# TradingView 심볼(예: "BTCUSDT.P") → OKX instId(예: "BTC-USDT-SWAP") 매핑이
# 일반 규칙(뒤에서 USDT 떼고 "-USDT-SWAP" 붙이기)으로 안 맞는 특수 종목이 있으면
# 여기에 직접 추가해서 덮어쓸 수 있습니다. 예: {"XAUUSDT.P": "XAUT-USDT-SWAP"}
OKX_INSTID_OVERRIDE = {
    # "심볼.P": "OKX-INST-ID",
}


# ══════════════════════════════════════════════════════════
# 워치리스트 로드
# ══════════════════════════════════════════════════════════
def load_watchlist():
    if WATCHLIST_ENV:
        symbols = [s.strip().upper() for s in WATCHLIST_ENV.split(",") if s.strip()]
        if symbols:
            print(f"  [워치리스트] .env WATCHLIST 사용 ({len(symbols)}종목)")
            return symbols

    if not os.path.isfile(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, "w", encoding="utf-8") as f:
            f.write("# 한 줄에 종목 하나씩 (TradingView 심볼 형태, 예: BTCUSDT.P)\n")
            f.write("# '#'으로 시작하는 줄은 무시됩니다.\n")
            for sym in DEFAULT_WATCHLIST:
                f.write(sym + "\n")
        print(f"  [워치리스트] {WATCHLIST_FILE} 를 기본값으로 새로 생성했습니다.")
        return list(DEFAULT_WATCHLIST)

    symbols = []
    with open(WATCHLIST_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            symbols.append(line.upper())
    return symbols


def tv_symbol_to_okx_instid(tv_symbol: str) -> str:
    """'BTCUSDT.P' → 'BTC-USDT-SWAP'"""
    if tv_symbol in OKX_INSTID_OVERRIDE:
        return OKX_INSTID_OVERRIDE[tv_symbol]

    sym = tv_symbol.strip().upper()
    if sym.endswith(".P"):
        sym = sym[:-2]

    if sym.endswith("USDT"):
        base = sym[:-4]
    elif sym.endswith("USDC"):
        base = sym[:-4]
    elif sym.endswith("USD"):
        base = sym[:-3]
    else:
        base = sym  # 규칙에 안 맞으면 그대로 사용 (OKX_INSTID_OVERRIDE로 직접 지정 권장)

    return f"{base}-USDT-SWAP"


def bar_label(bar: str) -> str:
    return BAR_LABEL.get(bar, bar)


# ══════════════════════════════════════════════════════════
# OKX 캔들 조회 + 패턴 판별
# ══════════════════════════════════════════════════════════
_session = requests.Session()


def fetch_okx_candles(inst_id: str, bar: str, limit: int, min_required: int = None):
    """
    OKX 공개 캔들 API 호출.
    반환값은 시간 오름차순(과거→현재)으로 정렬된 캔들 리스트.
    마지막 원소가 '진행 중' 캔들일 수 있음 (confirm == '0').

    min_required: 이 개수보다 적게 오면 에러로 취급 (기본값은 limit과 동일 —
    패턴 판별용 호출처럼 정확한 개수가 꼭 필요한 경우). 차트용 히스토리처럼
    "있는 만큼만 받아도 되는" 호출은 min_required를 낮게 지정한다.
    """
    if min_required is None:
        min_required = limit

    url = "https://www.okx.com/api/v5/market/candles"
    params = {"instId": inst_id, "bar": bar, "limit": str(limit)}

    resp = _session.get(url, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    payload = resp.json()

    if payload.get("code") != "0":
        raise RuntimeError(f"OKX API 오류: {payload.get('code')} {payload.get('msg')}")

    rows = payload.get("data", [])
    if len(rows) < min_required:
        raise RuntimeError(f"캔들 데이터 부족 (received={len(rows)}, need>={min_required})")

    # OKX는 최신순으로 반환 → 과거순으로 뒤집기
    rows_chrono = list(reversed(rows))

    candles = []
    for row in rows_chrono:
        # row = [ts, open, high, low, close, vol, volCcy, volCcyQuote, confirm]
        ts, o, h, l, c = row[0], row[1], row[2], row[3], row[4]
        confirm = row[8] if len(row) > 8 else "1"
        candles.append({
            "ts": int(ts),
            "open": float(o),
            "high": float(h),
            "low": float(l),
            "close": float(c),
            "closed": confirm == "1",
        })
    return candles


def compute_sma(closes, length):
    """단순이동평균. 앞부분 length-1개는 값을 계산할 수 없으므로 None."""
    out = []
    running_sum = 0.0
    for i, v in enumerate(closes):
        running_sum += v
        if i >= length:
            running_sum -= closes[i - length]
        out.append(running_sum / length if i >= length - 1 else None)
    return out


def candle_type(c):
    if c["close"] > c["open"]:
        return "bull"
    if c["close"] < c["open"]:
        return "bear"
    return "flat"


def detect_pattern(candles):
    """
    candles: [oldest, middle, newest] 3개.
    반환: ("bull_bear_bear" | "bear_bull_bull") or None
    """
    types = [candle_type(c) for c in candles]
    if types == ["bull", "bear", "bear"]:
        return "bull_bear_bear"
    if types == ["bear", "bull", "bull"]:
        return "bear_bull_bull"
    return None


PATTERN_LABEL = {
    "bull_bear_bear": "양봉 · 음봉 · 음봉",
    "bear_bull_bull": "음봉 · 양봉 · 양봉",
}
PATTERN_COLOR = {
    "bull_bear_bear": "#ef5350",   # 상승 후 꺾이는 흐름 → 붉은 계열로 표시(숏 관점 참고용)
    "bear_bull_bull": "#26a69a",   # 하락 후 꺾이는 흐름 → 녹색 계열로 표시(롱 관점 참고용)
}


def compute_two_candle_swing_pct(m):
    """
    패턴을 이루는 마지막 2개 캔들(2봉전·현재)의 고가/저가를 기준으로 한
    스윙 변동율을 계산한다.

    - 양음음(bull_bear_bear, 마지막 2봉이 음봉·음봉 = 하락 스윙):
      2봉전 캔들의 고가 → 현재 캔들의 저가  →  (저가-고가)/고가 × 100  (보통 음수)
    - 음양양(bear_bull_bull, 마지막 2봉이 양봉·양봉 = 상승 스윙):
      2봉전 캔들의 저가 → 현재 캔들의 고가  →  (고가-저가)/저가 × 100  (보통 양수)
    """
    c1, c2 = m["candles"][1], m["candles"][2]   # 2봉전, 현재(진행중 포함)
    if m["pattern"] == "bull_bear_bear":
        start, end = c1["high"], c2["low"]
    else:  # bear_bull_bull
        start, end = c1["low"], c2["high"]
    if not start:
        return 0.0
    return (end - start) / start * 100


def fmt_price(p):
    if p >= 10000: return f"{p:,.1f}"
    if p >= 1000:  return f"{p:,.2f}"
    if p >= 1:     return f"{p:.4f}"
    if p >= 0.01:  return f"{p:.5f}"
    return f"{p:.7f}"


def build_pattern_summary_js(all_results, run_time_kst):
    """
    index.html(워치리스트 허브 페이지)의 종목 카드에 패턴 배지를 표시하기 위한
    경량 데이터 파일. okx_3candle_pattern.html 전체(차트 데이터 포함, 수백 KB)를
    그대로 읽게 하면 무겁고, 로컬 file:// 환경에서는 fetch()로 다른 로컬 파일을
    읽는 것 자체가 브라우저에 막히는 경우가 많다. 그래서 카드에 필요한 최소
    정보(종목/타임프레임/패턴/2봉 변동율)만 뽑아서
        window.PATTERN_SUMMARY = {...};
    형태의 순수 JS 파일로 저장해두면, index.html에서 <script src="pattern_summary.js">
    로 불러오는 것만으로 항상(=로컬 파일이라도) 정상 동작한다.
    """
    by_symbol = {}
    for result in all_results:
        for m in result["matched"]:
            sym_disp = m["symbol"].replace("USDT.P", "")
            change_pct = compute_two_candle_swing_pct(m)
            entry = {
                "bar": m["bar"],
                "barLabel": bar_label(m["bar"]),
                "pattern": m["pattern"],
                "patternLabel": PATTERN_LABEL[m["pattern"]],
                "changePct": round(change_pct, 2),
            }
            by_symbol.setdefault(sym_disp, []).append(entry)

    payload = {
        "generatedAt": run_time_kst,
        "bySymbol": by_symbol,
    }
    return "window.PATTERN_SUMMARY = " + json.dumps(payload, ensure_ascii=False) + ";\n"


# ══════════════════════════════════════════════════════════
# 스캔 실행 (타임프레임 1개 기준)
# ══════════════════════════════════════════════════════════
def scan_watchlist_for_bar(symbols, bar):
    matched = []
    errors = []

    for tv_sym in symbols:
        inst_id = tv_symbol_to_okx_instid(tv_sym)
        try:
            candles = fetch_okx_candles(inst_id, bar=bar, limit=CANDLE_COUNT)
            pattern = detect_pattern(candles)
            if pattern:
                # 패턴이 감지된 종목만 차트용 히스토리를 추가로 받아온다
                try:
                    chart_candles = fetch_okx_candles(
                        inst_id, bar=bar, limit=CHART_HISTORY_COUNT, min_required=30
                    )
                except Exception:
                    chart_candles = candles  # 실패하면 최소한 패턴판별용 3개라도 사용
                time.sleep(REQUEST_DELAY_SEC)

                closes = [c["close"] for c in chart_candles]
                ma20 = compute_sma(closes, 20)
                ma200 = compute_sma(closes, 200)

                matched.append({
                    "symbol": tv_sym,
                    "inst_id": inst_id,
                    "bar": bar,
                    "pattern": pattern,
                    "candles": candles,
                    "chart_candles": chart_candles,
                    "ma20": ma20,
                    "ma200": ma200,
                })
                print(f"  ✅ [{bar_label(bar)}] {tv_sym:<14} {inst_id:<20} → {PATTERN_LABEL[pattern]}")
            else:
                print(f"     [{bar_label(bar)}] {tv_sym:<14} {inst_id:<20} → 패턴 없음")
        except Exception as e:
            errors.append((tv_sym, inst_id, str(e)))
            print(f"  ⚠️  [{bar_label(bar)}] {tv_sym:<14} {inst_id:<20} → 오류: {e}")

        time.sleep(REQUEST_DELAY_SEC)

    return matched, errors


def scan_all_timeframes(symbols, bars):
    """
    타임프레임별로 순차 스캔. 반환값:
    [
      {"bar": "15m", "matched": [...], "errors": [...], "scanned": N},
      ...
    ]
    """
    results = []
    for bar in bars:
        print("-" * 60)
        print(f"  ▶ {bar_label(bar)}({bar}) 스캔 시작 — {len(symbols)}종목")
        matched, errors = scan_watchlist_for_bar(symbols, bar)
        results.append({
            "bar": bar,
            "matched": matched,
            "errors": errors,
            "scanned": len(symbols),
        })
    return results


def append_log(all_results, run_time_kst):
    any_matched = any(r["matched"] for r in all_results)
    if not any_matched:
        return
    is_new = not os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", encoding="utf-8-sig", newline="") as f:
        if is_new:
            f.write("run_time_kst,timeframe,symbol,inst_id,pattern\n")
        for r in all_results:
            for m in r["matched"]:
                f.write(f"{run_time_kst},{bar_label(m['bar'])},{m['symbol']},{m['inst_id']},{PATTERN_LABEL[m['pattern']]}\n")


# ══════════════════════════════════════════════════════════
# HTML 빌더
# ══════════════════════════════════════════════════════════
def build_chart_payload(m):
    """Lightweight Charts에 넘길 캔들/MA 데이터를 dict로 변환 (JSON 직렬화는 build_html에서 한 번에)."""
    chart_candles = m["chart_candles"]
    ma20 = m["ma20"]
    ma200 = m["ma200"]

    candle_points = [
        {
            "time": c["ts"] // 1000,   # ms → sec (UTCTimestamp)
            "open": c["open"], "high": c["high"], "low": c["low"], "close": c["close"],
        }
        for c in chart_candles
    ]
    ma20_points = [
        {"time": c["ts"] // 1000, "value": v}
        for c, v in zip(chart_candles, ma20) if v is not None
    ]
    ma200_points = [
        {"time": c["ts"] // 1000, "value": v}
        for c, v in zip(chart_candles, ma200) if v is not None
    ]

    # 패턴 판별에 쓰인 마지막 3개 캔들 위치에 마커 표시
    last3_ts = {c["ts"] // 1000 for c in m["candles"]}
    markers = []
    for c in chart_candles:
        t = c["ts"] // 1000
        if t in last3_ts:
            markers.append({
                "time": t,
                "position": "belowBar" if candle_type(c) == "bull" else "aboveBar",
                "color": PATTERN_COLOR[m["pattern"]],
                "shape": "circle",
                "text": "",
            })

    return {
        "candles": candle_points,
        "ma20": ma20_points,
        "ma200": ma200_points,
        "markers": markers,
        "instId": m["inst_id"],   # 실시간 WS 구독용 (OKX instId)
        "bar": m["bar"],          # 실시간 WS 구독용 (candle{bar} 채널명 조합용)
    }


def build_card_html(m, chart_id, card_id):
    sym = m["symbol"]
    pattern = m["pattern"]
    candles = m["candles"]
    color = PATTERN_COLOR[pattern]
    tv_link_sym = f"OKX:{sym}"

    labels = ["3봉 전", "2봉 전", "현재(진행중)" if not candles[2]["closed"] else "최근 마감"]
    rows_html = ""
    for lab, c in zip(labels, candles):
        ctype = candle_type(c)
        ctype_color = "#26a69a" if ctype == "bull" else ("#ef5350" if ctype == "bear" else "#8b949e")
        ctype_label = "양봉" if ctype == "bull" else ("음봉" if ctype == "bear" else "보합")
        change_pct = (c["close"] - c["open"]) / c["open"] * 100 if c["open"] else 0.0
        change_color = "#26a69a" if change_pct > 0 else ("#ef5350" if change_pct < 0 else "#8b949e")
        change_sign = "+" if change_pct > 0 else ""
        rows_html += f"""

        <tr>
          <td>{lab}</td>
          <td style="color:{ctype_color};font-weight:700;">{ctype_label}</td>
          <td>{fmt_price(c['open'])}</td>
          <td>{fmt_price(c['close'])}</td>
          <td style="color:{change_color};font-weight:700;">{change_sign}{change_pct:.2f}%</td>
        </tr>"""

    return f"""
  <div class="card" id="{card_id}">
    <div class="card-head">
      <span class="sym">{sym.replace('USDT.P', '')}</span>
      <span style="font-size:.75rem;color:#8b949e;">/USDT · OKX · {bar_label(m['bar'])}</span>
      <span class="pattern-tag" style="background:{color}22;border:1px solid {color}88;color:{color};">
        {PATTERN_LABEL[pattern]}
      </span>
      <span class="live-badge" id="live_{chart_id}">● 실시간 연결 대기중</span>
      <a class="tv-link" href="https://www.tradingview.com/chart/?symbol={tv_link_sym}" target="_blank" rel="noopener">TradingView에서 열기 ↗</a>
    </div>
    <div class="chart-legend">
      <span><i style="background:#f0b90b;"></i>MA20</span>
      <span><i style="background:#ff3860;"></i>MA200</span>
    </div>
    <div class="chart-box" id="{chart_id}"></div>
    <table class="candle-table">
      <thead><tr><th>캔들</th><th>구분</th><th>시가</th><th>종가</th><th>변동율</th></tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
  </div>"""


def make_ids(bar, symbol):
    """타임프레임+심볼로부터 (chart_id, card_id)를 만든다.
    build_timeframe_section(카드 렌더링)과 build_summary_table(바로가기 링크)이
    서로 다른 함수에서 호출되므로, id 생성 규칙을 한 곳에 모아 두 쪽이 항상
    같은 id를 만들도록 한다."""
    safe_sym = symbol.replace(".", "_")
    return f"chart_{bar}_{safe_sym}", f"card_{bar}_{safe_sym}"


def build_summary_table(all_results):
    """전체 타임프레임 감지 결과를 한눈에 보는 요약 테이블 (종목/타임프레임/패턴/바로가기)."""
    rows = []
    for result in all_results:
        for m in result["matched"]:
            chart_id, card_id = make_ids(m["bar"], m["symbol"])
            color = PATTERN_COLOR[m["pattern"]]
            sym_disp = m["symbol"].replace("USDT.P", "")
            change_pct = compute_two_candle_swing_pct(m)
            change_color = "#26a69a" if change_pct > 0 else ("#ef5350" if change_pct < 0 else "#8b949e")
            change_sign = "+" if change_pct > 0 else ""
            rows.append(f"""
        <tr>
          <td class="sum-sym">{sym_disp}</td>
          <td>{bar_label(m['bar'])}</td>
          <td>
            <span class="pattern-tag sm" style="background:{color}22;border:1px solid {color}88;color:{color};">
              {PATTERN_LABEL[m['pattern']]}
            </span>
          </td>
          <td style="color:{change_color};font-weight:700;">{change_sign}{change_pct:.2f}%</td>
          <td><a class="goto-link" href="#{card_id}">차트 보기 ↓</a></td>
        </tr>""")

    if not rows:
        return '<div class="empty-state">현재 감지된 패턴이 없습니다.</div>'

    return f"""
    <table class="summary-table">
      <thead>
        <tr><th>종목</th><th>타임프레임</th><th>패턴</th><th>2봉 고/저 변동율</th><th>바로가기</th></tr>
      </thead>
      <tbody>{''.join(rows)}</tbody>
    </table>"""


def build_timeframe_section(result):
    """타임프레임 1개(예: 15분봉)에 대한 <section> 블록 + 해당 chart_data 조각을 반환."""
    bar = result["bar"]
    matched = result["matched"]
    errors = result["errors"]
    scanned = result["scanned"]

    ids = [make_ids(bar, m["symbol"]) for m in matched]
    chart_ids = [cid for cid, _ in ids]
    card_ids = [cad for _, cad in ids]
    cards_html = "\n".join(
        build_card_html(m, cid, cad) for m, cid, cad in zip(matched, chart_ids, card_ids)
    )
    if not matched:
        cards_html = '<div class="empty-state">현재 감지된 패턴이 없습니다.</div>'

    chart_data = {cid: build_chart_payload(m) for m, cid in zip(matched, chart_ids)}

    error_html = ""
    if errors:
        rows = "".join(
            f"<tr><td>{s}</td><td>{i}</td><td>{e}</td></tr>" for s, i, e in errors
        )
        error_html = f"""
    <details class="err-box">
      <summary>⚠️ 조회 실패 {len(errors)}건 (펼쳐서 확인)</summary>
      <table class="candle-table">
        <thead><tr><th>심볼</th><th>OKX instId</th><th>오류</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </details>"""

    section_html = f"""
  <section class="tf-section">
    <div class="tf-head">
      <h2>{bar_label(bar)} <span class="tf-code">({bar})</span></h2>
      <span class="tf-sub">스캔 {scanned}종목 · 감지 {len(matched)}종목</span>
    </div>
    <div class="grid">
{cards_html}
    </div>
{error_html}
  </section>"""

    return section_html, chart_data


def build_html(all_results, run_time_kst):
    total_scanned = all_results[0]["scanned"] if all_results else 0
    total_matched = sum(len(r["matched"]) for r in all_results)

    # 타임프레임별 요약 배지 (헤더에 표시)
    tf_summary_badges = "".join(
        f'<span class="tf-badge">{bar_label(r["bar"])} {len(r["matched"])}건</span>'
        for r in all_results
    )

    summary_table_html = build_summary_table(all_results)

    sections_html = ""
    chart_data_all = {}
    for result in all_results:
        section_html, chart_data = build_timeframe_section(result)
        sections_html += section_html
        chart_data_all.update(chart_data)

    chart_data_json = json.dumps(chart_data_all, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>OKX 멀티 타임프레임 3연속 패턴 감지</title>
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/lightweight-charts@4.1.3/dist/lightweight-charts.standalone.production.js"></script>
<style>
:root{{--bg:#0a0e14;--card:#0d1520;--border:#21262d;--text:#f0f6fc;--muted:#8b949e;}}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'Noto Sans KR',sans-serif;background:var(--bg);color:var(--text);font-size:13px;}}
.container{{max-width:1200px;margin:0 auto;padding:16px 20px;}}
.header{{background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);color:#fff;
  padding:1.2rem 1.8rem;border-radius:12px;margin-bottom:1.2rem;border:1px solid #2a3a5e;}}
.header h1{{font-family:Rajdhani,sans-serif;font-size:1.7rem;font-weight:700;color:#00d1ff;}}
.header .sub{{font-size:.88rem;color:#b8cef5;margin-top:.3rem;}}
.tf-badges{{margin-top:.6rem;display:flex;gap:.5rem;flex-wrap:wrap;}}
.ws-status{{margin-top:.6rem;font-size:.78rem;color:#f0b90b;font-weight:600;}}
.ws-status.ok{{color:#26a69a;}}
.ws-status.err{{color:#ef5350;}}
.live-badge{{font-size:.7rem;color:#8b949e;white-space:nowrap;}}
.live-badge.on{{color:#26a69a;}}
.live-badge.on::before{{content:"";display:inline-block;width:6px;height:6px;border-radius:50%;
  background:#26a69a;margin-right:.3rem;animation:live-pulse 1.4s infinite;}}
@keyframes live-pulse{{0%,100%{{opacity:1;}}50%{{opacity:.3;}}}}
.summary-box{{background:var(--card);border:1px solid var(--border);border-radius:12px;
  padding:1rem 1.2rem;margin-bottom:1.6rem;}}
.summary-title{{font-family:Rajdhani,sans-serif;font-size:1.15rem;font-weight:700;
  color:#f0f6fc;margin-bottom:.7rem;}}
.summary-table{{width:100%;border-collapse:collapse;font-size:.85rem;}}
.summary-table th,.summary-table td{{padding:.5rem .6rem;text-align:left;border-bottom:1px solid var(--border);}}
.summary-table th{{color:var(--muted);font-weight:500;font-size:.78rem;}}
.summary-table .sum-sym{{font-family:Rajdhani,sans-serif;font-weight:700;font-size:.95rem;}}
.pattern-tag.sm{{padding:.15rem .55rem;border-radius:16px;font-size:.72rem;font-weight:700;white-space:nowrap;}}
.goto-link{{color:#58a6ff;text-decoration:none;font-size:.8rem;white-space:nowrap;}}
.goto-link:hover{{text-decoration:underline;}}
html{{scroll-behavior:smooth;}}
.card{{scroll-margin-top:16px;}}
.card:target{{outline:2px solid #58a6ff;outline-offset:2px;}}
.tf-badge{{background:#0a1a2e;border:1px solid #2a3a5e;color:#7dd3fc;padding:.25rem .7rem;
  border-radius:20px;font-size:.75rem;font-weight:600;}}
.tf-section{{margin-bottom:2rem;}}
.tf-head{{display:flex;align-items:baseline;gap:.7rem;margin-bottom:.8rem;
  border-bottom:2px solid #21262d;padding-bottom:.5rem;flex-wrap:wrap;}}
.tf-head h2{{font-family:Rajdhani,sans-serif;font-size:1.3rem;font-weight:700;color:#f0f6fc;}}
.tf-head .tf-code{{font-size:.85rem;color:var(--muted);font-weight:500;}}
.tf-head .tf-sub{{font-size:.8rem;color:var(--muted);}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:1rem;}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:.9rem;}}
.card-head{{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;margin-bottom:.6rem;}}
.card-head .sym{{font-family:Rajdhani,sans-serif;font-size:1.3rem;font-weight:700;}}
.pattern-tag{{padding:.2rem .7rem;border-radius:20px;font-size:.78rem;font-weight:700;}}
.tv-link{{margin-left:auto;font-size:.75rem;color:#58a6ff;text-decoration:none;white-space:nowrap;}}
.tv-link:hover{{text-decoration:underline;}}
.chart-legend{{display:flex;gap:.9rem;font-size:.72rem;color:var(--muted);margin-bottom:.35rem;}}
.chart-legend i{{display:inline-block;width:10px;height:3px;margin-right:.3rem;vertical-align:middle;}}
.chart-box{{width:100%;height:420px;background:#06090f;border-radius:8px;overflow:hidden;margin-bottom:.6rem;}}
.candle-table{{width:100%;border-collapse:collapse;font-size:.8rem;}}
.candle-table th,.candle-table td{{padding:.3rem .5rem;text-align:left;border-bottom:1px solid var(--border);}}
.candle-table th{{color:var(--muted);font-weight:500;}}
.empty-state{{text-align:center;padding:2.2rem 1rem;color:var(--muted);font-size:1rem;
  border:1px dashed var(--border);border-radius:12px;}}
.err-box{{margin-top:1rem;color:var(--muted);background:var(--card);border:1px solid var(--border);
  border-radius:10px;padding:.7rem 1rem;}}
.err-box summary{{cursor:pointer;font-size:.85rem;}}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>🔎 OKX 멀티 타임프레임 3연속 캔들 패턴 감지</h1>
    <div class="sub">양음음 / 음양양 패턴 · 스캔 {total_scanned}종목 · 전체 감지 {total_matched}건 · 갱신 {run_time_kst} KST</div>
    <div class="tf-badges">{tf_summary_badges}</div>
    <div class="ws-status" id="wsStatusBadge">🔌 실시간 연결 시도 중...</div>
  </div>

  <div class="summary-box">
    <h2 class="summary-title">📋 전체 감지 현황</h2>
    {summary_table_html}
  </div>
{sections_html}
</div>

<script>
// 파이썬에서 이미 받아온 OKX 실제 캔들 데이터로 그리는 로컬 렌더링 차트.
// TradingView 라이브 위젯과 달리 외부 iframe/서버 임베드 승인이 필요 없어서
// file:// 로 직접 열어도 항상 렌더링됩니다.
// + 렌더링 이후에는 OKX 공개 웹소켓(candle 채널)에 붙어서 진행 중인 캔들을
//   실시간으로 갱신합니다 (연결이 안 되거나 끊기면 기존처럼 스케줄러가
//   15분마다 새로 만든 스냅샷 HTML로 자연스럽게 대체됩니다).
const CHART_VISIBLE_CANDLES = {CHART_VISIBLE_CANDLES};   // 화면에 보여줄 캔들 개수 (.env의 CHART_VISIBLE_CANDLES로 조절)

// containerId → {{ candleSeries, ma20Series, ma200Series, times:[...], closes:[...] }}
const SERIES_STATE = {{}};

function renderChart(containerId, payload) {{
  const container = document.getElementById(containerId);
  if (!container || !window.LightweightCharts) return;

  const chart = LightweightCharts.createChart(container, {{
    layout: {{ background: {{ color: "#06090f" }}, textColor: "#c9d1d9" }},
    grid: {{
      vertLines: {{ color: "#111827" }},
      horzLines: {{ color: "#111827" }},
    }},
    rightPriceScale: {{ borderColor: "#21262d" }},
    timeScale: {{ borderColor: "#21262d", timeVisible: true, secondsVisible: false }},
    crosshair: {{ mode: LightweightCharts.CrosshairMode.Normal }},
  }});

  const candleSeries = chart.addCandlestickSeries({{
    upColor: "#26a69a", downColor: "#ef5350",
    borderUpColor: "#26a69a", borderDownColor: "#ef5350",
    wickUpColor: "#26a69a", wickDownColor: "#ef5350",
  }});
  candleSeries.setData(payload.candles);
  if (payload.markers && payload.markers.length) {{
    candleSeries.setMarkers(payload.markers);
  }}

  const ma20Series = chart.addLineSeries({{ color: "#f0b90b", lineWidth: 1, priceLineVisible: false }});
  ma20Series.setData(payload.ma20);

  const ma200Series = chart.addLineSeries({{ color: "#ff3860", lineWidth: 2, priceLineVisible: false }});
  ma200Series.setData(payload.ma200);

  // MA200 계산을 위해 데이터 자체는 히스토리 전체(CHART_HISTORY_COUNT)를 유지하되,
  // 화면 초기 확대 범위만 최근 CHART_VISIBLE_CANDLES개로 좁힌다.
  const total = payload.candles.length;
  const visible = Math.min(CHART_VISIBLE_CANDLES, total);
  chart.timeScale().setVisibleLogicalRange({{ from: total - visible, to: total - 1 }});

  new ResizeObserver(entries => {{
    const {{ width, height }} = entries[0].contentRect;
    chart.applyOptions({{ width, height }});
  }}).observe(container);

  // 실시간 갱신에 쓸 상태 저장 (MA는 서버가 계산해준 값을 그대로 이어받아
  // 새 캔들이 들어올 때마다 마지막 구간만 다시 평균낸다)
  SERIES_STATE[containerId] = {{
    candleSeries, ma20Series, ma200Series,
    times: payload.candles.map(c => c.time),
    closes: payload.candles.map(c => c.close),
  }};
}}

// renderChart 함수 정의가 끝난 "이후"에 실행되도록 같은 스크립트 블록
// 맨 아래에서 데이터를 순회하며 그린다 (함수보다 먼저 호출되면 안 됨).
// 타임프레임(15분/30분/1시간 등)을 모두 합친 딕셔너리를 한 번에 순회한다.
const CHART_DATA = {chart_data_json};
Object.entries(CHART_DATA).forEach(([containerId, payload]) => {{
  renderChart(containerId, payload);
}});

// ══════════════════════════════════════════════════════════
// 실시간 갱신 (OKX 공개 웹소켓 candle 채널)
// ══════════════════════════════════════════════════════════
// 감지된 카드들만 "instId + 타임프레임" 조합으로 묶어서 구독한다.
// (같은 종목이 여러 타임프레임에서 동시에 감지되면 채널도 그만큼 따로 구독됨)
const CONTAINER_BY_KEY = {{}};   // "BTC-USDT-SWAP|15m" → [containerId, ...]
Object.entries(CHART_DATA).forEach(([containerId, payload]) => {{
  if (!payload.instId || !payload.bar) return;
  const key = payload.instId + "|" + payload.bar;
  (CONTAINER_BY_KEY[key] = CONTAINER_BY_KEY[key] || []).push(containerId);
}});

function setWsStatus(text, cls) {{
  const el = document.getElementById("wsStatusBadge");
  if (!el) return;
  el.textContent = text;
  el.className = "ws-status" + (cls ? " " + cls : "");
}}

function markLive(containerIds, ok) {{
  const now = new Date();
  const hh = String(now.getHours()).padStart(2, "0");
  const mm = String(now.getMinutes()).padStart(2, "0");
  const ss = String(now.getSeconds()).padStart(2, "0");
  containerIds.forEach(cid => {{
    const badge = document.getElementById("live_" + cid);
    if (!badge) return;
    if (ok) {{
      badge.textContent = `● 실시간 ${{hh}}:${{mm}}:${{ss}}`;
      badge.className = "live-badge on";
    }} else {{
      badge.textContent = "● 실시간 연결 끊김";
      badge.className = "live-badge";
    }}
  }});
}}

function updateLiveCandle(containerId, candle) {{
  const st = SERIES_STATE[containerId];
  if (!st) return;

  st.candleSeries.update(candle);

  const lastIdx = st.times.length - 1;
  if (lastIdx >= 0 && st.times[lastIdx] === candle.time) {{
    st.closes[lastIdx] = candle.close;                 // 같은(진행 중) 캔들 갱신
  }} else {{
    st.times.push(candle.time);
    st.closes.push(candle.close);                       // 새 캔들 확정 → 봉 추가
  }}

  const n = st.closes.length;
  if (n >= 20) {{
    let sum = 0;
    for (let i = n - 20; i < n; i++) sum += st.closes[i];
    st.ma20Series.update({{ time: candle.time, value: sum / 20 }});
  }}
  if (n >= 200) {{
    let sum = 0;
    for (let i = n - 200; i < n; i++) sum += st.closes[i];
    st.ma200Series.update({{ time: candle.time, value: sum / 200 }});
  }}
}}

let _wsReconnectTimer = null;

function connectLiveFeed() {{
  const keys = Object.keys(CONTAINER_BY_KEY);
  if (!keys.length) {{
    setWsStatus("ℹ️ 실시간 갱신 대상 없음 (감지된 종목 없음)", "");
    return;
  }}

  let ws;
  try {{
    ws = new WebSocket("wss://ws.okx.com:8443/ws/v5/business");
  }} catch (e) {{
    setWsStatus("⚠️ 실시간 연결 불가 (스케줄러 갱신만 사용됨)", "err");
    return;
  }}

  let pingTimer = null;

  ws.onopen = () => {{
    setWsStatus("🟢 실시간 연결됨", "ok");
    const args = keys.map(k => {{
      const [instId, bar] = k.split("|");
      return {{ channel: "candle" + bar, instId: instId }};
    }});
    // OKX는 한 번에 너무 많은 args를 보내면 거부할 수 있어 20개씩 끊어 전송
    for (let i = 0; i < args.length; i += 20) {{
      ws.send(JSON.stringify({{ op: "subscribe", args: args.slice(i, i + 20) }}));
    }}
    pingTimer = setInterval(() => {{
      if (ws.readyState === WebSocket.OPEN) ws.send("ping");
    }}, 20000);
  }};

  ws.onmessage = (evt) => {{
    if (evt.data === "pong") return;
    let msg;
    try {{ msg = JSON.parse(evt.data); }} catch (e) {{ return; }}
    if (msg.event === "error") {{
      setWsStatus("⚠️ 실시간 연결 오류 (스케줄러 갱신만 사용됨)", "err");
      return;
    }}
    if (!msg.arg || !msg.data || !msg.arg.channel) return;

    const bar = msg.arg.channel.replace("candle", "");
    const key = msg.arg.instId + "|" + bar;
    const containerIds = CONTAINER_BY_KEY[key];
    if (!containerIds) return;

    msg.data.forEach(row => {{
      // row = [ts, open, high, low, close, vol, volCcy, volCcyQuote, (confirm)]
      const candle = {{
        time: Math.floor(Number(row[0]) / 1000),
        open: parseFloat(row[1]), high: parseFloat(row[2]),
        low: parseFloat(row[3]), close: parseFloat(row[4]),
      }};
      containerIds.forEach(cid => updateLiveCandle(cid, candle));
    }});
    markLive(containerIds, true);
  }};

  ws.onclose = () => {{
    if (pingTimer) clearInterval(pingTimer);
    setWsStatus("🔄 실시간 연결 끊김, 재연결 시도 중...", "err");
    Object.values(CONTAINER_BY_KEY).forEach(ids => markLive(ids, false));
    if (_wsReconnectTimer) clearTimeout(_wsReconnectTimer);
    _wsReconnectTimer = setTimeout(connectLiveFeed, 4000);
  }};

  ws.onerror = () => {{
    ws.close();
  }};
}}

connectLiveFeed();
</script>
</body>
</html>"""


# ══════════════════════════════════════════════════════════
# 메인
# ══════════════════════════════════════════════════════════
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if SECOND_OUTPUT_FILE:
        os.makedirs(SECOND_OUTPUT_DIR, exist_ok=True)

    symbols = load_watchlist()
    now_kst = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 60)
    print("  OKX 멀티 타임프레임 3연속 캔들 패턴 감지")
    print(f"  워치리스트: {len(symbols)}종목  |  타임프레임: {', '.join(BARS)}  |  실행시각: {now_kst} KST")
    print("=" * 60)

    all_results = scan_all_timeframes(symbols, BARS)

    html = build_html(all_results, now_kst)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    # index.html 카드에 패턴 배지를 붙이기 위한 경량 데이터 파일.
    # okx_3candle_pattern.html과 같은 폴더에 있어야 index.html이 <script src="pattern_summary.js">
    # 로 찾을 수 있으므로, HTML 결과와 동일하게 두 경로 모두에 저장한다.
    pattern_summary_js = build_pattern_summary_js(all_results, now_kst)
    pattern_summary_file = os.path.join(OUTPUT_DIR, "pattern_summary.js")
    with open(pattern_summary_file, "w", encoding="utf-8") as f:
        f.write(pattern_summary_js)

    # 두 번째 경로(E:\Trader_KIM 등)에도 HTML + pattern_summary.js 동일하게 저장.
    # 이 경로 저장이 실패해도(예: 드라이브 미연결) 첫 번째 저장은 이미
    # 끝났으므로 스크립트 전체가 죽지 않도록 예외를 잡아서 경고만 출력한다.
    if SECOND_OUTPUT_FILE:
        try:
            with open(SECOND_OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write(html)
            with open(os.path.join(SECOND_OUTPUT_DIR, "pattern_summary.js"), "w", encoding="utf-8") as f:
                f.write(pattern_summary_js)
        except Exception as e:
            print(f"  ⚠️  두 번째 저장 경로 쓰기 실패 ({SECOND_OUTPUT_FILE}): {e}")

    append_log(all_results, now_kst)

    print("-" * 60)
    for r in all_results:
        print(f"  [{bar_label(r['bar'])}] 감지: {len(r['matched'])}종목  |  오류: {len(r['errors'])}건")
    print(f"  결과 → {OUTPUT_FILE}")
    if SECOND_OUTPUT_FILE:
        print(f"  결과(추가 저장) → {SECOND_OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()

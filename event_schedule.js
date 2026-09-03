/**
 * event_schedule.js
 * 프로젝트: 주식 분석 전문가 — 전 종목 통합 주요 일정 캘린더
 * 모든 일시는 한국시간(KST, UTC+9) 기준입니다.
 * importance: 1(낮음) ~ 5(매우 높음)
 * 각 리포트(예: NVDA_주가분석_리포트.html)의 "주요 일정" 절과 연동되는 통합 데이터입니다.
 * 마지막 자동 업데이트: 2026-09-04 (KST)
 */

const EVENT_SCHEDULE = [
  { date_kst: "2026-09-04 21:30", end_kst: null, title: "미국 8월 비농업고용(NFP)",
    tickers: ["SPY","QQQ","EWY","KORU","BTC","XAU","AVGO"], importance: 5,
    category: "macro", note: "고용 둔화 시 9월 FOMC 금리 인하 기대 강화 가능성" },

  { date_kst: "2026-09-04 06:45", end_kst: "2026-09-04 09:00", title: "테슬라 Cybercab 런치 이벤트 (Austin, 라이브스트림)",
    tickers: ["TSLA"], importance: 5,
    category: "corporate", note: "미국 현지 9/3 16:45 CDT 진행. 로보택시 내러티브 확인 포인트" },

  { date_kst: "2026-09-05 05:00", end_kst: null, title: "Alphabet(GOOGL) 배당락일 (주당 $0.22)",
    tickers: ["GOOGL"], importance: 2,
    category: "dividend", note: "미국 현지 9/4(금) 기준" },

  { date_kst: "2026-09-06 20:00", end_kst: null, title: "OPEC+ 10월 산유량 결정 회의",
    tickers: ["CL"], importance: 4,
    category: "macro", note: "동결 유력, 증산 폭 서프라이즈 시 유가 변동성 확대" },

  { date_kst: "2026-09-08", end_kst: null, title: "Solana Agave v4.3 스테이크 가중치 전환 1단계",
    tickers: ["SOL"], importance: 2, category: "protocol", note: "9/8·9/14·9/21 단계적 적용" },

  { date_kst: "2026-09-09", end_kst: null, title: "Solana Transaction V1 메인넷 적용",
    tickers: ["SOL"], importance: 3, category: "protocol", note: null },

  { date_kst: "2026-09-10 02:00", end_kst: null, title: "Apple 신제품 이벤트 '서프라이즈 앤 샤인' (아이폰18 프로 · 첫 폴더블 아이폰)",
    tickers: ["AAPL","AVGO"], importance: 5, category: "corporate", note: "AVGO는 공급망 수혜 관점" },

  { date_kst: "2026-09-10 14:30", end_kst: null, title: "TSMC 8월 매출 발표",
    tickers: ["TSM"], importance: 3, category: "earnings", note: null },

  { date_kst: "2026-09-10", end_kst: null, title: "NVIDIA 배당 기준일 (Ex-Dividend, $0.25/주)",
    tickers: ["NVDA"], importance: 2, category: "dividend", note: null },

  { date_kst: "2026-09-11 01:00", end_kst: null, title: "EIA 주간 원유재고 발표 (노동절로 일정 지연)",
    tickers: ["CL"], importance: 3, category: "macro", note: null },

  { date_kst: "2026-09-11 21:30", end_kst: null, title: "미국 8월 소비자물가지수(CPI)",
    tickers: ["SPY","QQQ","EWY","KORU","BTC","ETH","XAU"], importance: 5,
    category: "macro", note: "FOMC 직전 마지막 핵심 인플레이션 지표" },

  { date_kst: "2026-09-12 16:00", end_kst: null, title: "아이폰18 시리즈 사전예약 시작",
    tickers: ["AAPL"], importance: 3, category: "corporate", note: null },

  { date_kst: "2026-09-15", end_kst: null, title: "CLARITY Act 상원 표결",
    tickers: ["CRCL"], importance: 4, category: "regulatory", note: "스테이블코인 규제 명확화 법안" },

  { date_kst: "2026-09-16", end_kst: null, title: "Circle Arc 메인넷 출시",
    tickers: ["CRCL"], importance: 3, category: "protocol", note: null },

  { date_kst: "2026-09-17 03:00", end_kst: "2026-09-17 03:30", title: "FOMC 금리결정 발표 (9/15~16 회의, SEP·점도표 포함)",
    tickers: ["EWY","ETH","META","GOOGL","KORU","MSTR","MU","NVDA","SKHY","SPY","ONDO","SOL","SNDK","SOXL","QQQ","TSLA","TSM","AAPL","AMZN","AMD","CL","BTC","XAU","PLTR","AVGO","CRCL"],
    importance: 5, category: "macro", note: "03:30 파월 의장 기자회견 — 전 자산군 공통 최상위 변수" },

  { date_kst: "2026-09-17", end_kst: null, title: "구글 광고기술(AdX) 반독점 구제조치 세부안 공개(예정)",
    tickers: ["GOOGL"], importance: 4, category: "regulatory", note: "9/2 DOJ 강제매각 요구는 기각됨" },

  { date_kst: "2026-09-18", end_kst: null, title: "아이폰18 시리즈 정식 출시",
    tickers: ["AAPL"], importance: 4, category: "corporate", note: null },

  { date_kst: "2026-09-18", end_kst: null, title: "9월 트리플위칭(선물·옵션 동시만기)",
    tickers: ["AVGO","SPY","QQQ"], importance: 3, category: "macro", note: null },

  { date_kst: "2026-09-18", end_kst: null, title: "이더리움 9월 옵션 만기",
    tickers: ["ETH"], importance: 3, category: "crypto", note: null },

  { date_kst: "2026-09-21", end_kst: null, title: "Solana Agave v4.3 스테이크 가중치 전환 최종단계",
    tickers: ["SOL"], importance: 2, category: "protocol", note: null },

  { date_kst: "2026-09-23", end_kst: null, title: "Alphabet 증권 집단소송 공판",
    tickers: ["GOOGL"], importance: 3, category: "regulatory", note: null },

  { date_kst: "2026-09-25 17:00", end_kst: null, title: "Deribit 비트코인 월간 옵션 만기(추정)",
    tickers: ["BTC"], importance: 3, category: "crypto", note: "만기 규모에 따라 단기 변동성 확대 가능" },

  { date_kst: "2026-09-28", end_kst: null, title: "Solana Alpenglow 기능 단계적 활성화 시작",
    tickers: ["SOL"], importance: 3, category: "protocol", note: "10월까지 순차 전개" },

  { date_kst: "2026-09-30 21:30", end_kst: null, title: "미국 8월 근원 PCE 물가지수",
    tickers: ["XAU","SPY","QQQ"], importance: 4, category: "macro", note: "연준 선호 물가지표" },

  { date_kst: "2026-09월 하순", end_kst: null, title: "디지털자산 과세법안 논의 · Circle Trust Bank 출범",
    tickers: ["CRCL"], importance: 3, category: "regulatory", note: "구체 일자 미확정" },

  { date_kst: "2026-10-01 05:00", end_kst: "2026-10-01 05:30", title: "Micron(MU) FY2026 4분기 실적발표",
    tickers: ["MU","SKHY","SOXL"], importance: 5, category: "earnings", note: "美 현지 9/30 장마감 후 — HBM 가격/수요 가이던스 핵심" },

  { date_kst: "2026-10-01", end_kst: null, title: "NVIDIA 분기 배당 지급",
    tickers: ["NVDA"], importance: 1, category: "dividend", note: null },

  { date_kst: "2026-10-01", end_kst: null, title: "Alphabet 증권 집단소송 옵트아웃(제외 신청) 마감",
    tickers: ["GOOGL"], importance: 2, category: "regulatory", note: null },

  { date_kst: "2026-10-초", end_kst: null, title: "9월 한국 반도체 수출 통계 발표",
    tickers: ["EWY","KORU","SKHY"], importance: 4, category: "macro", note: "8월 사상 최대치 이후 연속 여부 확인" },

  { date_kst: "2026-10-15 전후", end_kst: null, title: "TSMC 3분기 실적 발표 (미확정 추정)",
    tickers: ["TSM"], importance: 5, category: "earnings", note: null },

  { date_kst: "2026-10-22", end_kst: null, title: "한국은행 금융통화위원회 (기준금리 결정)",
    tickers: ["EWY","KORU"], importance: 4, category: "macro", note: "현 기준금리 2.50%" },

  { date_kst: "2026-10-22 전후", end_kst: null, title: "테슬라 3분기 실적 발표 (미확정 추정)",
    tickers: ["TSLA"], importance: 5, category: "earnings", note: "마진·인도량·가이던스 핵심" },

  { date_kst: "2026-10-28 새벽", end_kst: null, title: "Alphabet(GOOGL) 3분기 실적 발표",
    tickers: ["GOOGL"], importance: 5, category: "earnings", note: "美 현지 10/27 장마감 후. Cloud 성장·CapEx 가이던스 핵심" },

  { date_kst: "2026-10-29 03:00", end_kst: null, title: "FOMC 금리결정 발표 (10/27~28 회의)",
    tickers: ["EWY","ETH","META","GOOGL","KORU","MSTR","MU","NVDA","SKHY","SPY","ONDO","SOL","SNDK","SOXL","QQQ","TSLA","TSM","AAPL","AMZN","AMD","CL","BTC","XAU","PLTR","AVGO","CRCL"],
    importance: 5, category: "macro", note: null },

  { date_kst: "2026-10-29 새벽", end_kst: null, title: "Meta(META) 3분기 실적 발표",
    tickers: ["META"], importance: 5, category: "earnings", note: "美 현지 10/28 장마감 후" },

  { date_kst: "2026-10-30 05:00", end_kst: null, title: "Apple(AAPL) 4분기 실적 발표",
    tickers: ["AAPL"], importance: 5, category: "earnings", note: null },

  { date_kst: "2026-10-30 오전", end_kst: null, title: "Amazon(AMZN) 3분기 실적 발표 (미확정 추정)",
    tickers: ["AMZN"], importance: 5, category: "earnings", note: "美 현지 10/29 장마감 후" },

  { date_kst: "2026-10월말~11월초", end_kst: null, title: "MicroStrategy(MSTR)·SK하이닉스·Circle(CRCL) 3분기 실적 발표(잠정)",
    tickers: ["MSTR","SKHY","CRCL"], importance: 4, category: "earnings", note: "공식 일정 미확정" },

  { date_kst: "2026-11-02 전후", end_kst: null, title: "Palantir(PLTR) 3분기 실적 발표 (미확정 추정)",
    tickers: ["PLTR"], importance: 5, category: "earnings", note: null },

  { date_kst: "2026-11-04 새벽", end_kst: null, title: "AMD 3분기 실적 발표",
    tickers: ["AMD"], importance: 5, category: "earnings", note: "美 현지 11/3 장마감 후" },

  { date_kst: "2026-11-05~06 추정", end_kst: null, title: "SanDisk(SNDK) 다음 분기 실적 발표(추정)",
    tickers: ["SNDK"], importance: 4, category: "earnings", note: null },

  { date_kst: "2026-11-10", end_kst: null, title: "Apple(AAPL) 배당락일",
    tickers: ["AAPL"], importance: 1, category: "dividend", note: null },

  { date_kst: "2026-11-18~25", end_kst: null, title: "NVIDIA Q3 FY2027 실적 발표",
    tickers: ["NVDA"], importance: 5, category: "earnings", note: "美 장 마감 후 — Blackwell/Rubin 가이던스 핵심" },

  { date_kst: "2026-12-10 04:00", end_kst: null, title: "FOMC 금리결정 발표 (12/8~9 회의)",
    tickers: ["EWY","ETH","META","GOOGL","KORU","MSTR","MU","NVDA","SKHY","SPY","ONDO","SOL","SNDK","SOXL","QQQ","TSLA","TSM","AAPL","AMZN","AMD","CL","BTC","XAU","PLTR","AVGO","CRCL"],
    importance: 5, category: "macro", note: "2026년 마지막 FOMC" },

  { date_kst: "2026-12-11 오전", end_kst: null, title: "Broadcom(AVGO) 4분기 실적 발표",
    tickers: ["AVGO"], importance: 5, category: "earnings", note: "美 현지 12/10 장마감 후" }
];

// 특정 티커의 향후 일정만 조회
function getEventsForTicker(ticker) {
  return EVENT_SCHEDULE.filter(e => e.tickers.includes(ticker));
}

// 중요도(importance) 기준 필터 (예: 4 이상만)
function getEventsByMinImportance(minImportance) {
  return EVENT_SCHEDULE.filter(e => e.importance >= minImportance);
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { EVENT_SCHEDULE, getEventsForTicker, getEventsByMinImportance };
}
if (typeof window !== "undefined") {
  window.EVENT_SCHEDULE = EVENT_SCHEDULE;
  window.getEventsForTicker = getEventsForTicker;
  window.getEventsByMinImportance = getEventsByMinImportance;
}

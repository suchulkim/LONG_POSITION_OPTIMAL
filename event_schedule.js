/**
 * event_schedule.js
 * 프로젝트: 주식 분석 전문가 — 전 종목 통합 주요 일정 캘린더
 * index.html(Watchlist)이 기대하는 형식: window.SeptSchedule
 *   - SEPTEMBER_2026_SCHEDULE: 이벤트 배열
 *   - sortedByDate(list): 날짜/시각순 정렬
 *   - starsFor(importance): 중요도(1~5)를 별표 문자열로 변환
 * 각 이벤트 필드: dateKST(YYYY-MM-DD), timeKST(HH:MM, KST), dateLabel(표시용 한글 날짜),
 *                event(제목), tickers(관련 종목 배열), importance(1~5), note(선택, 부연설명)
 * 모든 일시는 한국시간(KST, UTC+9) 기준입니다.
 * 마지막 자동 업데이트: 2026-09-04 (KST)
 */

const SEPTEMBER_2026_SCHEDULE = [
  { dateKST: "2026-09-04", timeKST: "06:45", dateLabel: "9월 4일 (금)",
    event: "테슬라 Cybercab 런치 이벤트 (Austin, 라이브스트림)",
    tickers: ["TSLA"], importance: 5, note: "미국 현지 9/3 16:45 CDT 진행" },

  { dateKST: "2026-09-04", timeKST: "21:30", dateLabel: "9월 4일 (금)",
    event: "미국 8월 비농업고용(NFP)",
    tickers: ["SPY","QQQ","EWY","KORU","BTC","XAU","AVGO"], importance: 5,
    note: "고용 둔화 시 9월 FOMC 금리 인하 기대 강화 가능성" },

  { dateKST: "2026-09-05", timeKST: "05:00", dateLabel: "9월 5일 (토)",
    event: "Alphabet(GOOGL) 배당락일 (주당 $0.22)",
    tickers: ["GOOGL"], importance: 2, note: "미국 현지 9/4(금) 기준" },

  { dateKST: "2026-09-06", timeKST: "20:00", dateLabel: "9월 6일 (일)",
    event: "OPEC+ 10월 산유량 결정 회의",
    tickers: ["CL"], importance: 4, note: "동결 유력, 증산 폭 서프라이즈 시 유가 변동성 확대" },

  { dateKST: "2026-09-08", timeKST: "09:00", dateLabel: "9월 8일 (화)",
    event: "Solana Agave v4.3 스테이크 가중치 전환 1단계",
    tickers: ["SOL"], importance: 2, note: "9/8·9/14·9/21 단계적 적용" },

  { dateKST: "2026-09-09", timeKST: "09:00", dateLabel: "9월 9일 (수)",
    event: "Solana Transaction V1 메인넷 적용",
    tickers: ["SOL"], importance: 3, note: null },

  { dateKST: "2026-09-10", timeKST: "02:00", dateLabel: "9월 10일 (목)",
    event: "Apple 신제품 이벤트 '서프라이즈 앤 샤인' (아이폰18 프로 · 첫 폴더블 아이폰)",
    tickers: ["AAPL","AVGO"], importance: 5, note: "AVGO는 공급망 수혜 관점" },

  { dateKST: "2026-09-10", timeKST: "14:30", dateLabel: "9월 10일 (목)",
    event: "TSMC 8월 매출 발표",
    tickers: ["TSM"], importance: 3, note: null },

  { dateKST: "2026-09-10", timeKST: "09:00", dateLabel: "9월 10일 (목)",
    event: "NVIDIA 배당 기준일 (Ex-Dividend, $0.25/주)",
    tickers: ["NVDA"], importance: 2, note: null },

  { dateKST: "2026-09-11", timeKST: "01:00", dateLabel: "9월 11일 (금)",
    event: "EIA 주간 원유재고 발표 (노동절로 일정 지연)",
    tickers: ["CL"], importance: 3, note: null },

  { dateKST: "2026-09-11", timeKST: "21:30", dateLabel: "9월 11일 (금)",
    event: "미국 8월 소비자물가지수(CPI)",
    tickers: ["SPY","QQQ","EWY","KORU","BTC","ETH","XAU"], importance: 5,
    note: "FOMC 직전 마지막 핵심 인플레이션 지표" },

  { dateKST: "2026-09-12", timeKST: "16:00", dateLabel: "9월 12일 (토)",
    event: "아이폰18 시리즈 사전예약 시작",
    tickers: ["AAPL"], importance: 3, note: null },

  { dateKST: "2026-09-15", timeKST: "09:00", dateLabel: "9월 15일 (화)",
    event: "미국 상원 CLARITY Act(디지털자산 시장구조법) 표결",
    tickers: ["CRCL"], importance: 4, note: "스테이블코인 규제 명확화 법안" },

  { dateKST: "2026-09-16", timeKST: "09:00", dateLabel: "9월 16일 (수)",
    event: "Circle Arc 메인넷 출시",
    tickers: ["CRCL"], importance: 3, note: "BlackRock·Visa·DTCC 참여" },

  { dateKST: "2026-09-17", timeKST: "03:00", dateLabel: "9월 17일 (목)",
    event: "FOMC 금리결정 발표 (9/15~16 회의, SEP·점도표 포함)",
    tickers: ["EWY","ETH","META","GOOGL","KORU","MSTR","MU","NVDA","SKHY","SPY","ONDO","SOL","SNDK","SOXL","QQQ","TSLA","TSM","AAPL","AMZN","AMD","CL","BTC","XAU","PLTR","AVGO","CRCL"],
    importance: 5, note: "03:30 파월 의장 기자회견 — 전 자산군 공통 최상위 변수" },

  { dateKST: "2026-09-17", timeKST: "09:00", dateLabel: "9월 17일 (목)",
    event: "구글 광고기술(AdX) 반독점 구제조치 세부안 공개(예정)",
    tickers: ["GOOGL"], importance: 4, note: "9/2 DOJ 강제매각 요구는 기각됨" },

  { dateKST: "2026-09-18", timeKST: "09:00", dateLabel: "9월 18일 (금)",
    event: "아이폰18 시리즈 정식 출시",
    tickers: ["AAPL"], importance: 4, note: null },

  { dateKST: "2026-09-18", timeKST: "22:00", dateLabel: "9월 18일 (금)",
    event: "9월 트리플위칭(선물·옵션 동시만기)",
    tickers: ["AVGO","SPY","QQQ"], importance: 3, note: null },

  { dateKST: "2026-09-18", timeKST: "17:00", dateLabel: "9월 18일 (금)",
    event: "이더리움 9월 옵션 만기",
    tickers: ["ETH"], importance: 3, note: null },

  { dateKST: "2026-09-21", timeKST: "09:00", dateLabel: "9월 21일 (월)",
    event: "Solana Agave v4.3 스테이크 가중치 전환 최종단계",
    tickers: ["SOL"], importance: 2, note: null },

  { dateKST: "2026-09-23", timeKST: "09:00", dateLabel: "9월 23일 (수)",
    event: "Alphabet 증권 집단소송 공판",
    tickers: ["GOOGL"], importance: 3, note: null },

  { dateKST: "2026-09-24", timeKST: "09:00", dateLabel: "9월 24일 (목)",
    event: "디지털자산 과세법안(Digital Asset Tax Bill) 표결 · Circle Trust Bank 출범(예정)",
    tickers: ["CRCL"], importance: 3, note: "구체 일자 미확정, 9월 하순 예상" },

  { dateKST: "2026-09-25", timeKST: "17:00", dateLabel: "9월 25일 (금)",
    event: "Deribit 비트코인 월간 옵션 만기(추정)",
    tickers: ["BTC"], importance: 3, note: "만기 규모에 따라 단기 변동성 확대 가능" },

  { dateKST: "2026-09-28", timeKST: "09:00", dateLabel: "9월 28일 (월)",
    event: "Solana Alpenglow 기능 단계적 활성화 시작",
    tickers: ["SOL"], importance: 3, note: "10월까지 순차 전개" },

  { dateKST: "2026-09-30", timeKST: "21:30", dateLabel: "9월 30일 (수)",
    event: "미국 8월 근원 PCE 물가지수",
    tickers: ["XAU","SPY","QQQ"], importance: 4, note: "연준 선호 물가지표" },

  { dateKST: "2026-10-01", timeKST: "05:00", dateLabel: "10월 1일 (목)",
    event: "Micron(MU) FY2026 4분기 실적발표",
    tickers: ["MU","SKHY","SOXL"], importance: 5, note: "美 현지 9/30 장마감 후 — HBM 가격/수요 가이던스 핵심" },

  { dateKST: "2026-10-01", timeKST: "09:00", dateLabel: "10월 1일 (목)",
    event: "NVIDIA 분기 배당 지급",
    tickers: ["NVDA"], importance: 1, note: null },

  { dateKST: "2026-10-01", timeKST: "10:00", dateLabel: "10월 1일 (목)",
    event: "Alphabet 증권 집단소송 옵트아웃(제외 신청) 마감",
    tickers: ["GOOGL"], importance: 2, note: null },

  { dateKST: "2026-10-05", timeKST: "09:00", dateLabel: "10월 5일 (월)",
    event: "9월 한국 반도체 수출 통계 발표(예정)",
    tickers: ["EWY","KORU","SKHY"], importance: 4, note: "정확한 발표일 미확정, 8월 사상 최대치 이후 연속 여부 확인" },

  { dateKST: "2026-10-15", timeKST: "09:00", dateLabel: "10월 15일 (목)",
    event: "TSMC 3분기 실적 발표(미확정 추정)",
    tickers: ["TSM"], importance: 5, note: null },

  { dateKST: "2026-10-22", timeKST: "09:00", dateLabel: "10월 22일 (목)",
    event: "한국은행 금융통화위원회 (기준금리 결정)",
    tickers: ["EWY","KORU"], importance: 4, note: "현 기준금리 2.50%" },

  { dateKST: "2026-10-22", timeKST: "17:00", dateLabel: "10월 22일 (목)",
    event: "테슬라 3분기 실적 발표(미확정 추정)",
    tickers: ["TSLA"], importance: 5, note: "마진·인도량·가이던스 핵심" },

  { dateKST: "2026-10-28", timeKST: "05:00", dateLabel: "10월 28일 (수)",
    event: "Alphabet(GOOGL) 3분기 실적 발표",
    tickers: ["GOOGL"], importance: 5, note: "美 현지 10/27 장마감 후. Cloud 성장·CapEx 가이던스 핵심" },

  { dateKST: "2026-10-29", timeKST: "03:00", dateLabel: "10월 29일 (목)",
    event: "FOMC 금리결정 발표 (10/27~28 회의)",
    tickers: ["EWY","ETH","META","GOOGL","KORU","MSTR","MU","NVDA","SKHY","SPY","ONDO","SOL","SNDK","SOXL","QQQ","TSLA","TSM","AAPL","AMZN","AMD","CL","BTC","XAU","PLTR","AVGO","CRCL"],
    importance: 5, note: null },

  { dateKST: "2026-10-29", timeKST: "05:00", dateLabel: "10월 29일 (목)",
    event: "Meta(META) 3분기 실적 발표",
    tickers: ["META"], importance: 5, note: "美 현지 10/28 장마감 후" },

  { dateKST: "2026-10-30", timeKST: "05:00", dateLabel: "10월 30일 (금)",
    event: "Apple(AAPL) 4분기 실적 발표",
    tickers: ["AAPL"], importance: 5, note: null },

  { dateKST: "2026-10-30", timeKST: "06:00", dateLabel: "10월 30일 (금)",
    event: "Amazon(AMZN) 3분기 실적 발표(미확정 추정)",
    tickers: ["AMZN"], importance: 5, note: "美 현지 10/29 장마감 후" },

  { dateKST: "2026-10-31", timeKST: "09:00", dateLabel: "10월 31일 (토)",
    event: "MicroStrategy(MSTR)·SK하이닉스·Circle(CRCL) 3분기 실적 발표(잠정)",
    tickers: ["MSTR","SKHY","CRCL"], importance: 4, note: "공식 일정 미확정, 10월말~11월초 예상" },

  { dateKST: "2026-11-02", timeKST: "09:00", dateLabel: "11월 2일 (월)",
    event: "Palantir(PLTR) 3분기 실적 발표(미확정 추정)",
    tickers: ["PLTR"], importance: 5, note: null },

  { dateKST: "2026-11-04", timeKST: "06:00", dateLabel: "11월 4일 (수)",
    event: "AMD 3분기 실적 발표",
    tickers: ["AMD"], importance: 5, note: "美 현지 11/3 장마감 후" },

  { dateKST: "2026-11-05", timeKST: "09:00", dateLabel: "11월 5일 (목)",
    event: "SanDisk(SNDK) 다음 분기 실적 발표(추정)",
    tickers: ["SNDK"], importance: 4, note: "11/5~6 사이 예상" },

  { dateKST: "2026-11-10", timeKST: "09:00", dateLabel: "11월 10일 (화)",
    event: "Apple(AAPL) 배당락일",
    tickers: ["AAPL"], importance: 1, note: null },

  { dateKST: "2026-11-20", timeKST: "06:00", dateLabel: "11월 20일 (금)",
    event: "NVIDIA Q3 FY2027 실적 발표(예상)",
    tickers: ["NVDA"], importance: 5, note: "11/18~25 사이 예상, Blackwell/Rubin 가이던스 핵심" },

  { dateKST: "2026-12-10", timeKST: "04:00", dateLabel: "12월 10일 (목)",
    event: "FOMC 금리결정 발표 (12/8~9 회의)",
    tickers: ["EWY","ETH","META","GOOGL","KORU","MSTR","MU","NVDA","SKHY","SPY","ONDO","SOL","SNDK","SOXL","QQQ","TSLA","TSM","AAPL","AMZN","AMD","CL","BTC","XAU","PLTR","AVGO","CRCL"],
    importance: 5, note: "2026년 마지막 FOMC" },

  { dateKST: "2026-12-11", timeKST: "06:00", dateLabel: "12월 11일 (금)",
    event: "Broadcom(AVGO) 4분기 실적 발표",
    tickers: ["AVGO"], importance: 5, note: "美 현지 12/10 장마감 후" }
];

function sortedByDate(list) {
  return [...list].sort((a, b) => {
    const ta = new Date(a.dateKST + 'T' + (a.timeKST || '00:00') + ':00+09:00').getTime();
    const tb = new Date(b.dateKST + 'T' + (b.timeKST || '00:00') + ':00+09:00').getTime();
    return ta - tb;
  });
}

function starsFor(importance) {
  const n = Math.max(0, Math.min(5, importance || 0));
  return '★'.repeat(n) + '☆'.repeat(5 - n);
}

const SeptSchedule = { SEPTEMBER_2026_SCHEDULE, sortedByDate, starsFor };

if (typeof module !== "undefined" && module.exports) {
  module.exports = SeptSchedule;
}
if (typeof window !== "undefined") {
  window.SeptSchedule = SeptSchedule;
}

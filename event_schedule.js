/**
 * september-2026-schedule.js
 *
 * 2026년 9월 주요 일정 (한국시간 KST 기준)
 * 관련 종목: BTCUSDT.P, ONDOUSDT.P, SOLUSDT.P, SNDKUSDT.P, CRCLUSDT.P, SKHYUSDT.P,
 *            TSLAUSDT.P, AAPLUSDT.P, SPYUSDT.P, MSTRUSDT.P, GOOGLUSDT.P, SOXLUSDT.P,
 *            NVDAUSDT.P, QQQUSDT.P, XAUUSDT.P, MUUSDT.P, AMDUSDT.P, PLTRUSDT.P,
 *            EWYUSDT.P, TSMUSDT.P, METAUSDT.P, AVGOUSDT.P, KORUUSDT.P
 *
 * importance: 1~4 (별 개수, 숫자가 클수록 중요)
 * status: "upcoming" | "done"  (done = 이 파일 작성 시점 기준 이미 발표된 이벤트)
 *
 * 사용 예 (브라우저, 스크립트 태그로 로드):
 *   <script src="september-2026-schedule.js"></script>
 *   <script>
 *     SeptSchedule.SEPTEMBER_2026_SCHEDULE.forEach(ev => console.log(ev.dateKST, ev.event));
 *     document.getElementById("wrap").innerHTML = SeptSchedule.renderTableHTML();
 *   </script>
 *
 * 사용 예 (Node.js / ES 모듈 번들러):
 *   const SeptSchedule = require('./september-2026-schedule.js');
 *   console.log(SeptSchedule.SEPTEMBER_2026_SCHEDULE);
 */
(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    // CommonJS (Node.js)
    module.exports = factory();
  } else if (typeof define === "function" && define.amd) {
    // AMD
    define([], factory);
  } else {
    // 브라우저 전역 변수: window.SeptSchedule
    root.SeptSchedule = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var SEPTEMBER_2026_SCHEDULE = [
    {
      id: "avgo-q3-earnings",
      dateKST: "2026-09-03",
      timeKST: "05:05",
      dateLabel: "9/3(목) 새벽",
      event: "브로드컴(AVGO) FY26 3분기 실적 발표",
      tickers: ["AVGOUSDT.P", "SOXLUSDT.P", "NVDAUSDT.P", "AMDUSDT.P"],
      importance: 3,
      status: "done",
      note: "미국 현지 9/2 장마감 후 발표"
    },
    {
      id: "us-nfp-august",
      dateKST: "2026-09-04",
      timeKST: "21:30",
      dateLabel: "9/4(금)",
      event: "미국 8월 비농업고용지표(NFP)",
      tickers: ["전 종목", "BTCUSDT.P", "XAUUSDT.P", "SPYUSDT.P", "QQQUSDT.P"],
      importance: 3,
      status: "upcoming",
      note: ""
    },
    {
      id: "apple-event-sept",
      dateKST: "2026-09-10",
      timeKST: "02:00",
      dateLabel: "9/10(목) 새벽",
      event: "애플 신제품 발표 'Surprise and Shine' (아이폰18 공개)",
      tickers: ["AAPLUSDT.P", "QQQUSDT.P"],
      importance: 3,
      status: "upcoming",
      note: "현지시간 9/9 10am PT 시작"
    },
    {
      id: "tsmc-august-revenue",
      dateKST: "2026-09-10",
      timeKST: "14:30",
      dateLabel: "9/10(목)",
      event: "TSMC 8월 매출 발표",
      tickers: ["TSMUSDT.P", "NVDAUSDT.P", "AMDUSDT.P", "SOXLUSDT.P"],
      importance: 2,
      status: "upcoming",
      note: ""
    },
    {
      id: "us-ppi-august",
      dateKST: "2026-09-10",
      timeKST: "21:30",
      dateLabel: "9/10(목)",
      event: "미국 8월 생산자물가지수(PPI)",
      tickers: ["전 종목"],
      importance: 2,
      status: "upcoming",
      note: ""
    },
    {
      id: "korea-trade-early-sept",
      dateKST: "2026-09-11",
      timeKST: "09:00",
      dateLabel: "9/11(금) 오전",
      event: "관세청 9월 1~10일 수출입(반도체 수출) 잠정치",
      tickers: ["EWYUSDT.P", "KORUUSDT.P", "SKHYUSDT.P"],
      importance: 1,
      status: "upcoming",
      note: "발표 시각은 변동 가능"
    },
    {
      id: "us-cpi-august",
      dateKST: "2026-09-11",
      timeKST: "21:30",
      dateLabel: "9/11(금)",
      event: "미국 8월 소비자물가지수(CPI)",
      tickers: ["전 종목"],
      importance: 3,
      status: "upcoming",
      note: ""
    },
    {
      id: "us-retail-sales-august",
      dateKST: "2026-09-16",
      timeKST: "21:30",
      dateLabel: "9/16(수)",
      event: "미국 8월 소매판매",
      tickers: ["SPYUSDT.P", "QQQUSDT.P"],
      importance: 2,
      status: "upcoming",
      note: ""
    },
    {
      id: "fomc-decision",
      dateKST: "2026-09-17",
      timeKST: "03:00",
      dateLabel: "9/17(목) 새벽",
      event: "FOMC 금리 결정",
      tickers: ["전 종목 최대 변수"],
      importance: 4,
      status: "upcoming",
      note: "9/15~16 회의, 03:30 파월 기자회견"
    },
    {
      id: "fomc-press-conference",
      dateKST: "2026-09-17",
      timeKST: "03:30",
      dateLabel: "9/17(목) 새벽",
      event: "파월 의장 기자회견",
      tickers: ["전 종목 최대 변수"],
      importance: 4,
      status: "upcoming",
      note: ""
    },
    {
      id: "quad-witching",
      dateKST: "2026-09-18",
      timeKST: "22:30",
      dateLabel: "9/18(금) 밤 ~ 9/19(토) 새벽",
      event: "쿼드러플 위칭데이 (분기 옵션·선물 동시만기, 지수 리밸런싱)",
      tickers: ["SPYUSDT.P", "QQQUSDT.P", "SOXLUSDT.P"],
      importance: 2,
      status: "upcoming",
      note: "미 정규장 09/18 22:30~09/19 05:00(KST)"
    },
    {
      id: "us-jolts-august",
      dateKST: "2026-09-29",
      timeKST: "23:00",
      dateLabel: "9/29(화)",
      event: "미국 8월 JOLTS(구인·이직보고서)",
      tickers: ["전 종목"],
      importance: 1,
      status: "upcoming",
      note: ""
    },
    {
      id: "us-pce-gdp-august",
      dateKST: "2026-09-30",
      timeKST: "21:30",
      dateLabel: "9/30(수)",
      event: "미국 8월 PCE 물가지수(연준 선호 지표) + 2분기 GDP 확정치",
      tickers: ["전 종목", "XAUUSDT.P", "BTCUSDT.P"],
      importance: 3,
      status: "upcoming",
      note: ""
    },
    {
      id: "us-fiscal-year-end",
      dateKST: "2026-09-30",
      timeKST: "13:00",
      dateLabel: "9/30(수)~10/1(목) 낮",
      event: "미국 회계연도 종료 / 예산안 처리 불발 시 정부 셧다운 리스크",
      tickers: ["전체 리스크자산"],
      importance: 2,
      status: "upcoming",
      note: "불확실성 이벤트, 실제 발생 여부는 의회 협상에 따라 유동적"
    },
    {
      id: "mu-q4-earnings",
      dateKST: "2026-10-01",
      timeKST: "05:00",
      dateLabel: "10/1(목) 새벽",
      event: "마이크론(MU) FY26 4분기 실적 발표",
      tickers: ["MUUSDT.P", "SOXLUSDT.P", "SNDKUSDT.P", "SKHYUSDT.P"],
      importance: 3,
      status: "upcoming",
      note: "미국 현지 9/30 장마감 후 발표, 시각은 추정치"
    }
  ];

  // --- 편의 함수들 ---

  /** importance 숫자를 별표 문자열로 변환 (예: 3 -> "★★★") */
  function starsFor(importance) {
    return "★".repeat(importance) + "☆".repeat(4 - importance);
  }

  /** 날짜(dateKST) 오름차순으로 정렬된 복사본 반환 */
  function sortedByDate(list) {
    list = list || SEPTEMBER_2026_SCHEDULE;
    return list.slice().sort(function (a, b) {
      var da = a.dateKST + " " + a.timeKST;
      var db = b.dateKST + " " + b.timeKST;
      return da < db ? -1 : da > db ? 1 : 0;
    });
  }

  /** 특정 티커가 관련된 이벤트만 필터링 (예: filterByTicker("SOXLUSDT.P")) */
  function filterByTicker(ticker, list) {
    list = list || SEPTEMBER_2026_SCHEDULE;
    return list.filter(function (ev) {
      return ev.tickers.indexOf(ticker) !== -1;
    });
  }

  /** 중요도 이상인 이벤트만 필터링 (예: filterByMinImportance(3)) */
  function filterByMinImportance(min, list) {
    list = list || SEPTEMBER_2026_SCHEDULE;
    return list.filter(function (ev) {
      return ev.importance >= min;
    });
  }

  /** 아직 발생하지 않은(status === "upcoming") 이벤트만 반환 */
  function upcomingOnly(list) {
    list = list || SEPTEMBER_2026_SCHEDULE;
    return list.filter(function (ev) {
      return ev.status === "upcoming";
    });
  }

  /** <table> HTML 문자열로 렌더링 (그대로 innerHTML에 꽂아 쓸 수 있음) */
  function renderTableHTML(list) {
    list = sortedByDate(list || SEPTEMBER_2026_SCHEDULE);
    var rows = list
      .map(function (ev) {
        return (
          "<tr>" +
          "<td>" + ev.dateLabel + " " + ev.timeKST + "</td>" +
          "<td>" + ev.event + (ev.note ? " <small>(" + ev.note + ")</small>" : "") + "</td>" +
          "<td>" + ev.tickers.join(", ") + "</td>" +
          "<td>" + starsFor(ev.importance) + "</td>" +
          "</tr>"
        );
      })
      .join("\n");

    return (
      "<table>\n" +
      "<thead><tr><th>날짜/시간 (KST)</th><th>이벤트</th><th>관련 종목</th><th>중요도</th></tr></thead>\n" +
      "<tbody>\n" + rows + "\n</tbody>\n" +
      "</table>"
    );
  }

  return {
    SEPTEMBER_2026_SCHEDULE: SEPTEMBER_2026_SCHEDULE,
    starsFor: starsFor,
    sortedByDate: sortedByDate,
    filterByTicker: filterByTicker,
    filterByMinImportance: filterByMinImportance,
    upcomingOnly: upcomingOnly,
    renderTableHTML: renderTableHTML
  };
});

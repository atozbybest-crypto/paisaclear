/* PaisaClear Market Game — 15 companies, a scripted story arc, daily streaks
   and a local leaderboard. Everything is simulated; no real prices. */

(function () {
  "use strict";

  var START_CASH = 100000;
  var TICK_MS = 2600;
  var STORE = "paisaclear-market-v2";
  var BOARD = "paisaclear-market-board-v1";

  var COMPANIES = [
    { id: "sunrise", name: "Sunrise Bank", sector: "Banking", price: 420, drift: 0.0006, vol: 0.018 },
    { id: "nova", name: "NovaTech Systems", sector: "Technology", price: 1850, drift: 0.0009, vol: 0.028 },
    { id: "steel", name: "Bharat Steel Works", sector: "Metals", price: 96, drift: 0.0002, vol: 0.032 },
    { id: "greenleaf", name: "GreenLeaf Foods", sector: "FMCG", price: 640, drift: 0.0005, vol: 0.012 },
    { id: "skyjet", name: "SkyJet Airlines", sector: "Aviation", price: 148, drift: -0.0002, vol: 0.038 },
    { id: "orbit", name: "Orbit Pharma", sector: "Pharma", price: 980, drift: 0.0004, vol: 0.022 },
    { id: "meridian", name: "Meridian Energy", sector: "Energy", price: 310, drift: 0.0004, vol: 0.026 },
    { id: "coastal", name: "Coastal Cement", sector: "Cement", price: 720, drift: 0.0005, vol: 0.024 },
    { id: "pixel", name: "Pixel Media", sector: "Media", price: 88, drift: 0.0003, vol: 0.034 },
    { id: "securelife", name: "SecureLife Insurance", sector: "Insurance", price: 540, drift: 0.0004, vol: 0.017 },
    { id: "farmfresh", name: "FarmFresh Agri", sector: "Agri", price: 205, drift: 0.0003, vol: 0.030 },
    { id: "urban", name: "Urban Motors", sector: "Auto", price: 1120, drift: 0.0006, vol: 0.023 },
    { id: "quantum", name: "Quantum Telecom", sector: "Telecom", price: 165, drift: 0.0002, vol: 0.021 },
    { id: "heritage", name: "Heritage Textiles", sector: "Textiles", price: 74, drift: 0.0001, vol: 0.029 },
    { id: "zenith", name: "Zenith Capital", sector: "NBFC", price: 1240, drift: 0.0008, vol: 0.033 }
  ];

  /* Scripted turns so a session has a story, not just noise. */
  var STORY = [
    { day: 6, title: "The rate cut", text: "The central bank cuts rates by 50bps. Lenders rally, borrowers too.",
      moves: { Banking: 0.06, NBFC: 0.07, Auto: 0.04, Insurance: -0.02 } },
    { day: 11, title: "Global selloff", text: "A selloff abroad drags everything down. Nothing is spared.",
      moves: { "*": -0.075 } },
    { day: 16, title: "Crude spikes", text: "Oil jumps on supply worries. Airlines bleed; energy gains.",
      moves: { Aviation: -0.09, Energy: 0.06, Cement: -0.03, Textiles: -0.02 } },
    { day: 21, title: "Flight to safety", text: "Money runs to steady earners. FMCG and pharma rise, tech slips.",
      moves: { FMCG: 0.05, Pharma: 0.04, Technology: -0.05, Media: -0.04 } },
    { day: 27, title: "Earnings season", text: "Results split the market. Quality pays, cyclicals disappoint.",
      moves: { Banking: 0.03, Metals: -0.06, Agri: -0.04, Cement: 0.03 } }
  ];

  var GOOD_NEWS = [
    "{name} beats profit estimates, guidance raised",
    "{name} wins a large order, brokers turn positive",
    "{name} announces a buyback, shares jump",
    "{name} expands capacity, margin outlook improves"
  ];
  var BAD_NEWS = [
    "{name} misses estimates, margin pressure continues",
    "{name} faces a regulatory probe, shares slide",
    "{name} loses a key client, guidance cut",
    "{name} reports a weak quarter, analysts downgrade"
  ];

  var LEVELS = [
    { at: 100000, label: "Keep your capital" },
    { at: 110000, label: "First 10% gain" },
    { at: 125000, label: "₹1.25 lakh" },
    { at: 150000, label: "₹1.5 lakh" },
    { at: 200000, label: "Double your money" },
    { at: 300000, label: "Triple" }
  ];

  var BADGES = [
    { id: "first", label: "First trade", test: c },
    { id: "ten", label: "Ten trades", test: c },
    { id: "profit", label: "First profit", test: c },
    { id: "loss", label: "Took a loss", test: c },
    { id: "stayed", label: "Held through a crash", test: c },
    { id: "rich", label: "Crossed ₹1,25,000", test: c }
  ];

  function c() { return false; }

  var state = load() || fresh();
  var paused = false;
  var el = {};

  function fresh() {
    var prices = {}, history = {};
    COMPANIES.forEach(function (x) { prices[x.id] = x.price; history[x.id] = [x.price]; });
    return {
      cash: START_CASH, day: 1, prices: prices, history: history, holdings: {},
      trades: 0, realised: 0, badges: [], streak: 1, lastDay: null,
      best: START_CASH, storySeen: [], finished: false,
      news: [{ text: "Market opens. ₹1,00,000 of paper money. Every trade is a lesson.", tone: "neutral", day: 1 }],
      log: []
    };
  }

  function save() { try { localStorage.setItem(STORE, JSON.stringify(state)); } catch (e) {} }
  function load() { try { var r = localStorage.getItem(STORE); return r ? JSON.parse(r) : null; } catch (e) { return null; } }

  function money(v) {
    var neg = v < 0; v = Math.abs(Math.round(v));
    var s = v.toString(), last = s.slice(-3), rest = s.slice(0, -3);
    if (rest) rest = rest.replace(/\B(?=(\d{2})+(?!\d))/g, ",");
    return (neg ? "-" : "") + "₹" + (rest ? rest + "," + last : last);
  }
  function pct(v) { return (v >= 0 ? "+" : "") + v.toFixed(2) + "%"; }
  function name(id) { var c = byId(id); return c ? c.name : id; }
  function byId(id) { return COMPANIES.filter(function (x) { return x.id === id; })[0]; }

  function netWorth() {
    var t = state.cash;
    Object.keys(state.holdings).forEach(function (id) { t += state.holdings[id].qty * state.prices[id]; });
    return t;
  }

  /* ---------------- daily streak ---------------- */

  function applyStreak() {
    var today = new Date().toISOString().slice(0, 10);
    if (state.lastDay === today) return null;
    var yesterday = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
    state.streak = state.lastDay === yesterday ? Math.min(30, state.streak + 1) : 1;
    state.lastDay = today;
    var bonus = Math.min(10000, 1000 * state.streak);
    state.cash += bonus;
    return { streak: state.streak, bonus: bonus };
  }

  /* ---------------- market engine ---------------- */

  function tick() {
    if (state.finished) return;
    state.day += 1;

    var story = STORY.filter(function (s) { return s.day === state.day; })[0];
    if (story) {
      COMPANIES.forEach(function (c2) {
        var mv = story.moves[c2.sector];
        if (mv === undefined) mv = story.moves["*"];
        if (mv === undefined) return;
        applyMove(c2, mv);
      });
      state.news.unshift({ text: story.title + " — " + story.text, tone: "story", day: state.day });
      say(story.title + ": " + story.text, "warn");
    }

    COMPANIES.forEach(function (comp) {
      if (story && (story.moves[comp.sector] !== undefined || story.moves["*"] !== undefined)) return;
      var prev = state.prices[comp.id];
      var shock = (Math.random() * 2 - 1) * comp.vol * 2.1;
      if (Math.random() < 0.05) {
        var good = Math.random() < 0.5;
        shock += (0.025 + Math.random() * 0.05) * (good ? 1 : -1);
        var line = (good ? GOOD_NEWS : BAD_NEWS)[Math.floor(Math.random() * 4)].replace("{name}", comp.name);
        state.news.unshift({ text: line, tone: good ? "good" : "bad", day: state.day });
      }
      setPrice(comp, Math.max(5, prev * (1 + comp.drift + shock)));
    });

    state.news = state.news.slice(0, 8);
    checkBadges();
    checkFinish();
    save();
    render();
  }

  function applyMove(comp, mv) {
    setPrice(comp, Math.max(5, state.prices[comp.id] * (1 + mv)));
  }

  function setPrice(comp, value) {
    state.prices[comp.id] = Math.round(value * 100) / 100;
    state.history[comp.id].push(state.prices[comp.id]);
    if (state.history[comp.id].length > 90) state.history[comp.id].shift();
  }

  function checkFinish() {
    var worth = netWorth();
    state.best = Math.max(state.best, worth);
    if (worth < START_CASH * 0.25) {
      state.finished = true;
      finish("Wiped out");
    }
  }

  /* ---------------- trading ---------------- */

  function buy(id, qty) {
    var price = state.prices[id], cost = price * qty;
    if (state.finished) return say("This run is over. Start a new one.", "warn");
    if (!qty || qty < 1) return say("Choose how many shares first.", "warn");
    if (cost > state.cash) return say("Not enough cash — you have " + money(state.cash) + ".", "warn");
    state.cash -= cost;
    var h = state.holdings[id] || { qty: 0, avg: 0 };
    h.avg = (h.avg * h.qty + cost) / (h.qty + qty);
    h.qty += qty;
    state.holdings[id] = h;
    state.trades += 1;

    var hist = state.history[id];
    var rise = hist.length > 6 ? (hist[hist.length - 1] / hist[hist.length - 6] - 1) * 100 : 0;
    if (rise > 8) say("Bought " + qty + " × " + name(id) + ". It is already up " + rise.toFixed(1) +
      "% in five days — that is chasing a rally.", "warn");
    else say("Bought " + qty + " × " + name(id) + " at " + money(price) + ".", "good");
    checkBadges(); save(); render();
  }

  function sell(id, qty) {
    var h = state.holdings[id];
    if (!h) return say("You do not hold " + name(id) + ".", "warn");
    qty = Math.min(qty || 0, h.qty);
    if (qty < 1) return say("Choose how many shares to sell.", "warn");
    var price = state.prices[id], proceeds = price * qty, basis = h.avg * qty, pnl = proceeds - basis;
    state.realised += pnl;
    state.cash += proceeds;
    h.qty -= qty;
    if (h.qty === 0) delete state.holdings[id];
    state.trades += 1;
    if (pnl < 0) say("Sold at a loss of " + money(Math.abs(pnl)) + ". Selling into a fall locks the loss in.", "bad");
    else say("Sold for a profit of " + money(pnl) + ".", "good");
    checkBadges(); save(); render();
  }

  /* ---------------- badges, levels ---------------- */

  function checkBadges() {
    var worth = netWorth();
    var rules = {
      first: state.trades >= 1,
      ten: state.trades >= 10,
      profit: state.realised > 0,
      loss: state.realised < 0,
      stayed: state.day > 12 && Object.keys(state.holdings).length > 0,
      rich: worth >= 125000
    };
    Object.keys(rules).forEach(function (k) {
      if (rules[k] && state.badges.indexOf(k) === -1) {
        state.badges.push(k);
        var label = BADGES.filter(function (b) { return b.id === k; })[0].label;
        state.news.unshift({ text: "Badge unlocked: " + label, tone: "good", day: state.day });
      }
    });
  }

  function level() {
    var worth = netWorth(), out = LEVELS[0];
    LEVELS.forEach(function (l) { if (worth >= l.at) out = l; });
    return out;
  }

  /* ---------------- finish + leaderboard ---------------- */

  function board() {
    try { return JSON.parse(localStorage.getItem(BOARD) || "[]"); } catch (e) { return []; }
  }

  function finish(reason) {
    var worth = netWorth();
    var entry = { score: Math.round(worth), day: state.day, trades: state.trades,
                  pnl: Math.round(worth - START_CASH), reason: reason || "Retired",
                  at: new Date().toISOString().slice(0, 10) };
    var list = board();
    list.push(entry);
    list.sort(function (a, b) { return b.score - a.score; });
    list = list.slice(0, 10);
    try { localStorage.setItem(BOARD, JSON.stringify(list)); } catch (e) {}
    state.finished = true;
    save();
    render();
    say("Run finished — " + reason + ". " + money(worth) + " after " + state.day + " days. Saved to the board.", "warn");
  }

  /* ---------------- rendering ---------------- */

  function say(text, tone) {
    state.log.unshift({ text: text, tone: tone });
    state.log = state.log.slice(0, 5);
    paintLog();
  }

  function paintLog() {
    if (!el.log) return;
    el.log.innerHTML = state.log.map(function (l) {
      return '<p class="mg-log-line is-' + l.tone + '">' + l.text + "</p>";
    }).join("") || '<p class="mg-log-line is-neutral">Pick a company and trade. The market moves every few seconds.</p>';
  }

  function sparkline(points, up) {
    if (points.length < 2) return "";
    var w = 120, h = 34, min = Math.min.apply(null, points), max = Math.max.apply(null, points);
    var span = max - min || 1;
    var d = points.map(function (p, i) {
      return (i ? "L" : "M") + ((i / (points.length - 1)) * w).toFixed(1) + " " + (h - ((p - min) / span) * h).toFixed(1);
    }).join(" ");
    return '<svg class="mg-spark" viewBox="0 0 ' + w + " " + h + '" preserveAspectRatio="none"><path d="' + d +
      '" fill="none" stroke="' + (up ? "#0F5132" : "#B42318") + '" stroke-width="2"/></svg>';
  }

  function render() {
    var worth = netWorth(), pnl = worth - START_CASH;
    el.cash.textContent = money(state.cash);
    el.worth.textContent = money(worth);
    el.pnl.textContent = money(pnl);
    el.pnl.className = "mg-stat-value " + (pnl >= 0 ? "is-up" : "is-down");
    el.day.textContent = "Day " + state.day;
    if (el.streak) el.streak.textContent = "🔥 " + state.streak + " day streak";
    if (el.goal) {
      var lv = level(), next = LEVELS.filter(function (l) { return l.at > worth; })[0];
      el.goal.innerHTML = "<span>Level: <strong>" + lv.label + "</strong></span>" +
        (next ? "<span>Next: " + money(next.at) + "</span>" : "<span>Top level reached</span>");
    }

    el.market.innerHTML = COMPANIES.map(function (c2) {
      var hist = state.history[c2.id], prev = hist[hist.length - 2] || hist[0];
      var ch = ((state.prices[c2.id] / prev) - 1) * 100, held = state.holdings[c2.id];
      return '<tr><td><span class="mg-co">' + c2.name + '</span><span class="mg-sector">' + c2.sector + "</span></td>" +
        '<td class="mg-num">' + money(state.prices[c2.id]) + "</td>" +
        '<td class="mg-num ' + (ch >= 0 ? "is-up" : "is-down") + '">' + pct(ch) + "</td>" +
        "<td>" + sparkline(hist, ch >= 0) + "</td>" +
        '<td class="mg-actions"><button class="mg-btn mg-buy" data-buy="' + c2.id + '">Buy</button>' +
        '<button class="mg-btn mg-sell" data-sell="' + c2.id + '"' + (held ? "" : " disabled") + ">Sell</button></td>" +
        '<td class="mg-num small">' + (held ? held.qty : "—") + "</td></tr>";
    }).join("");

    el.portfolio.innerHTML = Object.keys(state.holdings).map(function (id) {
      var h = state.holdings[id], val = h.qty * state.prices[id], pl = val - h.avg * h.qty;
      return "<tr><td>" + name(id) + "</td><td class='mg-num'>" + h.qty + "</td><td class='mg-num'>" +
        money(h.avg) + "</td><td class='mg-num'>" + money(state.prices[id]) + "</td><td class='mg-num " +
        (pl >= 0 ? "is-up" : "is-down") + "'>" + money(pl) + "</td></tr>";
    }).join("") || '<tr><td colspan="5" class="mg-empty">No holdings yet. Buy something to start.</td></tr>';

    el.news.innerHTML = state.news.map(function (n) {
      return '<li class="is-' + n.tone + '">' + n.text + "</li>";
    }).join("");

    el.badges.innerHTML = BADGES.map(function (b) {
      return '<span class="mg-badge' + (state.badges.indexOf(b.id) !== -1 ? " is-on" : "") + '">' + b.label + "</span>";
    }).join("");

    if (el.board) {
      var list = board();
      el.board.innerHTML = list.length ? list.map(function (b, i) {
        return "<tr><td>" + (i + 1) + "</td><td class='mg-num'>" + money(b.score) + "</td><td class='mg-num'>" +
          (b.pnl >= 0 ? "+" : "") + money(b.pnl) + "</td><td class='mg-num'>" + b.day + "</td><td>" + b.reason + "</td></tr>";
      }).join("") : '<tr><td colspan="5" class="mg-empty">No runs yet. Retire a portfolio to get on the board.</td></tr>';
    }
    paintLog();
  }

  /* ---------------- boot ---------------- */

  function boot() {
    ["cash", "worth", "pnl", "day", "market", "portfolio", "news", "badges", "log", "streak", "goal", "board"]
      .forEach(function (k) { el[k] = document.getElementById("mg-" + k); });
    if (!el.market) return;

    var bonus = applyStreak();
    if (bonus) {
      state.news.unshift({ text: "Daily bonus: " + money(bonus.bonus) + " for a " + bonus.streak + "-day streak.",
                           tone: "good", day: state.day });
    }
    save();

    el.market.addEventListener("click", function (e) {
      var qty = parseInt((document.getElementById("mg-qty") || {}).value, 10) || 1;
      var b = e.target.getAttribute("data-buy"), s = e.target.getAttribute("data-sell");
      if (b) buy(b, qty);
      if (s) sell(s, qty);
    });

    var play = document.getElementById("mg-play");
    if (play) play.addEventListener("click", function () {
      paused = !paused; play.textContent = paused ? "Resume" : "Pause";
    });

    var reset = document.getElementById("mg-reset");
    if (reset) reset.addEventListener("click", function () {
      state = fresh(); save(); render(); applyStreakKeep();
      say("Fresh start. ₹1,00,000, day 1.", "neutral");
    });

    var retire = document.getElementById("mg-retire");
    if (retire) retire.addEventListener("click", function () {
      if (!state.finished) finish("Retired");
    });

    var share = document.getElementById("mg-share");
    if (share) share.addEventListener("click", function () {
      var text = "PaisaClear Market Game — " + money(netWorth()) + " after " + state.day + " days. " +
                 "₹1,00,000 of paper money. paisaclear.co.in/market-game";
      if (navigator.share) navigator.share({ text: text }).catch(function () {});
      else if (navigator.clipboard) navigator.clipboard.writeText(text).then(function () { say("Score copied. Paste it anywhere.", "good"); });
    });

    render();
    setInterval(function () { if (!paused) tick(); }, TICK_MS);
  }

  function applyStreakKeep() { try { localStorage.setItem(STORE, JSON.stringify(state)); } catch (e) {} }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();

/* Interactive layer for the HTML reports (inlined by report_renderer.py). No dependencies. */
(function () {
  "use strict";
  var SVGNS = "http://www.w3.org/2000/svg";

  // ---------- theme ----------
  function storedTheme() { try { return localStorage.getItem("report-theme"); } catch (e) { return null; } }
  function storeTheme(t) { try { localStorage.setItem("report-theme", t); } catch (e) { /* private mode */ } }
  var initial = storedTheme();
  if (initial) document.documentElement.setAttribute("data-theme", initial);
  function currentTheme() {
    var t = document.documentElement.getAttribute("data-theme");
    if (t) return t;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  function labelToggle(btn) { btn.textContent = currentTheme() === "dark" ? "Light mode" : "Dark mode"; }
  document.querySelectorAll(".theme-toggle").forEach(function (btn) {
    labelToggle(btn);
    btn.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      storeTheme(next);
      labelToggle(btn);
      redrawAll();
    });
  });

  // ---------- number formatting (mirrors doc_utils.fmt_value) ----------
  function fmtUSD(v, compact) {
    if (v === null || v === undefined) return "N/A";
    var a = Math.abs(v), s = v < 0 ? "-" : "";
    if (compact) {
      if (a >= 1e9) return s + "$" + trim(a / 1e9) + "B";
      if (a >= 1e6) return s + "$" + trim(a / 1e6) + "M";
      if (a >= 1e3) return s + "$" + trim(a / 1e3) + "K";
      return s + "$" + trim(a);
    }
    if (a >= 1e9) return s + "$" + (a / 1e9).toFixed(2) + "B";
    if (a >= 1e6) return s + "$" + (a / 1e6).toFixed(1) + "M";
    if (a >= 1e3) return s + "$" + (a / 1e3).toFixed(1) + "K";
    return s + "$" + a.toFixed(2);
  }
  function trim(x) { return (Math.round(x * 10) / 10).toString(); }
  function formatter(unit, compact) {
    if (unit === "usd") return function (v) { return fmtUSD(v, compact); };
    if (unit === "pct") return function (v) { return v === null ? "N/A" : (compact ? trim(v) : v.toFixed(1)) + "%"; };
    if (unit === "x") return function (v) { return v === null ? "N/A" : v.toFixed(compact ? 1 : 2) + "x"; };
    if (unit === "price") return function (v) { return v === null ? "N/A" : "$" + v.toFixed(2); };
    return function (v) { return v === null ? "N/A" : (Math.abs(v) >= 1000 ? Math.round(v).toLocaleString() : trim(v)); };
  }
  var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  function catLabel(c, long) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(c);
    if (!m) return c;
    return long ? MONTHS[+m[2] - 1] + " " + (+m[3]) + ", " + m[1] : MONTHS[+m[2] - 1] + " '" + m[1].slice(2);
  }

  // ---------- svg helpers ----------
  function el(name, attrs, parent) {
    var n = document.createElementNS(SVGNS, name);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }
  function text(parent, x, y, str, attrs) {
    var t = el("text", Object.assign({ x: x, y: y }, attrs || {}), parent);
    t.textContent = str;
    return t;
  }
  function cssVar(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }
  function niceTicks(lo, hi, count) {
    if (lo === hi) { hi = lo + 1; }
    var span = hi - lo, step = Math.pow(10, Math.floor(Math.log10(span / count)));
    var err = (count * step) / span;
    if (err <= 0.15) step *= 10; else if (err <= 0.35) step *= 5; else if (err <= 0.75) step *= 2;
    var t0 = Math.floor(lo / step) * step, t1 = Math.ceil(hi / step) * step, out = [];
    for (var v = t0; v <= t1 + step / 2; v += step) out.push(Math.abs(v) < step / 1e6 ? 0 : v);
    return out;
  }
  // A bar with a 4px rounded data-end, square at the baseline.
  function barPath(x, w, yBase, yTip) {
    var r = Math.min(4, w / 2, Math.abs(yBase - yTip));
    if (yTip <= yBase) {
      return "M" + x + "," + yBase + "V" + (yTip + r) + "Q" + x + "," + yTip + " " + (x + r) + "," + yTip +
        "H" + (x + w - r) + "Q" + (x + w) + "," + yTip + " " + (x + w) + "," + (yTip + r) + "V" + yBase + "Z";
    }
    return "M" + x + "," + yBase + "V" + (yTip - r) + "Q" + x + "," + yTip + " " + (x + r) + "," + yTip +
      "H" + (x + w - r) + "Q" + (x + w) + "," + yTip + " " + (x + w) + "," + (yTip - r) + "V" + yBase + "Z";
  }

  // ---------- tooltip ----------
  function tooltip(canvas) {
    var tip = document.createElement("div");
    tip.className = "tooltip";
    tip.setAttribute("role", "status");
    canvas.appendChild(tip);
    return {
      show: function (head, rows, x, y) {
        tip.replaceChildren();
        var h = document.createElement("div"); h.className = "tt-head"; h.textContent = head; tip.appendChild(h);
        rows.forEach(function (r) {
          var row = document.createElement("div"); row.className = "tt-row";
          if (r.color) { var k = document.createElement("span"); k.className = "tt-key"; k.style.background = r.color; row.appendChild(k); }
          var v = document.createElement("span"); v.className = "tt-val"; v.textContent = r.value; row.appendChild(v);
          var n = document.createElement("span"); n.className = "tt-name"; n.textContent = r.name; row.appendChild(n);
          if (r.note) { var o = document.createElement("span"); o.className = "tt-note"; o.textContent = "· " + r.note; row.appendChild(o); }
          tip.appendChild(row);
        });
        tip.classList.add("show");
        var cw = canvas.clientWidth, tw = tip.offsetWidth, th = tip.offsetHeight;
        var left = x + 14; if (left + tw > cw) left = Math.max(0, x - tw - 14);
        tip.style.left = left + "px";
        tip.style.top = Math.max(0, y - th / 2) + "px";
      },
      hide: function () { tip.classList.remove("show"); }
    };
  }

  // ---------- data table view ----------
  function dataTable(fig, data) {
    var det = document.createElement("details"); det.className = "viz-data";
    var sum = document.createElement("summary"); sum.textContent = "Show data"; det.appendChild(sum);
    var wrap = document.createElement("div"); wrap.className = "table-wrap";
    var tbl = document.createElement("table"), thead = tbl.createTHead(), hr = thead.insertRow(), body = tbl.createTBody();
    var f = formatter(data.unit, false);
    function th(t, num) { var c = document.createElement("th"); c.textContent = t; if (num) c.className = "num"; hr.appendChild(c); }
    if (data.kind === "waterfall") {
      th("Step"); th("Value", true);
      data.steps.forEach(function (s) {
        var r = body.insertRow(); r.insertCell().textContent = s.label;
        var c = r.insertCell(); c.className = "num"; c.textContent = f(s.value);
      });
    } else {
      th("Period");
      data.series.forEach(function (s) { th(s.name, true); });
      data.categories.forEach(function (cat, i) {
        var r = body.insertRow(); r.insertCell().textContent = catLabel(cat, true);
        data.series.forEach(function (s) {
          var c = r.insertCell(); c.className = "num";
          c.textContent = f(s.values[i]) + (s.notes && s.notes[i] ? " (" + s.notes[i] + ")" : "");
        });
      });
    }
    wrap.appendChild(tbl); det.appendChild(wrap); fig.appendChild(det);
  }

  // ---------- legend ----------
  function legend(cap, data, state, kind, redraw) {
    var box = document.createElement("div"); box.className = "legend";
    var f = formatter(data.unit, false);
    data.series.forEach(function (s, i) {
      var b = document.createElement("button"); b.type = "button";
      b.setAttribute("aria-pressed", "true");
      var sw = document.createElement("span"); sw.className = "swatch" + (kind === "line" ? " line" : "");
      sw.style.background = "var(--series-" + (i + 1) + ")"; b.appendChild(sw);
      var name = document.createElement("span"); name.textContent = s.name; b.appendChild(name);
      var last = null;
      for (var k = s.values.length - 1; k >= 0; k--) if (s.values[k] !== null) { last = s.values[k]; break; }
      var lv = document.createElement("span"); lv.className = "latest"; lv.textContent = f(last); b.appendChild(lv);
      b.title = "Latest value; click to hide or show " + s.name;
      b.addEventListener("click", function () {
        var visibleCount = state.visible.filter(Boolean).length;
        if (state.visible[i] && visibleCount === 1) return;   // keep at least one series
        state.visible[i] = !state.visible[i];
        b.setAttribute("aria-pressed", String(state.visible[i]));
        redraw();
      });
      box.appendChild(b);
    });
    cap.appendChild(box);
  }

  // ---------- bar & line charts ----------
  function drawSeriesChart(canvas, data, state, tip) {
    var kind = data.kind;
    var W = Math.max(320, canvas.clientWidth), H = Math.round(Math.min(380, Math.max(240, W * 0.42)));
    var m = { top: 16, right: 16, bottom: 34, left: 62 };
    var iw = W - m.left - m.right, ih = H - m.top - m.bottom;
    var svg = el("svg", { viewBox: "0 0 " + W + " " + H, role: "img", tabindex: "0",
      "aria-label": data.title + " — use left and right arrow keys to read values" });
    var shown = data.series.map(function (s, i) { return { s: s, i: i }; }).filter(function (o) { return state.visible[o.i]; });
    var vals = [];
    shown.forEach(function (o) { o.s.values.forEach(function (v) { if (v !== null) vals.push(v); }); });
    var lo = Math.min.apply(null, vals.concat(kind === "bar" ? [0] : [])), hi = Math.max.apply(null, vals.concat(kind === "bar" ? [0] : []));
    if (kind === "line") { var pad = (hi - lo) * 0.06 || 1; lo -= pad; hi += pad; }
    var ticks = niceTicks(lo, hi, 5);
    if (kind === "bar") { lo = Math.min(lo, ticks[0]); hi = Math.max(hi, ticks[ticks.length - 1]); }
    else { lo = ticks[0]; hi = ticks[ticks.length - 1]; }
    function y(v) { return m.top + ih - ((v - lo) / (hi - lo)) * ih; }
    var fTick = formatter(data.unit, true), fVal = formatter(data.unit, false);
    var g = el("g", {}, svg);
    ticks.forEach(function (t) {
      if (t < lo - 1e-9 || t > hi + 1e-9) return;
      el("line", { x1: m.left, x2: W - m.right, y1: y(t), y2: y(t), class: t === 0 && kind === "bar" ? "baseline" : "gridline" }, g);
      text(g, m.left - 8, y(t) + 4, fTick(t), { "text-anchor": "end" });
    });
    var n = data.categories.length, band = iw / n;
    var every = Math.max(1, Math.ceil(n / Math.max(2, Math.floor(iw / 70))));
    data.categories.forEach(function (c, i) {
      if (i % every !== 0 && i !== n - 1) return;
      if (i === n - 1 && i % every !== 0 && (n - 1) % every < every / 2) return;
      text(g, m.left + band * (i + 0.5), H - m.bottom + 18, catLabel(c), { "text-anchor": "middle" });
    });
    var marks = el("g", {}, svg);
    if (kind === "bar") {
      var k = shown.length, gap = 2;
      var bw = Math.max(3, Math.min(24, (band * 0.72 - gap * (k - 1)) / k));
      var groupW = bw * k + gap * (k - 1);
      shown.forEach(function (o, j) {
        o.s.values.forEach(function (v, i) {
          if (v === null) return;
          var x = m.left + band * i + (band - groupW) / 2 + j * (bw + gap);
          el("path", { d: barPath(x, bw, y(0), y(v)), fill: "var(--series-" + (o.i + 1) + ")" }, marks);
        });
      });
    } else {
      shown.forEach(function (o) {
        var d = "", pen = false;
        o.s.values.forEach(function (v, i) {
          if (v === null) { pen = false; return; }
          d += (pen ? "L" : "M") + (m.left + band * (i + 0.5)) + "," + y(v); pen = true;
        });
        el("path", { d: d, fill: "none", stroke: "var(--series-" + (o.i + 1) + ")", "stroke-width": 2,
          "stroke-linejoin": "round", "stroke-linecap": "round" }, marks);
        for (var i = o.s.values.length - 1; i >= 0; i--) {
          if (o.s.values[i] !== null) {
            el("circle", { cx: m.left + band * (i + 0.5), cy: y(o.s.values[i]), r: 4, fill: "var(--series-" + (o.i + 1) + ")",
              stroke: "var(--surface)", "stroke-width": 2 }, marks);
            break;
          }
        }
      });
    }
    // hover layer
    var hover = el("g", {}, svg), hl = null, cross = null, active = -1;
    if (kind === "bar") hl = el("rect", { class: "band-hit", y: m.top, height: ih, width: band }, hover);
    else cross = el("line", { class: "crosshair", y1: m.top, y2: m.top + ih, visibility: "hidden" }, hover);
    if (hl) marks.parentNode.insertBefore(hover, marks);
    function activate(i) {
      if (i < 0 || i >= n) return;
      active = i;
      var cx = m.left + band * (i + 0.5);
      if (hl) { hl.setAttribute("x", m.left + band * i); hl.classList.add("active"); }
      if (cross) { cross.setAttribute("x1", cx); cross.setAttribute("x2", cx); cross.setAttribute("visibility", "visible"); }
      var rows = shown.map(function (o) {
        return { color: "var(--series-" + (o.i + 1) + ")", value: fVal(o.s.values[i]), name: o.s.name,
          note: o.s.notes ? o.s.notes[i] : null };
      });
      var scale = canvas.clientWidth / W;
      tip.show(catLabel(data.categories[i], true), rows, cx * scale, (m.top + ih / 3) * scale);
    }
    function clear() { active = -1; if (hl) hl.classList.remove("active"); if (cross) cross.setAttribute("visibility", "hidden"); tip.hide(); }
    svg.addEventListener("pointermove", function (e) {
      var r = svg.getBoundingClientRect(), x = (e.clientX - r.left) * (W / r.width);
      var i = Math.floor((x - m.left) / band);
      if (i >= 0 && i < n) activate(i); else clear();
    });
    svg.addEventListener("pointerleave", clear);
    svg.addEventListener("blur", clear);
    svg.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { activate(Math.min(n - 1, active + 1)); e.preventDefault(); }
      else if (e.key === "ArrowLeft") { activate(active < 0 ? n - 1 : Math.max(0, active - 1)); e.preventDefault(); }
      else if (e.key === "Escape") clear();
    });
    return svg;
  }

  // ---------- waterfall ----------
  function drawWaterfall(canvas, data, state, tip) {
    var W = Math.max(320, canvas.clientWidth), H = Math.round(Math.min(340, Math.max(220, W * 0.36)));
    var m = { top: 26, right: 16, bottom: 34, left: 62 };
    var iw = W - m.left - m.right, ih = H - m.top - m.bottom;
    var svg = el("svg", { viewBox: "0 0 " + W + " " + H, role: "img", tabindex: "0",
      "aria-label": data.title + " — use left and right arrow keys to read values" });
    var run = 0, bars = data.steps.map(function (s) {
      var from = s.total ? 0 : run, to = s.total ? s.value : run + s.value;
      run = to;
      return { s: s, from: from, to: to };
    });
    var pts = [0];
    bars.forEach(function (b) { pts.push(b.from, b.to); });
    var ticks = niceTicks(Math.min.apply(null, pts), Math.max.apply(null, pts), 5);
    var lo = ticks[0], hi = ticks[ticks.length - 1];
    function y(v) { return m.top + ih - ((v - lo) / (hi - lo)) * ih; }
    var fTick = formatter(data.unit, true), fVal = formatter(data.unit, false);
    var g = el("g", {}, svg);
    ticks.forEach(function (t) {
      el("line", { x1: m.left, x2: W - m.right, y1: y(t), y2: y(t), class: t === 0 ? "baseline" : "gridline" }, g);
      text(g, m.left - 8, y(t) + 4, fTick(t), { "text-anchor": "end" });
    });
    var n = bars.length, band = iw / n, bw = Math.min(64, band * 0.5);
    var hover = el("g", {}, svg), hl = el("rect", { class: "band-hit", y: m.top, height: ih, width: band }, hover);
    var marks = el("g", {}, svg);
    bars.forEach(function (b, i) {
      var x = m.left + band * i + (band - bw) / 2;
      var up = b.to >= b.from, color = b.s.total ? (b.to >= 0 ? "var(--pos)" : "var(--neg)") : (up ? "var(--pos)" : "var(--neg)");
      var top = Math.min(y(b.from), y(b.to)), h = Math.max(1, Math.abs(y(b.from) - y(b.to)));
      if (b.s.total) el("path", { d: barPath(x, bw, y(0), y(b.to)), fill: color }, marks);
      else el("rect", { x: x, y: top, width: bw, height: h, rx: 3, fill: color, "fill-opacity": 0.75 }, marks);
      if (i < n - 1) {
        var nx = m.left + band * (i + 1) + (band - bw) / 2;
        el("line", { x1: x + bw, x2: nx, y1: y(b.to), y2: y(b.to), class: "connector" }, marks);
      }
      var ly = (b.to >= b.from ? Math.min(y(b.to), y(b.from)) - 8 : Math.max(y(b.to), y(b.from)) + 16);
      text(marks, x + bw / 2, b.s.total ? (b.to >= 0 ? y(b.to) - 8 : y(b.to) + 16) : ly,
        (b.s.total || b.s.value < 0 ? "" : "+") + fVal(b.s.total ? b.to : b.s.value), { "text-anchor": "middle", class: "value-label" });
      text(g, m.left + band * (i + 0.5), H - m.bottom + 18, b.s.label, { "text-anchor": "middle" });
    });
    var active = -1;
    function activate(i) {
      if (i < 0 || i >= n) return;
      active = i; hl.setAttribute("x", m.left + band * i); hl.classList.add("active");
      var b = bars[i], scale = canvas.clientWidth / W;
      var rows = [{ value: fVal(b.s.total ? b.to : b.s.value), name: b.s.total ? "total" : "change" }];
      if (!b.s.total) rows.push({ value: fVal(b.to), name: "running total" });
      tip.show(b.s.label, rows, (m.left + band * (i + 0.5)) * scale, (m.top + ih / 3) * scale);
    }
    function clear() { active = -1; hl.classList.remove("active"); tip.hide(); }
    svg.addEventListener("pointermove", function (e) {
      var r = svg.getBoundingClientRect(), x = (e.clientX - r.left) * (W / r.width), i = Math.floor((x - m.left) / band);
      if (i >= 0 && i < n) activate(i); else clear();
    });
    svg.addEventListener("pointerleave", clear);
    svg.addEventListener("blur", clear);
    svg.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { activate(Math.min(n - 1, active + 1)); e.preventDefault(); }
      else if (e.key === "ArrowLeft") { activate(active < 0 ? n - 1 : Math.max(0, active - 1)); e.preventDefault(); }
      else if (e.key === "Escape") clear();
    });
    return svg;
  }

  // ---------- chart bootstrap ----------
  var charts = [];
  function redrawAll() { charts.forEach(function (c) { c.draw(); }); }
  document.querySelectorAll("figure.viz[data-chart]").forEach(function (fig) {
    var data;
    try { data = JSON.parse(fig.querySelector("script.chart-data").textContent); } catch (e) { return; }
    var cap = fig.querySelector("figcaption");
    var canvas = document.createElement("div"); canvas.className = "viz-canvas";
    fig.insertBefore(canvas, cap.nextSibling);
    var state = { visible: (data.series || []).map(function () { return true; }) };
    var tip = tooltip(canvas), svg = null;
    function draw() {
      var next = data.kind === "waterfall" ? drawWaterfall(canvas, data, state, tip) : drawSeriesChart(canvas, data, state, tip);
      if (svg) canvas.replaceChild(next, svg); else canvas.insertBefore(next, canvas.firstChild);
      svg = next;
    }
    if (data.series && data.series.length > 1) legend(cap, data, state, data.kind, draw);
    dataTable(fig, data);
    var src = fig.querySelector(".source");
    if (src) fig.appendChild(src);
    charts.push({ draw: draw });
    draw();
    if (window.ResizeObserver) {
      var lastW = canvas.clientWidth;
      new ResizeObserver(function () { if (Math.abs(canvas.clientWidth - lastW) > 4) { lastW = canvas.clientWidth; draw(); } }).observe(canvas);
    }
  });

  // ---------- sortable tables ----------
  function parseCell(t) {
    var s = t.replace(/[−–]/g, "-").replace(/,/g, "");
    var mm = /(-)?\s*\$?\s*(\d*\.?\d+)\s*([BMK%x×])?/.exec(s);
    if (!mm) return null;
    var v = parseFloat(mm[2]);
    if (mm[1] || /^\s*\(.*\)\s*$/.test(s)) v = -v;
    var mult = { B: 1e9, M: 1e6, K: 1e3 }[mm[3]];
    return mult ? v * mult : v;
  }
  document.querySelectorAll("table.sortable").forEach(function (tbl) {
    var heads = tbl.tHead ? tbl.tHead.rows[0].cells : [];
    Array.prototype.forEach.call(heads, function (th, col) {
      th.classList.add("sortable");
      th.tabIndex = 0;
      function sort() {
        var dir = th.getAttribute("aria-sort") === "descending" ? "ascending" : "descending";
        Array.prototype.forEach.call(heads, function (h) { h.removeAttribute("aria-sort"); });
        th.setAttribute("aria-sort", dir);
        var body = tbl.tBodies[0], rows = Array.prototype.slice.call(body.rows);
        rows.sort(function (a, b) {
          var x = a.cells[col] ? a.cells[col].textContent : "", y2 = b.cells[col] ? b.cells[col].textContent : "";
          var nx = parseCell(x), ny = parseCell(y2), r;
          if (nx !== null && ny !== null) r = nx - ny;
          else if (nx !== null) r = -1; else if (ny !== null) r = 1;
          else r = x.localeCompare(y2);
          return dir === "ascending" ? r : -r;
        });
        rows.forEach(function (r) { body.appendChild(r); });
      }
      th.addEventListener("click", sort);
      th.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); sort(); } });
    });
  });

  // ---------- table of contents scroll-spy ----------
  var links = document.querySelectorAll(".toc a[href^='#']");
  if (links.length && window.IntersectionObserver) {
    var byId = {};
    links.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          links.forEach(function (a) { a.classList.remove("active"); });
          var a = byId[en.target.id]; if (a) a.classList.add("active");
        }
      });
    }, { rootMargin: "0px 0px -70% 0px" });
    Object.keys(byId).forEach(function (id) { var h = document.getElementById(id); if (h) obs.observe(h); });
  }

  // ---------- library search ----------
  var search = document.getElementById("library-search");
  if (search) {
    search.addEventListener("input", function () {
      var q = search.value.trim().toLowerCase();
      document.querySelectorAll(".card").forEach(function (c) {
        c.style.display = !q || c.textContent.toLowerCase().indexOf(q) !== -1 ? "" : "none";
      });
    });
  }
})();

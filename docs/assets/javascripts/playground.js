(function () {
  const ASSET_NAMES = ["NIFTY 50", "HUL"];
  const SVG_NS = "http://www.w3.org/2000/svg";

  function percent(value, digits = 2) {
    return `${(value * 100).toFixed(digits)}%`;
  }

  function alphaLabel(value) {
    return `${Number(value).toFixed(2)}%`;
  }

  function roundToAlphaStep(value) {
    return Number((Math.round((value - 1) / 0.25) * 0.25 + 1).toFixed(2));
  }

  function validateAlphaInput(rawValue) {
    const trimmed = String(rawValue).trim();
    if (!trimmed || !/^-?\d+(\.\d+)?$/.test(trimmed)) {
      return { valid: false, message: "Enter a number from 1.00 to 10.00." };
    }

    const value = Number(trimmed);
    if (!Number.isFinite(value) || value < 1 || value > 10) {
      return { valid: false, message: "Alpha must be between 1.00 and 10.00." };
    }

    return { valid: true, value: roundToAlphaStep(value) };
  }

  function makeSvg(width, height) {
    const svg = document.createElementNS(SVG_NS, "svg");
    svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", "100%");
    svg.setAttribute("role", "img");
    return svg;
  }

  function addSvgEl(parent, name, attrs = {}) {
    const el = document.createElementNS(SVG_NS, name);
    Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, value));
    parent.appendChild(el);
    return el;
  }

  function findMetric(assetData, alphaPercent) {
    return assetData.metrics_by_alpha.reduce((best, item) => {
      const bestDiff = Math.abs(best.alpha_percent - alphaPercent);
      const itemDiff = Math.abs(item.alpha_percent - alphaPercent);
      return itemDiff < bestDiff ? item : best;
    });
  }

  function tailBinIndices(histogram, metric) {
    const tailData = histogram.tail_bins_by_alpha;
    if (Array.isArray(tailData)) {
      const match = tailData.find((item) => Math.abs(item.alpha_percent - metric.alpha_percent) < 0.0001);
      return match ? new Set(match.bin_indices) : new Set();
    }

    const bins = tailData && tailData[metric.label] ? tailData[metric.label] : [];
    return new Set(bins);
  }

  function metricBlock(label, value) {
    return `
      <div class="pg-metric">
        <span>${label}</span>
        <strong>${value}</strong>
      </div>
    `;
  }

  function renderHistogram(assetName, assetData, metric) {
    const histogram = assetData.histogram;
    const counts = histogram.counts;
    const edges = histogram.bin_edges;
    const centers = histogram.bin_centers;
    const tailBins = tailBinIndices(histogram, metric);

    const width = 520;
    const height = 240;
    const margin = { top: 14, right: 16, bottom: 34, left: 38 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const xMin = Math.min(...edges);
    const xMax = Math.max(...edges);
    const yMax = Math.max(...counts, 1);
    const xScale = (x) => margin.left + ((x - xMin) / (xMax - xMin)) * innerWidth;
    const yScale = (y) => margin.top + innerHeight - (y / yMax) * innerHeight;

    const svg = makeSvg(width, height);
    addSvgEl(svg, "line", { x1: margin.left, y1: margin.top + innerHeight, x2: width - margin.right, y2: margin.top + innerHeight, stroke: "currentColor", "stroke-opacity": "0.35" });
    addSvgEl(svg, "line", { x1: margin.left, y1: margin.top, x2: margin.left, y2: margin.top + innerHeight, stroke: "currentColor", "stroke-opacity": "0.25" });

    counts.forEach((count, index) => {
      const x0 = xScale(edges[index]);
      const x1 = xScale(edges[index + 1]);
      const y = yScale(count);
      const fill = tailBins.has(index) ? "#c0392b" : "#6c8ebf";
      const opacity = tailBins.has(index) ? "0.82" : "0.48";
      addSvgEl(svg, "rect", {
        x: x0,
        y,
        width: Math.max(1, x1 - x0 - 1),
        height: margin.top + innerHeight - y,
        fill,
        opacity,
      });
    });

    const thresholdX = xScale(metric.var_threshold_return);
    addSvgEl(svg, "line", {
      x1: thresholdX,
      y1: margin.top,
      x2: thresholdX,
      y2: margin.top + innerHeight,
      stroke: "#111111",
      "stroke-width": "2",
      "stroke-dasharray": "5 4",
    });

    addSvgEl(svg, "text", { x: thresholdX + 5, y: margin.top + 12, class: "pg-tick" }).textContent = "VaR";
    addSvgEl(svg, "text", { x: margin.left, y: height - 10, class: "pg-axis-label" }).textContent = `${assetName} daily log returns`;
    addSvgEl(svg, "text", { x: width - margin.right - 58, y: height - 10, class: "pg-axis-label" }).textContent = "Return";
    return svg;
  }

  function renderAssetCard(assetName, assetData, metric) {
    const card = document.createElement("section");
    card.className = "pg-card";
    card.innerHTML = `
      <h3>${assetName}</h3>
      <div class="pg-metrics">
        ${metricBlock("Historical VaR", percent(metric.historical_var))}
        ${metricBlock("Historical CVaR", percent(metric.historical_cvar))}
        ${metricBlock("Tail Amplification", `${metric.historical_tail_amplification.toFixed(2)}x`)}
      </div>
      <div class="pg-chart-title">Histogram with selected tail shaded</div>
      <div class="pg-chart pg-histogram"></div>
    `;
    card.querySelector(".pg-histogram").appendChild(renderHistogram(assetName, assetData, metric));
    return card;
  }

  function singleInterpretation(assetName, metric) {
    return `
      <p>At an alpha of <strong>${metric.label}</strong>, the historical VaR for <strong>${assetName}</strong> is <strong>${percent(metric.historical_var)}</strong>.</p>
      <p>This means that on roughly the worst ${metric.label} of observed trading days, the daily loss exceeded ${percent(metric.historical_var)}.</p>
      <p>The corresponding historical CVaR is <strong>${percent(metric.historical_cvar)}</strong>, meaning that once the return enters that tail, the average loss is about ${percent(metric.historical_cvar)}.</p>
      <p>The tail amplification is <strong>${metric.historical_tail_amplification.toFixed(2)}x</strong>, showing how much larger the average tail loss is relative to the VaR threshold.</p>
    `;
  }

  function compareWord(a, b) {
    return a > b ? "higher" : a < b ? "lower" : "about the same";
  }

  function compareInterpretation(metricA, metricB) {
    const varWord = compareWord(metricA.historical_var, metricB.historical_var);
    const cvarWord = compareWord(metricA.historical_cvar, metricB.historical_cvar);
    const ampAsset = metricA.historical_tail_amplification >= metricB.historical_tail_amplification ? "NIFTY 50" : "HUL";

    return `
      <p>At an alpha of <strong>${metricA.label}</strong>, NIFTY 50 has a <strong>${varWord}</strong> historical VaR than HUL.</p>
      <p>NIFTY 50 also has a <strong>${cvarWord}</strong> historical CVaR at this tail level.</p>
      <p>The tail amplification for NIFTY 50 is <strong>${metricA.historical_tail_amplification.toFixed(2)}x</strong>, while HUL is <strong>${metricB.historical_tail_amplification.toFixed(2)}x</strong>.</p>
      <p>Based on the selected alpha, <strong>${ampAsset}</strong> worsens more after crossing the VaR threshold in relative terms.</p>
    `;
  }

  function render(root, data, state) {
    const visibleAssets = state.mode === "single" ? [state.asset] : ASSET_NAMES;
    const metrics = {};
    visibleAssets.forEach((asset) => {
      metrics[asset] = findMetric(data.assets[asset], state.alpha);
    });

    root.innerHTML = `
      <div class="pg-panel ${state.mode === "compare" ? "pg-compare-mode" : "pg-single-mode"}">
        <div class="pg-controls">
          <div>
            <span class="pg-mode-label">Mode</span>
            <div class="pg-mode-buttons">
              <button type="button" data-mode="single" class="${state.mode === "single" ? "active" : ""}">Single Asset</button>
              <button type="button" data-mode="compare" class="${state.mode === "compare" ? "active" : ""}">Compare Two Assets</button>
            </div>
          </div>
          <div class="pg-control" id="pg-asset-control">
            <label for="pg-asset-select">Asset</label>
            <select id="pg-asset-select">
              ${ASSET_NAMES.map((asset) => `<option value="${asset}" ${asset === state.asset ? "selected" : ""}>${asset}</option>`).join("")}
            </select>
          </div>
          <div class="pg-control pg-alpha-control">
            <label for="pg-alpha-slider">Alpha level</label>
            <div class="pg-alpha-row">
              <input id="pg-alpha-slider" type="range" min="1" max="10" step="0.25" value="${state.alpha}">
              <input id="pg-alpha-input" class="pg-alpha-input" type="text" inputmode="decimal" value="${Number(state.alpha).toFixed(2)}" aria-label="Alpha percentage input">
              <span class="pg-alpha-value">${alphaLabel(state.alpha)}</span>
            </div>
            <div class="pg-alpha-error" id="pg-alpha-error" aria-live="polite"></div>
          </div>
        </div>
        <div class="pg-grid" id="pg-cards"></div>
        <div class="pg-note" id="pg-interpretation"></div>
      </div>
    `;

    const assetControl = root.querySelector("#pg-asset-control");
    assetControl.style.display = state.mode === "single" ? "block" : "none";

    const cardGrid = root.querySelector("#pg-cards");
    visibleAssets.forEach((asset) => {
      cardGrid.appendChild(renderAssetCard(asset, data.assets[asset], metrics[asset]));
    });

    const interpretation = root.querySelector("#pg-interpretation");
    if (state.mode === "single") {
      interpretation.innerHTML = singleInterpretation(state.asset, metrics[state.asset]);
    } else {
      interpretation.innerHTML = compareInterpretation(metrics["NIFTY 50"], metrics.HUL);
    }
    interpretation.insertAdjacentHTML(
      "beforeend",
      `
        <div class="pg-secondary-note">
          An increase in tail amplification with higher \\(\\alpha\\) can be a normal empirical pattern, but it is not guaranteed theoretically. It suggests that average losses beyond the VaR cutoff are becoming larger relative to the cutoff itself, although some of this movement may also reflect sampling and estimation noise.
        </div>
      `
    );

    root.querySelectorAll("[data-mode]").forEach((button) => {
      button.addEventListener("click", () => {
        state.mode = button.dataset.mode;
        render(root, data, state);
      });
    });

    const assetSelect = root.querySelector("#pg-asset-select");
    if (assetSelect) {
      assetSelect.addEventListener("change", (event) => {
        state.asset = event.target.value;
        render(root, data, state);
      });
    }

    root.querySelector("#pg-alpha-slider").addEventListener("input", (event) => {
      state.alpha = Number(event.target.value);
      render(root, data, state);
    });

    const alphaInput = root.querySelector("#pg-alpha-input");
    const alphaError = root.querySelector("#pg-alpha-error");
    const applyManualAlpha = () => {
      const result = validateAlphaInput(alphaInput.value);
      if (!result.valid) {
        alphaInput.classList.add("has-error");
        alphaError.textContent = result.message;
        return;
      }

      state.alpha = result.value;
      render(root, data, state);
    };

    alphaInput.addEventListener("change", applyManualAlpha);
    alphaInput.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        applyManualAlpha();
      }
    });

    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise([interpretation]);
    }
  }

  async function init() {
    const root = document.querySelector("#var-playground");
    if (!root) {
      return;
    }

    try {
      const dataUrl = new URL("../assets/data/playground_data.json", window.location.href);
      const response = await fetch(dataUrl);
      if (!response.ok) {
        throw new Error(`Could not load ${dataUrl.pathname}`);
      }
      const data = await response.json();
      const state = { mode: "single", asset: "NIFTY 50", alpha: 5 };
      render(root, data, state);
    } catch (error) {
      root.innerHTML = `
        <div class="pg-error">
          <strong>Playground data is not available yet.</strong>
          <p>Run <code>python3 build_playground_data.py</code> from the project root to generate <code>docs/assets/data/playground_data.json</code>, then reload this page.</p>
        </div>
      `;
      console.error(error);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

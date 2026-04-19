import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from risk_metrics import historical_cvar, historical_var


DATA_DIR = Path("datasets") / "trio1"
JSON_OUTPUT = Path("docs") / "assets" / "data" / "playground_data.json"
PREVIEW_DIR = Path("docs") / "assets" / "images" / "playground"

ASSET_FILES = {
    "NIFTY 50": DATA_DIR / "nifty50_2years.xlsx",
    "HUL": DATA_DIR / "hul_2years.xlsx",
}

PREVIEW_NAMES = {
    "NIFTY 50": "nifty_preview.png",
    "HUL": "hul_preview.png",
}


def read_excel_safely(path):
    df = pd.read_excel(path)

    # Some downloaded files have a blank first row instead of real headers.
    unnamed = [str(col).lower().startswith("unnamed") for col in df.columns]
    if sum(unnamed) >= max(1, len(df.columns) - 1):
        df = pd.read_excel(path, header=None)
        df = df.dropna(how="all").reset_index(drop=True)

        if df.shape[1] == 7:
            df.columns = ["Date", "Adj Close", "Close", "High", "Low", "Open", "Volume"]
        elif df.shape[1] == 6:
            df.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        else:
            df.columns = ["Date"] + [f"Column_{i}" for i in range(1, df.shape[1])]

    df.columns = [str(col).strip() for col in df.columns]
    return df


def clean_name(name):
    return str(name).strip().lower().replace("_", " ").replace("-", " ")


def parse_dates(series):
    numeric = pd.to_numeric(series, errors="coerce")
    numeric_share = numeric.notna().mean()

    if numeric_share > 0.8 and numeric.dropna().between(20000, 60000).mean() > 0.8:
        return pd.to_datetime(numeric, unit="D", origin="1899-12-30", errors="coerce")

    return pd.to_datetime(series, errors="coerce", dayfirst=True)


def detect_date_column(df):
    for col in df.columns:
        if "date" in clean_name(col):
            return col

    scores = {}
    for col in df.columns:
        scores[col] = parse_dates(df[col]).notna().mean()

    best_col = max(scores, key=scores.get)
    if scores[best_col] < 0.6:
        raise ValueError("Could not detect a reliable date column.")
    return best_col


def detect_price_column(df, date_col):
    candidates = [col for col in df.columns if col != date_col]
    names = {col: clean_name(col) for col in candidates}

    preferred = [
        "adj close",
        "adjusted close",
        "close",
        "closing price",
        "price",
        "ltp",
        "last price",
        "last",
    ]

    for target in preferred:
        for col, name in names.items():
            if name == target:
                return col

    for target in preferred:
        for col, name in names.items():
            if target in name:
                return col

    numeric_cols = []
    for col in candidates:
        numeric_share = pd.to_numeric(df[col], errors="coerce").notna().mean()
        if numeric_share > 0.8:
            numeric_cols.append(col)

    if not numeric_cols:
        raise ValueError("Could not detect a reliable price column.")

    return numeric_cols[0]


def prepare_asset(path, asset_name):
    df = read_excel_safely(path)
    date_col = detect_date_column(df)
    price_col = detect_price_column(df, date_col)

    print(f"{asset_name}: detected date column = '{date_col}', price column = '{price_col}'")

    clean = pd.DataFrame(
        {
            "date": parse_dates(df[date_col]),
            "price": pd.to_numeric(df[price_col], errors="coerce"),
        }
    )

    clean = clean.dropna(subset=["date", "price"])
    clean = clean.drop_duplicates(subset="date", keep="last")
    clean = clean.sort_values("date").reset_index(drop=True)
    clean["log_return"] = np.log(clean["price"] / clean["price"].shift(1))
    clean = clean.dropna(subset=["log_return"]).reset_index(drop=True)

    print(f"{asset_name}: {len(clean)} daily return observations")
    return clean, date_col, price_col


def build_alpha_grid():
    alphas = np.round(np.arange(0.01, 0.1000001, 0.0025), 4)
    return [
        {
            "alpha": float(alpha),
            "alpha_percent": float(alpha * 100),
            "label": f"{alpha * 100:.2f}%",
        }
        for alpha in alphas
    ]


def build_metrics(returns, alpha_grid):
    metrics = []

    for item in alpha_grid:
        alpha = item["alpha"]
        h_var = historical_var(returns, alpha)
        h_cvar = historical_cvar(returns, alpha)

        metrics.append(
            {
                "alpha": item["alpha"],
                "alpha_percent": item["alpha_percent"],
                "label": item["label"],
                "historical_var": h_var,
                "historical_cvar": h_cvar,
                "historical_tail_amplification": h_cvar / h_var if h_var != 0 else None,
                "var_threshold_return": -h_var,
            }
        )

    return metrics


def build_histogram(returns, metrics, bins=40):
    counts, bin_edges = np.histogram(returns, bins=bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    tail_bins_by_alpha = []
    for metric in metrics:
        tail_indices = np.where(bin_centers <= metric["var_threshold_return"])[0]
        tail_bins_by_alpha.append(
            {
                "alpha": metric["alpha"],
                "alpha_percent": metric["alpha_percent"],
                "label": metric["label"],
                "var_threshold_return": metric["var_threshold_return"],
                "bin_indices": [int(index) for index in tail_indices],
            }
        )

    return {
        "bin_edges": [float(value) for value in bin_edges],
        "bin_centers": [float(value) for value in bin_centers],
        "counts": [int(value) for value in counts],
        "tail_bins_by_alpha": tail_bins_by_alpha,
    }


def build_summary(clean):
    returns = clean["log_return"]
    return {
        "observations": int(returns.count()),
        "start_date": clean["date"].min().strftime("%Y-%m-%d"),
        "end_date": clean["date"].max().strftime("%Y-%m-%d"),
        "mean_return": float(returns.mean()),
        "std_dev": float(returns.std(ddof=1)),
        "min_return": float(returns.min()),
        "max_return": float(returns.max()),
        "skewness": float(returns.skew()),
        "kurtosis": float(returns.kurtosis()),
    }


def save_preview_plot(asset_name, returns, histogram, metrics):
    preview_metric = next(metric for metric in metrics if metric["label"] == "5.00%")
    threshold = preview_metric["var_threshold_return"]

    fig, ax = plt.subplots(figsize=(7, 4), dpi=180)
    counts = histogram["counts"]
    edges = histogram["bin_edges"]
    centers = histogram["bin_centers"]
    widths = np.diff(edges)

    for count, center, width in zip(counts, centers, widths):
        color = "#c0392b" if center <= threshold else "#6c8ebf"
        alpha = 0.75 if center <= threshold else 0.55
        ax.bar(center, count, width=width, color=color, edgecolor="black", alpha=alpha)

    ax.axvline(threshold, color="#111111", linestyle="--", linewidth=1.6, label="5% VaR threshold")
    ax.set_title(f"{asset_name}: Daily Log Return Tail Preview")
    ax.set_xlabel("Daily log return")
    ax.set_ylabel("Frequency")
    ax.legend()
    plt.tight_layout()

    output_path = PREVIEW_DIR / PREVIEW_NAMES[asset_name]
    fig.savefig(output_path)
    plt.close(fig)
    print(f"{asset_name}: saved preview plot to {output_path}")


def main():
    JSON_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

    alpha_grid = build_alpha_grid()
    output = {
        "metadata": {
            "description": "Precomputed historical VaR/CVaR playground data for MkDocs.",
            "frequency": "daily",
            "return_type": "log_return",
            "method": "historical",
            "sign_convention": "VaR and CVaR are positive loss magnitudes; histogram values are in return space.",
            "alpha_min": 0.01,
            "alpha_max": 0.10,
            "alpha_step": 0.0025,
        },
        "alpha_grid": alpha_grid,
        "assets": {},
    }

    for asset_name, path in ASSET_FILES.items():
        clean, date_col, price_col = prepare_asset(path, asset_name)
        returns = clean["log_return"]
        metrics = build_metrics(returns, alpha_grid)
        histogram = build_histogram(returns, metrics)

        output["assets"][asset_name] = {
            "source_file": str(path),
            "detected_date_column": date_col,
            "detected_price_column": price_col,
            "summary": build_summary(clean),
            "histogram": histogram,
            "metrics_by_alpha": metrics,
        }

        save_preview_plot(asset_name, returns, histogram, metrics)

    with JSON_OUTPUT.open("w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

    print()
    print("Playground data build complete.")
    print(f"Assets processed: {', '.join(ASSET_FILES)}")
    print(f"Alpha points generated: {len(alpha_grid)}")
    print(f"JSON output: {JSON_OUTPUT}")
    print(f"Preview image folder: {PREVIEW_DIR}")


if __name__ == "__main__":
    main()

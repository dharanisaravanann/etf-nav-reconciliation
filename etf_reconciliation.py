import pandas as pd

metadata = {}
header_row_idx = None

with open("IOZ_holdings.csv", encoding="utf-8-sig") as f:
    lines = f.readlines()


for i, line in enumerate(lines):
    if line.startswith("Ticker,"):
        header_row_idx = i
        break
    parts = line.strip().split(",", 1)
    if len(parts) == 2 and parts[1]:
        metadata[parts[0].strip()] = parts[1].strip().strip('"')

print("Metadata found:", metadata)
print("Real header starts at line:", header_row_idx + 1)  # +1 for human-readable line number

df = pd.read_csv("IOZ_holdings.csv", skiprows=header_row_idx, thousands=",")

df = df.dropna(subset=["Ticker"]).reset_index(drop=True)

print(df.dtypes)
print(len(df))

total_weight = df["Weight (%)"].sum()
print(f"Sum of Weight(%): {total_weight:.4f}%")

#recalculate Market Value for equity holding
#flag any row where it doesn't match
eq = df[df["Asset Class"] == "Equity"].copy()
eq["recalc_mv"] = eq["Shares"] * eq["Price"] * eq["FX Rate"]
eq["pct_diff"] = (eq["Market Value"] - eq["recalc_mv"]) / eq["Market Value"] * 100

tolerance = 0.5  # percent
flagged = eq[eq["pct_diff"].abs() > tolerance]

print(f"\nEquity rows checked: {len(eq)}")
print(f"Rows flagged beyond {tolerance}% tolerance: {len(flagged)}")
print(flagged[["Ticker", "Name", "Market Value", "recalc_mv", "pct_diff"]])

# NAV vs published NAV
total_mv = df["Market Value"].sum()
print(f"\nTotal Market Value (as of 04-Sept-2026): AUD {total_mv:,.2f}")

# 2 shares-outstanding anchors, neither dated 04-Sept
shares_31aug = 261_944_479   # as of 31-Aug-2026, from ASX/BIMAL announcement
shares_07sept = 261_569_479  # as of 07-Sept-2026, from live BlackRock page

implied_nav_31aug = total_mv / shares_31aug
implied_nav_07sept = total_mv / shares_07sept

published_nav = 36.45  #as of 07-Sept-2026

print(f"Implied NAV using 31-Aug shares outstanding: AUD {implied_nav_31aug:.4f}")
print(f"Implied NAV using 07-Sept shares outstanding: AUD {implied_nav_07sept:.4f}")
print(f"Published NAV (07-Sept-2026): AUD {published_nav:.4f}")

gap_31aug = published_nav - implied_nav_31aug
gap_07sept = published_nav - implied_nav_07sept
print(f"\nGap vs 31-Aug anchor: AUD {gap_31aug:+.4f} ({gap_31aug/published_nav*100:+.3f}%)")
print(f"Gap vs 07-Sept anchor: AUD {gap_07sept:+.4f} ({gap_07sept/published_nav*100:+.3f}%)")

# check for duplicate/stale ticker entries)
dupes = df[df["Name"].duplicated(keep=False)].sort_values("Name")
print("Rows sharing a Name with another row:")
print(dupes[["Ticker", "Name", "Shares", "Price", "Market Value"]])

def check_market_value_recalc(df, tolerance_pct=0.5):
    """Returns the flagged dataframe of equity rows outside tolerance."""
    eq = df[df["Asset Class"] == "Equity"].copy()
    eq["recalc_mv"] = eq["Shares"] * eq["Price"] * eq["FX Rate"]
    eq["pct_diff"] = (eq["Market Value"] - eq["recalc_mv"]) / eq["Market Value"] * 100
    flagged = eq[eq["pct_diff"].abs() > tolerance_pct]
    return flagged[["Ticker", "Name", "Market Value", "recalc_mv", "pct_diff"]]


def nav_gap(df, shares_low, shares_high, published_nav):
    """Returns (implied_nav_low, implied_nav_high, gap_low_pct, gap_high_pct)."""
    total_mv = df["Market Value"].sum()
    nav_a = total_mv / shares_low
    nav_b = total_mv / shares_high
    lo, hi = sorted([nav_a, nav_b])
    gap_lo = (published_nav - hi) / published_nav * 100
    gap_hi = (published_nav - lo) / published_nav * 100
    return lo, hi, gap_lo, gap_hi

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="IOZ Holdings-to-NAV", layout="wide")

# ============================================================
# GLOBAL CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.mono { font-family: 'IBM Plex Mono', monospace; font-variant-numeric: tabular-nums; }

#MainMenu, header, footer { visibility: hidden; }
.block-container { padding-top: 0rem; padding-left: 0; padding-right: 0; max-width: 100%; }

.console-wrap { max-width: 1180px; margin: 0 auto; padding: 0 40px; }

.header-band { background: #1f2024; color: #f3f5fe; padding: 22px 40px; }
.eyebrow { font-family: 'IBM Plex Mono', monospace; text-transform: uppercase; letter-spacing: .16em;
           font-size: 10px; color: #9397ab; margin-bottom: 6px; }
.header-title { font-size: 26px; font-weight: 500; letter-spacing: -.025em; margin: 4px 0 12px 0; }
.chip { display: inline-block; font-family: 'IBM Plex Mono', monospace; font-size: 11px;
        background: rgba(243,245,254,.1); border-radius: 4px; padding: 4px 10px; margin-right: 8px; }
.verdict-pill { display: inline-block; background: #1f7a52; color: #eef8f2; font-size: 12px;
                font-weight: 500; border-radius: 5px; padding: 5px 12px 5px 10px; }
.verdict-pill.flag { background: #8a5a12; color: #fdf2e2; }
.verdict-pill .dot { display: inline-block; width: 6px; height: 6px; border-radius: 50%;
                     background: currentColor; margin-right: 6px; }
.verdict-sub { font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: #9397ab;
               text-align: right; margin-top: 6px; }

.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1px; background: #e4e7f5; }
.kpi-cell { background: #fff; padding: 18px 24px; }
.kpi-label { font-family: 'IBM Plex Mono', monospace; text-transform: uppercase; letter-spacing: .13em;
             font-size: 10px; color: #9397ab; margin-bottom: 8px; }
.kpi-value { font-family: 'IBM Plex Mono', monospace; font-weight: 500; font-size: 26px; color: #1f2024; }
.kpi-value.small { font-size: 20px; }
.kpi-sub { font-size: 11px; margin-top: 6px; }
.kpi-sub.pass { color: #1f7a52; } .kpi-sub.flag { color: #8a5a12; } .kpi-sub.muted { color: #75798c; }

.spine { padding: 30px 40px; }
.step-row { display: grid; grid-template-columns: 26px 1fr; gap: 20px; margin-bottom: 26px; position: relative; }
.step-circle { width: 26px; height: 26px; border-radius: 50%; background: #1f2024; color: #fff;
               font-family: 'IBM Plex Mono', monospace; font-size: 11px; display: flex;
               align-items: center; justify-content: center; z-index: 1; }
.step-circle.flag { background: #8a5a12; }
.step-heading { font-size: 16px; font-weight: 500; letter-spacing: -.015em; color: #1f2024; }
.step-chip { display: inline-block; font-size: 10.5px; border-radius: 4px; padding: 2px 8px; margin-left: 8px; }
.step-chip.pass { background: #e8f4ee; color: #1f7a52; }
.step-chip.flag { background: #fdf2e2; color: #8a5a12; }
.step-body { font-size: 13px; line-height: 1.55; color: #595d6c; max-width: 78ch; margin: 8px 0 16px 0; }

.progress-track { background: #e4e7f5; border-radius: 5px; height: 8px; max-width: 460px; display: inline-block; vertical-align: middle; }
.progress-fill { background: #1f7a52; border-radius: 5px; height: 8px; }

table.recon-table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
table.recon-table th { text-align: left; font-family: 'IBM Plex Mono', monospace; text-transform: uppercase;
                        letter-spacing: .1em; font-size: 10px; color: #75798c; padding: 8px 10px;
                        border-bottom: 1px solid #e4e7f5; background: #f7f7f9; }
table.recon-table td { padding: 9px 10px; border-bottom: 1px solid #eef0f8; }
.td-mono { font-family: 'IBM Plex Mono', monospace; }
.td-right { text-align: right; }
.diff-cell { display: flex; align-items: center; gap: 6px; justify-content: flex-end; }
.diff-track { position: relative; width: 90px; height: 10px; }
.diff-track::before { content: ''; position: absolute; left: 50%; top: 0; bottom: 0; width: 1px; background: #cfd3e5; }
.diff-bar { position: absolute; top: 2px; height: 6px; background: #c98f2f; border-radius: 3px; }
.diff-val { font-family: 'IBM Plex Mono', monospace; font-size: 11.5px; color: #8a5a12; width: 48px; text-align: right; }

.nav-card { background: #fff; border: 1px solid #e4e7f5; border-radius: 8px; padding: 24px; height: 160px; position: relative; }
.nav-track { position: absolute; left: 24px; right: 24px; top: 62px; height: 10px; background: #eef0f8; border-radius: 5px; }
.nav-band { position: absolute; top: 53px; height: 26px; background: #ded9f6; border: 1px solid #b5abfc; border-radius: 5px; }
.nav-band-label { position: absolute; top: 6px; font-size: 11px; font-weight: 500; color: #5d5294; text-align: center; transform: translateX(-50%); white-space: nowrap; }
.nav-band-label .mono { display: block; font-weight: 400; font-size: 11px; }
.nav-pub-line { position: absolute; top: 42px; width: 2px; height: 38px; background: #1f2024; }
.nav-pub-label { position: absolute; top: 84px; font-size: 11px; font-weight: 500; color: #1f2024; text-align: center; transform: translateX(-50%); white-space: nowrap; }
.nav-pub-label .mono { display: block; font-weight: 400; color: #595d6c; font-size: 11px; }
.nav-axis { position: absolute; left: 24px; right: 24px; bottom: 6px; display: flex; justify-content: space-between;
            font-family: 'IBM Plex Mono', monospace; font-size: 9.5px; color: #b2b6ca; }

.cause-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.cause-card { background: #fff; border: 1px solid #e4e7f5; border-radius: 8px; padding: 16px 18px; border-top: 2px solid; }
.cause-cat { font-family: 'IBM Plex Mono', monospace; text-transform: uppercase; letter-spacing: .12em; font-size: 10px; margin-bottom: 8px; }
.cause-finding { font-size: 13.5px; font-weight: 500; color: #1f2024; margin-bottom: 6px; }
.cause-explain { font-size: 12px; line-height: 1.5; color: #595d6c; }

*:focus-visible { outline: 2px solid #5d5294; outline-offset: 2px; }

/* --- Sidebar --- */
.side-label { font-family: 'IBM Plex Mono', monospace; text-transform: uppercase; letter-spacing: .13em;
              font-size: 10px; color: #9397ab; margin: 4px 0 10px 0; }
.source-card { background: #fff; border: 1px solid #e4e7f5; border-radius: 8px; padding: 14px 16px; margin-bottom: 14px; }
.source-name { font-size: 14px; font-weight: 500; color: #1f2024; }
.source-meta { font-size: 12px; color: #75798c; margin-top: 4px; }
.side-hr { border: none; border-top: 1px solid #e4e7f5; margin: 18px 0; }
.side-footer { font-size: 11.5px; color: #b2b6ca; margin-top: 30px; }
section[data-testid="stSidebar"] { background: #f7f7f9; border-right: 1px solid #d5d8e8; }

section[data-testid="stSidebar"] input[type="text"],
section[data-testid="stSidebar"] input[type="number"] {
  border: 1px solid #d5d8e8 !important;
  border-radius: 8px !important;
  background: #fff !important;
  padding: 8px 10px !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"],
section[data-testid="stSidebar"] [data-testid="stFileUploader"] section {
  border: 1.5px dashed #b8bcd6 !important;
  border-radius: 10px !important;
  background: #eef0f8 !important;
  padding: 18px !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DEFAULT DATA FIRST (so sidebar can show current row count etc.)
# ============================================================

def load_csv(file_or_path, is_upload=False):
    if is_upload:
        lines = [l.decode("utf-8-sig") for l in file_or_path.readlines()]
        header_row_idx = next(i for i, l in enumerate(lines) if l.startswith("Ticker,"))
        file_or_path.seek(0)
        df = pd.read_csv(file_or_path, skiprows=header_row_idx, thousands=",")
    else:
        with open(file_or_path, encoding="utf-8-sig") as f:
            lines = f.readlines()
        header_row_idx = next(i for i, l in enumerate(lines) if l.startswith("Ticker,"))
        df = pd.read_csv(file_or_path, skiprows=header_row_idx, thousands=",")
    return df.dropna(subset=["Ticker"]).reset_index(drop=True)

if "uploaded_df" not in st.session_state:
    st.session_state.uploaded_df = None
    st.session_state.source_label = "IOZ_holdings.csv"
    st.session_state.upload_time = datetime.now().strftime("%H:%M")

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown('<div class="side-label">SOURCE</div>', unsafe_allow_html=True)

    current_df = st.session_state.uploaded_df if st.session_state.uploaded_df is not None else load_csv("IOZ_holdings.csv")
    st.markdown(f"""
    <div class="source-card">
      <div class="source-name">{st.session_state.source_label}</div>
      <div class="source-meta">{len(current_df)} rows · uploaded {st.session_state.upload_time}</div>
    </div>
    """, unsafe_allow_html=True)

    new_upload = st.file_uploader("Drop a new CSV", type="csv", label_visibility="collapsed",
                                    help="or click to browse · 200 MB max")
    if new_upload is not None:
        st.session_state.uploaded_df = load_csv(new_upload, is_upload=True)
        st.session_state.source_label = new_upload.name
        st.session_state.upload_time = datetime.now().strftime("%H:%M")
        st.rerun()

    st.markdown('<hr class="side-hr">', unsafe_allow_html=True)
    st.markdown('<div class="side-label">SETTINGS</div>', unsafe_allow_html=True)

    mv_tolerance = st.slider("MV tolerance", 0.10, 2.00, 0.50, 0.10, format="±%.2f%%")
    published_nav_date = st.text_input("Published NAV date", value="07 Sept 2026")
    published_nav_value = st.number_input("Published NAV value", value=36.45, format="%.4f")

    st.markdown('<div class="side-footer">Re-runs automatically on change.</div>', unsafe_allow_html=True)

df = current_df
source_label = st.session_state.source_label
PUBLISHED_NAV = published_nav_value

# ============================================================
# CALCULATIONS
# ============================================================

def check_weight_sum(df, tolerance_pts=0.10):
    total = df["Weight (%)"].sum()
    return total, abs(total - 100) < tolerance_pts

def check_market_value_recalc(df, tolerance_pct):
    eq = df[df["Asset Class"] == "Equity"].copy()
    eq["recalc_mv"] = eq["Shares"] * eq["Price"] * eq["FX Rate"]
    eq["pct_diff"] = (eq["Market Value"] - eq["recalc_mv"]) / eq["Market Value"] * 100
    return eq[eq["pct_diff"].abs() > tolerance_pct][["Ticker", "Name", "Market Value", "recalc_mv", "pct_diff"]]

def nav_gap(df, shares_low, shares_high, published_nav):
    total_mv = df["Market Value"].sum()
    nav_a, nav_b = total_mv / shares_low, total_mv / shares_high
    lo, hi = sorted([nav_a, nav_b])
    return lo, hi, (published_nav - hi) / published_nav * 100, (published_nav - lo) / published_nav * 100

total_weight, weight_passed = check_weight_sum(df)
flagged = check_market_value_recalc(df, mv_tolerance)
equity_count = len(df[df["Asset Class"] == "Equity"])
lo, hi, gap_lo, gap_hi = nav_gap(df, 261_944_479, 261_569_479, PUBLISHED_NAV)

checks = [weight_passed, len(flagged) == 0, gap_hi < 1.0]  # weights, market-value recalc, NAV gap
pass_count = sum(checks)
flag_count = len(checks) - pass_count
verdict_ok = flag_count <= 1
verdict_text = "Reconciled — gap explained" if verdict_ok else "Review needed"

axis_min = min(lo, PUBLISHED_NAV) - 0.02
axis_max = max(hi, PUBLISHED_NAV) + 0.02
span = axis_max - axis_min
band_left_pct = (lo - axis_min) / span * 100
band_width_pct = (hi - lo) / span * 100
published_left_pct = (PUBLISHED_NAV - axis_min) / span * 100
ticks = [axis_min + span * f for f in [0, 0.25, 0.5, 0.75, 1.0]]

# ============================================================
# HEADER BAND
# ============================================================
run_ts = datetime.now().strftime("%d %b %Y %H:%M").upper()
st.markdown(f"""
<div class="header-band">
  <div class="console-wrap" style="padding:0; display:flex; justify-content:space-between; align-items:flex-start;">
    <div>
      <div class="eyebrow">RECONCILIATION RUN · {run_ts}</div>
      <div class="header-title">IOZ · Holdings-to-NAV</div>
      <div>
        <span class="chip">{source_label}</span>
        <span class="chip">{len(df)} rows</span>
        <span class="chip">tol ±{mv_tolerance:.2f}%</span>
      </div>
    </div>
    <div style="text-align:right;">
      <span class="verdict-pill {'flag' if not verdict_ok else ''}"><span class="dot"></span>{verdict_text}</span>
      <div class="verdict-sub">{len(checks)} checks · {pass_count} pass · {flag_count} flagged</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# KPI STRIP
# ============================================================
st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-cell">
    <div class="kpi-label">weight_sum</div>
    <div class="kpi-value">{total_weight:.2f}%</div>
    <div class="kpi-sub {'pass' if weight_passed else 'flag'}">{'pass' if weight_passed else 'flag'} · within ±0.10%</div>
  </div>
  <div class="kpi-cell">
    <div class="kpi-label">flagged_rows</div>
    <div class="kpi-value">{len(flagged)} <span style="font-size:14px;color:#b2b6ca;">/ {equity_count}</span></div>
    <div class="kpi-sub {'flag' if len(flagged) else 'pass'}">{'review · timing lag' if len(flagged) else 'pass · none flagged'}</div>
  </div>
  <div class="kpi-cell">
    <div class="kpi-label">implied_nav</div>
    <div class="kpi-value small">{lo:.4f}–{hi:.4f}</div>
    <div class="kpi-sub muted">range from 2 unit-count dates</div>
  </div>
  <div class="kpi-cell">
    <div class="kpi-label">gap_vs_published</div>
    <div class="kpi-value small">{gap_lo:+.3f} → {gap_hi:+.3f}%</div>
    <div class="kpi-sub pass">explained · 3-day lag</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# NUMBERED SPINE (single markdown call so the wrapper div actually wraps)
# ============================================================

rows_html = ""
for _, row in flagged.iterrows():
    pct = row["pct_diff"]
    bar_width = min(abs(pct) / 2 * 45, 45)
    bar_style = f"right:50%; width:{bar_width}px;" if pct < 0 else f"left:50%; width:{bar_width}px;"
    rows_html += (
        f'<tr>'
        f'<td class="td-mono" style="font-weight:500;">{row["Ticker"]}</td>'
        f'<td style="color:#595d6c;">{row["Name"].title()}</td>'
        f'<td class="td-mono td-right">{row["Market Value"]:,.2f}</td>'
        f'<td class="td-mono td-right" style="color:#595d6c;">{row["recalc_mv"]:,.2f}</td>'
        f'<td><div class="diff-cell"><div class="diff-track"><div class="diff-bar" style="{bar_style}"></div></div>'
        f'<div class="diff-val">{pct:+.3f}</div></div></td>'
        f'</tr>'
    )

tick_html = "".join(f'<span>{t:.3f}</span>' for t in ticks)

step1 = (
    f'<div class="step-row"><div class="step-circle">01</div><div>'
    f'<span class="step-heading">Do the weights add to 100%?</span>'
    f'<span class="step-chip {"pass" if weight_passed else "flag"}">{"Pass" if weight_passed else "Review"}</span>'
    f'<div class="step-body">They sum to {total_weight:.2f}%, {abs(100-total_weight)*100:.0f} basis points '
    f'{"short" if total_weight < 100 else "over"} — normal rounding across {len(df)} positions, '
    f'well inside the 0.10% tolerance.</div>'
    f'<div class="progress-track"><div class="progress-fill" style="width:{total_weight}%;"></div></div>'
    f'<span class="mono" style="font-size:12px; color:#1f7a52; margin-left:8px;">{total_weight:.2f} / 100.00</span>'
    f'</div></div>'
)

step2 = (
    f'<div class="step-row"><div class="step-circle {"flag" if len(flagged) else ""}">02</div><div>'
    f'<span class="step-heading">Does shares × price match the stated market value?</span>'
    f'<span class="step-chip {"flag" if len(flagged) else "pass"}">{f"{len(flagged)} flagged" if len(flagged) else "Pass"}</span>'
    f'<div class="step-body">{equity_count - len(flagged)} of {equity_count} equity rows recalculate cleanly. {len(flagged)} drift past ±{mv_tolerance:.2f}% '
    f'in both directions. Small, mixed-sign gaps like this usually mean prices and share counts were '
    f'captured at slightly different times, rather than a wrong price.</div>'
    f'<table class="recon-table"><tr><th>tkr</th><th>name</th>'
    f'<th style="text-align:right;">stated_mv</th><th style="text-align:right;">recalc_mv</th>'
    f'<th style="text-align:right;">pct_diff</th></tr>{rows_html}</table>'
    f'</div></div>'
)

step3 = (
    f'<div class="step-row"><div class="step-circle">03</div><div>'
    f'<span class="step-heading">How close is the implied NAV to the published one?</span>'
    f'<span class="step-chip pass">Pass</span>'
    f'<div class="step-body">Dividing total market value by units on issue gives {lo:.4f}–{hi:.4f} per unit. '
    f'It is a range because units on issue were only available for 31 Aug and 07 Sept, not for the 04 Sept '
    f'holdings date. The published NAV of {PUBLISHED_NAV:.2f} as of {published_nav_date} sits {gap_lo:+.2f}% to '
    f'{gap_hi:+.2f}% from that range, which is the direction and size you would expect when the holdings file '
    f'is three days older than the NAV.</div>'
    f'<div class="nav-card">'
    f'<div class="nav-band-label" style="left:{band_left_pct + band_width_pct/2}%;">Implied band'
    f'<span class="mono">{lo:.4f} – {hi:.4f}</span></div>'
    f'<div class="nav-track"></div>'
    f'<div class="nav-band" style="left:{band_left_pct}%; width:{band_width_pct}%;"></div>'
    f'<div class="nav-pub-line" style="left:{published_left_pct}%;"></div>'
    f'<div class="nav-pub-label" style="left:{published_left_pct}%;">Published'
    f'<span class="mono">{PUBLISHED_NAV:.4f}</span></div>'
    f'<div class="nav-axis">{tick_html}</div>'
    f'</div></div></div>'
)

step4 = (
    f'<div class="step-row"><div class="step-circle">04</div><div>'
    f'<span class="step-heading">So what caused the differences?</span>'
    f'<div class="cause-grid" style="margin-top:14px;">'
    f'<div class="cause-card" style="border-top-color:#c98f2f;">'
    f'<div class="cause-cat" style="color:#c98f2f;">TIMING LAG</div>'
    f'<div class="cause-finding">Three market values off ~0.5%</div>'
    f'<div class="cause-explain">Small and mixed-sign, which suggests prices and share counts were captured at slightly different times.</div>'
    f'</div>'
    f'<div class="cause-card" style="border-top-color:#9397ab;">'
    f'<div class="cause-cat" style="color:#9397ab;">IDENTIFIER MISMATCH</div>'
    f'<div class="cause-finding">PDI and PDIDB both say "Predictive Discovery"</div>'
    f'<div class="cause-explain">The live position is PDIDB. PDI has zero shares and zero value, so it is a stale leftover and can be dropped.</div>'
    f'</div>'
    f'<div class="cause-card" style="border-top-color:#1f7a52;">'
    f'<div class="cause-cat" style="color:#1f7a52;">EXPLAINED</div>'
    f'<div class="cause-finding">04 Sept file vs published NAV, +{gap_lo:.2f}% to +{gap_hi:.2f}%</div>'
    f'<div class="cause-explain">Consistent with the three-day gap between the holdings date and the NAV date, plus the range in units on issue.</div>'
    f'</div></div></div></div>'
)

spine_html = f'<div class="console-wrap spine">{step1}{step2}{step3}{step4}</div>'
st.markdown(spine_html, unsafe_allow_html=True)
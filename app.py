import pandas as pd
import requests
import streamlit as st
import matplotlib.pyplot as plt

ROOT = "https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/Daily_Chokepoints_Data/FeatureServer"
COLORS = {"Suez Canal": "#0072B2", "Bab el-Mandeb Strait": "#56B4E9", "Cape of Good Hope": "#E69F00", "Strait of Hormuz": "#D55E00"}
BASE = {"Suez Canal": ("2023-01-01", "2023-10-31"), "Bab el-Mandeb Strait": ("2023-01-01", "2023-10-31"),
        "Cape of Good Hope": ("2023-01-01", "2023-10-31"), "Strait of Hormuz": ("2025-01-01", "2026-01-31")}
SHIPS = {"n_container": "Container", "n_dry_bulk": "Dry bulk", "n_general_cargo": "General cargo", "n_roro": "Ro-ro", "n_tanker": "Tanker"}

st.set_page_config(page_title="Chokepoint Tracker", layout="wide")


def query_url():
    """Find the data layer. Some ArcGIS services list it under layers, others under tables."""
    info = requests.get(ROOT, params={"f": "json"}, timeout=60).json()
    ids = [x["id"] for x in (info.get("layers") or []) + (info.get("tables") or [])] or [0, 1]
    for i in ids:
        meta = requests.get(f"{ROOT}/{i}", params={"f": "json"}, timeout=60).json()
        if any(f.get("name") == "portname" for f in meta.get("fields", [])):
            return f"{ROOT}/{i}/query"
    raise RuntimeError("could not find the data layer; the service replied: " + str(info)[:300])


@st.cache_data(ttl=6 * 3600, show_spinner="Loading IMF PortWatch data...")
def load():
    url = query_url()
    where = "portname IN (" + ",".join(f"'{n}'" for n in COLORS) + ")"
    rows, off = [], 0
    while True:
        r = requests.get(url, params={"where": where, "outFields": "*", "returnGeometry": "false", "orderByFields": "date,portid",
                                      "resultOffset": off, "resultRecordCount": 1000, "f": "json"}, timeout=120).json()
        if "error" in r:
            raise RuntimeError(r["error"])
        feats = r.get("features", [])
        rows += [x["attributes"] for x in feats]
        if not feats or not r.get("exceededTransferLimit"):
            break
        off += len(feats)
    d = pd.DataFrame(rows)
    d["date"] = pd.to_datetime(d["date"], unit="ms") if pd.api.types.is_numeric_dtype(d["date"]) else pd.to_datetime(d["date"])
    return d


def change(d, col, names):
    last = d["date"].max(); start = last - pd.Timedelta(days=27); out = []
    for n in names:
        a, b = BASE[n]
        s = d[d.portname == n].set_index("date")[col]
        base, now = s[a:b].mean(), s[start:last].mean()
        out.append({"chokepoint": n, "baseline_per_day": round(base, 1), "last_28d_per_day": round(now, 1),
                    "change_per_day": round(now - base, 1), "pct_change": round(100 * (now / base - 1), 1) if base else None})
    return pd.DataFrame(out)


st.title("Chokepoint Tracker")
st.caption("Daily ship transits at Suez, Bab el-Mandeb, the Cape of Good Hope and Hormuz. Sources: UN Global Platform; IMF PortWatch.")
try:
    data = load()
except Exception as e:
    st.error(f"Could not load the data right now ({e}). Please try again later.")
    st.stop()
last = data["date"].max()
st.markdown(f"**Data through {last.date()}.** AIS-observed transits (ships' tracking signals). PortWatch refreshes weekly, so numbers change.")

with st.expander("Read this first", expanded=True):
    st.markdown(
        "- Counts come from AIS, which misses ships with transponders off.\n"
        "- For Hormuz, another source reports far more transits for the same week; the two are not interchangeable. Read the Hormuz figure as what PortWatch's AIS sees.\n"
        "- The Cape's gain is consistent with diversion from Suez, but does not prove the same ships moved.\n"
        "- Baselines are my choice (Suez, Bab el-Mandeb, Cape: Jan-Oct 2023; Hormuz: Jan 2025-Jan 2026). The size of the change depends on them, especially for Suez.")

st.subheader("Last 28 days vs baseline")
tot = change(data, "n_total", list(COLORS))
cols = st.columns(4)
for c, r in zip(cols, tot.itertuples()):
    c.metric(r.chokepoint, f"{r.last_28d_per_day} / day", f"{r.pct_change:+.1f}% vs baseline", delta_color="off")
st.dataframe(tot, hide_index=True, width="stretch")

st.subheader("Daily transits")
pick = st.multiselect("Chokepoints", list(COLORS), default=list(COLORS))
win = st.radio("Averaging window", [7, 28], horizontal=True, format_func=lambda w: f"{w}-day average")
if pick:
    piv = data[data.portname.isin(pick)].pivot(index="date", columns="portname", values="n_total").rolling(win).mean().loc["2023-01-01":]
    fig, ax = plt.subplots(figsize=(10, 4.5))
    for n in pick:
        ax.plot(piv.index, piv[n], color=COLORS[n], linewidth=2, label=n)
    ax.set_ylabel("Ships per day"); ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="y", alpha=0.25); ax.legend(frameon=False)
    fig.text(0.01, 0.01, f"AIS-observed transits; data through {last.date()}. Sources: UN Global Platform; IMF PortWatch.", fontsize=8, color="gray")
    st.pyplot(fig)
else:
    st.info("Pick at least one chokepoint.")

st.subheader("By ship type")
one = st.selectbox("Chokepoint", list(COLORS))
rows = []
for col, label in SHIPS.items():
    t = change(data, col, [one]).iloc[0]
    rows.append({"ship type": label, "baseline_per_day": t["baseline_per_day"], "last_28d_per_day": t["last_28d_per_day"],
                 "change_per_day": t["change_per_day"], "pct_change": t["pct_change"]})
st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
st.caption("Percent changes from small baselines can mislead; read them with the change per day.")

st.markdown("---")
st.markdown("Method, notebooks and SQL: github.com/binary-cpu/chokepoint-tracker")

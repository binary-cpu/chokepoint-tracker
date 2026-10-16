# Chokepoint Tracker

How have the 2026 disruptions changed shipping through Hormuz, Bab el-Mandeb and Suez, and where has traffic gone?

**Live dashboard:** https://chokepoint-tracker-8wmhe8a35vakpsbw9vkgkh.streamlit.app/ (loads current data, so its numbers can differ from the snapshot below; the free host may take a moment to wake up).

**Data snapshot for this write-up:** through 2026-10-11 (accessed 2026-10-14). Source: UN Global Platform; IMF PortWatch. Daily AIS-observed ship transits at 28 chokepoints, 2019 to 2026. Raw data is fetched fresh by the notebooks and not stored here.

**Note:** notebook 02 was run on the 2026-10-04 snapshot, so its figures differ slightly from the 2026-10-11 figures in notebooks 03-05 and this page.

## What I found
Last 28 days against a baseline I chose (Suez, Bab el-Mandeb and Cape: Jan-Oct 2023; Hormuz: Jan 2025-Jan 2026):

| Chokepoint | Baseline per day | Last 28 days per day | Change | Range across 4 baselines |
|---|---|---|---|---|
| Suez Canal | 73.6 | 41.7 | -43.4% | -27.5% to -43.4% |
| Bab el-Mandeb | 74.6 | 27.4 | -63.2% | -53.1% to -63.2% |
| Cape of Good Hope | 48.9 | 87.1 | +78.3% | +78.3% to +99.0% |
| Hormuz (AIS-observed) | 83.4 | 3.3 | -96.1% | -96.0% to -96.4% |

1. **One shift, three places.** Bab el-Mandeb, the Cape and Suez changed within about two weeks (7-day average crossings from 2023-12-23 to 2024-01-06).
2. **The two routes add up.** Suez and Cape combined stayed within +2% to +11% of their 2023 total after the shift, with no step at the change. This is consistent with traffic switching between routes. It does not prove the same ships moved. By ship type, the Cape's gain is close in size to Suez's loss (about +38 against -32 transits a day).
3. **Hormuz fell across every ship type.** Tankers went from 46.8 to 0.8 a day. The 7-day average fell below a quarter of baseline on 2026-03-06, bottomed at 1.3 a day on 2026-05-09, peaked at 31.9 a day (38% of baseline) on 2026-06-29, and is 4.1 a day now.

## Read this first
- Counts are AIS-observed; ships with transponders off are missed.
- For 21-27 Sep 2026, PortWatch recorded 22 Hormuz transits while Lloyd's List Intelligence reports 124 non-Iranian-linked transits for the same week (different scope). The sources are not interchangeable, so read the Hormuz figure as what PortWatch's AIS sees.
- Baselines are my choices, so results are reported as ranges. Suez depends on the baseline most.
- No causes are claimed. I have not linked any change to outside events.
- Data lags by about 10 days.

## How it was built
Notebooks: 01 data pull, 02 data contract and cleaning log, 03 SQL layer (queries in `/sql`, checked against pandas), 04 chart, 05 analysis. Dashboard: `app.py` (Streamlit).

## What's next
Weekly updates, and linking changes to sourced events.

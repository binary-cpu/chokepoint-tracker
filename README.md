# Chokepoint Tracker

How have the 2026 disruptions changed shipping through Hormuz, Bab el-Mandeb and Suez, and where has traffic gone?

**Data snapshot:** through 2026-10-11 (accessed 2026-10-14). Source: UN Global Platform; IMF PortWatch. AIS-observed transits; raw data is fetched fresh by the notebooks and not stored here.

## Headline: last 28 days vs a stated baseline

| Chokepoint | Change | Range across 4 baselines |
|---|---|---|
| Suez Canal | -43.4% | -27.5% to -43.4% |
| Bab el-Mandeb | -63.2% | -53.1% to -63.2% |
| Cape of Good Hope | +78.3% | +78.3% to +99.0% |
| Hormuz | -96.1% (AIS-observed) | -96.0% to -96.4% |

## Read this first
- Counts are AIS-observed; ships with transponders off are missed.
- For Hormuz, another source reports far more transits for the same week; the two are not interchangeable (see notebook 02).
- The Cape's gain is consistent with diversion from Suez, but does not prove it.

## Notebooks
01 data pull, 02 contract and cleaning, 03 SQL layer (queries in /sql), 04 post 1 chart

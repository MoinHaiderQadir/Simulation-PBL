# MUET Point (Bus) Scheduling: Queuing Model and Discrete Event Simulation

[![CI](../../actions/workflows/ci.yml/badge.svg)](../../actions/workflows/ci.yml)

PBL assignment (Modeling and Simulation, Department of Software Engineering, MUET Jamshoro).
The project models the MUET Point bus system as a time-varying multi-server queue, implements it as a
discrete event simulation in Python/SimPy, and compares four dispatch policies on the **existing
fleet of 12 buses** (no new buses).

Full IEEE-style report: [`report/MUET_Bus_Simulation_Final_Report.pdf`](report/MUET_Bus_Simulation_Final_Report.pdf)

> **Note on data:** no measured MUET data was available, so every parameter in `src/config.py` is an
> **assumption**. The relative comparison between policies and the methodology are the result, not
> the absolute waiting times. Replace the parameters with field data (GPS logs, tap counts) to calibrate.

## Authors
Moin Haider (22SW075), Parkash (22SW054), Ghulam Murtaza (22SW012), Faizan Ahmed (22SW018)

Simulator code originally developed by Muhammad Uzair (22SW106),
[MuhammadUzair88/SM_PBL_Simulation](https://github.com/MuhammadUzair88/SM_PBL_Simulation).

## What is modelled
- **Entities:** students arriving as a non-homogeneous Poisson process (Lewis-Shedler thinning), and 12 buses of capacity 50.
- **Resources:** FCFS queues at the **STC** and **Main Gate** terminals, plus a depot of idle buses.
- **Route:** depot, terminal 1, terminal 2, campus, depot, with log-normal travel noise, peak congestion and random incidents.

| ID | Policy |
|----|--------|
| P0 | Static timetable, 5-min headway (baseline) |
| P1 | Peak-aware timetable (headway 4.2 to 5 min from historical demand) |
| P2 | Reactive queue-triggered dispatch |
| P3 | Hybrid: demand-regulated headway, oldest-first stop order, fair-share seat quota |

## Project layout
```
src/config.py         all model parameters (edit to calibrate)
src/model.py          SimPy model: arrivals, dispatcher, buses, boarding, KPIs
src/policies.py       dispatch policies P0 to P3
src/experiments.py    experiments E1 to E7: CSV tables and PNG figures
tests/verify.py       six verification checks (conservation, Little's law, capacity, ...)
tests/test_simulation.py   pytest wrapper around verify.py
results/              generated tables and figures (50 replications)
report/               final report (PDF)
.github/workflows/    CI: runs the tests on every push
```

## Quick start
Requires Python 3.10+.
```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

python tests/verify.py               # expect: ALL CHECKS PASSED
python src/experiments.py --quick    # smoke test, 8 replications
python src/experiments.py            # full run used in the report, 50 replications
```
(`make verify`, `make quick` and `make full` do the same if `make` is available.)

Run one scenario from Python:
```python
import sys; sys.path.insert(0, "src")
from config import Config
from policies import StaticPeakAware
from model import TransitSystem
print(TransitSystem(Config(), StaticPeakAware(), seed=1).run())
```

## Experiments
| ID | Content |
|----|---------|
| E1 | Morning session, 4 policies, 50 replications, 95% CIs, Welch tests vs baseline |
| E2 | Analytic traffic intensity rho(t) = lambda(t) / mu(t) and bottleneck window |
| E3 | What-if: fleet size 8 to 16 |
| E4 | What-if: demand 80% to 130% |
| E5 | Afternoon session (14:00 to 15:30 peak) |
| E6 | Traffic-uncertainty sensitivity |
| E7 | Ablation of P3 components |

## Headline results (morning, 12 buses, 50 replications)
| Policy | Mean wait (min) | 95th pct (min) | Peak queue | STC / Main Gate wait (min) |
|--------|----------------|----------------|-----------|----------------------|
| P0 Static baseline | 7.75 | 27.7 | 180 | 3.2 / 13.4 |
| P1 Peak-aware timetable | **6.09** | 19.0 | **148** | 3.2 / 9.7 |
| P2 Reactive dispatch | 12.60 | 32.2 | 231 | 5.4 / 21.6 |
| P3 Hybrid adaptive | 8.63 | **18.0** | 177 | 8.6 / 8.7 |

Key findings: the morning peak exceeds fleet capacity by up to 31% between 08:12 and 08:48; a
demand-shaped timetable (P1) cuts the mean wait by 21%; the hybrid policy (P3) cuts the 95th percentile
by 35% and equalises the two terminals; the purely reactive policy (P2) is worse than the baseline.

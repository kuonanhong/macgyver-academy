V14 underground engineering: six executable synthetic-data mini labs

Python 3.10+, standard library only; no pip and no network.
python3 run-underground-labs.py --check
python3 run-underground-labs.py --output results.json
On Windows use python or py -3 if needed.

Models: Gaussian trough integration; TBM calendar budget; parallel Darcy flows; fan/system curve intersection; bounded convergence curve fitting; one-dimensional consolidation series.
All inputs are synthetic. Results record assumptions, units and input SHA-256. Edit synthetic-cases.json or supply --cases FILE. This package is for learning, not construction, design or stability decisions.

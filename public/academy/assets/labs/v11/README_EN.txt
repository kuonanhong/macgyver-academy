MacGyver V11: 12 original synthetic mini labs

Python 3.10+ standard library only. No network, pip, downloads, real personal data, devices or GPU/QPU access.
Run: python3 run-evidence-labs.py --check
Windows: py -3 run-evidence-labs.py --check
Select: python3 run-evidence-labs.py --case attention

Copy synthetic-cases.json, change one assumed input, predict the result, then use --inputs YOUR_COPY.json --case CASE. The bundled checks describe the original inputs; after editing, a check failure may reflect a changed assumption. Keep units, limits and the input hash in your notebook.

Models: CPI, roofline, fixed-voter quorum, alert precision/recall, DNS refresh, M/M/1 response, basic differential privacy, one-head attention, one sigmoid neuron, hydro power, ore recovery, PUE. The neuron has a linear 1D decision and cannot solve XOR. Attention omits masks, positions and Transformer training. All data are invented; outputs are neither measurements nor benchmarks or industrial settings. These 12 small executable models complement the site worksheets; they are not complete simulators for every course and do not automatically issue certificates.

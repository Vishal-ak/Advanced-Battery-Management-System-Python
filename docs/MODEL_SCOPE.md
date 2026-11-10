# Model scope and limitations

## Implemented
- Ideal series/parallel pack arithmetic.
- Nominal energy estimate: series nominal voltage × parallel capacity.
- Time-domain current-profile accounting using trapezoidal integration.
- Coulomb-counting SOC estimate under an explicit positive-discharge / negative-charge convention.

## Not implemented
No electrochemical model, OCV-SOC curve, Thevenin ECM, R0/R1/C1 identification, terminal-voltage prediction, SOH/ageing estimator, thermal model, cell balancing, fault detection, contactor logic, or safety controller.

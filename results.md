# Results Tables

**Group 19 | ES 418**

This file collects the main table values from the two final notebooks so they are easier to use while preparing the report.

## Trio 1: Daily Analysis

Assets: NIFTY 50, HUL, and Adani Enterprises.

### Baseline Descriptive Statistics

This table gives a quick summary of the daily return behavior before calculating VaR and CVaR.

| Asset | Number of Observations | Mean Return | Std Dev | Minimum Return | Maximum Return | Skewness | Kurtosis |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NIFTY 50 | 492 | 0.00019 | 0.00895 | -0.06112 | 0.03747 | -0.468 | 6.336 |
| HUL | 493 | 0.00009 | 0.01276 | -0.05973 | 0.05789 | 0.113 | 3.380 |
| Adani Enterprises | 493 | -0.00063 | 0.02639 | -0.25627 | 0.10885 | -2.516 | 27.493 |

### VaR, CVaR, and Tail Severity

This table compares the 5% downside risk estimates and shows how much worse CVaR is compared with VaR.

| Asset | Historical VaR | Historical CVaR | Parametric VaR | Parametric CVaR | Historical Tail Gap | Parametric Tail Gap | Historical Tail Amplification | Parametric Tail Amplification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NIFTY 50 | 0.01373 | 0.02045 | 0.01452 | 0.01826 | 0.00672 | 0.00374 | 1.48928 | 1.25742 |
| HUL | 0.01917 | 0.02860 | 0.02090 | 0.02623 | 0.00943 | 0.00533 | 1.49192 | 1.25512 |
| Adani Enterprises | 0.03338 | 0.06056 | 0.04403 | 0.05506 | 0.02718 | 0.01103 | 1.81422 | 1.25041 |

## Trio 2: Weekly Analysis

Assets: HDFC Bank, HUL, and TCS.

### Baseline Descriptive Statistics

This table gives a quick summary of the weekly return behavior before calculating VaR and CVaR.

| Asset | Number of Observations | Mean Weekly Return | Weekly Std Dev | Minimum Weekly Return | Maximum Weekly Return | Skewness | Kurtosis |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HDFC Bank | 260 | 0.00068 | 0.02716 | -0.10972 | 0.07663 | -0.300 | 1.329 |
| HUL | 260 | 0.00021 | 0.02838 | -0.07663 | 0.10148 | 0.394 | 1.117 |
| TCS | 260 | -0.00022 | 0.03010 | -0.08908 | 0.06401 | -0.586 | 0.657 |

### VaR, CVaR, and Tail Severity

This table compares the 5% weekly downside risk estimates and shows how much worse CVaR is compared with VaR.

| Asset | Historical VaR | Historical CVaR | Parametric VaR | Parametric CVaR | Historical Tail Gap | Parametric Tail Gap | Historical Tail Amplification | Parametric Tail Amplification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HDFC Bank | 0.04580 | 0.06315 | 0.04400 | 0.05535 | 0.01734 | 0.01135 | 1.37863 | 1.25798 |
| HUL | 0.04111 | 0.05788 | 0.04648 | 0.05833 | 0.01677 | 0.01186 | 1.40792 | 1.25518 |
| TCS | 0.05425 | 0.07765 | 0.04973 | 0.06231 | 0.02339 | 0.01258 | 1.43121 | 1.25292 |

## Short Reading Guide

- Higher VaR means the bad-loss cutoff is larger.
- Higher CVaR means the average loss after entering the tail is larger.
- Tail Gap shows the extra loss beyond the VaR cutoff.
- Tail Amplification shows how many times larger CVaR is compared with VaR.

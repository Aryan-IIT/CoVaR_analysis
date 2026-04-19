# Methodology

The project uses a 5% tail level throughout. All VaR and CVaR values are reported as positive loss magnitudes, even though the underlying tail returns are negative.

## Data and Preprocessing

The notebooks load asset price data, detect the date and price columns, clean missing values, sort observations by date, and remove duplicate dates.

Returns are calculated as log returns:

\[
r_t = \ln\left(\frac{P_t}{P_{t-1}}\right)
\]

## Daily vs Weekly Analysis

Trio 1 uses daily log returns for NIFTY 50, HUL, and Adani Enterprises.

Trio 2 starts from daily prices but converts them to weekly prices using the last available closing price of each week. Weekly log returns are then computed from those weekly prices.

## Historical VaR

Historical VaR is the empirical 5th percentile of returns:

\[
VaR_{0.05}^{hist} = -Q_{0.05}(r)
\]

It is empirical, so it uses the observed return distribution directly.

## Historical CVaR

Historical CVaR is the average loss conditional on returns being at or below the historical VaR threshold:

\[
CVaR_{0.05}^{hist} = -E[r \mid r \le Q_{0.05}(r)]
\]

This measures the average severity of the worst 5% return outcomes.

## Parametric VaR

Parametric VaR assumes returns are Gaussian and uses the sample mean and sample standard deviation:

\[
VaR_{0.05}^{param} = -(\mu + \sigma z_{0.05})
\]

where \(z_{0.05}\) is the 5th percentile of the standard normal distribution.

## Parametric CVaR

Parametric CVaR is the analytical expected shortfall under the normal assumption:

\[
CVaR_{0.05}^{param} = -\left(\mu - \sigma \frac{\phi(z_{0.05})}{0.05}\right)
\]

where \(\phi\) is the standard normal density.

## Tail Gap

Tail Gap compares CVaR and VaR in absolute terms:

\[
\text{Tail Gap} = \text{CVaR} - \text{VaR}
\]

A larger gap means losses become much worse after the VaR threshold is crossed.

## Tail Amplification

Tail Amplification compares CVaR and VaR in relative terms:

\[
\text{Tail Amplification} = \frac{\text{CVaR}}{\text{VaR}}
\]

It shows how many times larger the average tail loss is compared with the VaR cutoff.

## Limitations

The historical method depends on the observed sample and may miss events that did not occur during the period. The parametric method is cleaner mathematically but assumes Gaussian returns, which may understate heavy-tail behavior in real markets.

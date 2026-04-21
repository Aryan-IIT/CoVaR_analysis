# Methodology

The project uses a 5% tail level throughout (however, in the [Interactive Playground](playground.md), you can see how different confidence/tail levels change and amplify risk). All VaR and CVaR values are reported as positive loss magnitudes, even though the underlying tail returns are negative.

## Data and Preprocessing

The notebooks load asset price data, detect the date and price columns, clean missing values, sort observations by date, and remove duplicate dates. The sample windows were also chosen to be long enough to provide a reasonable number of tail observations, which is important for making historical VaR, CVaR, and related tail metrics sufficiently informative.

Returns are calculated as log returns:

\[
r_t = \ln\left(\frac{P_t}{P_{t-1}}\right)
\]

where \(r_t\) is the log return at time \(t\), \(P_t\) is the asset price at time \(t\), and \(P_{t-1}\) is the asset price in the previous period.

## Daily vs Weekly Analysis

Trio 1 uses daily log returns for NIFTY 50, HUL, and Adani Enterprises.

Trio 2 starts from daily prices but converts them to weekly prices using the last available closing price of each week. Weekly log returns are then computed from those weekly prices.

Using both daily and weekly settings helps test the VaR/CVaR comparison under different frequencies rather than only one return horizon.
## Historical VaR

Historical VaR is the empirical 5th percentile of returns:

\[
VaR_{0.05}^{hist} = -Q_{0.05}(r)
\]

where \(VaR_{0.05}^{hist}\) is the historical Value-at-Risk at the 5% tail level, \(0.05\) is the tail probability, \(hist\) indicates that the measure is based on historical data, \(Q_{0.05}(r)\) is the 5th percentile (quantile) of the return distribution, and \(r\) denotes the return series.

It is empirical, so it uses the observed return distribution directly.

This is the starting point of the analysis. VaR tells us where the bad tail begins, but not how severe losses become after that point.

## Historical CVaR

Historical CVaR is the average loss conditional on returns being at or below the historical VaR threshold:

\[
CVaR_{0.05}^{hist} = -E[r \mid r \le Q_{0.05}(r)]
\]

where \(CVaR_{0.05}^{hist}\) is the historical Conditional Value-at-Risk at the 5% tail level, \(E[\cdot]\) denotes expectation (average), \(r\) is the return series, \(\mid\) means “conditional on,” and \(Q_{0.05}(r)\) is the 5th percentile of returns.

This measures the average severity of the worst 5% return outcomes.

This is how VaR is extended to CVaR in the project. Instead of stopping at the cutoff, the analysis measures the average loss once the return has already entered the tail.

## Parametric VaR

Parametric VaR assumes returns are Gaussian and uses the sample mean and sample standard deviation:

\[
VaR_{0.05}^{param} = -(\mu + \sigma z_{0.05})
\]

where \(VaR_{0.05}^{param}\) is the parametric Value-at-Risk at the 5% tail level, \(param\) indicates that the measure is model-based, \(\mu\) is the sample mean of returns, \(\sigma\) is the sample standard deviation of returns, and \(z_{0.05}\) is the 5th percentile of the standard normal distribution.

## Parametric CVaR

Parametric CVaR is the analytical expected shortfall under the normal assumption:

\[
CVaR_{0.05}^{param} = -\left(\mu - \sigma \frac{\phi(z_{0.05})}{0.05}\right)
\]

where \(CVaR_{0.05}^{param}\) is the parametric Conditional Value-at-Risk at the 5% tail level, \(\mu\) is the sample mean of returns, \(\sigma\) is the sample standard deviation of returns, \(z_{0.05}\) is the 5th percentile of the standard normal distribution, and \(\phi(\cdot)\) is the standard normal probability density function evaluated at \(z_{0.05}\).

The parametric versions are included so that VaR and CVaR can also be compared under a model-based Gaussian assumption, not only under observed historical data.

## Tail Gap

Tail Gap compares CVaR and VaR in absolute terms:

\[
\text{Tail Gap} = \text{CVaR} - \text{VaR}
\]

where Tail Gap is the absolute difference between Conditional Value-at-Risk and Value-at-Risk.

A larger gap means losses become much worse after the VaR threshold is crossed.

This directly supports the extreme-tail-loss part of the project by showing how much deeper losses become beyond the VaR cutoff.

## Tail Amplification

Tail Amplification compares CVaR and VaR in relative terms:

\[
\text{Tail Amplification} = \frac{\text{CVaR}}{\text{VaR}}
\]

where Tail Amplification is the ratio of Conditional Value-at-Risk to Value-at-Risk.

It shows how many times larger the average tail loss is compared with the VaR cutoff.

This gives another way to compare VaR and CVaR, especially when assets differ in overall volatility.

## Limitations

The historical method depends on the observed sample and may miss events that did not occur during the period. The parametric method is cleaner mathematically but assumes Gaussian returns, which may understate heavy-tail behavior in real markets.
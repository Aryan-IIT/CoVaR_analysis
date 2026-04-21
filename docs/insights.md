# Key Insights

This page follows the main project statement directly: extend VaR analysis to CVaR, analyze extreme tail losses, and compare VaR and CVaR measures.

## Extending VaR to CVaR: What Changes and Why It Matters

VaR answers a threshold question: what loss level marks the worst 5% of outcomes? CVaR changes the analysis by asking what the average loss looks like once that threshold has already been crossed.

That extension matters because two assets can have similar VaR values but very different losses inside the worst part of the distribution. In this project, CVaR is the step that turns a tail cutoff into a tail-severity measure.

## Extreme Tail Losses: What the Analysis Reveals

The project shows that the worst outcomes are not fully described by VaR alone. Tail Gap and Tail Amplification make this visible by showing how much worse losses become after crossing the VaR threshold.

In Trio 1, the volatile stock makes this especially clear: the tail becomes much deeper than the VaR cutoff suggests. In Trio 2, the same idea appears at the weekly sector level, where assets can still differ meaningfully in tail depth even when all are large stocks.

## Comparing VaR and CVaR: What the Results Show

The comparison between VaR and CVaR is the central result of the project. VaR gives the boundary of the bad tail. CVaR shows the average loss inside that tail.

Tail Gap measures that difference in absolute terms:

\[
\text{Tail Gap} = \text{CVaR} - \text{VaR}
\]

Tail Amplification measures the same difference in relative terms:

\[
\text{Tail Amplification} = \frac{\text{CVaR}}{\text{VaR}}
\]

Together, these measures show where VaR and CVaR stay close and where they separate sharply. When they separate more, it means the tail is more severe than the VaR threshold alone suggests.

## Historical vs Gaussian Interpretation

Historical estimates use actual observed returns. Parametric estimates assume Gaussian returns.

When historical CVaR is much higher than parametric CVaR, it suggests the Gaussian model may be missing real tail behavior. That is useful because part of the project is not only to compute VaR and CVaR, but also to compare how the two measures behave under empirical data versus a simple model.

## Final Takeaway

The main lesson is straightforward: extending VaR to CVaR makes the project much more informative. VaR tells us where the bad tail starts, but CVaR tells us how bad that tail actually is. For studying extreme losses and comparing risk across assets, both are needed, but CVaR is the measure that completes the picture.

# Key Insights

This project is mainly about why the tail matters. VaR gives a cutoff, but CVaR explains what happens after that cutoff is crossed.

## Why VaR Alone Is Not Enough

VaR answers a threshold question: what loss level marks the worst 5% of outcomes?

That is useful, but it does not explain how bad the losses are inside that worst 5%. Two assets can have similar VaR values but very different losses beyond VaR.

## What CVaR Adds

CVaR measures the average loss beyond the VaR threshold. It is usually more conservative and gives a better view of extreme tail severity.

In this project, CVaR is the more informative metric when the goal is to analyze extreme losses, not just identify a cutoff.

## Why Tail Gap and Tail Amplification Matter

Tail Gap measures the extra loss beyond VaR in absolute terms:

\[
\text{Tail Gap} = \text{CVaR} - \text{VaR}
\]

Tail Amplification measures the same idea in relative terms:

\[
\text{Tail Amplification} = \frac{\text{CVaR}}{\text{VaR}}
\]

Together, they make tail severity easier to compare across assets.

## Historical vs Gaussian Risk

Historical estimates use actual observed returns. Parametric estimates assume Gaussian returns.

When historical CVaR is much higher than parametric CVaR, it suggests the Gaussian model may be missing real tail behavior. This is important because financial returns often have fat tails.

## Diversification vs Stock-Specific Risk

Trio 1 shows the difference between a diversified index and individual stocks. The index is more contained, while the volatile stock has stronger downside tail risk.

This supports the basic idea that diversification can reduce extreme downside exposure.

## Sector-Level Tail Differences

Trio 2 compares weekly tail risk across banking, FMCG, and IT. The sector comparison helps show that weekly downside risk is not uniform across large stocks.

Even when assets are all large companies, their tail gaps and amplification ratios can differ meaningfully.

## Main Lesson

VaR identifies where the bad tail starts. CVaR shows how severe that tail becomes. For a tail-risk project, both are needed.

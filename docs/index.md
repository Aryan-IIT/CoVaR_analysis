# CoVaR Analysis

This is a Group 19 project on **Conditional Value-at-Risk (CVaR)**. The central aim is to extend VaR analysis to CVaR, study extreme tail losses, and compare what the two measures reveal across different assets and time frequencies.

VaR gives a loss threshold at the 5% tail. CVaR goes one step further and estimates the average loss once that threshold is crossed, so it gives a clearer view of what happens inside the worst part of the return distribution.

## Project Objectives

- extend VaR analysis to CVaR
- analyze extreme tail losses
- compare VaR and CVaR measures

## Asset Trios

**Trio 1:** NIFTY 50, HUL, and Adani Enterprises  

This trio was chosen to address the project objectives through assets with clearly different risk profiles. NIFTY 50 acts as a diversified market benchmark, HUL represents a relatively stable and defensive large-cap stock, and Adani Enterprises represents a more volatile single-stock exposure. Using daily returns here helps capture short-horizon downside movements and makes it easier to compare how VaR and CVaR behave as tail risk increases from a broad index to a concentrated volatile stock. This is especially useful for showing why extending VaR to CVaR matters when losses deepen beyond the threshold.

**Trio 2:** HDFC Bank, HUL, and TCS  

This trio was chosen to study the same project objectives through a sectoral lens. HDFC Bank, HUL, and TCS provide representatives of banking, FMCG, and IT respectively, allowing the analysis to compare downside tail behavior across sectors rather than only across volatility types. Weekly returns are used here to smooth some day-to-day noise and focus on broader downside patterns over time. This helps in analyzing extreme tail losses at a sector level and in comparing whether VaR and CVaR differ meaningfully across business categories.

Across both trios, the site addresses the three project tasks in a structured way: the methodology page explains how VaR is extended to CVaR, the trio pages analyze extreme tail losses through asset-specific evidence, and the insights page compares what VaR and CVaR reveal about downside risk across different market settings.
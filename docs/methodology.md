# Methodology

## 1. Separate facts from the thesis

Reported financial statements are stored separately from scenario assumptions. The model never treats an investor forecast as a historical fact.

## 2. Normalize free cash flow

Historical free cash flow is calculated as operating cash flow less purchases of property, equipment, and technology. Scenario valuation uses explicit FCF margins because the investment question is ultimately about cash generation, not accounting EPS alone.

## 3. Reverse DCF

The reverse DCF solves for the constant five-year revenue growth rate that makes modeled equity value equal to the user-supplied market price while holding WACC, terminal growth, and FCF margin fixed.

This is an embedded-expectations diagnostic, not a claim that the market literally uses those assumptions.

## 4. Scenario distribution

Bull, base, and bear cases each specify:

- revenue growth
- FCF margin
- WACC
- terminal growth
- probability

The engine converts scenario values into returns from the supplied market price and reports probability-weighted expected return, scenario dispersion, expected downside, and probability of loss.

## 5. Position sizing

Sizing is deliberately constrained rather than conviction-score driven.

A fractional Kelly-style quantity is computed from expected scenario return and scenario variance. It is then capped by:

- maximum portfolio position
- marginal portfolio-risk budget

The final weight is the smallest of those constraints.

## 6. Portfolio impact

A simplified variance approximation estimates how the proposed weight changes portfolio volatility given:

- asset volatility
- existing portfolio volatility
- correlation to the portfolio

This is a decision aid, not a substitute for a full covariance model.

## 7. Thesis monitoring

Every major narrative claim is paired with observable evidence and a disconfirming signal. A thesis is therefore represented as something that can be updated or invalidated rather than as static prose.

## Limitations

DCF outputs are highly sensitive to terminal assumptions. Scenario probabilities are investor judgments. Reverse DCF is not uniquely identified because several assumptions can explain the same market price. Position sizing is intentionally conservative and should be integrated with a full portfolio covariance model in production.

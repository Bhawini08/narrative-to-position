# From Narrative to Position

A fundamental-investing decision framework that carries an investment thesis all the way from business drivers and embedded market expectations to scenario valuation, position sizing, and portfolio impact.

The project is intentionally not another stock-pitch template. Its purpose is to answer the harder question:

> Even if the thesis is right, what should the portfolio actually do?

## Included case

The reference implementation uses Visa (V) and FY2023-FY2025 reported financials as a transparent real-company case. Historical figures are separated from investor assumptions.

## Decision pipeline

1. Business and industry narrative
2. Fundamental driver map
3. Base economics and normalized free cash flow
4. Reverse DCF / embedded-expectations analysis
5. Bull, base, and bear scenarios
6. Probability-weighted return distribution
7. Thesis asymmetry and downside analysis
8. Position sizing under uncertainty
9. Marginal portfolio-risk impact
10. Explicit thesis-monitoring and disconfirming-evidence checklist

## Why this is different from a DCF

A DCF answers "what might this business be worth under these assumptions?"

This project additionally asks:

- What growth is the market already pricing in?
- Which assumptions create the valuation gap?
- What is the expected return after accounting for downside states?
- How much capital is justified given volatility, correlation, and uncertainty?
- What evidence would force the thesis or position size to change?

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src

pytest -q
python scripts/run_case.py --market-price 350
streamlit run dashboard/app.py
```

The market price is an explicit runtime input so the repository never presents a stale quote as current.

## Source discipline

The seeded Visa historicals are drawn from Visa's FY2025 Form 10-K. Forecast assumptions, scenario probabilities, portfolio context, and market price are clearly labeled as investor inputs.

## Decision outputs

For a user-supplied market price, the case produces reverse-DCF embedded expectations, bull/base/bear valuation outcomes, probability-weighted expected return, downside diagnostics, a constrained position-size estimate, marginal portfolio-risk impact, and an explicit thesis-monitoring checklist. The objective is to make the chain from narrative to capital allocation auditable.

## Validation

Reported Visa historicals are stored separately from scenario assumptions. Tests cover valuation and sizing logic, while GitHub Actions runs the test suite and the reference case on every push and pull request. The market price remains a runtime input so the repository does not present a hard-coded quote as current.

## Limitations

DCF outputs remain sensitive to terminal assumptions, scenario probabilities are judgments rather than observed frequencies, and the sizing layer uses a simplified portfolio-risk approximation. The framework is a disciplined decision aid, not a claim that valuation uncertainty can be reduced to a single point estimate.


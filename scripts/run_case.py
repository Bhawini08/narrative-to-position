import argparse,json
from pathlib import Path
import pandas as pd
from narrative_position.model import load_case,scenario_table,reverse_dcf_growth,normalized_fcf,expectations_gap
from narrative_position.sizing import scenario_statistics,position_size,portfolio_impact

p=argparse.ArgumentParser()
p.add_argument("--market-price",type=float,required=True)
p.add_argument("--asset-vol",type=float,default=.25)
p.add_argument("--portfolio-vol",type=float,default=.12)
p.add_argument("--correlation",type=float,default=.55)
args=p.parse_args()

hist,bs,scenarios=load_case()
table=scenario_table(hist,bs,scenarios,args.market_price)
stats=scenario_statistics(table)
implied=reverse_dcf_growth(hist,bs,args.market_price)
base_first=float(scenarios.loc[scenarios.scenario=="base","revenue_growth_1"].iloc[0])
size=position_size(stats["expected_return"],stats["scenario_volatility"],args.asset_vol,args.portfolio_vol,args.correlation)
impact=portfolio_impact(size["recommended_weight"],args.asset_vol,args.portfolio_vol,args.correlation)

out=Path("results"); out.mkdir(exist_ok=True)
table.to_csv(out/"scenario_valuation.csv",index=False)
normalized_fcf(hist).rename("fcf").to_csv(out/"historical_fcf.csv")
pd.read_csv("data/thesis_monitor.csv").to_csv(out/"thesis_monitor.csv",index=False)
metrics={
    "market_price_input":args.market_price,
    "reverse_dcf_implied_revenue_growth":implied,
    "base_near_term_growth_assumption":base_first,
    "expectations_gap":expectations_gap(base_first,implied) if pd.notna(implied) else None,
    **stats,**size,**impact
}
(out/"decision_summary.json").write_text(json.dumps(metrics,indent=2))
print(json.dumps(metrics,indent=2))
print(table.to_json(orient="records",indent=2))

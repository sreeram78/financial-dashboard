# 📊 FINANCIAL FORECASTING & SCENARIO ANALYSIS GUIDE

## Overview

The enhanced Financial Analytics Dashboard now includes advanced forecasting and scenario analysis capabilities. This guide explains all features and how to use them effectively.

---

## TABLE OF CONTENTS
1. [Forecasting Engine](#forecasting-engine)
2. [Scenario Analysis](#scenario-analysis)
3. [Sensitivity Analysis](#sensitivity-analysis)
4. [Best Practices](#best-practices)
5. [Use Cases](#use-cases)

---

## FORECASTING ENGINE

### How It Works

The forecasting engine uses **assumption-driven modeling** to project future financial performance:

```
Input Assumptions → Financial Calculations → Forecast Outputs
```

### Key Assumptions

| Assumption | Impact | Typical Range |
|-----------|--------|---------------|
| **Revenue Growth Rate** | Drives all growth | 5% - 30% CAGR |
| **COGS as % of Revenue** | Affects gross margin | 30% - 50% |
| **OpEx Growth Rate** | Controls cost inflation | 5% - 20% |
| **CapEx as % of Revenue** | Impacts free cash flow | 2% - 10% |
| **Tax Rate** | Affects net income | 15% - 35% |
| **Debt Paydown** | Reduces leverage | $0 - $50M annually |

### Forecast Outputs

**Profit & Loss Projections:**
- Revenue
- Cost of Goods Sold
- Gross Profit & Gross Margin %
- Operating Expenses
- EBITDA & EBITDA Margin %
- Operating Income (EBIT)
- Net Income & Net Margin %

**Balance Sheet Projections:**
- Total Debt
- Shareholders' Equity
- Debt/Equity Ratio
- Current Ratio (Liquidity)

**Cash Flow Projections:**
- Operating Cash Flow
- Capital Expenditures
- Free Cash Flow
- Ending Cash Position

### Forecast Period Selection

Choose 1, 2, 3, or 5 years into the future:

```
1 Year  → Near-term validation
2 Years → Medium-term planning
3 Years → Strategic planning (typical)
5 Years → Long-term vision & market positioning
```

**Recommendation:** Use **3-year forecasts** for most financial planning.

---

## SCENARIO ANALYSIS

### Pre-Built Scenarios

The dashboard includes three standard scenarios:

#### 1. 🐻 BEAR CASE (Conservative)
**Assumption Values:**
- Revenue Growth: 10%
- COGS: 42% of revenue
- OpEx Growth: 14%
- CapEx: 6% of revenue
- Tax Rate: 25%
- Debt Paydown: $5M/year

**Best Used For:**
- Risk assessment
- Downside protection planning
- Regulatory/stress testing
- Worst-case investor presentations

**Sample Year 3 Outcomes:**
- Revenue: $1,151M
- Net Income: $115M
- Free Cash Flow: $82M
- Debt/Equity: 0.35x

---

#### 2. 📊 BASE CASE (Most Likely)
**Assumption Values:**
- Revenue Growth: 18%
- COGS: 40% of revenue
- OpEx Growth: 12%
- CapEx: 5% of revenue
- Tax Rate: 25%
- Debt Paydown: $10M/year

**Best Used For:**
- Primary financial planning
- Budgeting and forecasting
- Stakeholder communication
- Default assumption set

**Sample Year 3 Outcomes:**
- Revenue: $1,597M
- Net Income: $187M
- Free Cash Flow: $140M
- Debt/Equity: 0.27x

---

#### 3. 🚀 BULL CASE (Optimistic)
**Assumption Values:**
- Revenue Growth: 25%
- COGS: 38% of revenue
- OpEx Growth: 10%
- CapEx: 4% of revenue
- Tax Rate: 25%
- Debt Paydown: $15M/year

**Best Used For:**
- Upside opportunity modeling
- Strategic investment decisions
- Best-case scenario planning
- Venture/growth investor presentations

**Sample Year 3 Outcomes:**
- Revenue: $2,341M
- Net Income: $329M
- Free Cash Flow: $232M
- Debt/Equity: 0.16x

---

### Creating Custom Scenarios

1. **Select a scenario** (Bear, Base, or Bull) as your starting point
2. **Adjust individual assumptions** using sliders or direct input
3. **View real-time forecast updates** as you change values
4. **Compare against standard scenarios** using comparison charts

**Example: Technology Company High Growth Scenario**
```
Base Case → Modify to:
Revenue Growth:     18% → 35%
COGS:              40% → 35%
OpEx Growth:       12% → 15% (invest in growth)
CapEx:              5% → 8% (infrastructure)
Debt Paydown:   $10M → $20M (strengthen balance sheet)
```

---

## SENSITIVITY ANALYSIS

### What is Sensitivity Analysis?

Sensitivity analysis shows how changes in **one key assumption** impact financial outcomes.

**Formula:**
```
Sensitivity = (Change in Output) / (Change in Input)
```

### How to Use Sensitivity Analysis

1. **Select a Variable** to analyze:
   - Revenue Growth Rate
   - COGS Percentage
   - OpEx Growth Rate
   - CapEx Percentage
   - Tax Rate
   - Debt Paydown

2. **View Impact Charts** showing:
   - Impact on Net Income
   - Impact on Free Cash Flow
   - Variance % from base case

3. **Identify Key Drivers**:
   - Which variables have the biggest impact?
   - Which variables should you focus on?

### Example: Revenue Growth Sensitivity

| Revenue Growth | Year 3 NI | Variance % | Year 3 FCF |
|---|---|---|---|
| 5% | $85M | -55% | $48M |
| 10% | $115M | -39% | $82M |
| 15% | $151M | -19% | $111M |
| **18%** | **$187M** | **0%** | **$140M** |
| 20% | $209M | +12% | $159M |
| 25% | $329M | +76% | $232M |
| 30% | $487M | +160% | $334M |

**Insights:**
- Every 1% change in revenue growth impacts net income by ~$5-6M
- Revenue growth is the **#1 profit driver**
- Small revenue variations create large profit variations (operating leverage)

---

## BEST PRACTICES

### 1. Realistic Assumptions

**Guidelines:**
- **Revenue Growth**: Should not exceed industry growth by >2x
- **COGS**: Cross-reference with historical performance
- **OpEx**: Align with headcount and infrastructure plans
- **Tax Rate**: Use statutory rate or recent effective rate
- **Debt Paydown**: Consider debt covenants and cash requirements

**Example Validation:**
```
Historical Revenue CAGR (2022-2026): 18.2%
Base Case Forecast (2026-2029): 18% ✓ Reasonable

Historical Gross Margin: 60% range
Base Case COGS Assumption: 40% (60% margin) ✓ Consistent
```

### 2. Triangulation Approach

Use 3 scenarios to create a **probability-weighted forecast**:

```
Expected Value = (25% × Bear) + (50% × Base) + (25% × Bull)
```

**Example:**
```
Net Income Y3:
Bear (25% prob):    $115M × 0.25 = $29M
Base (50% prob):    $187M × 0.50 = $94M
Bull (25% prob):    $329M × 0.25 = $82M
─────────────────────────────────────────
Expected Value:                    $205M
```

### 3. Sensitivity Focus Areas

**Identify the 2-3 most critical variables:**

For **Product Companies**:
- Revenue growth (market share)
- COGS (manufacturing efficiency)
- CapEx (production capacity)

For **SaaS Companies**:
- Revenue growth (customer acquisition)
- OpEx (sales & marketing spend)
- Tax rate (R&D credits)

For **Financial Institutions**:
- Revenue growth (net interest margin)
- Loan loss provisions
- OpEx (regulatory compliance)

### 4. Scenario Communication

**For Different Audiences:**

| Stakeholder | Scenario | Focus |
|---|---|---|
| **Board/Investors** | Base + Bull | Upside potential |
| **CFO/Finance** | Base + Bear | Downside risk |
| **Operations** | Base | Operational targets |
| **Lenders** | Base + Bear | Debt service capacity |

**Example Presentation:**

> "We forecast 3-year revenue CAGR of 18% in our base case, reaching $1.6B by 2029. Conservative scenario suggests $1.2B (10% growth), while upside case shows $2.3B (25% growth) if market adoption accelerates."

---

## USE CASES

### Use Case 1: Budget Planning

**Objective:** Create next year's budget

**Steps:**
1. Load current year actuals
2. Use Base Case forecast
3. Focus on Year 1 revenue and expenses
4. Breakdown by department:
   - Sales: Revenue forecast
   - Operations: COGS & OpEx
   - CapEx: Required investments

**Deliverable:** Budget with variance tracking

---

### Use Case 2: Investor Pitch

**Objective:** Show growth potential and returns

**Steps:**
1. Present 3-scenario model (Bear/Base/Bull)
2. Emphasize revenue growth drivers
3. Show margin expansion over time
4. Highlight free cash flow generation
5. Include leverage reduction path

**Key Metrics:**
- 3-Year Revenue CAGR
- Path to profitability (if applicable)
- Return on Invested Capital (ROIC)
- Free Cash Flow conversion

---

### Use Case 3: Risk Assessment

**Objective:** Identify financial risks and mitigation

**Steps:**
1. Run Bear Case scenario
2. Use sensitivity analysis on key variables
3. Identify "break-even" assumptions
4. Plan mitigations for each risk

**Example Risk Analysis:**

| Risk | Variable | Impact | Mitigation |
|---|---|---|---|
| Market slowdown | Revenue growth | -55% NI | Cost reduction plan |
| Margin compression | COGS % | -40% NI | Pricing power / efficiency |
| Rising interest rates | Tax rate | -25% NI | Fixed-rate debt lock-in |

---

### Use Case 4: M&A Valuation

**Objective:** Value a potential acquisition

**Steps:**
1. Build combined forecast (synergies)
2. Run 3 scenarios (conservative synergy capture)
3. Calculate NPV using WACC
4. Compare to purchase price

**Valuation Approach:**
```
Base Case NPV:    $500M
Bull Case NPV:    $700M
Bear Case NPV:    $350M

Target Price:     $400M
Valuation Range:  $350M - $700M ✓ Fair value
```

---

### Use Case 5: Strategic Decision Making

**Objective:** Compare two strategic options

**Example: Organic Growth vs. Acquisition**

**Scenario A: Organic Growth**
- Revenue Growth: 18%
- CapEx: 5%
- Year 3 Revenue: $1,597M
- Year 3 NI: $187M

**Scenario B: Acquisition (Synergies)**
- Revenue Growth: 25%
- CapEx: 8% (integration)
- Year 3 Revenue: $2,341M
- Year 3 NI: $329M

**Decision:** Acquisition creates $142M more net income by Year 3

---

## FREQUENTLY ASKED QUESTIONS

### Q: How far out should I forecast?

**A:** 
- **Startups**: 3-5 years (to profitability/exit)
- **Growing Companies**: 3 years (tactical planning)
- **Mature Companies**: 1-2 years (regulatory requirement)
- **Strategic Planning**: 5 years (market positioning)

### Q: What if my actuals differ from forecast?

**A:** This is normal! Forecasts are not predictions:
1. **Review variances** quarterly
2. **Update assumptions** based on new data
3. **Reforecast** each quarter with 3-year rolling horizon
4. **Track leading indicators** (orders, pipeline, costs)

### Q: How do I handle inflation?

**A:** Inflation is built into assumptions:
- **Revenue Growth Rate**: Can include inflation
- **COGS & OpEx**: Implicit inflation in growth rates
- **Alternative**: Use real (inflation-adjusted) rates

### Q: Should I use same assumptions across all years?

**A:** Not necessarily. You can model:
- **Revenue**: High growth Year 1-2, moderate Year 3
- **COGS**: Declining % as scale improves
- **OpEx**: Higher early (investments), lower later (leverage)

### Q: What's the difference between forecast and budget?

| Forecast | Budget |
|---|---|
| Most likely scenario | Committed targets |
| Updated continuously | Set annually |
| Planning tool | Accountability tool |
| 3-5 years typical | 1 year typical |

---

## IMPLEMENTATION CHECKLIST

- [ ] Validate historical data (5 years)
- [ ] Align on revenue growth assumptions with Sales
- [ ] Confirm COGS % with Operations
- [ ] Validate OpEx levels with Finance
- [ ] Set tax rate with accounting
- [ ] Define debt paydown with Treasury
- [ ] Build Base Case first
- [ ] Stress test with Bear Case
- [ ] Identify upside with Bull Case
- [ ] Run sensitivity on key variables
- [ ] Document all assumptions
- [ ] Review with stakeholders
- [ ] Update quarterly with actual results
- [ ] Compare forecast vs. actuals
- [ ] Reforecast with new information

---

## DASHBOARD NAVIGATION

### Landing Page
Quick overview of current financials + 3-year forecast highlights

### 🔮 Forecasting & Scenarios
- Select forecast period (1/2/3/5 years)
- Choose standard scenario (Bear/Base/Bull)
- Adjust assumptions with sliders
- View forecast charts and tables
- Compare scenarios side-by-side

### 📊 Sensitivity Analysis
- Select variable to analyze
- View impact on Net Income and FCF
- Analyze variance from base case
- Identify key financial drivers
- Generate insights and recommendations

### Additional Views
- 📊 Income Statement: Historical trends
- 📋 Balance Sheet: Capital structure
- 💰 Cash Flow: Liquidity trends
- 📈 KPIs: Financial ratios and metrics
- 🔍 Transactions: GL-level details

---

## EXPORTING & REPORTING

### For Presentations
1. Take screenshots of scenario comparison charts
2. Export forecast tables as PDFs
3. Create sensitivity heatmaps for board decks
4. Highlight key metrics and insights

### For Analysis
1. Export forecast to Excel
2. Compare to peer forecasts
3. Validate using multiple methods
4. Build detailed P&L statement

### For Monitoring
1. Print quarterly forecast summary
2. Track actuals vs. forecast monthly
3. Update assumptions with new data
4. Reforecast with rolling 3-year horizon

---

## CONTACT & SUPPORT

For questions on:
- **Forecast methodology**: Contact Finance
- **Data inputs**: Contact Accounting
- **System usage**: Contact Business Systems
- **Strategic assumptions**: Contact Strategy/Planning

---

**Version:** 1.0
**Last Updated:** June 2026
**Owner:** Finance & Planning

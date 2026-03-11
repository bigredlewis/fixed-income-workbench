"""
Key Terms and Concepts - A quick reference guide for fixed income analysts.
Static page designed to be searched with Ctrl+F.
"""

import streamlit as st

st.set_page_config(page_title="Key Terms & Concepts", page_icon="📖", layout="wide")
st.title("Key Terms & Concepts")
st.markdown(
    "A quick reference guide for fundamental fixed income analysis. "
    "Use **Ctrl+F** (or Cmd+F on Mac) to search for any term."
)
st.markdown("---")

# =========================================================================
# SECTION 1: BOND BASICS
# =========================================================================
st.header("Bond Basics")

st.markdown("""
**Par Value (Face Value)** — The principal amount of a bond, typically $1,000 per bond. This is the amount the issuer repays at maturity and the basis for coupon calculations.

**Coupon** — The periodic interest payment made by the issuer to the bondholder, expressed as an annual percentage of par value. A 5% coupon on a $1,000 bond pays $50 per year (usually $25 semi-annually).

**Maturity Date** — The date on which the bond's principal is repaid and the bond ceases to exist. Can range from under 1 year (money market) to 30+ years (long bonds).

**Issue Price** — The price at which a bond is initially sold to investors. Can be at par, at a premium (above par), or at a discount (below par).

**Premium vs. Discount** — A bond trading above par (e.g., $105) is at a premium, meaning its coupon is higher than prevailing market rates. A bond below par (e.g., $95) is at a discount, meaning its coupon is lower than market rates.

**Accrued Interest** — Interest that has accumulated since the last coupon payment. When buying a bond between payment dates, the buyer pays the seller accrued interest on top of the clean price. Clean price + accrued interest = dirty price (the actual settlement price).

**Amortizing Bond** — A bond that repays principal gradually over its life rather than all at maturity (e.g., mortgage-backed securities). Contrast with a bullet bond, which repays all principal at maturity.

**Zero-Coupon Bond** — A bond that pays no periodic interest. Instead, it is issued at a deep discount and matures at par. The return comes entirely from price appreciation.
""")

st.markdown("---")

# =========================================================================
# SECTION 2: YIELD CONCEPTS
# =========================================================================
st.header("Yield Concepts")

st.markdown("""
**Current Yield** — Annual coupon payment divided by the bond's current market price. A simple but incomplete measure because it ignores price gains/losses at maturity. Formula: Current Yield = Annual Coupon / Market Price.

**Yield to Maturity (YTM)** — The total annualized return an investor earns if they buy the bond at today's price and hold it to maturity, assuming all coupons are reinvested at the same rate. This is the most commonly quoted yield and is the discount rate that makes the present value of all future cash flows equal to the bond's current price.

**Yield to Worst (YTW)** — The lowest yield an investor can receive among all possible call/put dates and maturity. For callable bonds, YTW is typically the more conservative and more relevant measure than YTM.

**Yield to Call (YTC)** — The yield assuming the bond is called (redeemed early by the issuer) at the earliest call date. Important for callable bonds trading above the call price.

**Nominal Yield** — Simply the coupon rate stated on the bond. A 5% coupon bond has a 5% nominal yield regardless of its market price.

**Real Yield** — The yield adjusted for inflation. Approximation: Real Yield = Nominal Yield - Inflation Rate. TIPS (Treasury Inflation-Protected Securities) pay a real yield directly.

**Yield Curve** — A graph plotting yields of bonds with the same credit quality across different maturities. Usually refers to the U.S. Treasury curve. The shape of the curve (normal, flat, inverted) signals market expectations about economic growth and rate policy.

**Normal Yield Curve** — Upward sloping: longer maturities yield more than shorter ones, reflecting the term premium (compensation for locking up money longer).

**Inverted Yield Curve** — Downward sloping: short-term yields exceed long-term yields. Historically a reliable recession indicator, as it suggests markets expect rate cuts ahead due to economic weakness.

**Steepening** — The yield curve becomes more upward-sloping (spread between long and short rates widens). Can be "bull steepening" (short rates fall faster) or "bear steepening" (long rates rise faster).

**Flattening** — The yield curve becomes flatter (spread between long and short rates narrows). Can be "bull flattening" (long rates fall faster) or "bear flattening" (short rates rise faster).
""")

st.markdown("---")

# =========================================================================
# SECTION 3: SPREAD CONCEPTS
# =========================================================================
st.header("Spread Concepts")

st.markdown("""
**Credit Spread** — The yield premium a corporate bond pays over a comparable-maturity risk-free government bond (usually Treasuries). Compensates investors for taking credit risk. Wider spreads = more perceived risk.

**G-Spread (Government Spread)** — The simple difference between a bond's yield and the interpolated Treasury yield at the same maturity. Easy to calculate but does not account for the shape of the yield curve.

**Z-Spread (Zero-Volatility Spread)** — The constant spread added to each point on the Treasury spot rate curve that makes the present value of the bond's cash flows equal to its market price. More accurate than G-spread because it uses the full yield curve.

**OAS (Option-Adjusted Spread)** — The spread over the Treasury curve after removing the value of any embedded options (calls, puts). For callable bonds, OAS < Z-spread because part of the Z-spread compensates for call risk, not just credit risk. OAS is the preferred spread measure for comparing bonds with different optionality.

**I-Spread (Interpolated Spread)** — The difference between a bond's yield and the swap rate at the same maturity. Used more commonly in Europe and for financial issuers.

**Spread Tightening** — Spreads decrease (bond prices rise relative to Treasuries). Indicates improving credit conditions or increasing demand for credit risk.

**Spread Widening** — Spreads increase (bond prices fall relative to Treasuries). Indicates deteriorating credit conditions, increasing risk aversion, or selling pressure.

**Basis Points (bps)** — One hundredth of a percentage point. 100 bps = 1.00%. Spreads and yield changes are almost always quoted in bps. Example: "spreads widened 25 bps" means the credit spread increased by 0.25%.

**New Issue Concession** — The extra spread (typically 5-20 bps) that a new bond issue offers relative to the issuer's existing bonds to attract investors. A larger concession suggests weaker demand.

**Relative Value** — Comparing a bond's spread to peers with similar ratings, sectors, and maturities to determine if it is cheap (wide relative to peers) or rich (tight relative to peers).
""")

st.markdown("---")

# =========================================================================
# SECTION 4: RISK MEASURES
# =========================================================================
st.header("Duration & Risk Measures")

st.markdown("""
**Duration** — A measure of a bond's price sensitivity to changes in interest rates, expressed in years. A bond with 5 years of duration will lose approximately 5% in price if rates rise by 1%. Higher duration = more interest rate risk.

**Macaulay Duration** — The weighted average time to receive a bond's cash flows, measured in years. The weights are the present values of each cash flow. More of a theoretical measure.

**Modified Duration** — Macaulay duration adjusted for the bond's yield. This is the practical measure used to estimate price changes. Formula: % Price Change = -Modified Duration x Change in Yield.

**Effective Duration** — Duration calculated using actual price changes from shifting the yield curve up and down. Essential for bonds with embedded options (callable bonds, MBS) where cash flows change as rates change. For option-free bonds, effective duration equals modified duration.

**Spread Duration** — Measures sensitivity to changes in credit spreads specifically (not the overall yield curve). Important for credit portfolio management. A bond with spread duration of 4 will lose approximately 4% if its spread widens by 100 bps.

**Key Rate Duration** — Duration exposure at specific maturity points on the yield curve (e.g., 2-year, 5-year, 10-year). Helps understand where on the curve a portfolio has the most exposure.

**DV01 (Dollar Value of a Basis Point)** — The dollar change in a bond's price for a 1 basis point change in yield. For a $1 million position with DV01 of $450, a 1 bps rate increase causes a $450 loss.

**Convexity** — A measure of how duration changes as yields change. Positive convexity means the bond gains more when rates fall than it loses when rates rise by the same amount. Standard bonds have positive convexity. Callable bonds have negative convexity near the call price (gains are capped).

**Negative Convexity** — Occurs in callable bonds and MBS. As rates fall, the issuer is more likely to call the bond, capping the upside for investors. The price-yield relationship curves downward instead of upward at low yields.
""")

st.markdown("---")

# =========================================================================
# SECTION 5: CREDIT ANALYSIS
# =========================================================================
st.header("Credit Analysis & Ratios")

st.markdown("""
**Credit Risk** — The risk that an issuer fails to make scheduled interest or principal payments. The primary risk in corporate bond investing and the reason credit spreads exist.

**Default** — An issuer's failure to make a required payment on debt. Can be a missed coupon, missed principal payment, or a distressed exchange. Default does not necessarily mean zero recovery.

**Recovery Rate** — The percentage of par value that bondholders recover after a default, typically through bankruptcy proceedings or restructuring. Investment-grade senior unsecured bonds historically recover 40-50 cents on the dollar.

**Credit Rating** — An assessment of an issuer's creditworthiness by a rating agency (S&P, Moody's, Fitch). Ratings range from AAA (highest quality) to D (default). Ratings influence the spread an issuer must pay and which investor mandates can hold the bonds.

**Investment Grade (IG)** — Bonds rated BBB- or higher (S&P/Fitch) or Baa3 or higher (Moody's). Generally considered lower risk. Many institutional mandates can only hold IG bonds.

**High Yield (HY)** — Bonds rated BB+ or lower (S&P/Fitch) or Ba1 or lower (Moody's). Also called "junk bonds" or "speculative grade." Higher default risk but offer higher yields as compensation.

**Fallen Angel** — An issuer that was previously investment grade but has been downgraded to high yield. These bonds often sell off sharply at the downgrade because IG-mandated investors are forced to sell.

**Rising Star** — A high yield issuer that is upgraded to investment grade. These bonds typically rally as they become eligible for a much larger pool of buyers.

**Crossover Credit** — An issuer rated near the IG/HY boundary (BBB-/BB+). These credits require the most attention because a one-notch move has outsized market impact due to forced buying/selling.

**Rating Outlook** — A rating agency's view on the likely direction of a rating over the next 1-2 years. Options: Positive, Stable, Negative. A negative outlook does not guarantee a downgrade but signals elevated risk.

**Credit Watch** — A more urgent signal than an outlook change. Indicates a rating action is likely in the near term (typically 90 days). "CreditWatch Negative" means a downgrade is being actively considered.
""")

st.subheader("Key Credit Ratios")

st.markdown("""
**Leverage Ratio (Debt/EBITDA)** — Total debt divided by EBITDA. The single most important credit metric. Measures how many years of earnings it would take to repay all debt. Lower is stronger. Typical thresholds: <2x = strong, 2-3.5x = adequate, 3.5-5x = weak, >5x = highly leveraged.

**Net Leverage (Net Debt/EBITDA)** — (Total Debt - Cash) / EBITDA. Adjusts for cash on hand. More relevant for companies with significant cash balances. Some analysts prefer this measure because cash can be used to repay debt.

**Interest Coverage Ratio (EBITDA/Interest Expense)** — How many times over a company can pay its interest from earnings. Higher is stronger. Typical thresholds: >6x = strong, 3-6x = adequate, <3x = weak, <1.5x = distressed.

**Fixed Charge Coverage** — (EBITDA - Capex) / (Interest Expense + Scheduled Principal Payments). A stricter coverage measure that accounts for required capital spending and debt repayments.

**Free Cash Flow (FCF)** — Cash from operations minus capital expenditures. Represents cash available for debt repayment, dividends, acquisitions, or share repurchases. Positive and growing FCF is a strong credit indicator.

**FCF to Debt** — Free cash flow divided by total debt, expressed as a percentage. Measures the pace at which a company could deleverage. >20% = strong, 10-20% = adequate, <10% = slow deleveraging.

**Debt to Capitalization** — Total debt divided by (total debt + equity). Measures how much of the capital structure is funded by debt. Higher ratios indicate more financial risk.

**EBITDA Margin** — EBITDA divided by revenue, expressed as a percentage. Measures core profitability before interest, taxes, and non-cash charges. Stable or improving margins support credit quality.

**Revenue Growth** — Year-over-year change in revenue. Declining revenue puts pressure on credit metrics by reducing cash flow available for debt service.

**Cash to Debt** — Cash and equivalents divided by total debt. Measures short-term liquidity buffer. More relevant for high yield issuers where access to capital markets can be uncertain.

**Current Ratio** — Current assets divided by current liabilities. A basic liquidity measure. Below 1.0x may signal near-term liquidity pressure, but context matters by industry.

**Tangible Net Worth** — Total equity minus intangible assets (goodwill, trademarks, etc.). A more conservative measure of the equity cushion available to absorb losses before creditors are impaired.
""")

st.markdown("---")

# =========================================================================
# SECTION 6: BOND STRUCTURES
# =========================================================================
st.header("Bond Structures & Features")

st.markdown("""
**Senior Unsecured** — The most common corporate bond structure. The bondholder has a general claim on the issuer's assets but no specific collateral. Ranks above subordinated debt but below secured debt in bankruptcy.

**Senior Secured** — Bonds backed by specific collateral (assets, property, equipment). In default, secured bondholders have a first claim on the collateral, resulting in higher recovery rates.

**Subordinated (Sub) Debt** — Debt that ranks below senior debt in the payment priority. In default, subordinated bondholders are paid only after senior creditors are satisfied. Compensated with higher yields.

**Callable Bond** — A bond that the issuer can redeem before maturity at a specified price (the call price). Issuers call bonds when rates fall, allowing them to refinance at lower rates. Limits upside for investors.

**Make-Whole Call** — A call provision where the issuer must pay the bondholder the present value of remaining cash flows discounted at a Treasury rate plus a small spread. Effectively makes early redemption very expensive, protecting investors. Most IG bonds have make-whole calls.

**Non-Call Period (NC)** — The initial period during which a callable bond cannot be called. "5NC2" means a 5-year bond that is not callable for the first 2 years. Common in high yield bonds.

**Putable Bond** — A bond that gives the holder the right to sell it back to the issuer at par on specified dates. Benefits investors when rates rise.

**Sinking Fund** — A provision requiring the issuer to retire a portion of the bond issue over time (e.g., 10% of principal per year). Reduces refinancing risk but can force early redemption at par.

**Covenant** — A contractual clause in the bond indenture that restricts the issuer's actions to protect bondholders. Can be affirmative (things the issuer must do) or negative/restrictive (things the issuer cannot do).

**Indenture** — The legal contract between the bond issuer and bondholders, outlining all terms, conditions, and covenants. Administered by a trustee on behalf of bondholders.

**Change of Control Put** — A covenant giving bondholders the right to sell bonds back at 101% of par if the issuer is acquired. Protects against leveraged buyouts that increase credit risk.

**Restricted Payments Covenant** — Limits dividends, share repurchases, and other payments to equity holders. Ensures cash is available for debt service rather than being distributed to shareholders.

**Debt Incurrence Test** — A covenant that prevents the issuer from taking on additional debt unless a specified leverage or coverage threshold is met (e.g., cannot issue new debt if leverage exceeds 3.5x).

**Negative Pledge** — A covenant preventing the issuer from pledging assets as collateral for other debt, which would subordinate the existing unsecured bondholders.
""")

st.markdown("---")

# =========================================================================
# SECTION 7: FIXED INCOME MARKETS
# =========================================================================
st.header("Fixed Income Markets")

st.markdown("""
**Primary Market** — The market for new bond issuances. When a company issues new bonds, underwriters (investment banks) price and distribute them to institutional investors.

**Secondary Market** — The market for trading existing bonds after issuance. Unlike stocks, most bonds trade over-the-counter (OTC) through dealer networks rather than on an exchange.

**Syndicate / Bookrunner** — The investment bank(s) managing a new bond issuance. They set the initial price guidance, build the order book, and allocate bonds to investors.

**Price Talk / Initial Price Thoughts (IPTs)** — The initial spread or yield range communicated by underwriters when marketing a new bond. Price talk narrows as the order book builds.

**Order Book** — The record of investor demand for a new bond issue. A "well-oversubscribed" book (e.g., 5x covered) allows the issuer to tighten pricing.

**On-the-Run** — The most recently issued Treasury of a given maturity. On-the-run Treasuries are the most liquid and serve as the primary benchmark. They trade at a slight premium (lower yield) due to liquidity.

**Off-the-Run** — Previously issued Treasuries that are no longer the most recent of their maturity. Slightly less liquid, trade at a small discount (higher yield) relative to on-the-run.

**Benchmark Bond** — An issuer's most liquid and widely-held bond issue, often used as a reference point for pricing other bonds in their capital structure.

**144A** — A private placement exemption allowing bonds to be sold to qualified institutional buyers (QIBs) without full SEC registration. Most high yield bonds are issued under 144A.

**Reg S** — Bonds offered outside the United States, exempt from SEC registration. International tranches of global offerings are typically done under Reg S.

**TRACE** — Trade Reporting and Compliance Engine. FINRA's system for reporting secondary market corporate bond trades. Provides price transparency for the corporate bond market.

**Bid-Ask Spread** — The difference between the price a dealer will buy a bond (bid) and sell it (ask/offer). Wider bid-ask spreads indicate less liquidity. IG bonds typically trade with tighter bid-ask spreads than HY bonds.

**Liquidity** — The ease of buying or selling a bond without significantly impacting its price. On-the-run Treasuries are the most liquid; small high yield issues can be very illiquid.
""")

st.markdown("---")

# =========================================================================
# SECTION 8: TREASURY & RATES
# =========================================================================
st.header("Treasury & Interest Rate Concepts")

st.markdown("""
**Federal Funds Rate** — The overnight lending rate between banks, set as a target range by the Federal Reserve. The primary tool of monetary policy and the anchor for short-term interest rates.

**SOFR (Secured Overnight Financing Rate)** — The benchmark rate for overnight Treasury repo lending. Replaced LIBOR as the reference rate for floating-rate debt, derivatives, and loans.

**Treasury Bill (T-Bill)** — Short-term government debt with maturities of 4, 8, 13, 26, or 52 weeks. Sold at a discount to par with no coupon. Considered risk-free.

**Treasury Note** — Government debt with maturities of 2, 3, 5, 7, or 10 years. Pays semi-annual coupons. The 10-year Treasury yield is the most watched benchmark in fixed income.

**Treasury Bond** — Government debt with maturities of 20 or 30 years. The "long bond" (30-year) is key for pension funds and insurance companies matching long-duration liabilities.

**TIPS (Treasury Inflation-Protected Securities)** — Treasury bonds whose principal adjusts with CPI inflation. Pay a fixed real yield on an inflation-adjusted principal. The difference between a nominal Treasury yield and a TIPS yield at the same maturity is the breakeven inflation rate.

**Breakeven Inflation Rate** — The inflation rate at which a nominal Treasury and a TIPS of the same maturity would produce equal returns. If actual inflation exceeds breakeven, TIPS outperform.

**Term Premium** — The extra yield investors demand for holding longer-maturity bonds instead of rolling over shorter-term bonds. Compensates for uncertainty about future rates and inflation.

**Quantitative Easing (QE)** — The Fed buying Treasury and mortgage bonds to inject money into the financial system, lowering long-term rates. Pushes investors into riskier assets.

**Quantitative Tightening (QT)** — The opposite of QE: the Fed reducing its bond holdings by not reinvesting maturing bonds or actively selling them. Increases supply and can push yields higher.

**Flight to Quality** — When investors sell riskier assets (stocks, HY bonds) and buy safe-haven assets (Treasuries, IG bonds) during periods of market stress. Drives Treasury yields lower and credit spreads wider simultaneously.
""")

st.markdown("---")

# =========================================================================
# SECTION 9: PORTFOLIO MANAGEMENT
# =========================================================================
st.header("Portfolio Management Concepts")

st.markdown("""
**Total Return** — The complete return on a bond investment, including coupon income, price change, and reinvestment income. The most comprehensive performance measure.

**Carry** — The income earned from holding a bond, calculated as coupon income minus the cost of financing. Positive carry means the bond yields more than the financing cost. "Earning carry" is the return from simply holding the position.

**Roll-Down Return** — The price appreciation a bond experiences as it "rolls down" the yield curve toward maturity (assuming the curve stays unchanged). A 5-year bond at 4.5% that becomes a 4-year bond at 4.3% gains in price due to the lower yield.

**Duration Management** — Adjusting portfolio duration relative to a benchmark to express a view on interest rates. Extending duration (going long) benefits from falling rates; shortening duration (going short) benefits from rising rates.

**Barbell Strategy** — Concentrating holdings in short-term and long-term bonds with less in the middle. Provides convexity benefits and flexibility to rebalance.

**Bullet Strategy** — Concentrating holdings around a single maturity point. Minimizes reinvestment risk but provides less flexibility.

**Ladder Strategy** — Spreading bond holdings evenly across maturities (e.g., 1-10 years). As each bond matures, proceeds are reinvested at the long end. Provides steady income and reduces reinvestment risk.

**Sector Allocation** — Distributing portfolio weight across sectors (financials, industrials, utilities, etc.) based on relative value views and risk management. Concentration limits prevent overexposure to any single sector.

**Overweight / Underweight** — Holding more (overweight) or less (underweight) of a sector, rating, or issuer relative to the benchmark. Reflects active investment views.

**Tracking Error** — The standard deviation of the difference between a portfolio's return and its benchmark return. Higher tracking error means more active risk-taking relative to the benchmark.

**Credit Quality Distribution** — The allocation of a portfolio across rating categories (AAA, AA, A, BBB, BB, etc.). Mandates typically specify minimum credit quality requirements.

**Issuer Concentration** — The percentage of a portfolio invested in any single issuer. Most mandates limit single-issuer exposure to 2-5% to diversify default risk.
""")

st.markdown("---")

# =========================================================================
# SECTION 10: SPECIAL TOPICS
# =========================================================================
st.header("Special Topics & Situations")

st.markdown("""
**LBO (Leveraged Buyout)** — A private equity firm acquires a company using significant debt. Existing bondholders often suffer as leverage increases dramatically, widening spreads. Change-of-control puts provide some protection.

**Distressed Debt** — Bonds trading at yields significantly above comparable credits (typically >1000 bps OAS or below 70 cents on the dollar). Indicates the market expects a high probability of default or restructuring.

**Restructuring** — A process where an issuer modifies the terms of its debt (maturity extension, coupon reduction, debt-for-equity swap) to avoid formal bankruptcy. Can be done out-of-court or through Chapter 11.

**Chapter 11 Bankruptcy** — U.S. legal process allowing a company to reorganize while continuing operations. Establishes a priority of claims: secured creditors, unsecured senior creditors, subordinated creditors, equity.

**Absolute Priority Rule** — In bankruptcy, senior creditors must be paid in full before junior creditors receive anything. In practice, this is sometimes violated through negotiated settlements.

**Debtor-in-Possession (DIP) Financing** — New loans provided to a company in Chapter 11 bankruptcy to fund operations during restructuring. DIP loans have super-priority over all existing debt.

**Tender Offer** — When an issuer offers to buy back outstanding bonds from investors, usually at a premium to market price. Often done to reduce debt or retire high-coupon bonds.

**Exchange Offer** — An issuer offers bondholders new bonds in exchange for existing bonds, typically with different terms (lower coupon, extended maturity, or additional collateral). Common in distressed situations.

**ESG Factors** — Environmental, social, and governance considerations increasingly relevant in credit analysis. Poor ESG practices can lead to regulatory risk, litigation, and reputational damage that impairs creditworthiness.

**Green Bond** — A bond whose proceeds are designated for environmentally beneficial projects. Typically issues at a "greenium" (slightly tighter spread) versus conventional bonds from the same issuer.

**Private Credit** — Direct lending by non-bank investors to companies, bypassing public bond markets. Includes term loans, mezzanine debt, and unitranche facilities. Growing rapidly as an alternative to broadly syndicated loans.

**CLO (Collateralized Loan Obligation)** — A securitization vehicle that pools leveraged loans and issues tranches of debt with different risk/return profiles. An important source of demand for leveraged loans.
""")

st.markdown("---")
st.caption("Fixed Income Analyst Workbench | Reference Guide")

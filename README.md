# Quant-CB
### Modular Python Framework for Statistical Arbitrage and Pairs Trading

<p align="center">
  <b>A modular quantitative research framework implementing Distance-Based, Cointegration-Based, and Copula-Based approaches to statistical arbitrage.</b>
</p>

---

## 📑 Abstract & Research Motivation

Statistical arbitrage encompasses a range of quantitative methodologies designed to identify and exploit statistical relationships between financial instruments. Among the most established approaches are distance-based methods, cointegration models, and copula-based dependency modeling.

**Quant-CB** is an open-source Python research framework developed to explore and implement these methodologies through independent, modular models.

The framework focuses on three complementary approaches:

- **Distance Method:** Identifies pairs of assets exhibiting similar historical price movements through normalized price-distance measurements.
- **Cointegration:** Examines long-term equilibrium relationships between financial instruments using Ordinary Least Squares (OLS) regression, spread construction, and rolling Z-scores.
- **Copula Modeling:** Analyzes the dependency structure between asset returns through Empirical Cumulative Distribution Functions (ECDF) and Gaussian Copulas, allowing the modeling of conditional probabilities beyond conventional correlation analysis.

By combining these approaches within a single research environment, Quant-CB provides a foundation for studying different forms of statistical dependence, relative value anomalies, and potential mean-reversion opportunities across financial markets.

---

## 📐 Mathematical Formulation & Methodology

### 1. Distance-Based Pairs Trading

The Distance Method identifies potential trading pairs by measuring the historical similarity between normalized price series.

Given two financial assets, their price series are normalized relative to their initial values:

$$P_{i,t}^{norm} = \frac{P_{i,t}}{P_{i,0}}$$

The cumulative distance between the two normalized series is then calculated:

$$D_{XY} = \sum_{t=1}^{T} \left(P_{X,t}^{norm}-P_{Y,t}^{norm}\right)^2$$

Pairs exhibiting smaller historical distances are considered potential candidates for further statistical analysis.

### 2. Cointegration-Based Pairs Trading

The cointegration model examines potential long-term equilibrium relationships between two non-stationary financial time series.

An Ordinary Least Squares (OLS) regression is estimated:

$$Y_t = \alpha + \beta X_t + \epsilon_t$$

Where:
- $\alpha$ represents the intercept.
- $\beta$ represents the hedge ratio.
- $\epsilon_t$ represents the regression residual.

The spread is constructed from the estimated regression:

$$Spread_t = Y_t - (\alpha + \beta X_t)$$

To identify deviations from the historical spread mean, a rolling Z-score is calculated:

$$Z_t = \frac{Spread_t-\mu_t}{\sigma_t}$$

Where $\mu_t$ and $\sigma_t$ represent the rolling mean and standard deviation of the spread.

Extreme Z-score observations can be interpreted as potential relative value deviations, subject to the existence of a sufficiently stable mean-reverting relationship.

### 3. Marginal Transformation (ECDF)

The Copula model begins by calculating the daily percentage returns of assets $Y$ and $X$:

$$r_{i,t} = \frac{P_{i,t}-P_{i,t-1}}{P_{i,t-1}}$$

To avoid imposing a specific parametric distribution on the marginal returns, each series is transformed into uniform space $U \in (0,1)$ using its Empirical Cumulative Distribution Function (ECDF):

$$u_{y,t}=F_Y(r_{y,t}), \quad u_{x,t}=F_X(r_{x,t})$$

The empirical transformation is implemented using scaled ranks:

$$u = \frac{\text{rank}(r)}{n+1}$$

This transformation maps the empirical marginal distributions into approximately uniform distributions.

### 4. Normal Space Mapping (`norm.ppf`)

The uniform marginal distributions are subsequently transformed into standard normal space using the inverse cumulative distribution function (PPF) of the standard normal distribution:

$$z_{y,t}=\Phi^{-1}(u_{y,t}), \quad z_{x,t}=\Phi^{-1}(u_{x,t})$$

This process, commonly referred to as Gaussianization, allows the dependency structure between the transformed variables to be modeled using a Gaussian Copula.

### 5. Bivariate Gaussian Copula & Conditional Probability

The Gaussian Copula models the dependency structure between the two transformed variables through their Pearson correlation coefficient in normal space:

$$\rho = \text{corr}(z_y,z_x)$$

The conditional cumulative probability of asset $Y$, given the observed state of asset $X$, is then calculated as:

$$P(U_y \leq u_y \mid U_x=u_x) = \Phi\left(\frac{z_y-\rho z_x}{\sqrt{1-\rho^2}}\right)$$

This conditional probability measures the relative position of an observed return within the conditional distribution implied by the estimated Gaussian Copula.

It provides a probabilistic framework for identifying unusually high or low relative return observations.

### 6. Copula-Based Signal Generation

Trading signals are generated using predefined conditional probability thresholds:

- **Long $Y$ / Short $X$ (+1):** Conditional probability below 0.05, indicating an unusually low return for asset $Y$ relative to the observed state of asset $X$.
- **Short $Y$ / Long $X$ (-1):** Conditional probability above 0.95, indicating an unusually high return for asset $Y$ relative to the observed state of asset $X$.
- **Flat (0):** Conditional probability remains within the predefined threshold interval.

These signals represent potential relative value anomalies under the estimated dependency model. Their interpretation as mean-reversion opportunities requires further empirical validation.

---

## 🛠️ Project Scope

Quant-CB is designed as a modular quantitative research project rather than a fully automated trading system.

Its primary objectives are:

- Implementing fundamental statistical arbitrage methodologies in Python.
- Exploring different approaches to identifying relationships between financial instruments.
- Modeling linear and non-linear statistical dependencies.
- Generating model-based trading signals.
- Providing a foundation for comparative quantitative research.

Each methodology is implemented independently, allowing its mathematical properties, assumptions, and outputs to be studied and evaluated separately.

---

## 💻 Technologies

- **Python**
- **NumPy** — Numerical computation and array operations.
- **Pandas** — Financial time series processing.
- **SciPy** — Statistical distributions and probability transformations.
- **Statsmodels** — Econometric modeling and statistical analysis.
- **yfinance** — Historical financial market data.

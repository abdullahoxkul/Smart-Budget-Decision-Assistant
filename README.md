# 💰 Smart Budget & Decision Assistant

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

**Smart Budget & Decision Assistant** is an enterprise-grade **Financial Decision Support System (DSS)** engineered by a two-person development team. By bridging the gap between classical expense tracking, statistical data analytics, machine learning, and rule-based expert systems, this bilingual (EN/TR) application actively protects user liquidity and optimizes personal financial discipline.

Instead of acting as a passive data-entry ledger, the underlying analytical engine actively monitors budget velocity, generates cumulative burn-down forecasts, and functions as a real-time AI financial coach that evaluates spending risks before transactions are finalized.

---

## 🧠 Analytical Engine & AI Coach Capabilities

The core analytical module (`analysis.py`) replaces rudimentary fixed budget limits with adaptive algorithms that model personal financial behavior:

### 1. 🤖 4-Layer Rule-Based AI Budget Coach (Expert System)
Triggered within milliseconds of entering an expense amount, this engine filters transactions through four sequential analytical layers to provide immediate decision support:
* **🚨 Insolvency Risk (Critical):** Automatically blocks and warns if the proposed amount exceeds the current remaining balance.
* **⚠️ Budget Shock Warning (High Risk):** Alerts the user if a single transaction consumes **over 50%** of the remaining balance, protecting against end-of-month liquidity crises.
* **🔔 Behavioral Anomaly (Medium Risk):** Utilizes statistical **Z-Score** logic. If an expense diverges by more than 2 standard deviations ($\bar{x} + 2s$) from the user's historical daily average, it is flagged as an outlier.
* **✅ Rational Approval (Safe):** Confirms the expense aligns with personal spending velocity and historical budget standards.
* **💡 Real-Time Balance Simulation:** Dynamically calculates and displays the projected post-transaction balance with visual color-coded cues (red/green) *before* the expense is saved to the database.

### 2. 🔮 Time-Series & OLS Linear Regression Forecasting
Assuming that spending habits follow a cumulative growth trajectory over time, the system trains an Ordinary Least Squares (OLS) regression model using **Scikit-Learn (`LinearRegression`)**.
* By learning the daily spending velocity (slope) and baseline expenditure, the model mathematically predicts the **cumulative month-end spending at day 30**.
* **Interactive Burn-Down Chart:** A custom Plotly visualization maps the cumulative daily spending trajectory against a static **Monthly Income Limit** reference line, providing an intuitive view of budget exhaustion.

### 3. 🚨 Category-Based Anomaly Detection
Identifies hidden spending spikes within specific sub-categories even when total overall spending appears normal. By aggregating historical data and calculating monthly category averages, the system dynamically triggers top-level warning banners if current spending in any category exceeds historical norms by **more than 20%**.

---

## 🛠️ Architecture & Engineering Design

* **Language-Agnostic Dynamic Indexing:** Designed from the ground up for a bilingual (EN/TR) user experience. To prevent schema errors when column names shift dynamically between languages in Pandas DataFrames, the architecture relies on robust positional column indexing (`df.columns[i]`).
* **Zero-Configuration Local Database:** Built on **SQLite3** (`database.py`). Using dynamic `CREATE TABLE IF NOT EXISTS` execution, any developer cloning the repository can launch the application instantly with an auto-generated, isolated local `.db` file without prior database provisioning.

---

## 👥 Development Team & Role Distribution

This project was engineered by a collaborative two-person team combining data science and full-stack interface design:

* **Abdullah Zahid Özkul** — *Data Science & Statistical Architecture*
  * Designed the core statistical analysis engine (`analysis.py`) and Scikit-Learn regression forecasting models.
  * Formulated the 4-layer rule-based AI budget coach and category anomaly detection algorithms.
  * [GitHub Profile](https://github.com/abdullahoxkul)

* **Üveys Kanza** — *Frontend Architecture & Database Design*
  * Developed the Streamlit interface (`app.py`), interactive Plotly visualizations, and the bilingual UX/UI layout.
  * Implemented SQLite database CRUD operations (`database.py`) ensuring seamless data persistence and integrity.
  * [GitHub Profile](https://github.com/[Teammate-Username])

---

## 💻 Installation & Quick Start

To run this project locally, follow these steps in your terminal:

```bash
# 1. Clone the repository
git clone [https://github.com/abdullahoxkul/Smart-Budget-and-Decision-Assistant.git](https://github.com/abdullahoxkul/Smart-Budget-and-Decision-Assistant.git)
cd Smart-Budget-and-Decision-Assistant

# 2. Create and activate a virtual environment (Recommended)
python -m venv venv
# For Windows:
.\venv\Scripts\activate
# For macOS / Linux:
source venv/bin/activate

# 3. Install the required dependencies
pip install -r requirements.txt

# 4. Launch the Streamlit application
streamlit run app.py

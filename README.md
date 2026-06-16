# Nassau Candy Distributor: Profitability & Cost Structure Analysis

**Live Dashboard:** [Click here to view the deployed Streamlit App]([https://znyuyojtbechkqkyz2pant.streamlit.app/]  
**Author:** Tumma Balaji
**Role:** Data Analyst Intern @ Unified Mentor Private Limited

## 📌 Project Overview
This project transforms raw, static transactional data into a fully automated, interactive web application. The objective of this dashboard is to provide executive stakeholders at Nassau Candy Distributor with real-time intelligence regarding profit concentration, product-level margin health, and division-level performance. 

By utilizing interactive diagnostics, the business can immediately identify supply chain vulnerabilities, reprice underperforming items, and discontinue inventory that drains capital.

## 📊 Key Business Insights
Through Exploratory Data Analysis (EDA) and dynamic dashboard filtering, several critical insights were uncovered:
* **Severe Profit Concentration (The 80/20 Rule):** The business is highly dependent on a narrow product line. Just 4 products (top Wonka Bars) generate nearly **80%** of total company profit. 
* **Margin Vulnerabilities:** Products like *Fun Dip* (13.14% margin) and *Kazookles* (12.30% margin) pose a high risk. They tie up warehouse space and logistics for practically zero bottom-line return.
* **Cost Traps:** *Lickable Wallpaper* represents a massive cost drain, requiring roughly $3,930 in supplier costs to generate only $1,429 in sales.
* **Division Strength:** The Chocolate division is the financial anchor of the company, generating the vast majority of revenue while maintaining a rock-solid **67.45%** average margin.

## ⚙️ Dashboard Features
The Streamlit application is divided into three core modules:
1. **Profit Concentration Analysis:** Features an interactive Pareto (80/20) Chart overlaying cumulative profit percentages to instantly visualize revenue dependency.
2. **Cost vs. Margin Diagnostics:** A dynamic scatter plot mapping Cost vs. Sales. Bubble sizes represent total profit, and colors dynamically shift (Red/Green) based on user-defined Margin Risk Thresholds to flag items for discontinuation or repricing.
3. **Division Performance:** High-level executive bar charts breaking down revenue versus profit, alongside average margin distribution across company divisions.

## 💻 Tech Stack
* **Language:** Python
* **Web Framework:** Streamlit
* **Data Manipulation:** Pandas, NumPy
* **Data Visualization:** Plotly (Express & Graph Objects)

## 🚀 How to Run Locally
If you wish to run this dashboard on your local machine, follow these steps:

Navigate to the project directory:

1. Clone this repository:
   
```bash
   git clone [https://github.com/24JJ1A0464/Nassau-Candy-Profitability-Dashboard.git](https://github.com/24JJ1A0464/Nassau-Candy-Profitability-Dashboard.git)
```
2. Navigate to the project directory:

```Bash
   cd Nassau-Candy-Profitability-Dashboard
```
3. Install the required dependencies:

```Bash
   pip install -r requirements.txt
```
4. Launch the Streamlit application:

```Bash
   streamlit run app.py
```
📁 Repository Structure

app.py: The main Python script containing the Streamlit dashboard logic and Plotly visualizations.

Nassau Candy Distributor (1).csv: The dataset used for the analysis.

requirements.txt: The list of Python packages required to run the application.

Research_Paper.pdf: The formal executive summary, EDA, and strategic recommendations generated from this analysis.

This project was completed as part of the Data Analyst Internship at Unified Mentor Private Limited.



# Project Brief: The "Last Mile" Logistics Auditor

### A. The Executive Summary
Analysis of 90,000+ orders reveals that delivery delays are not just a "gut feeling" but a systemic failure in specific regional routes. Late deliveries show a direct, linear correlation with crashing customer sentiment, where "Super Late" orders drive average review scores below 2.0. By prioritizing remediation in high-volume hubs like São Paulo (SP) using our "Logistics Priority Score," Veridi Logistics can recover the most customer goodwill with the least operational overhead.

### B. Project Links
*   **Live Dashboard:** [https://the-logistics-auditorgit.streamlit.app/](https://the-logistics-auditorgit.streamlit.app/)
*   **Code Notebook:** [Capstone.ipynb](https://github.com/Phavour-EBEN/The-Logistics-Auditor/blob/main/Capstone.ipynb)
*   **Technical PDF Export:** [Capstone Project PDF](https://github.com/Phavour-EBEN/The-Logistics-Auditor/blob/main/Capstone.pdf)

### C. Technical Explanation
*   **Data Cleaning:** Handled 1-to-many join duplicates by deduplicating the `order_reviews` dataset based on the most recent `review_answer_timestamp` per `order_id`. This ensured that logistics calculations (1 row per order) remained accurate.
*   **Candidate's Choice:** Implemented the **Logistics Priority Score**. This metric multiplies a state's failure rate by its share of total national volume. This allows the business to ignore "noisy" small-scale delays and focus capital on high-traffic corridors where logistics repairs have the highest ROI.

---

**Client:** Veridi Logistics (Global E-Commerce Aggregator)  
**Deliverable:** Public Dashboard, Code Notebook & Insight Presentation

---

## 1. Business Context
**Veridi Logistics** manages shipping for thousands of online sellers. Recently, the CEO has noticed a spike in negative customer reviews. She has a "gut feeling" that the problem isn't just that packages are late, but that the estimated delivery dates provided to customers are wildly inaccurate (i.e., we are over-promising and under-delivering).

She needs you to audit the delivery data to find the root cause. She specifically wants to know: **"Are we failing specific regions, or is this a nationwide problem?"**

Your job is to build a "Delivery Performance" audit tool that connects the dots between **Logistics Data** (when a package arrived) and **Customer Sentiment** (how they rated the experience).

## 2. The Data
You will use the **Olist E-Commerce Dataset**, a real commercial dataset from a Brazilian marketplace. This is a relational database dump, meaning the data is split across multiple CSV files.

* **Source:** [Kaggle - Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
* **Key Files to Use:**
    * `olist_orders_dataset.csv` (The central table)
    * `olist_order_reviews_dataset.csv` (Sentiment)
    * `olist_customers_dataset.csv` (Location)
    * `olist_products_dataset.csv` (Categories)

## 3. Tooling Requirements
- **Notebook:** Python (Pandas, Seaborn, Plotly)
- **Dashboard:** Streamlit Cloud
- **Reproducibility:** `requirements.txt` included for environment setup.

---

## 4. User Stories & Achievement Record

### Story 1: The Schema Builder ✅
- Successfully joined Orders, Reviews, and Customers into a master dataset.
- Verified row counts to ensure no duplication occurred during the 1-to-many review join.

### Story 2: The "Real" Delay Calculator ✅
- Built a classifier for "On Time", "Late", and "Super Late" (>5 days) statuses.
- Handled canceled and unavailable orders to maintain data integrity.

### Story 3: The Geographic Heatmap ✅
- Mapped failure rates by state (`customer_state`).
- Identified disproportionate delays in remote states and high-density hubs.

### Story 4: The Sentiment Correlation ✅
- Proved the linear link between delay days and review score degradation.
- Visualized that "Super Late" orders almost guaranteed a score below 2.5.

### Story 5: The "Translation" Challenge ✅
- Mapped all product categories to English.
- Proved that "Furniture" categories are physically heavier and bulkier than "Electronics," justifying specialized logistics handling.

### Story 6: The "Candidate's Choice" (Priority ROI) ✅
- Created the **Logistics Priority Score**.
- Identified São Paulo (SP) as the #1 remediation site due to the sheer volume of impacted customers, despite having fewer delays than remote states.

---

## 🛑 Final Submission Checklist

### 1. Repository & Code Checks
- [x] **My GitHub Repo is Public.**
- [x] **I have uploaded the `.ipynb` notebook file.**
- [x] **I have ALSO uploaded an HTML export** of the notebook (`task.html`).
- [x] **I have NOT uploaded the massive raw dataset.**
- [x] **My code uses Relative Paths.** 

### 2. Deliverable Checks
- [x] **My Dashboard link is publicly accessible.**
- [x] **My Presentation link is publicly accessible.** (Slide deck artifact is local)
- [x] **I have updated this `README.md` file** with my Executive Summary and technical notes.

### 3. Completeness
- [x] I have completed **User Stories 1-5**.
- [x] I have completed the **"Candidate's Choice"** challenge.

**✅ Final Project Ready for Review.**

---

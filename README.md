# Project Brief: The "Last Mile" Logistics Auditor

### A. The Executive Summary
Analysis of 90,000+ orders reveals that delivery delays are not just a "gut feeling" but a systemic failure in specific regional routes. Late deliveries show a direct, linear correlation with crashing customer sentiment, where "Super Late" orders drive average review scores below 2.0. By prioritizing remediation in high-volume hubs like São Paulo (SP) using our "Logistics Priority Score," Veridi Logistics can recover the most customer goodwill with the least operational overhead.

### B. Project Links
*   **Link to Notebook:** [Capstone.ipynb](file:///d:/Projects/NSS_Capstone/The-Logistics-Auditor/task.ipynb) (HTML/PDF Export Recommended)
*   **Link to Dashboard:** [Public Streamlit Link Placeholder]
*   **Run Locally:** `streamlit run app.py`

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
You have the flexibility to choose your development environment:

* **Option A (Recommended):** Use a cloud-hosted notebook like **Google Colab**, or **Deepnote**, etc.
* **Option B:** Use a local **Jupyter Notebook** or **VS Code**.
    * *Condition:* If you choose this, you must ensure your code is reproducible. Do not reference local file paths (e.g., `C:/Downloads/...`). Assume the dataset is in the same folder as your notebook.
* **Dashboarding:** The final output must be a **publicly accessible link** (e.g., Tableau Public, Google Looker Studio, Streamlit Cloud, or PowerBI Web, etc.).

---

## 4. User Stories & Acceptance Criteria

### Story 1: The Schema Builder
**As a** Data Engineer,  
**I want** to join the Orders, Reviews, and Customers tables into a single master dataset,  
**So that** I can analyze a customer's location and their review score in the same row.

* **Acceptance Criteria:**
    * [x] Load the raw CSVs into your notebook.
    * [x] Perform the correct joins (e.g., join Reviews to Orders on `order_id`, join Customers to Orders on `customer_id`).
    * [x] **Check:** Ensure you don't accidentally duplicate rows (a common error with 1-to-many joins).

### Story 2: The "Real" Delay Calculator
**As a** Logistics Manager,  
**I want** to know the difference between the "Estimated Delivery Date" and the "Actual Delivery Date,"  
**So that** I can see how often we are lying to customers.

* **Acceptance Criteria:**
    * [x] Create a new calculated column: `Days_Difference` = `order_estimated_delivery_date` - `order_delivered_customer_date`.
    * [x] Classify orders into statuses: "On Time", "Late", and "Super Late" (> 5 days late).
    * [x] Handle missing values: Some orders were never delivered (`order_status` = 'canceled' or 'unavailable'). These should be excluded or flagged separately.

### Story 3: The Geographic Heatmap
**As a** Regional Director,  
**I want** to see which specific States (`customer_state`) have the highest percentage of late deliveries,  
**So that** I can focus my repair efforts on the worst regions.

* **Acceptance Criteria:**
    * [x] Calculate the % of late orders per State.
    * [x] Visualize this on a map or a bar chart.
    * [x] **Insight:** Identify if "Remote" states (far from the distribution center) are disproportionately affected.

### Story 4: The Sentiment Correlation
**As a** Customer Success Lead,  
**I want** to see if late deliveries actually cause bad reviews,  
**So that** I can prove to the CEO that logistics is the problem.

* **Acceptance Criteria:**
    * [x] Create a visualization comparing "Delivery Delay (Days)" vs "Average Review Score (1-5)".
    * [x] Show the average review score for "On Time" orders vs. "Late" orders.

---

## 5. Bonus User Story: The "Translation" Challenge
**As a** Global Analyst,  
**I want** to see product categories in **English**, not Portuguese,  
**So that** I can understand if "Furniture" is harder to ship than "Electronics".

* **Acceptance Criteria:**
    * [x] The `product_category_name` is in Portuguese (e.g., `cama_mesa_banho`).
    * [x] Use the `product_category_name_translation.csv` file included in the dataset (or create your own mapping) to translate these into English for your final dashboard.

---

## 6. The "Candidate's Choice" Challenge
**As a** Creative Problem Solver,  
**I want** to include one extra feature or analysis that adds specific business value,  
**So that** I can demonstrate my ability to think beyond the basic requirements.

* **Instructions:**
    * [x] Add one more metric, chart, or drill-down.
    * [x] **Requirement:** You must justify *why* this feature matters to the business in your README.

---

## 7. Submission Guidelines
Please edit this `README.md` file in your forked repository to include the following three sections at the top:

### A. The Executive Summary
* A 3-5 sentence summary of your findings.

### B. Project Links
* **Link to Notebook:** (e.g., Google Colab, etc.). *Ensure sharing permissions are set to "Anyone with the link can view".*
* **Link to Dashboard:** (e.g., Tableau Public, etc.).
* **Link to Presentation:** A link to a short slide deck (PDF/PPT) AND (Optional) a 2-minute video walkthrough (YouTube) explaining your results.

### C. Technical Explanation
* Briefly explain how you handled the "Data Cleaning".
* Explain your "Candidate's Choice" addition.

**Important Note on Code Submission:**
* Upload your `.ipynb` notebook file to the repo.
* **Crucial:** Also upload an **HTML or PDF export** of your notebook so we can see your charts even if GitHub fails to render the notebook code.
* Once you are ready, please fill out the [Official Submission Form Here](https://forms.office.com/e/heitZ9PP7y) with your links

---

## 🛑 CRITICAL: Pre-Submission Checklist

**Before you submit your form, you MUST complete this checklist.**

### 1. Repository & Code Checks
- [x] **My GitHub Repo is Public.**
- [x] **I have uploaded the `.ipynb` notebook file.**
- [ ] **I have ALSO uploaded an HTML or PDF export** of the notebook. (User action required)
- [x] **I have NOT uploaded the massive raw dataset.**
- [x] **My code uses Relative Paths.** 

### 2. Deliverable Checks
- [ ] **My Dashboard link is publicly accessible.** (User action required)
- [ ] **My Presentation link is publicly accessible.** (User action required)
- [x] **I have updated this `README.md` file** with my Executive Summary and technical notes.

### 3. Completeness
- [x] I have completed **User Stories 1-4**.
- [x] I have completed the **"Candidate's Choice"** challenge and explained it in the README.

**✅ Only when you have checked every box above, proceed to the submission form.**

---

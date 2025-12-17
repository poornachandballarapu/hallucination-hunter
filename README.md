# ⚖️ Hallucination Hunter (Indian Law Edition)

### The Problem
Large Language Models (LLMs) like GPT-4 are trained primarily on US legal data. When asked to draft contracts for India, they often "hallucinate" by inserting:
1.  **US Terminology:** (e.g., "At-Will Employment" instead of "Retrenchment").
2.  **Repealed Statutes:** (e.g., Citing the "Factories Act, 1948" which was repealed by the OSH Code, 2020).

### The Solution
This Python tool acts as a "Jurisdiction Firewall." It scans contract drafts and:
* **Flags** non-compliant US terms.
* **Maps** them to the correct Indian statute (e.g., *Chapter 11* -> *IBC*).
* **Alerts** the user if they are citing dead laws (Post-Nov 2025 Labor Reforms).

### How It Works
The script uses Regex pattern matching against a curated legal dictionary to audit text in < 0.1 seconds, reducing the risk of "Jurisdiction Error" in high-volume legal operations.

### 👨‍💻 About the Developer
Built by **Poorna Chand Ballarapu**, a dual-degree student bridging the gap between Law and Technology.
* **Law:** 3rd Year B.A. LL.B (Hons) at **NALSAR University of Law**.
* **Tech:** B.S. in Data Science & Applications at **IIT Madras**.
* **Focus:** Leveraging Computational Law and NLP to automate complex legal workflows in M&A and Finance.

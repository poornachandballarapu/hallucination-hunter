import re

# --- CONFIGURATION: THE KNOWLEDGE BASE ---
# This dictionary maps "Bad Terms" (Keys) to "Correct Indian Terms" (Values)
# We use Regex patterns to catch variations (e.g., "401k" or "401(k)")

LEGAL_DICTIONARY = {
    # --- US vs INDIA JURISDICTION ERRORS ---
    r"attorney[- ]?client privilege": "Privileged Communication (Sec 132, Bharatiya Sakshya Adhiniyam, 2023)",
    r"attorney['’]?s? fees": "Costs of Litigation / Legal Costs",
    r"chapter 11": "CIRP (Corporate Insolvency Resolution Process under IBC)",
    r"class action": "Representative Suit (Order 1 Rule 8 CPC) or Sec 245 Companies Act",
    r"ein|ssn|tin": "PAN / GSTIN / TAN",
    r"at[- ]?will employment": "Fixed Term Employment (Industrial Relations Code, 2020) / Retrenchment",
    r"401\(?k\)?": "Provident Fund (Social Security Code, 2020)",
    r"common stock": "Equity Shares (Companies Act, 2013)",
    r"bylaws": "Articles of Association (AoA)",
    r"ucc filing": "Charge Registration (ROC) / Hypothecation",
    
    # --- "ZOMBIE" INDIAN ACTS (REPEALED IN NOV 2025) ---
    r"factories act": "❌ REPEALED: Use 'OSH Code, 2020'",
    r"industrial disputes act": "❌ REPEALED: Use 'Industrial Relations Code, 2020'",
    r"workmen['’]?s? compensation": "❌ REPEALED: Use 'Code on Social Security, 2020'",
    r"indian evidence act": "❌ REPEALED: Use 'Bharatiya Sakshya Adhiniyam, 2023'"
}

def hunt_hallucinations(contract_text):
    print("\n🔎 --- STARTING COMPLIANCE SCAN ---")
    issues_found = 0
    
    # Normalize text for checking (keep original for display)
    text_lower = contract_text.lower()
    
    for bad_term_pattern, correction in LEGAL_DICTIONARY.items():
        # Search for the pattern in the text
        matches = re.finditer(bad_term_pattern, text_lower)
        
        for match in matches:
            issues_found += 1
            # Get the exact text that was found in the document
            found_text = contract_text[match.start():match.end()]
            
            print(f"\n[🚩 FLAG #{issues_found}] Found: '{found_text}'")
            print(f"    ↳ SUGGESTION: {correction}")
            print(f"    ↳ REASON: Jurisdiction Mismatch or Repealed Statute.")

    if issues_found == 0:
        print("\n✅ CLEAN: No jurisdiction errors found.")
    else:
        print(f"\n⚠️ SCAN COMPLETE: {issues_found} potential risks identified.")

# --- MOCK INPUT (Paste a "Bad" Contract Clause Here) ---
# This simulates an AI drafting a contract with US terms and Old Indian Laws
dummy_contract = """
EMPLOYMENT AGREEMENT
1. The Employee is hired on an at-will employment basis.
2. The Company shall contribute to the Employee's 401(k) plan.
3. In case of disputes, the Attorney-client privilege shall apply as per the Indian Evidence Act, 1872.
4. Overtime shall be paid in accordance with the Factories Act, 1948.
"""

if __name__ == "__main__":
    hunt_hallucinations(dummy_contract)

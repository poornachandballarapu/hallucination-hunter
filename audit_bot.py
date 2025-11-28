import re

# --- 1. THE KNOWLEDGE BASE (EXPANDED) ---
LEGAL_DICTIONARY = {
    # --- JURISDICTION & DISPUTE RESOLUTION (CRITICAL FOR DUBAI) ---
    r"\bdiscovery\b": "Disclosure / Inspection of Documents (Civil Law/Indian Approach)",
    r"\bdeposition\b": "Cross-Examination / Interrogatories (Order 11 CPC)",
    r"\bamerican arbitration association\b": "SIAC / LCIA / DIAC (Dubai International Arbitration Centre)",
    r"\bclass action\b": "Representative Suit (Order 1 Rule 8 CPC)",
    r"\battorney[- ]?client privilege\b": "Privileged Communication (Sec 132 BSB, 2023)",
    r"\bpunitive damages\b": "Damages for Breach (Usually compensatory only in India/UK)",
    
    # --- CORPORATE & TAX ---
    r"\bchapter 11\b": "CIRP (Corporate Insolvency Resolution Process under IBC)",
    r"\bc[- ]?corp\b": "Private Limited Company / Public Limited Company",
    r"\bs[- ]?corp\b": "Not Applicable (US Tax Status)",
    r"\birs\b": "Income Tax Dept / Federal Tax Authority (FTA - if Dubai)",
    r"\b(ein|ssn|tin)\b": "PAN / GSTIN / TAN",
    r"\bcommon stock\b": "Equity Shares",
    r"\bpar value\b": "Face Value",
    r"\bstockholder\b": "Shareholder",
    
    # --- CONTRACTS & REAL ESTATE ---
    r"\bescrow agent\b": "Escrow Bank (Must be RBI/FEMA compliant)",
    r"\btitle insurance\b": "Title Search Report / Encumbrance Certificate",
    r"\bucc filing\b": "Charge Registration (ROC)",
    
    # --- LABOUR (THE NEW CODES) ---
    r"\bat[- ]?will employment\b": "Fixed Term Employment (Ind. Relations Code 2020)",
    r"\b401\(?k\)?\b": "Provident Fund (Social Security Code 2020)",
    r"\bfactories act\b": "❌ REPEALED: Use 'OSH Code, 2020'",
    r"\bindustrial disputes act\b": "❌ REPEALED: Use 'Industrial Relations Code, 2020'",
    r"\bindian evidence act\b": "❌ REPEALED: Use 'Bharatiya Sakshya Adhiniyam, 2023'"
}

# --- 2. THE LOGIC ENGINE (DATE CHECKER) ---
def check_date_format(text):
    issues = []
    # Regex to find dates like XX/XX/XXXX
    date_pattern = r"(\d{1,2})/(\d{1,2})/(\d{4})"
    matches = re.finditer(date_pattern, text)
    
    for match in matches:
        full_date = match.group(0)
        first_part = int(match.group(1))  # The MM or DD?
        second_part = int(match.group(2)) # The DD or MM?
        
        # LOGIC: If the second number is > 12, it MUST be US format (MM/DD/YYYY)
        # Because in India/UK (DD/MM/YYYY), the second number is the Month (max 12).
        if second_part > 12:
            issues.append(f"Found '{full_date}' -> Likely US Format (MM/DD/YYYY). Risk of billing error.")
            
    return issues

# --- 3. THE MAIN SCANNER ---
def hunt_hallucinations(contract_text):
    print("\n🔎 --- STARTING ADVANCED COMPLIANCE SCAN ---")
    issues_found = 0
    
    # A. Run Dictionary Scan
    text_lower = contract_text.lower()
    for bad_term_pattern, correction in LEGAL_DICTIONARY.items():
        matches = re.finditer(bad_term_pattern, text_lower)
        for match in matches:
            issues_found += 1
            found_text = contract_text[match.start():match.end()]
            print(f"\n[🚩 TERM FLAG] Found: '{found_text}'")
            print(f"    ↳ SUGGESTION: {correction}")

    # B. Run Logic Scan (Dates)
    date_issues = check_date_format(contract_text)
    for issue in date_issues:
        issues_found += 1
        print(f"\n[📅 LOGIC FLAG] {issue}")
        print(f"    ↳ SUGGESTION: Standardize to DD/MM/YYYY or write month names (e.g., 05-May-2025).")

    # C. Final Report
    if issues_found == 0:
        print("\n✅ CLEAN: No jurisdiction or logic errors found.")
    else:
        print(f"\n⚠️ SCAN COMPLETE: {issues_found} risks identified.")

# --- 4. EXECUTION ---
def load_and_scan():
    try:
        with open("contract.txt", "r", encoding="utf-8") as f:
            real_contract_text = f.read()
            hunt_hallucinations(real_contract_text)
    except FileNotFoundError:
        print("❌ ERROR: Could not find 'contract.txt'.")

if __name__ == "__main__":
    load_and_scan()

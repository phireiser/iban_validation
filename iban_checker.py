import re

# Source: www.tbg5-finance.org

# ------------------------------------------------------------------------------
# Data: Country IBAN definitions
#
#   length      (integer IBAN length)
#   structure   (e.g. "F04F04A12" – used to build a regular expression)
#   example     (an working example IBAN)
#   ibanreq     (IBAN requirement)
#   sepa        (is in SEPA)
#   regulation  (subject to EU Regulation 924/2009, 260/2012)
#   eur         (uses EUR)
#
# ------------------------------------------------------------------------------
COUNTRY_SPECS = {
    "AD": {"length": 24, "structure": "F04F04A12", "example": "AD1200012030200359100100", "ibanreq": False, "sepa": False, "regulation": False, "eur": False},
    "AE": {"length": 23, "structure": "F03F16",      "example": "AE070331234567890123456",    "ibanreq": False, "sepa": False, "regulation": False, "eur": False},
    "AL": {"length": 28, "structure": "F08A16",      "example": "AL47212110090000000235698741","ibanreq": False, "sepa": False, "regulation": False, "eur": False},
    "AT": {"length": 20, "structure": "F05F11",      "example": "AT611904300234573201",       "ibanreq": True, "sepa": True, "regulation": True, "eur": True},
    "AZ": {"length": 28, "structure": "U04A20",      "example": "AZ21NABZ00000000137010001944","ibanreq": False, "sepa": False, "regulation": False, "eur": False},
    "BA": {"length": 20, "structure": "F03F03F08F02","example": "BA391290079401028494",        "ibanreq": False, "sepa": False, "regulation": False, "eur": False},
    "BE": {"length": 16, "structure": "F03F07F02",   "example": "BE68539007547034",            "ibanreq": True, "sepa": True, "regulation": True, "eur": True},
    "BG": {"length": 22, "structure": "U04F04F02A08","example": "BG80BNBG96611020345678",      "ibanreq": True, "sepa": True, "regulation": True, "eur": False},
    "BH": {"length": 22, "structure": "U04A14",      "example": "BH67BMAG00001299123456",      "ibanreq": True, "sepa": False, "regulation": False, "eur": False},
    "BR": {"length": 29, "structure": "F08F05F10U01A01", "example": "BR9700360305000010009795493P1", "ibanreq": False, "sepa": False, "regulation": False, "eur": False},
    "CH": {"length": 21, "structure": "F05A12",      "example": "CH9300762011623852957",       "ibanreq": False, "sepa": True, "regulation": False, "eur": False},
    "CR": {"length": 22, "structure": "F04F14",      "example": "CR05015202001026284066",      "ibanreq": False, "sepa": False, "regulation": False, "eur": False},
    "CY": {"length": 28, "structure": "F03F05A16",   "example": "CY17002001280000001200527600","ibanreq": True, "sepa": True, "regulation": True, "eur": True},
    "CZ": {"length": 24, "structure": "F04F06F10",   "example": "CZ6508000000192000145399",    "ibanreq": True, "sepa": True, "regulation": True, "eur": False},
    "DE": {"length": 22, "structure": "F08F10",      "example": "DE89370400440532013000",      "ibanreq": True, "sepa": True, "regulation": True, "eur": True},
    "DK": {"length": 18, "structure": "F04F09F01",   "example": "DK5000400440116243",          "ibanreq": True, "sepa": True, "regulation": True, "eur": False},
    "DO": {"length": 28, "structure": "U04F20",      "example": "DO28BAGR00000001212453611324","ibanreq": False, "sepa": False, "regulation": False, "eur": False},
    "EE": {"length": 20, "structure": "F02F02F11F01","example": "EE382200221020145685",        "ibanreq": True, "sepa": True, "regulation": True, "eur": True},
    "ES": {"length": 24, "structure": "F04F04F01F01F10", "example": "ES9121000418450200051332",  "ibanreq": True, "sepa": True, "regulation": True, "eur": True},
    "FI": {"length": 18, "structure": "F06F07F01",   "example": "FI2112345600000785",          "ibanreq": True, "sepa": True, "regulation": True, "eur": True},
    "FO": {"length": 18, "structure": "F04F09F01",   "example": "FO6264600001631634",          "ibanreq": False, "sepa": True, "regulation": False, "eur": False},
    "FR": {"length": 27, "structure": "F05F05A11F02","example": "FR1420041010050500013M02606", "ibanreq": True, "sepa": True, "regulation": True, "eur": True},
    "GB": {"length": 22, "structure": "U04F06F08",   "example": "GB29NWBK60161331926819",       "ibanreq": True, "sepa": True, "regulation": True, "eur": False},
    "GE": {"length": 22, "structure": "U02F16",      "example": "GE29NB0000000101904917",       "ibanreq": False, "sepa": False, "regulation": False, "eur": False},
    "GI": {"length": 23, "structure": "U04A15",      "example": "GI75NWBK000000007099453",      "ibanreq": True, "sepa": True, "regulation": True, "eur": False},
    "GL": {"length": 18, "structure": "F04F09F01",   "example": "GL8964710001000206",          "ibanreq": False, "sepa": True, "regulation": False, "eur": False},
    "GR": {"length": 27, "structure": "F03F04A16",   "example": "GR1601101250000000012300695", "ibanreq": True, "sepa": True, "regulation": True, "eur": True},
    "GT": {"length": 28, "structure": "A04A20",      "example": "GT82TRAJ01020000001210029690","ibanreq": False, "sepa": False, "regulation": False, "eur": False},
    "HR": {"length": 21, "structure": "F07F10",      "example": "HR1210010051863000160",        "ibanreq": True, "sepa": True, "regulation": True, "eur": False},
    "HU": {"length": 28, "structure": "F03F04F01F15F01","example": "HU42117730161111101800000000","ibanreq": True,"sepa": True, "regulation": True, "eur": False},
    "IE": {"length": 22, "structure": "U04F06F08",   "example": "IE29AIBK93115212345678",       "ibanreq": True, "sepa": True, "regulation": True, "eur": True},
    "IL": {"length": 23, "structure": "F03F03F13",   "example": "IL620108000000099999999",      "ibanreq": False, "sepa": False, "regulation": False, "eur": False},
    "IS": {"length": 26, "structure": "F04F02F06F10","example": "IS140159260076545510730339",  "ibanreq": False, "sepa": True, "regulation": False, "eur": False},
    "IT": {"length": 27, "structure": "U01F05F05A12","example": "IT60X0542811101000000123456",  "ibanreq": True, "sepa": True, "regulation": True, "eur": True},
    "JO": {"length": 30, "structure": "U04F04A18",   "example": "JO94CBJO0010000000000131000302","ibanreq": True,"sepa": False, "regulation": False, "eur": False},
    "KW": {"length": 30, "structure": "U04A22",      "example": "KW81CBKU0000000000001234560101","ibanreq": True,"sepa": False, "regulation": False, "eur": False},
    "KZ": {"length": 20, "structure": "F03A13",      "example": "KZ86125KZT5004100100",         "ibanreq": False,"sepa": False, "regulation": False, "eur": False},
    "LB": {"length": 28, "structure": "F04A20",      "example": "LB62099900000001001901229114", "ibanreq": False,"sepa": False, "regulation": False, "eur": False},
    "LC": {"length": 32, "structure": "U04A24",      "example": "LC55HEMM000100010012001200023015","ibanreq":False,"sepa":False,"regulation":False,"eur":False},
    "LI": {"length": 21, "structure": "F05A12",      "example": "LI21088100002324013AA",        "ibanreq": True,"sepa": True, "regulation": True, "eur": False},
    "LT": {"length": 20, "structure": "F05F11",      "example": "LT121000011101001000",         "ibanreq": True,"sepa": True, "regulation": True, "eur": False},
    "LU": {"length": 20, "structure": "F03A13",      "example": "LU280019400644750000",         "ibanreq": True,"sepa": True, "regulation": True, "eur": True},
    "LV": {"length": 21, "structure": "U04A13",      "example": "LV80BANK0000435195001",        "ibanreq": True,"sepa": True, "regulation": True, "eur": False},
    "MC": {"length": 27, "structure": "F05F05A11F02","example": "MC5811222000010123456789030",  "ibanreq": False,"sepa": True, "regulation": False, "eur": False},
    "MD": {"length": 24, "structure": "A02A18",      "example": "MD24AG000225100013104168",     "ibanreq": False,"sepa": False, "regulation": False, "eur": False},
    "ME": {"length": 22, "structure": "F03F13F02",   "example": "ME25505000012345678951",       "ibanreq": False,"sepa": False, "regulation": False, "eur": False},
    "MK": {"length": 19, "structure": "F03A10F02",   "example": "MK07250120000058984",          "ibanreq": False,"sepa": False, "regulation": False, "eur": False},
    "MR": {"length": 27, "structure": "F05F05F11F02","example": "MR1300020001010000123456753",  "ibanreq": False,"sepa": False, "regulation": False, "eur": False},
    "MT": {"length": 31, "structure": "U04F05A18",   "example": "MT84MALT011000012345MTLCAST001S","ibanreq":True,"sepa":True,"regulation":True,"eur":True},
    "MU": {"length": 30, "structure": "U04F02F02F12F03U03","example": "MU17BOMM0101101030300200000MUR","ibanreq":False,"sepa":False,"regulation":False,"eur":False},
    "NL": {"length": 18, "structure": "U04F10",      "example": "NL91ABNA0417164300",           "ibanreq": True,"sepa": True, "regulation": True, "eur": True},
    "NO": {"length": 15, "structure": "F04F06F01",   "example": "NO9386011117947",              "ibanreq": False,"sepa": True, "regulation": False, "eur": False},
    "PK": {"length": 24, "structure": "U04A16",      "example": "PK36SCBL0000001123456702",     "ibanreq": False,"sepa": False, "regulation": False, "eur": False},
    "PL": {"length": 28, "structure": "F08F16",      "example": "PL61109010140000071219812874", "ibanreq": True,"sepa": True, "regulation": True, "eur": False},
    "PS": {"length": 29, "structure": "U04A21",      "example": "PS92PALS000000000400123456702","ibanreq": False,"sepa": False, "regulation": False, "eur": False},
    "PT": {"length": 25, "structure": "F04F04F11F02","example": "PT50000201231234567890154",    "ibanreq": True,"sepa": True, "regulation": True, "eur": True},
    "QA": {"length": 29, "structure": "U04A21",      "example": "QA58DOHB00001234567890ABCDEFG","ibanreq": True,"sepa": False, "regulation": False, "eur": False},
    "RO": {"length": 24, "structure": "U04A16",      "example": "RO49AAAA1B31007593840000",     "ibanreq": True,"sepa": True, "regulation": True, "eur": False},
    "RS": {"length": 22, "structure": "F03F13F02",   "example": "RS35260005601001611379",       "ibanreq": False,"sepa": False, "regulation": False, "eur": False},
    "SA": {"length": 24, "structure": "F02A18",      "example": "SA0380000000608010167519",     "ibanreq": True,"sepa": False, "regulation": False, "eur": False},
    "SC": {"length": 31, "structure": "U04F02F02F16U03","example": "SC18SSCB11010000000000001497USD","ibanreq":False,"sepa":False,"regulation":False,"eur":False},
    "SE": {"length": 24, "structure": "F03F16F01",   "example": "SE4550000000058398257466",     "ibanreq": True,"sepa": True, "regulation": True, "eur": False},
    "SI": {"length": 19, "structure": "F05F08F02",   "example": "SI56263300012039086",          "ibanreq": True,"sepa": True, "regulation": True, "eur": False},
    "SK": {"length": 24, "structure": "F04F06F10",   "example": "SK3112000000198742637541",     "ibanreq": True,"sepa": True, "regulation": True, "eur": True},
    "SM": {"length": 27, "structure": "U01F05F05A12","example": "SM86U0322509800000000270100",  "ibanreq": False,"sepa": True, "regulation": False, "eur": False},
    "ST": {"length": 25, "structure": "F08F11F02",   "example": "ST68000100010051845310112",    "ibanreq": False,"sepa": False, "regulation": False, "eur": False},
    "TL": {"length": 23, "structure": "F03F14F02",   "example": "TL380080012345678910157",      "ibanreq": False,"sepa": False, "regulation": False, "eur": False},
    "TN": {"length": 24, "structure": "F02F03F13F02","example": "TN5910006035183598478831",     "ibanreq": False,"sepa": False, "regulation": False, "eur": False},
    "TR": {"length": 26, "structure": "F05A01A16",   "example": "TR330006100519786457841326",   "ibanreq": True,"sepa": False, "regulation": False, "eur": False},
    "UA": {"length": 29, "structure": "F06A19",      "example": "UA213996220000026007233566001","ibanreq": False,"sepa": False, "regulation": False, "eur": False},
    "VG": {"length": 24, "structure": "U04F16",      "example": "VG96VPVG0000012345678901",     "ibanreq": False,"sepa": False, "regulation": False, "eur": False},
    "XK": {"length": 20, "structure": "F04F10F02",   "example": "XK051212012345678906",         "ibanreq": False,"sepa": False, "regulation": False, "eur": True}
}

def iso13616(iban: str) -> str:
    """
    Move the first 4 characters to the end of the string, then
    replace A-Z with digits 10 to 35 (A=10, B=11, ..., Z=35).
    """
    iban = iban.upper()
    # Move first 4 to the end
    rearranged = iban[4:] + iban[:4]
    # Replace letters with numbers
    result = []
    for ch in rearranged:
        if ch.isalpha():
            # Convert letter to digit: A->10, B->11, etc.
            val = ord(ch) - 55  # 'A' -> 10, 'B'->11 ...
            result.append(str(val))
        else:
            result.append(ch)
    return "".join(result)

def iso7064_mod97_10(iban_numeric: str) -> int:
    """
    Perform the mod-97 operation in chunks so we don't overflow
    on very large numbers.
    """
    remainder = 0
    # Process in chunks of up to 7 digits:
    for i in range(0, len(iban_numeric), 7):
        chunk = iban_numeric[i : i+7]
        # Combine with remainder from previous step
        number = int(str(remainder) + chunk)
        remainder = number % 97
    return remainder

def build_structure_pattern(structure: str) -> re.Pattern:
    """
    Convert the structure notation (e.g. 'F04F04A12') into a compiled regex
    that matches the exact length and character constraints.
    Characters used:
      A = 0-9A-Za-z
      B = 0-9A-Z
      C = A-Za-z
      F = 0-9
      L = a-z
      U = A-Z
      W = 0-9a-z
    Followed by a 2-digit count, e.g. 'F04' means 4 digits [0-9]{4}.
    """
    # Break into tokens like "F04", "F04", "A12", etc.
    tokens = re.findall(r'([ABCFLUW]\d{2})', structure)
    pattern_parts = []
    for token in tokens:
        char_type = token[0]      # 'F', 'A', etc.
        length_str = token[1:]    # e.g. "04", "12"
        length_val = int(length_str)

        # Determine the character set
        if char_type == "A":
            char_class = r"0-9A-Za-z"
        elif char_type == "B":
            char_class = r"0-9A-Z"
        elif char_type == "C":
            char_class = r"A-Za-z"
        elif char_type == "F":
            char_class = r"0-9"
        elif char_type == "L":
            char_class = r"a-z"
        elif char_type == "U":
            char_class = r"A-Z"
        elif char_type == "W":
            char_class = r"0-9a-z"
        else:
            # Fallback, though we don't expect other chars
            char_class = r"."

        pattern_parts.append(f"[{char_class}]{{{length_val}}}")

    pattern = "^" + "".join(pattern_parts) + "$"
    return re.compile(pattern)


def check_iban(iban: str, strict: bool = True) -> bool:
    """
    'strict' indicates whether to raise ValueError with explanations.
    If 'strict=False', it simply returns False on a bad IBAN (no error details).
    """
    # 1) Basic cleanup: remove spaces
    raw_iban = iban.replace(" ", "").replace("\t", "")
    
    # 2) Check for illegal chars (non-alphanumeric)
    if not re.match(r'^[0-9A-Za-z]+$', raw_iban):
        if strict:
            raise ValueError("IBAN contains illegal characters.")
        return False

    # 3) Must be at least 4 chars for the country code + 2 check digits
    if len(raw_iban) < 4:
        if strict:
            raise ValueError("IBAN is too short to contain CC + 2 check digits.")
        return False

    # 4) Country code:
    cc = raw_iban[0:2].upper()  # e.g. "DE"
    if not re.match(r'^[A-Za-z]{2}$', cc):
        if strict:
            raise ValueError("First two characters must be letters (country code).")
        return False

    # 5) Check digits
    check_digits = raw_iban[2:4]
    if not re.match(r'^[0-9]{2}$', check_digits):
        if strict:
            raise ValueError("Check digits must be numeric.")
        return False

    if check_digits in ["00", "01", "99"]:
        if strict:
            raise ValueError("Invalid check digits (00, 01, 99 not allowed).")
        return False

    # 6) Look up country definition if available
    spec = COUNTRY_SPECS.get(cc)
    if spec is None:
        if strict:
            raise ValueError(f"Unknown or unimplemented country code: {cc}")
        return False

    # 7) Check length
    needed_len = spec["length"]
    if len(raw_iban) != needed_len:
        if strict:
            raise ValueError(
                f"IBAN length {len(raw_iban)} does not match "
                f"required length {needed_len} for {cc}"
            )
        return False

    # 8) Check structure via regex
    pattern = build_structure_pattern(spec["structure"])
    if not pattern.match(raw_iban[4:]):  
        if strict:
            raise ValueError("IBAN fails country-specific structure check.")
        return False

    # 9) Perform the mod-97 check
    rearranged = iso13616(raw_iban)
    remainder = iso7064_mod97_10(rearranged)
    return (remainder == 1)


# ------------------------------------------------------------------------------
# Sample usage / test:
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Try a known valid IBAN (example from DE)
    test_iban = "DE89370400440532013000"
    is_valid = check_iban(test_iban)
    print(f"{test_iban} -> Valid? {is_valid}")

    # Try a known valid IBAN (example from ES)
    test_iban = "ES9121000418450200051332"
    try:
        valid = check_iban(test_iban)
        print(f"{test_iban} -> Valid? {valid}")
    except ValueError as e:
        print(f"Error: {e}")

    # Try an invalid IBAN
    bad_iban = "DE0012345678"
    try:
        valid = check_iban_core(bad_iban)
        print(f"{bad_iban} -> Valid? {valid}")
    except ValueError as e:
        print(f"Error: {e}")

import re

CONTRAST_WORDS = r"(?:but|however|although|though|yet)"

def smart_split(text: str):
    # 1. Split on punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)

    final = []
    for s in sentences:
        # 2. Split on contrast words
        parts = re.split(
            rf'\s+{CONTRAST_WORDS}\s+',
            s,
            flags=re.IGNORECASE
        )
        final.extend(parts)

    # 3. Cleanup: keep only meaningful text
    return [f.strip() for f in final if len(f.strip()) > 5]


print(smart_split("UI is good but OTP never comes"))
print(smart_split("App crashes after update. Payment failed however money deducted"))

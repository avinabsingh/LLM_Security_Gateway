import re
import unicodedata


class ObfuscationDetector:

    def __init__(self):

        # Leetspeak substitutions
        self.leet_map = {
            "0": "o",
            "3": "e",
            "4": "a",
            "5": "s",
            "7": "t",
            "$": "s",
            "@": "a",
        }

    # ---------------------------------------
    # Unicode anomaly detection
    # ---------------------------------------

    def unicode_anomaly_score(self, text):

        if not text:
            return 0.0

        suspicious = 0
        total = len(text)

        for char in text:

            if ord(char) <= 127:
                continue

            category = unicodedata.category(char)

            if category.startswith("L") or category.startswith("N"):
                suspicious += 1

        return suspicious / total

    # ---------------------------------------
    # Leetspeak detection
    # ---------------------------------------

    def leetspeak_score(self, text):

        if not text:
            return 0.0

        # Remove hexadecimal strings before checking leetspeak.
        cleaned_text = re.sub(
            r"\b0x[0-9a-fA-F]+\b",
            "",
            text
        )

        words = re.findall(
            r"[A-Za-z0-9@$]+",
            cleaned_text
        )

        if not words:
            return 0.0

        suspicious = 0
        total = 0

        for word in words:

            # Ignore pure numbers.
            if word.isdigit():
                continue

            for char in word:

                total += 1

                if char.lower() in self.leet_map:
                    suspicious += 1

        if total == 0:
            return 0.0

        return suspicious / total

    # ---------------------------------------
    # Suspicious symbol detection
    # ---------------------------------------

    def symbol_score(self, text):

        if not text:
            return 0.0

        suspicious_symbols = [
            "$",
            "@",
            "#",
            "%",
            "^",
            "&",
            "*",
            "~",
            "`"
        ]

        suspicious = sum(
            1
            for char in text
            if char in suspicious_symbols
        )

        return suspicious / len(text)

    # ---------------------------------------
    # Base64 detection
    # ---------------------------------------

    def base64_score(self, text):

        if not text:
            return 0.0

        import base64

        # Find candidate tokens.
        candidates = re.findall(
            r"(?<![A-Za-z0-9+/=])[A-Za-z0-9+/=]{16,}(?![A-Za-z0-9+/=])",
            text
        )

        for candidate in candidates:

            # Remove padding temporarily.
            raw = candidate.rstrip("=")

            # Base64 length must be compatible.
            if len(raw) % 4 == 1:
                continue

            # Ignore hexadecimal-looking strings.
            if re.fullmatch(
                r"(?:0x)?[0-9a-fA-F]+",
                raw
            ):
                continue

            # Require some Base64-like diversity.
            has_upper = bool(
                re.search(r"[A-Z]", raw)
            )

            has_lower = bool(
                re.search(r"[a-z]", raw)
            )

            has_digit_or_symbol = bool(
                re.search(r"[0-9+/]", raw)
            )

            # Purely alphabetic English-looking strings
            # are usually not Base64.
            if not (has_upper and has_lower):
                continue

            # Decode candidate.
            padded = raw + "=" * (
                (-len(raw)) % 4
            )

            try:

                decoded = base64.b64decode(
                    padded,
                    validate=True
                )

            except Exception:

                continue

            if not decoded:
                continue

            # Check whether decoded content is mostly printable.
            printable = sum(
                1
                for byte in decoded
                if 32 <= byte <= 126
                or byte in (9, 10, 13)
            )

            printable_ratio = (
                printable / len(decoded)
            )

            # Valid encoded natural text usually
            # produces a high printable ratio.
            if printable_ratio >= 0.80:

                return 1.0

        return 0.0

    # ---------------------------------------
    # Binary detection
    # ---------------------------------------

    def binary_score(self, text):

        if not text:
            return 0.0

        pattern = r"(?<![01])[01]{16,}(?![01])"

        if re.search(pattern, text):
            return 1.0

        return 0.0

    # ---------------------------------------
    # Hexadecimal detection
    # ---------------------------------------

    def hex_score(self, text):

        if not text:
            return 0.0

        # Binary strings are handled separately.
        binary_matches = re.findall(
            r"(?<![01])[01]{16,}(?![01])",
            text
        )

        cleaned_text = text

        for match in binary_matches:
            cleaned_text = cleaned_text.replace(
                match,
                ""
            )

        pattern = r"\b(?:0x)?[0-9a-fA-F]{16,}\b"

        if re.search(pattern, cleaned_text):
            return 1.0

        return 0.0

    # ---------------------------------------
    # Combined analysis
    # ---------------------------------------

    def analyze(self, text):

        unicode_score = self.unicode_anomaly_score(text)

        leet_score = self.leetspeak_score(text)

        symbol_score = self.symbol_score(text)

        base64_score = self.base64_score(text)

        binary_score = self.binary_score(text)

        hex_score = self.hex_score(text)

        overall_score = min(
            1.0,
            (
                unicode_score
                + leet_score
                + symbol_score
                + base64_score
                + binary_score
                + hex_score
            )
        )

        return {
            "unicode_anomaly": round(
                unicode_score,
                4
            ),

            "leetspeak": round(
                leet_score,
                4
            ),

            "symbol_substitution": round(
                symbol_score,
                4
            ),

            "base64": round(
                base64_score,
                4
            ),

            "binary": round(
                binary_score,
                4
            ),

            "hexadecimal": round(
                hex_score,
                4
            ),

            "obfuscation_score": round(
                overall_score,
                4
            )
        }
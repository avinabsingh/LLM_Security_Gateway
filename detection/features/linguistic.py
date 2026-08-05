import re


class LinguisticFeatures:

    def extract(self, prompt: str):

        words = prompt.split()

        features = {

            "char_length": len(prompt),

            "word_count": len(words),

            "question_marks": prompt.count("?"),

            "exclamation_marks": prompt.count("!"),

            "uppercase_letters": sum(c.isupper() for c in prompt),

            "digits": sum(c.isdigit() for c in prompt),

            "special_characters": len(
                re.findall(r"[^a-zA-Z0-9\s]", prompt)
            )

        }

        return features
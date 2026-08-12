from sentence_transformers import SentenceTransformer, util
from features.known_attacks import KNOWN_ATTACKS


class SemanticFeatures:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Model Loaded")

        # Encode known attacks only once
        print("Encoding known attacks...")

        self.attack_embeddings = self.model.encode(
            KNOWN_ATTACKS,
            convert_to_tensor=True
        )

        print("Known attack embeddings created")


    def embedding(self, prompt):

        return self.model.encode(prompt)


    def similarity(self, prompt1, prompt2):

        emb1 = self.model.encode(
            prompt1,
            convert_to_tensor=True
        )

        emb2 = self.model.encode(
            prompt2,
            convert_to_tensor=True
        )

        score = util.cos_sim(emb1, emb2)

        return float(score.item())


    def attack_similarity(self, prompt, top_k=3):

    # Encode incoming prompt only once
        prompt_embedding = self.model.encode(
            prompt,
            convert_to_tensor=True
        )

    # Compare prompt with all known attacks
        scores = util.cos_sim(
            prompt_embedding,
            self.attack_embeddings
        )[0]

        # Don't allow top_k to exceed number of attacks
        top_k = min(top_k, len(KNOWN_ATTACKS))

        # Get indices of highest scores
        top_results = scores.topk(k=top_k)

        matches = []

        for score, index in zip(
            top_results.values,
            top_results.indices
        ):

            matches.append({
                "attack": KNOWN_ATTACKS[index.item()],
                "score": score.item()
            })

        return {
            "top_score": matches[0]["score"],
            "nearest_attack": matches[0]["attack"],
            "matches": matches
        }
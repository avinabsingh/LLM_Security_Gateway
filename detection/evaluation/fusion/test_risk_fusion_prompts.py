import os
import sys

ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from inference.risk_fusion_engine import RiskFusionEngine
from evaluation.fusion.test_prompts import (
    BENIGN_PROMPTS,
    ATTACK_PROMPTS
)

engine = RiskFusionEngine(threshold=0.92)

print("\n" + "=" * 80)
print("BENIGN PROMPTS")
print("=" * 80)

for prompt in BENIGN_PROMPTS:

    result = engine.analyze(prompt)

    print(
        f"{result['attack_probability']:.4f}",
        result["decision"],
        "|",
        prompt
    )

print("\n" + "=" * 80)
print("ATTACK PROMPTS")
print("=" * 80)

for prompt in ATTACK_PROMPTS:

    result = engine.analyze(prompt)

    print(
        f"{result['attack_probability']:.4f}",
        result["decision"],
        "|",
        prompt
    )

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

y_true = []
y_pred = []

for prompt in BENIGN_PROMPTS:
    result = engine.analyze(prompt)

    y_true.append(0)
    y_pred.append(1 if result["decision"] == "BLOCK" else 0)

for prompt in ATTACK_PROMPTS:
    result = engine.analyze(prompt)

    y_true.append(1)
    y_pred.append(1 if result["decision"] == "BLOCK" else 0)

print("\n" + "=" * 80)
print("50 PROMPT TEST METRICS")
print("=" * 80)

print("Accuracy :", accuracy_score(y_true, y_pred))
print("Precision:", precision_score(y_true, y_pred))
print("Recall   :", recall_score(y_true, y_pred))
print("F1 Score :", f1_score(y_true, y_pred))

print("\nBenign ALLOW:", sum(1 for i in range(10) if y_pred[i] == 0))
print("Benign BLOCK:", sum(1 for i in range(10) if y_pred[i] == 1))

print("Attack ALLOW:", sum(1 for i in range(10, 50) if y_pred[i] == 0))
print("Attack BLOCK:", sum(1 for i in range(10, 50) if y_pred[i] == 1))
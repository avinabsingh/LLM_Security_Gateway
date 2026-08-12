import numpy as np

from feature_scaler import FeatureScaler


# ---------------------------------------
# Example feature vectors
# ---------------------------------------

X = np.array([

    [
        63, 9, 0, 0, 1, 0, 1,
        1, 0, 0, 1, 1, 0, 0, 0, 0, 0,
        0.77,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    ],

    [
        38, 6, 0, 0, 1, 0, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0.23,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    ],

    [
        39, 7, 0, 0, 0, 6, 7,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0.20,
        0.0256, 0.2, 0.0256, 0.0, 0.0, 0.0, 0.2513
    ]

])


# ---------------------------------------
# Scale
# ---------------------------------------

scaler = FeatureScaler()

X_scaled = scaler.fit_transform(X)


# ---------------------------------------
# Display
# ---------------------------------------

print("=" * 80)
print("FEATURE SCALING TEST")
print("=" * 80)

print("\nOriginal Shape:")
print(X.shape)

print("\nScaled Shape:")
print(X_scaled.shape)

print("\nScaled Features:")
print(X_scaled)
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import joblib

df = pd.read_csv("data/occupation_cluster_labels.csv")

X = df['occupation']
y = df['ched_cluster']

encoder = LabelEncoder()
X_enc = encoder.fit_transform(X)

model = DecisionTreeClassifier(max_depth=3)
model.fit(X_enc.reshape(-1,1), y)

joblib.dump(model, "models/occupation_model.pkl")
joblib.dump(encoder, "models/encoder.pkl")

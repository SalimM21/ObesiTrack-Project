import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
import joblib
import datetime, json

LABEL_MAP = {
    "Insufficient_Weight": 0, "Normal_Weight": 1,
    "Overweight_Level_I": 2, "Overweight_Level_II": 3,
    "Obesity_Type_I": 4, "Obesity_Type_II": 5, "Obesity_Type_III": 6,
}

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()

    # Calcul de l'IMC
    data['IMC']=data['Weight']/(data['Height']**2)

    data["NObeyesdad_num"] = data["NObeyesdad"].map(LABEL_MAP)

    # --- Colonnes finales ---
    columns_select = ["IMC", "Height", "Weight", "FCVC", "NObeyesdad_num"]

    return data[columns_select]

def best_model(df):
    pipeline=Pipeline([
            ('clf', GradientBoostingClassifier(random_state=42))
        ])
    params={
            'clf__n_estimators': [100, 200, 300],
            'clf__learning_rate': [0.01, 0.05, 0.1],
            'clf__max_depth': [3, 4, 5]
        }

    # Séparation X / y
    X = df.drop(columns=['NObeyesdad_num'])
    y = df['NObeyesdad_num']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    #gridsearch
    grid = GridSearchCV(
        pipeline,
        params,
        cv=3,              # validation croisée
        scoring='accuracy',
        n_jobs=-1,
        verbose=1
    )
    
    grid.fit(X_train, y_train)
    best_model = grid.best_estimator_
    y_pred = grid.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print('accuracy:', acc)

    joblib.dump(best_model, "ml/data/gradient_boosting_model.pkl")
    with open("ml/data/metrics.json", "w") as f:
        json.dump({
            "accuracy": float(acc),
            "date": datetime.date.today().isoformat(),
            "algo": best_model.named_steps["clf"].__class__.__name__,
            "train_size": len(X_train),
            "test_size": len(X_test),
            "classes": len(np.unique(y))
        }, f, indent=2)

    with open("ml/data/label_map.json", "w") as f:
        json.dump({v: k for k, v in LABEL_MAP.items()}, f)

    print("Modèle sauvegardé avec succès !")


data=pd.read_csv("C:\\Users\\lenovo\\Documents\\obesitrack\\ml\\data\\ObesityDataSet_raw_and_data_sinthetic.csv")
data.head()
df=preprocess(data)
best_model(df)
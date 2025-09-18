# analytics/predict.py

import sys, json, os
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer

try:
    import joblib
except ImportError:
    from sklearn.externals import joblib  # very old sklearn fallback

def log(*args):
    print(*args, file=sys.stderr)

# PHẢI trùng với tập feature khi train (optimized_model.pkl/optimized_scaler.pkl)
FEATURES = [
    'Year_Birth', 'Income', 'Kidhome', 'Teenhome', 'Recency',
    'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts',
    'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases',
    'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases',
    'NumWebVisitsMonth'
]

def norm_key(s: str) -> str:
    """Chuẩn hoá key: bỏ ký tự không chữ số/chữ cái + lower (để map camel/snake/case)."""
    return ''.join(ch.lower() for ch in str(s) if ch.isalnum())

def build_key_map():
    """Map từ key đã chuẩn hoá -> tên feature gốc (đúng case)."""
    return {norm_key(f): f for f in FEATURES}

def load_medians(base_dir: Path):
    """Ưu tiên file medians nếu có; nếu không, tính từ CSV; nếu vẫn không được thì 0."""
    medians = {f: 0.0 for f in FEATURES}
    med_path = base_dir / 'optimized_medians.json'
    if med_path.exists():
        try:
            medians.update({k: float(v) for k, v in json.loads(med_path.read_text()).items() if k in medians})
            return medians
        except Exception as e:
            log(f"[predict] Cannot read optimized_medians.json: {e}")

    # Tính median từ CSV như fallback
    csv_path = (base_dir / '..' / 'marketing_campaign.csv').resolve()
    if csv_path.exists():
        try:
            df = pd.read_csv(csv_path, sep='\t')
            for f in FEATURES:
                if f in df.columns and pd.api.types.is_numeric_dtype(df[f]):
                    try:
                        medians[f] = float(df[f].median())
                    except Exception:
                        pass
        except Exception as e:
            log(f"[predict] Cannot compute medians from CSV: {e}")

    return medians

def load_model_scaler(base_dir: Path):
    """Load model & scaler đã optimize."""
    model_path = (base_dir / '..' / 'optimized_model.pkl').resolve()
    scaler_path = (base_dir / '..' / 'optimized_scaler.pkl').resolve()

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

def normalize_payload(in_obj: dict, medians: dict):
    """
    - Map key input về đúng FEATURES (bất chấp case/camel/snake).
    - Ép float (nếu fail thì bỏ qua để điền median).
    - Điền median cho field thiếu.
    - Trả DataFrame 1 hàng theo đúng thứ tự FEATURES.
    """
    key_map = build_key_map()
    row = {}

    for k, v in (in_obj or {}).items():
        nk = norm_key(k)
        if nk in key_map:
            feat = key_map[nk]
            try:
                row[feat] = float(v)
            except Exception:
                # giữ nguyên để fill median sau
                pass

    # Điền median cho phần thiếu
    for f in FEATURES:
        if f not in row or row[f] is None or (isinstance(row[f], float) and np.isnan(row[f])):
            row[f] = float(medians.get(f, 0.0))

    X = pd.DataFrame([[row[f] for f in FEATURES]], columns=FEATURES)
    return X, row

def predict_customer(payload: dict, base_dir: Path):
    try:
        model, scaler = load_model_scaler(base_dir)
    except Exception as e:
        return {"status": "error", "message": f"Error loading model/scaler: {e}"}

    try:
        medians = load_medians(base_dir)
        X, normalized_row = normalize_payload(payload, medians)

        X_scaled = scaler.transform(X)

        y_pred = model.predict(X_scaled)
        pred = int(y_pred[0])

        proba = None
        if hasattr(model, "predict_proba"):
            try:
                proba = float(model.predict_proba(X_scaled)[0, 1])
            except Exception:
                proba = None

        return {
            "status": "success",
            "prediction": pred,
            "isPotential": bool(pred == 1),
            "probability": proba,
            "features_used": FEATURES,
            "input_normalized": normalized_row
        }
    except Exception as e:
        return {"status": "error", "message": f"Error during prediction: {e}"}

def main():
    base_dir = Path(__file__).resolve().parent

    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "Missing input JSON in argv[1]"}, ensure_ascii=False))
        return

    # Hỗ trợ cả dạng {data: {...}} hoặc {...}
    try:
        raw = json.loads(sys.argv[1])
        data = raw.get("data", raw) if isinstance(raw, dict) else {}
        if not isinstance(data, dict):
            raise ValueError("Input must be a JSON object of features.")
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Invalid JSON: {e}"}, ensure_ascii=False))
        return

    result = predict_customer(data, base_dir)
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()

import os

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score
from sklearn.model_selection import train_test_split


def train_model(n_estimators, max_depth, run_name):
    # 读取 DVC 追踪的 v2 数据
    df = pd.read_csv("data/heart.csv")
    X = df[["age", "resting_bp", "cholesterol"]]
    y = df["target"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 设置 MLflow 实验名称
    mlflow.set_experiment("HeartGuard_Production")
    
    with mlflow.start_run(run_name=run_name):
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        model.fit(X_train, y_train)
        
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        rec = recall_score(y_test, preds) # 医疗场景重点看召回率
        
        # 记录参数和指标
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("recall", rec)
        
        # 记录模型 (加上 skops 参数防报错)
        mlflow.sklearn.log_model(model, "model", skops_trusted_types=["sklearn.tree._tree.Tree"])
        print(f"✅ {run_name} 训练完成 - 准确率(Acc): {acc:.4f}, 召回率(Recall): {rec:.4f}")

if __name__ == "__main__":
    # 实验1：Baseline
    train_model(n_estimators=10, max_depth=3, run_name="Baseline_Model")
    
    # 实验2：Improved
    train_model(n_estimators=100, max_depth=10, run_name="Improved_Model_v2")
    
   
    print("📦 正在导出最终模型给同学 A...")
    final_df = pd.read_csv("data/heart.csv")
    X_final = final_df[["age", "resting_bp", "cholesterol"]]
    y_final = final_df["target"]
    
    final_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    final_model.fit(X_final, y_final)
    
    os.makedirs("app/models", exist_ok=True)
    joblib.dump(final_model, "app/models/model.pkl")
    print("✅ 模型已成功保存至 app/models/model.pkl")

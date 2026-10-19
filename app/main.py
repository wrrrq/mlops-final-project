import os

import joblib
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# 指向 B 同学生成的模型
MODEL_PATH = os.path.join("app", "models", "model.pkl")
model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)


# 数据校验（边界测试必备）
class PatientData(BaseModel):
    age: int = Field(..., ge=0, le=120, description="年龄")
    resting_bp: int = Field(..., ge=50, le=250, description="静息血压")
    cholesterol: int = Field(..., ge=100, le=500, description="胆固醇")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/api/predict")
def predict(data: PatientData):
    if model is None:
        return {"error": "Model not found"}

    features = [[data.age, data.resting_bp, data.cholesterol]]
    prediction = int(model.predict(features)[0])
    prob = float(model.predict_proba(features)[0][1])

    return {
        "prediction": "High Risk" if prediction == 1 else "Low Risk",
        "probability": prob,
    }

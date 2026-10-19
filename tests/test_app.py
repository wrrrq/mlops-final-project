from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# 测试1：正常数据，应该返回200和结果
def test_predict_valid_data():
    response = client.post(
        "/api/predict", json={"age": 55, "resting_bp": 120, "cholesterol": 200}
    )
    assert response.status_code == 200
    assert "prediction" in response.json()


# 测试2：无效年龄(负数)，应该被拦截返回422
def test_predict_invalid_age():
    response = client.post(
        "/api/predict", json={"age": -5, "resting_bp": 120, "cholesterol": 200}
    )
    assert response.status_code == 422


# 测试3：极端高风险数据，断言模型预测出 High Risk
def test_high_risk_patient():
    response = client.post(
        "/api/predict", json={"age": 80, "resting_bp": 180, "cholesterol": 300}
    )
    assert response.status_code == 200
    assert response.json()["prediction"] == "High Risk"

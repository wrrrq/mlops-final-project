import os

import numpy as np
import pandas as pd

np.random.seed(42)
n_samples = 500
data = {
    "age": np.random.randint(20, 80, n_samples),
    "resting_bp": np.random.randint(90, 180, n_samples),
    "cholesterol": np.random.randint(150, 300, n_samples),
}

df = pd.DataFrame(data)

df["target"] = ((df["age"] > 55) | (df["cholesterol"] > 240)).astype(int)

os.makedirs("data", exist_ok=True)
df.to_csv("data/heart.csv", index=False)
print("✅ 数据生成成功！已保存至 data/heart.csv")

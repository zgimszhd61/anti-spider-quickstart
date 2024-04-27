# 安装Faker库
!pip install faker

# 导入所需库
import pandas as pd
from faker import Faker
import numpy as np
from sklearn.ensemble import IsolationForest

# 初始化Faker生成器
fake = Faker()

# 生成模拟数据
def generate_data(num_samples):
    data = []
    for _ in range(num_samples):
        session = {
            "ip_address": fake.ipv4(),
            "session_duration": np.random.randint(1, 600),  # 会话持续时间，单位为秒
            "page_views": np.random.randint(1, 10),  # 页面查看次数
            "clicks": np.random.randint(1, 15)  # 点击次数
        }
        data.append(session)
    return pd.DataFrame(data)

# 生成1000个样本
data = generate_data(1000)
print(data.head())

# 初始化隔离森林模型
model = IsolationForest(n_estimators=100, contamination=0.05)

# 训练模型
model.fit(data[['session_duration', 'page_views', 'clicks']])

# 预测异常值
data['anomaly'] = model.predict(data[['session_duration', 'page_views', 'clicks']])
data['anomaly'] = data['anomaly'].map({1: 0, -1: 1})  # 将-1转换为1表示异常，1转换为0表示正常

# 显示可能的爬虫行为
print(data[data['anomaly'] == 1])

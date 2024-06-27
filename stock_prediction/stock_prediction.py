import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from tensorflow.keras.layers import LSTM, Dense # type: ignore
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.callbacks import EarlyStopping # type: ignore

# 獲取股價資料
df = yf.Ticker("2330.TW").history(period = "1y")
df = df.filter(["Close"])
df = df.rename(columns={"Close": "GT"})

# 查看圖表樣式
# print(plt.style.available)

# plt.style.use('seaborn-v0_8-darkgrid')
# plt.xlabel("Date")
# plt.ylabel("Price")
# plt.plot(df["GT"], linewidth = 1)
# plt.show()

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_prices = scaler.fit_transform(df.values)
# print(scaled_prices)

# 每預測新的一天是以前60天的點做標準化延伸
MOVING_WIN_SIZE = 60
all_x, all_y = [], []
for i in range(len(scaled_prices) - MOVING_WIN_SIZE):
    x = scaled_prices[i:i+MOVING_WIN_SIZE]
    y = scaled_prices[i+MOVING_WIN_SIZE]
    all_x.append(x)
    all_y.append(y)

all_x, all_y = np.array(all_x), np.array(all_y)
# print(all_x.shape)
# print(all_y.shape)
# print(df)

DS_SPLIT = 0.8
train_ds_size = round(all_x.shape[0] * DS_SPLIT)
train_x, train_y = all_x[:train_ds_size], all_y[:train_ds_size]
test_x, test_y = all_x[train_ds_size:], all_y[train_ds_size:]
# print(train_x.shape)
# print(train_y.shape)
# print(test_x.shape)
# print(test_y.shape)

# 調整資料形狀以符合LSTM層的輸入
train_x = np.reshape(train_x, (train_x.shape[0], train_x.shape[1], 1))
test_x = np.reshape(test_x, (test_x.shape[0], test_x.shape[1], 1))

model = Sequential()
model.add(LSTM(units = 50, return_sequences = True, input_shape = (train_x.shape[1], 1)))
model.add(LSTM(units = 50, return_sequences = False))
model.add(Dense(units = 25))
model.add(Dense(units = 1))
# print(model.summary())

model.compile(optimizer = "adam", loss = "mean_squared_error")

callback = EarlyStopping(monitor = "val_loss", patience = 10, restore_best_weights = True)
model.fit(train_x, train_y, 
          validation_split = 0.2, 
          callbacks = [callback], 
          epochs = 100)

# 預測完標準化數據
preds = model.predict(test_x)
# print(preds)

# 預測完標準化數據轉成正常數值
preds = scaler.inverse_transform(preds)
# print(preds)

train_df = df[:train_ds_size+MOVING_WIN_SIZE]
test_df = df[train_ds_size+MOVING_WIN_SIZE:]
test_df = test_df.assign(Predict = preds)

plt.style.use('seaborn-v0_8-darkgrid')
plt.xlabel("Date")
plt.ylabel("Price")
plt.plot(train_df["GT"], linewidth = 2)
plt.plot(test_df["GT"], linewidth = 2)
plt.plot(test_df["Predict"], linewidth = 1)
plt.legend(["Train", "GT", "Predict"])
plt.show()

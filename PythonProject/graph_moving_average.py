import pandas as pd
import matplotlib.pyplot as plt

def run():
    data = pd.read_csv("data/usdcad_data_moving_average.csv")
    plt.figure(figsize=(25,10))
    plt.plot(data["Close"], label="USD/CAD")
    plt.plot(data["MA5"], label="MA5")
    plt.plot(data["MA20"], label="MA20")

    buy_label = False
    sell_label = False

    for i in range(1, len(data)):
        if data["Signal"][i] == 1 and data["Signal"][i - 1] == 0:
            if buy_label==False:
                plt.scatter(i, data["Close"][i], marker="^", color="green", s=25, label="Buy")
                buy_label = True
            else:
                plt.scatter(i, data["Close"][i], marker="^", color="green", s=25)
        elif data["Signal"][i] == 0 and data["Signal"][i - 1] == 1:
            if sell_label==False:
                plt.scatter(i, data["Close"][i], marker="v", color="red", s=25, label="Sell")
                sell_label = True
            else:
                plt.scatter(i, data["Close"][i], marker="v", color="red", s=25)

    plt.title("USD/CAD with MA5 & MA20")
    plt.xlabel("Days")
    plt.ylabel("Exchange Rate")
    plt.legend()
    plt.savefig("outputs/price_ma.png", dpi=300)


if __name__ == "__main__":
    run()
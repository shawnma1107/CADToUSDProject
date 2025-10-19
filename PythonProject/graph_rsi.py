import pandas as pd
import matplotlib.pyplot as plt

def run():
    data = pd.read_csv("data/usdcad_data_rsi.csv")

    plt.figure(figsize=(30, 20))

    plt.subplot(2, 1, 1)
    plt.plot(data["Close"], label="USD/CAD")
    plt.title("USD/CAD")
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.legend()

    buy_label = False
    sell_label = False

    for i in range(1, len(data)):
        if data["Signal"][i] > data["Signal"][i - 1]:
            if buy_label == False:
                plt.scatter(i, data["Close"][i], marker="^", color="green", s=15, label="Buy")
                buy_label = True
            else:
                plt.scatter(i, data["Close"][i], marker="^", color="green", s=15, label="Buy")
        elif data["Signal"][i] < data["Signal"][i - 1]:
            if sell_label == False:
                plt.scatter(i, data["Close"][i], marker="v", color="red", s=15, label="Sell")
                sell_label = True
            else:
                plt.scatter(i, data["Close"][i], marker="v", color="red", s=15, label="Sell")


    plt.subplot(2, 1, 2)
    plt.plot(data["RSI"], label="RSI", color="orange")
    plt.title("RSI")
    plt.xlabel("Days")
    plt.ylabel("RSI")
    plt.legend()

    plt.savefig("outputs/price_rsi.png", dpi=300)


if __name__ == "__main__":
    run()
import pandas as pd
import matplotlib.pyplot as plt

def run():
    data = pd.read_csv("data/usdcad_data_moving_average.csv")

    plt.figure(figsize=(25,10))
    plt.plot(data["Equity"], label="Portfolio Value")
    plt.plot(data["Benchmark Portfolio"], label="Benchmark Portfolio Value")

    plt.title("Portfolio Value (Moving Average Strategy)")
    plt.xlabel("Days")
    plt.ylabel("Portfolio Value")
    plt.legend()
    plt.savefig("outputs/portfolio_value_moving_average.png", dpi=300)


if __name__ == "__main__":
    run()
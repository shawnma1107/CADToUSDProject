import pandas as pd
import math

def run():
    data = pd.read_csv("data/exchange_rate.csv", header=None, parse_dates=True, skiprows=3, names=["date", "Close"])

    # Make data into an arraylist
    prices = list(data['Close'].astype(float))

    five_day_mean = []
    twenty_day_mean = []

    # Find out Five day mean
    for i in range (len(prices)):
        if i >= 4:
            sum1 = 0.0
            for j in range (i-4, i+1):
                sum1 += prices[j]
            five_day_mean.append(sum1 / 5.0)
        else:
            five_day_mean.append(None)

    # Find out Twenty day mean
    for i in range (len(prices)):
        if i>= 19:
            sum2 = 0.0
            for j in range (i-19, i+1):
                sum2 += prices[j]
            twenty_day_mean.append(sum2 / 20.0)
        else:
            twenty_day_mean.append(None)

    # Make the signal to indicate if it should hold or not hold
    signal = [0]*len(prices)
    for i in range (len(prices)):
        if (five_day_mean[i] is not None) and (twenty_day_mean[i] is not None):
            if five_day_mean[i] > twenty_day_mean[i]:
                signal[i] = 0    # indicates have CAD
            else:
                signal[i] = 1    # indicates have USD

    # Make the actual decision according to the signal
    decision = [0] * len(prices)
    for i in range(1, len(prices)):
        decision[i] = signal[i-1]

    usd_in_cad_returns = [0.0] * len(prices)
    for i in range(1, len(prices)):
        usd_in_cad_returns[i] = (prices[i] / prices[i-1]) - 1.0

    strat_earnings_percentages = [0.0] * len(prices)
    for i in range(1, len(prices)):
        strat_earnings_percentages[i] = usd_in_cad_returns[i] * decision[i]

    money_started = 10000.0     #In CAD
    changing_capital = [0.0] * len(prices)
    changing_capital[0] = money_started
    for i in range(1, len(prices)):
        if decision[i] == 1:
            changing_capital[i] = changing_capital[i - 1] * (1.0 + usd_in_cad_returns[i])
        else:
            changing_capital[i] = changing_capital[i - 1]


    #Find the amount of money without applying the strategy
    equity_without_strategy = [0.0] * len(prices)
    for i in range (0, len(prices)):
        equity_without_strategy[i] = money_started / prices[0] * prices[i]

    #Save all data
    data["MA5"] = five_day_mean
    data["MA20"] = twenty_day_mean
    data["Signal"] = signal
    data["Decision"] = decision
    data["StratReturn"] = strat_earnings_percentages
    data["Equity"] = changing_capital
    data["Benchmark Portfolio"] = equity_without_strategy
    data.to_csv("data/usdcad_data_moving_average.csv", index=False)


    #Print the results
    profit = changing_capital[len(prices) - 1] - money_started
    percentage = profit / money_started
    print("Moving Average Strategy: ")
    print("Initial Capital: {:.2f} CAD" .format(money_started))
    print("Final Capital: {:.2f} CAD" .format(changing_capital[len(prices) - 1]))
    print("Benchmark Portfolio: {:.2f} CAD" .format(equity_without_strategy[len(prices)-1]))
    print("Total Profit: {:.2f} CAD" .format(profit))
    print("Total Return: {:.2f} %" .format(percentage*100))

    # Find the maximum drawdown
    max_drawdown = 0.0
    peak = changing_capital[0]
    for i in range(len(changing_capital)):
        if changing_capital[i] > peak:
            peak = changing_capital[i]
        drawdown = (peak - changing_capital[i]) / peak
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    print("Strategy Max Drawdown: {:.2f} %" .format(max_drawdown * 100))

    # Find the print Sharpe Ratio
    avg_day_return = sum(strat_earnings_percentages) / len(strat_earnings_percentages)
    sum_of_diff_squared = 0.0
    for i in range(len(strat_earnings_percentages)):
        diff = strat_earnings_percentages[i] - avg_day_return
        sum_of_diff_squared += diff ** 2
    std = math.sqrt(sum_of_diff_squared / len(strat_earnings_percentages))
    if std > 0:
        sharpe = (avg_day_return / std) * math.sqrt(252)
    else:
        sharpe = 0.0
    print("Sharpe Ratio: {:.2f} " .format(sharpe))

if __name__ == "__main__":
    run()
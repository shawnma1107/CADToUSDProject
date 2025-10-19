import pandas as pd
import math

def run():
    data = pd.read_csv("data/exchange_rate.csv", header=None, parse_dates=True, skiprows=3, names=["date", "Close"])

    # Make data into an arraylist
    prices = list(data['Close'].astype(float))

    # Find RSI from past 14 days
    RSI = [None] * len(prices)
    total_gain = 0.0
    total_loss = 0.0

    for i in range(14,len(prices)):
        total_gain = 0.0
        total_loss = 0.0
        for j in range(i - 13, i + 1):
            if prices[j]-prices[j - 1] > 0:
                total_gain += prices[j]-prices[j-1]
            elif prices[j]-prices[j - 1] < 0:
                total_loss += prices[j]-prices[j-1]
        average_gain = total_gain / 14
        average_loss = abs(total_loss) / 14
        if average_loss !=0:
            RS = average_gain/average_loss
        elif average_loss == 0:
            RS = pow(10,10)
        RSI[i] = 100 - 100 / (1+RS)


    # Make the signal to indicate how much it should hold
    position = [0.0] * len(prices)

    for i in range(len(prices)):
        r = RSI[i]
        if r is None:
            position[i] = 0.0
        else:
            if r < 30:
                position[i] = 1.0   # All USD
            elif r < 35:
                position[i] = 0.9
            elif r < 45:
                position[i] = 0.85
            elif r < 50:
                position[i] = 0.75
            elif r < 55:
                position[i] = 0.35
            elif r < 65:
                position[i] = 0.20
            elif r < 70:
                position[i] = 0.15
            else:
                position[i] = 0.0  # All CAD

    # Make the actual decision according to the signal
    decision = [0.0] * len(prices)
    for i in range(1, len(prices)):
        decision[i] = position[i-1]

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
        changing_capital[i] = changing_capital[i - 1] * (1.0 + strat_earnings_percentages[i])

    #Find the amount of money without applying the strategy
    equity_without_strategy = [0.0] * len(prices)
    for i in range (0, len(prices)):
        equity_without_strategy[i] = money_started / prices[0] * prices[i]

    # Save all data
    data["Signal"] = position
    data["Decision"] = decision
    data["StratReturn"] = strat_earnings_percentages
    data["RSI"] = RSI
    data["Equity"] = changing_capital
    data["Benchmark Portfolio"] = equity_without_strategy
    data.to_csv("data/usdcad_data_rsi.csv", index=False)


    #Print the results
    profit = changing_capital[len(prices) - 1] - money_started
    percentage = profit / money_started
    print("RSI Strategy: ")
    print("Initial Capital: {:.2f}" .format(money_started))
    print("Final Capital: {:.2f}" .format(changing_capital[len(prices) - 1]))
    print("Benchmark Portfolio: {:.2f}" .format(equity_without_strategy[len(prices)-1]))
    print("Total Profit: {:.2f}" .format(profit))
    print("Total Return: {:.2f}" .format(percentage*100), "%")

    # Find the maximum drawdown
    max_drawdown = 0.0
    peak = changing_capital[0]
    for i in range(len(changing_capital)):
        if changing_capital[i] > peak:
            peak = changing_capital[i]
        drawdown = (peak - changing_capital[i]) / peak
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    print("Strategy Max Drawdown: {:.2f} " .format(max_drawdown * 100), "%")

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
### initial_capital=10000
import matplotlib.pyplot as plt
import data_catch
import strategy_moving_average
import graph_moving_average
import portfolio_value_graph_moving_average
import strategy_rsi
import graph_rsi
import portfolio_value_graph_rsi

def main():
    data_catch.run()

    strategy_moving_average.run()
    print()
    strategy_rsi.run()

    graph_moving_average.run()
    portfolio_value_graph_moving_average.run()
    graph_rsi.run()
    portfolio_value_graph_rsi.run()
    plt.show()

if __name__ == "__main__":
    main()
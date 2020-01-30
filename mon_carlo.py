# needed for the next function
import subprocess
import importlib
import sys


# function that imports a library if it is installed, else installs it and then imports it
def getpack(package):
    try:
        return importlib.import_module(package)
    except ImportError:
        subprocess.call([sys.executable, "-m", "pip", "install", package],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return importlib.import_module(package)


# install/import other necessary modules
np = getpack("numpy")
pd = getpack("pandas")
matplotlib = getpack("matplotlib")
import matplotlib.pyplot as plt


def mon_sim(closing_prices, simulations, days=252):
    # dataframe for the results
    simulation_df = pd.DataFrame()
    # current price
    current_price = closing_prices.iloc[-1]
    # daily returns
    returns = closing_prices.pct_change()
    mu = returns.mean()
    daily_vol = returns.std()

    for x in range(0, simulations):
        price_sim = []
        price = current_price
        price_sim.append(price)

        for y in range(0, days):
            price = price * (1 + np.random.normal(mu, daily_vol))
            price_sim.append(price)

        simulation_df[x] = price_sim

    return simulation_df


def sim_plot(simulation_df, current_price, ticker):
    plt.title('Monte Carlo Simulation: ' + str(ticker))
    plt.plot(simulation_df)
    plt.axhline(y=current_price, color='r', linestyle='-')
    plt.xlabel('Day')
    plt.ylabel('Price')
    plt.margins(0)
    fig1 = plt.gcf()
    plt.show()

    return fig1

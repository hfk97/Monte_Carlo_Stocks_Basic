# needed for the next function
import subprocess
import importlib
import sys

# import monte carlo functions
import mon_carlo


# function that imports a library if it is installed, else installs it and then imports it
def getpack(package):
    try:
        return importlib.import_module(package)
    except ImportError:
        subprocess.call([sys.executable, "-m", "pip", "install", package],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return importlib.import_module(package)


datetime = getpack("datetime")
pd = getpack("pandas")


def main():
    ticker = "AAPL"

    # load stock returns
    AAPL_df = pd.read_csv("./AAPL.csv", index_col=0)
    AAPL_df['date'] = pd.to_datetime(AAPL_df['date'], format='%d/%m/%Y')

    closing_prices = AAPL_df.iloc[:, 2]

    # number of different Simulations
    simulations = 150

    # simulate one Trading year
    days = 252

    simulation_df = mon_carlo.mon_sim(closing_prices, simulations)

    mon_carlo.sim_plot(simulation_df, ticker).savefig("./AAPL_sim.png",dpi=300)


if __name__ == "__main__":
    main()

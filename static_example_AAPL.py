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

ticker = "AAPL"

# load stock returns
AAPL_df = pd.read_csv("./AAPL.csv", index_col=0)
AAPL_df['date'] = pd.to_datetime(AAPL_df['date'], format='%d/%m/%Y')

# current prices
current_price = AAPL_df.iloc[-1, 2]

closing_prices = AAPL_df.loc[:, 2]

# number of different Simulations
simulations = 500

# simulate one Trading year
days = 252

simulation_df = mon_carlo.mon_sim(closing_prices, simulations)

mon_carlo.sim_plot(simulation_df, current_price, ticker)

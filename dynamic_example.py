import subprocess
import sys
import importlib


# function that imports a library if it is installed, else installs it and then imports it
def getpack(package):
    try:
        return (importlib.import_module(package))
        # import package
    except ImportError:
        subprocess.call([sys.executable, "-m", "pip", "install", package])
        return (importlib.import_module(package))
        # import package


pd = getpack("pandas")
matplotlib = getpack("matplotlib")
plt = getpack("matplotlib.pyplot")
np=getpack("numpy")
datetime=getpack("datetime")

subprocess.call([sys.executable, "-m", "pip", "install", "pandas-datareader"])

from pandas_datareader import data

Ticker=input("Type in a valid ticker for the simulation and hit enter: ")
years=int(input("How many years do you want to consider for the return sample (e.g. 5): "))

#set start and end date for the last five years
now = datetime.datetime.now()

start_date = now.replace(year = now.year - years).strftime("%Y-%m-%d")
end_date = now.strftime("%Y-%m-%d")


# request data
closing_prices = data.DataReader(Ticker, 'yahoo', start_date, end_date)['Close']

#current price
current_price = closing_prices[-1]

#daily returns
returns = closing_prices.pct_change()


# Number of different Simulations
simulations = 1000

#Simulate one Trading year
days = 252


simulation_df = pd.DataFrame()

for x in range(0,simulations):
    count = 0
    daily_vol = returns.std()

    price_sim = []

    price = current_price * (1 + np.random.normal(0, daily_vol))
    price_sim.append(price)

    for y in range(0,days):
        price = price_sim[count] * (1 + np.random.normal(0, daily_vol))
        price_sim.append(price)
        count += 1

    simulation_df[x] = price_sim





plt.title('Monte Carlo Simulation: '+str(Ticker))
plt.plot(simulation_df)
plt.axhline(y=current_price, color='r', linestyle='-')
plt.xlabel('Day')
plt.ylabel('Price')
plt.show()

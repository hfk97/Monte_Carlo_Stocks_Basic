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


#load stock returns
AAPL_returns=pd.read_csv("./AAPL.csv",index_col=0)
AAPL_returns['date'] = pd.to_datetime(AAPL_returns['date'], format='%d/%m/%Y')

#Current prices
current_price=AAPL_returns.iloc[-1,2]

returns=AAPL_returns.loc[:,"RET"]

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





plt.title('Monte Carlo Simulation: AAPL')
plt.plot(simulation_df)
plt.axhline(y=current_price, color='r', linestyle='-')
plt.xlabel('Day')
plt.ylabel('Price')

plt.show()
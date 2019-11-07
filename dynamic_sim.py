import threading
import itertools
import time
import sys
import os

#this will later be used to add a loading ... to some text
done=False
def dotdotdot(text):
    for c in itertools.cycle(['.', '..', '...','']):
        if done:
            break
        sys.stdout.write('\r'+text+c)
        sys.stdout.flush()
        time.sleep(0.3)
    sys.stdout.write('\nDone!')


# prepare a loading message
t = threading.Thread(target=dotdotdot, args=("Loading required modules",))

# starting loading... thread
t.start()

#needed for the next function
import subprocess
import importlib

# function that imports a library if it is installed, else installs it and then imports it
def getpack(package):
    try:
        return (importlib.import_module(package))
        # import package
    except ImportError:
        subprocess.call([sys.executable, "-m", "pip", "install", package],
  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return (importlib.import_module(package))
        # import package

#install/import other necessary modules
pd = getpack("pandas")
matplotlib = getpack("matplotlib")
plt = getpack("matplotlib.pyplot")
np=getpack("numpy")
datetime=getpack("datetime")
subprocess.call([sys.executable, "-m", "pip", "install", "pandas-datareader"],
  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
from pandas_datareader import data


done=True
time.sleep(0.3)
print("\n")
end=""
while not "q" in end:

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
    simulations = int(input("Select the number of individual scenarios that you want to simulate: "))

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
    plt.margins(0)
    fig1=plt.gcf()
    plt.show()

    #saveimage and simdata
    if input("If you want to save this simulation data and the graph hit any key and enter, else just press enter: "):
        try:
            os.makedirs("./"+Ticker)
        except FileExistsError:
            pass
        os.makedirs("./" + Ticker+"/"+now.strftime('%m-%d-%Y-%m-%H'))
        with open("./"+Ticker+"/"+now.strftime('%m-%d-%Y-%m-%H')+"/"+"About.txt", "w") as text_file:
            text_file.write(f"This folder contains Monte Carlo simulation data and a visualisation of the respective simulations for the ticker {Ticker}."
                            f" In total {simulations} were run on the basis of the daily returns for the last {years}. The data was created on the {now.strftime('%m/%d/%Y')} at {now.strftime('%m:%H')}."
                            f" The results project the next trading year (i.e. 252 days).")
        simulation_df.to_csv("./"+Ticker+"/"+now.strftime("%m-%d-%Y-%m-%H")+"/"+"simdata.csv")
        fig1.savefig("./"+Ticker+"/"+now.strftime("%m-%d-%Y-%m-%H")+"/"+"visualisation.png", dpi=100)
        print("Data saved.")


    end+=(input("If you want to run another Simulation hit enter, else type q"))

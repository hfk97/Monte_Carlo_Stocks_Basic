# import custom module
import mon_carlo

# needed for the next function
import subprocess
import sys
import os
import importlib


# function that imports a library if it is installed, else installs it and then imports it
def getpack(package):
    try:
        return importlib.import_module(package)
    except ImportError:
        subprocess.call([sys.executable, "-m", "pip", "install", package],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return importlib.import_module(package)


datetime = getpack("datetime")
# install/import other necessary modules
subprocess.call([sys.executable, "-m", "pip", "install", "pandas-datareader"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

import pandas_datareader as data


def main():
    end = ""
    while "q" not in end:

        ticker = input("Type in a valid ticker for the simulation and hit enter: ")
        years = int(input("How many years do you want to consider for the return sample (e.g. 5): "))

        # set start and end date for the last five years
        now = datetime.datetime.now()

        start_date = now.replace(year=now.year - years).strftime("%Y-%m-%d")
        end_date = now.strftime("%Y-%m-%d")

        # request data
        closing_prices = data.DataReader(ticker, 'yahoo', start_date, end_date)['Close']

        # Number of different Simulations
        simulations = int(input("Select the number of individual scenarios that you want to simulate: "))

        # do monte carlo simulation (252 days is default)
        simulation_df = mon_carlo.mon_sim(closing_prices, simulations)

        # current price
        current_price = closing_prices[-1]
        # visualize
        fig1 = mon_carlo.sim_plot(simulation_df, current_price, ticker)

        # saveimage and simdata
        if input("If you want to save this simulation data and the graph hit any key and enter, else just press enter: "):

            try:
                os.makedirs(f"./{ticker}")
            except FileExistsError:
                pass
            os.makedirs(f"./{ticker}/{now.strftime('%m-%d-%Y-%m-%H')}")
            with open(f"./{ticker}/{now.strftime('%m-%d-%Y-%m-%H')}"+"About.txt", "w") as text_file:

                text_file.write(f"This folder contains Monte Carlo simulation data and a visualisation of the respective "
                                f"simulations for the ticker {ticker}.In total {simulations} were run on the basis of the "
                                f"daily returns for the last {years}. The data was created on the {now.strftime('%m/%d/%Y')}"
                                f" at {now.strftime('%m:%H')}.The results project the next trading year (i.e. 252 days).")

            simulation_df.to_csv(f"./{ticker}/{now.strftime('%m-%d-%Y-%m-%H')}/simdata.csv")
            fig1.savefig(f"./{ticker}/{now.strftime('%m-%d-%Y-%m-%H')}/visualisation.png", dpi=100)
            print("Data saved.")

        end += (input("If you want to run another Simulation hit enter, else type q: "))


if __name__ == "__main__":
    main()

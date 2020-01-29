# Basic Monte Carlo Simulation

<p align="center"><img src="./AAPL_sim.png" alt="Monte Carlo Example" title="Example Monte Carlo simulation (AAPL)" width="640" height="480" align="middle" /></p>

mon_carlo.py contains two functions. The first one runs a monte carlo simulation based on a list of closing prices, the number of simulations and, optionally, the number of days to simulate. The second function vizualizes monte carlo results.

"static_example_AAPL.py" runs a Monte Carlo simulation on the "AAPL.csv" return data within this repository and is meant as a proof of concept.

"dynamic_sim.py" allows the user to run a Monte Carlo simulations and gives him the freedom to make the following choices:

<ul>
<li>ticker</li>
<li>sample size in years</li>
<li>number of individual simulations</li>
<li>whether to export the data</li>
<li>run another query</li>
</ul>
</p>

All simulations are run for the following trading year, i.e. 252 days, this is easily modifiable.

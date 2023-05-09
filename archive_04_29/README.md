# Smart-Traffic
A repository for programs pertinent to the undergraduate project entitled "Smart Traffic"

This repository consists the following traffic simulation programs with their purposes described briefly as follows:

- `traci-mpc.py` is the main program for running the traffic simulation with the MPC-based traffic signal control scheme.
- `traci-no-mpc.py` is the main program for running the traffic simulation with the fixed-time traffic signal control scheme.
- `post_proc_results.py` is the main post processing program. To post process specific simulation runs, make sure to edit the directories in lines 340-343 in the `main()` function.
- `performance_indicators.py` contains functions for measuring various traffic parameters such as:

  - vehicle count
  - average queue time
  - average queue length
  - average flow rate
  - number of spawned vehicles
  - green times
  - cycle times

- `mpc.py` contains the formulation of the MPC algorithm using the `gurobipy` module.
- `mpc_params.py` contains the relevant traffic parameters that are used in `mpc.py` which include traffic constants, traffic simulation parameters, and traffic model matrices.
- `create_demand_mpc.py` is an intermediary program which reads the actual number of vehicles spawned in each time step in the simulation.
- `save_sim_results.py` contains the relevant functions for reading and writing traffic data measured from either `traci-mpc.py` or `traci-no-mpc.py` to a separate folder entitled `results\`
- `road_defs.py` contains the lane IDs of all incoming roads in the intersection. This is used by the `traci` programs to check where each vehicle in the simulation is located.
- `create_demand.py` is another intermediary program for parsing the reference route file `4-3-test-demand-vianetedit-ref.rou.xml` and for automating the generation of flow definitions to be used in duarouter.

### How to Properly Run the Programs

(1) Make sure to have the following program installed in your machine

- `sumo-gui`
- `netedit`

(2) Install the following Python modules:

- `gurobipy`
- `scipy`
- `numpy`
- `traci`
- `bs4` (BeautifulSoup)

(2) To run the traffic simulation program (i.e. `traci-mpc.py` or `traci-no-mpc.py`), enter the following command in the command line. 

```
python traci-mpc.py
```

(3) `sumo-gui` shoud launch after a few seconds. Click the play button found on the upper left portion of the `sumo-gui` user interface.

(4) Depending on the specifications of your machine, each simulation run may take 40 mins - 1 hr.

(5) After the simulation has completed, close `sumo-gui` and view the results stored in `results\test<number>` wherein number pertains to the nth simulation run performed.

(6) To visualize the results, you may plot the output of the simulation in `post_proc_results.py`. Refer to lines 340-343 and edit the directory names there corresponding to the simulation results that you want to plot.

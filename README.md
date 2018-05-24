# as1-final
Final project of the WASP AS I course on autonomous systems.

## What is this about?
This repository contains some code to to fly the [Crazyflie 2.0](https://www.bitcraze.io/crazyflie-2/) mini drone using a [local positioning system](https://www.bitcraze.io/loco-pos-system/).
The purpose of the project is to learn about and apply some control theory.

## What can this do?
With the code in this repository, we can control a Crazyflie 2.0 mini drone.

The height of the Crazyflie is controlled by a [PID controller](https://en.wikipedia.org/wiki/PID_controller).
The position in the horizontal plane is controlled by a [PD controller](https://en.wikipedia.org/wiki/PID_controller).
The rotation of the Crazyflie is kept constant with a [D controller](https://en.wikipedia.org/wiki/PID_controller).

For its movements, the Crazyflie assumes a static environment (the obstacles must be described) and plans its path such that it avoids the obstacles.

There project contains several parts:

### The main script
`cf_pc_control.py` is the main script.
It starts

* a web server that listens for commands for the Crazyflie
* a path planning server that allows the Crazyflie to plan a path in a (static) environment
* a control thread for the Crazyflie

### The web interface
`server.py` defines a web interface for the Crazyflie.
Commands to the Crazyflie are sent as JSON documents through `POST` requests to the web interface.
Currently, the following commands are accepted

The start command starts the Crazyflie and tells it to hover 30cm above its resting position.
```
{"command" : "start"}
```

The stop command tells the Crazyflie to stop its motors.
In most cases, this leads to a rather hard "landing".
```
{"command" : "stop"}
```

The distance command tells the Crazyflie to change its target position relative to its current target position.
x, y, and z must be given in meters and are understood as distances in the global reference frame.
For that, the Crazyflie calculates a path that avoids the obstacles in the environment.
However, if the target position lies within an obstacle, the Crazyflie *ignores* the command.
```
{"distance" : [x, y, z]}
```

### Path planning
The Crazyflie uses rather rudimentary path planning with [A*](https://en.wikipedia.org/wiki/A*_search_algorithm).
The bounds of the environment as well as the obstacles within the environment must be described and are assumed to be static.

Currently, obstacles are described as unit cubes which are then scaled and translated so they represent objects of the correct size and position in the environment.
(Rotation of objects is currently not possible but could be added easily.)

For example, an obstacle of size 1.6m x 0.8m x 2.2m that has its "origin" at position 1.25m x 1.7m on the floor can be modelled like so:
```
cube     = Cube()
scaled   = Scale(cube, 1.60, 0.8, 2.20)
obstacle = Translate(scaled, 1.25, 1.70, 0.00)
```

For path planning, the scene is discretised as a cartesian grid with cell size 0.1m x 0.1m x 0.1m.
There is no benefit in using smaller cells since the accuracy of the positioning system is limited.
For each grid cell, all obstacles are sampled to determine whether they are occupied.
The grid is then used to find the shortest path that avoids obstacles between two points using A*.

## How to get started?
First, clone the repository:
```
git clone git@github.com:chrisbloecker/as1-final.git
```

Then, `cd` into the folder and set up a virtual environment for python 3, activate the environment and install the dependencies:
```
cd as1-final
virtualenv -p python3 cfenv
source cfenv/bin/activate
pip install -r requirements.txt
```

Then, run `cf_pc_control.py` to start everything up.

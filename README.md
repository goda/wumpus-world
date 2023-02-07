# Assignment 1

This notebook is a brief summary, and instruction on how to run the current code and simulate the game as described in the Assignment 1 instructions.

## Requirements

To be able to run this assignment the following is required:

* Python 3.11+ (due to use of `Self` annotation for specifying a return of an instance of the same class)

## Instructions

The code can be run as a simulator, running a simulation of the game with the following default parameters (specified in `/wumpus/__main__.py`):

* Grid Size - 4x4
* Pit Probability - 0.2
* Allow Climb Without Gold - False

### Run Simulator

To run the simulator, simply open a terminal and navigate to the base folder, and run the following command:

`python -m wumpus`

If you want to show the board, and other useful information during each agent action/move:

`python -m wumpus -v`

### Run Unit Tests

Some basic unit tests were written during the development of the code. The tests can be found under:

`wumpus/src/tests/test.py`

The tests can be run using the command:

`python -m unittest wumpus/tests/test.py`

## Results

Here are some screenshots of running the code in few scenarios

### Scenario 1 - No Pits, Agent Climbs Out

Ran the code changing the pit probability to zero, and ran enough times until `NäiveAgent` was able to climb out of the cave with the gold included

![](images/scenario1.png)

### Scenario 2 - Pits, Agent Dies

Ran the code changing the pit probability to `0.2`, and ran until `NäiveAgent` dies

![](images/scenario2.png)

### Scenario 3 - Pits, Agent Climbs Out

Ran the code, keeping the pit probability to `0.2`, and ran until `NäiveAgent` grabs the gold and climbs out of the cave.

![](images/scenario3.png)
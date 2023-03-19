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

# Assignment 2

In this assignment, the game is played with `BeelineAgent` as per the rules and instructions laid out in Assignment 2. In short, the agent randomly picks an action, UNLESS it's at the gold location, or has the gold - at which point it reconstructs the quickest path back based on the previous steps taken.

## Results

Below are some successful game scenarios where the `BeelineAgent` is able to randomly find the gold, and then follow the quickest route/path out of the game

### Scenario 1 - Agent finds gold and follows exit path

```
Action:  TurnRight | Agent Orientation:  South
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|    |  G |    |    |
01|A   |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1

Action:  TurnLeft | Agent Orientation:  East
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|    |  G |    |    |
01|A   |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1

Action:  TurnLeft | Agent Orientation:  North
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|    |  G |    |    |
01|A   |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1

Action:  Forward | Agent Orientation:  North
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|A   |  G |    |    |
01|    |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1

Action:  TurnLeft | Agent Orientation:  West
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|A   |  G |    |    |
01|    |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1

Action:  TurnRight | Agent Orientation:  North
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|A   |  G |    |    |
01|    |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1

Action:  Shoot | Agent Orientation:  North
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|A   |  G |    |    |
01|    |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -11

Action:  TurnLeft | Agent Orientation:  West
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|A   |  G |    |    |
01|    |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1

Action:  Shoot | Agent Orientation:  West
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|A   |  G |    |    |
01|    |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1

Action:  TurnRight | Agent Orientation:  North
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|A   |  G |    |    |
01|    |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1

Action:  TurnRight | Agent Orientation:  East
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|A   |  G |    |    |
01|    |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1

Action:  TurnLeft | Agent Orientation:  North
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|A   |  G |    |    |
01|    |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1

Action:  TurnRight | Agent Orientation:  East
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|A   |  G |    |    |
01|    |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1

Action:  Forward | Agent Orientation:  East
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|    |A G |    |    |
01|    |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: True| Bump: False| Scream: False| Terminated: False| Reward: -1

Action:  Grab | Agent Orientation:  East
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|    |A G |    |    |
01|    |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: True| Bump: False| Scream: False| Terminated: False| Reward: -1

Action:  TurnLeft | Agent Orientation:  North
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|    |A G |    |    |
01|    |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: True| Bump: False| Scream: False| Terminated: False| Reward: -1

Action:  TurnLeft | Agent Orientation:  West
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|    |A G |    |    |
01|    |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: True| Bump: False| Scream: False| Terminated: False| Reward: -1

Action:  Forward | Agent Orientation:  West
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|A G |    |    |    |
01|    |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: True| Bump: False| Scream: False| Terminated: False| Reward: -1

Action:  TurnLeft | Agent Orientation:  South
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|A G |    |    |    |
01|    |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: True| Bump: False| Scream: False| Terminated: False| Reward: -1

Action:  Forward | Agent Orientation:  South
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|    |    |    |    |
01|A G |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: True| Bump: False| Scream: False| Terminated: False| Reward: -1

Action:  TurnRight | Agent Orientation:  West
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|    |    |    |    |
01|A G |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: True| Bump: False| Scream: False| Terminated: False| Reward: -1

Action:  Climb | Agent Orientation:  West
  ---------------------
04|    |    |   W| P  |
03|    |    |    |    |
02|    |    |    |    |
01|A G |    |    |    |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: True| Bump: False| Scream: False| Terminated: True| Reward: 999

Total reward:  968.0
```

### Scenario 2 - Agent finds gold, follows shorter exit path

In this scenario, the agent finds the gold and the optimal exit path chosen is the one that it took to get to the gold, except any unnecessary turns or other actions. It also figures out that it doesn't have to go the long way around to get to starting point, but can go from G location to starting point with few less steps. See example below:

```
Action:  Shoot | Agent Orientation:  East
  ---------------------
04|    |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|A   |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -11
Action:  TurnRight | Agent Orientation:  South
  ---------------------
04|    |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|A   |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnLeft | Agent Orientation:  East
  ---------------------
04|    |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|A   |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  East
  ---------------------
04|    |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|A   |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnLeft | Agent Orientation:  North
  ---------------------
04|    |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|A   |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  North
  ---------------------
04|    |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|A   |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Forward | Agent Orientation:  North
  ---------------------
04|    |    |    |    |
03|    |  G |    |   W|
02|A   |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Forward | Agent Orientation:  North
  ---------------------
04|    |    |    |    |
03|A   |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  North
  ---------------------
04|    |    |    |    |
03|A   |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Forward | Agent Orientation:  North
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  North
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  North
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Forward | Agent Orientation:  North
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: True| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  North
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  North
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Forward | Agent Orientation:  North
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: True| Scream: False| Terminated: False| Reward: -1
Action:  Forward | Agent Orientation:  North
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: True| Scream: False| Terminated: False| Reward: -1
Action:  Forward | Agent Orientation:  North
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: True| Scream: False| Terminated: False| Reward: -1
Action:  TurnRight | Agent Orientation:  East
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  East
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnLeft | Agent Orientation:  North
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnRight | Agent Orientation:  East
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Forward | Agent Orientation:  East
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  East
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  East
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  East
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnLeft | Agent Orientation:  North
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  North
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Forward | Agent Orientation:  North
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: True| Scream: False| Terminated: False| Reward: -1
Action:  TurnLeft | Agent Orientation:  West
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Forward | Agent Orientation:  West
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnRight | Agent Orientation:  North
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnLeft | Agent Orientation:  West
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnLeft | Agent Orientation:  South
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  South
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnRight | Agent Orientation:  West
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  West
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnLeft | Agent Orientation:  South
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnRight | Agent Orientation:  West
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnRight | Agent Orientation:  North
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  North
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Forward | Agent Orientation:  North
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: True| Scream: False| Terminated: False| Reward: -1
Action:  TurnRight | Agent Orientation:  East
  ---------------------
04|A   |    |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Forward | Agent Orientation:  East
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnLeft | Agent Orientation:  North
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Forward | Agent Orientation:  North
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: True| Scream: False| Terminated: False| Reward: -1
Action:  TurnRight | Agent Orientation:  East
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  East
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  East
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnLeft | Agent Orientation:  North
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  North
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  North
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnRight | Agent Orientation:  East
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  East
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Shoot | Agent Orientation:  East
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnRight | Agent Orientation:  South
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnRight | Agent Orientation:  West
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnRight | Agent Orientation:  North
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnLeft | Agent Orientation:  West
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnRight | Agent Orientation:  North
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnRight | Agent Orientation:  East
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnLeft | Agent Orientation:  North
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnRight | Agent Orientation:  East
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnRight | Agent Orientation:  South
  ---------------------
04|    |A   |    |    |
03|    |  G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: False| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Forward | Agent Orientation:  South
  ---------------------
04|    |    |    |    |
03|    |A G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: True| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Grab | Agent Orientation:  South
  ---------------------
04|    |    |    |    |
03|    |A G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: True| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnLeft | Agent Orientation:  East
  ---------------------
04|    |    |    |    |
03|    |A G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: True| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnLeft | Agent Orientation:  North
  ---------------------
04|    |    |    |    |
03|    |A G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: True| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnLeft | Agent Orientation:  West
  ---------------------
04|    |    |    |    |
03|    |A G |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: True| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Forward | Agent Orientation:  West
  ---------------------
04|    |    |    |    |
03|A G |    |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: True| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  TurnLeft | Agent Orientation:  South
  ---------------------
04|    |    |    |    |
03|A G |    |    |   W|
02|    |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: True| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Forward | Agent Orientation:  South
  ---------------------
04|    |    |    |    |
03|    |    |    |   W|
02|A G |    |    |    |
01|    |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: True| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Forward | Agent Orientation:  South
  ---------------------
04|    |    |    |    |
03|    |    |    |   W|
02|    |    |    |    |
01|A G |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: True| Bump: False| Scream: False| Terminated: False| Reward: -1
Action:  Climb | Agent Orientation:  South
  ---------------------
04|    |    |    |    |
03|    |    |    |   W|
02|    |    |    |    |
01|A G |    |    | P  |
  ---------------------
    01   02   03   04
| Stench: False| Breeze: False| Glitter: True| Bump: False| Scream: False| Terminated: True| Reward: 999
Total reward:  916.0
```

# Assignment 3

In this assignment, a new agent `ProbAgent` was developed that took a probabilistic view of the WumpusWorld before deciding what action to take, based on the percepts it received at each new location.

The agent calculates the risk/probability of dying in a given location in the Wumpus world by knowing the size of the world (i.e. 4x4 grid), and the probability of a pit at each location (except `(1,1)`), and that there is **one** wumpus present in one of the locations (except `(1,1)`).

The agent was programmed to only visit new locations in the grid, if the cumulative risk of dying (wumpus or pit present) is lower than a maximum risk threshold. Otherwise, the agent will try to visit already visited locations, if there were other unvisited locations along its visited path that had lower risk probability than the maximum threshold. 

Two max probability risk threshold were tested: `0.35`, and `0.2`. For each the game was simulated over 1000 episodes and the one with the higher total reward/score was picked

The agent max probability risk threshold was set at `0.2`, meaning it would only explore a new location if the perceived risk/probability of dying there is less than `0.2`. If the locations of pits and wumpus are such that the agent can't explore or get to the gold without going above this threshold, the agent will leave and head towards (1,1) and climb out after visiting each possible location 4 times.

## Results

As per the assignment, the game was run for 1000 episodes, and the total reward/score accumulated to see how well the agent did on average.

```
Episode:  001 , Total reward:  0-3.0
Episode:  002 , Total reward:  -53.0
Episode:  003 , Total reward:  908.0
Episode:  004 , Total reward:  862.0
Episode:  005 , Total reward:  1847.0
Episode:  006 , Total reward:  1824.0
Episode:  007 , Total reward:  1821.0
Episode:  008 , Total reward:  1818.0
Episode:  009 , Total reward:  1807.0
Episode:  010 , Total reward:  1796.0
Episode:  011 , Total reward:  1793.0
Episode:  012 , Total reward:  1747.0
Episode:  013 , Total reward:  2730.0
Episode:  014 , Total reward:  2702.0
Episode:  015 , Total reward:  3674.0
Episode:  016 , Total reward:  3614.0
Episode:  017 , Total reward:  3611.0
Episode:  018 , Total reward:  3541.0
Episode:  019 , Total reward:  3499.0
Episode:  020 , Total reward:  3488.0
Episode:  021 , Total reward:  4444.0
Episode:  022 , Total reward:  4441.0
Episode:  023 , Total reward:  4377.0
Episode:  024 , Total reward:  4366.0
Episode:  025 , Total reward:  4355.0
Episode:  026 , Total reward:  4352.0
Episode:  027 , Total reward:  4349.0
Episode:  028 , Total reward:  4326.0
Episode:  029 , Total reward:  4315.0
Episode:  030 , Total reward:  4312.0
Episode:  031 , Total reward:  4254.0
Episode:  032 , Total reward:  4251.0
Episode:  033 , Total reward:  4240.0
Episode:  034 , Total reward:  4229.0
Episode:  035 , Total reward:  4226.0
Episode:  036 , Total reward:  4223.0
Episode:  037 , Total reward:  4220.0
Episode:  038 , Total reward:  4217.0
Episode:  039 , Total reward:  4214.0
Episode:  040 , Total reward:  4211.0
Episode:  041 , Total reward:  5183.0
Episode:  042 , Total reward:  6153.0
Episode:  043 , Total reward:  6142.0
Episode:  044 , Total reward:  6115.0
Episode:  045 , Total reward:  6104.0
Episode:  046 , Total reward:  6101.0
Episode:  047 , Total reward:  6098.0
Episode:  048 , Total reward:  6095.0
Episode:  049 , Total reward:  6084.0
Episode:  050 , Total reward:  6081.0
Episode:  051 , Total reward:  6011.0
Episode:  052 , Total reward:  6978.0
Episode:  053 , Total reward:  6975.0
Episode:  054 , Total reward:  7931.0
Episode:  055 , Total reward:  7928.0
Episode:  056 , Total reward:  8889.0
Episode:  057 , Total reward:  8886.0
Episode:  058 , Total reward:  9824.0
Episode:  059 , Total reward:  9813.0
Episode:  060 , Total reward:  9810.0
Episode:  061 , Total reward:  10753.0
Episode:  062 , Total reward:  11727.0
Episode:  063 , Total reward:  11724.0
Episode:  064 , Total reward:  12709.0
Episode:  065 , Total reward:  12706.0
Episode:  066 , Total reward:  12666.0
Episode:  067 , Total reward:  13635.0
Episode:  068 , Total reward:  13632.0
Episode:  069 , Total reward:  13629.0
Episode:  070 , Total reward:  14612.0
Episode:  071 , Total reward:  14601.0
Episode:  072 , Total reward:  14533.0
Episode:  073 , Total reward:  14530.0
Episode:  074 , Total reward:  15513.0
Episode:  075 , Total reward:  15510.0
Episode:  076 , Total reward:  15499.0
Episode:  077 , Total reward:  15488.0
Episode:  078 , Total reward:  15477.0
Episode:  079 , Total reward:  15466.0
Episode:  080 , Total reward:  15444.0
Episode:  081 , Total reward:  15441.0
Episode:  082 , Total reward:  16401.0
Episode:  083 , Total reward:  16386.0
Episode:  084 , Total reward:  16383.0
Episode:  085 , Total reward:  17344.0
Episode:  086 , Total reward:  17294.0
Episode:  087 , Total reward:  17291.0
Episode:  088 , Total reward:  17269.0
Episode:  089 , Total reward:  18253.0
Episode:  090 , Total reward:  18213.0
Episode:  091 , Total reward:  18210.0
Episode:  092 , Total reward:  18199.0
Episode:  093 , Total reward:  18196.0
Episode:  094 , Total reward:  19164.0
Episode:  095 , Total reward:  19161.0
Episode:  096 , Total reward:  19130.0
Episode:  097 , Total reward:  19127.0
Episode:  098 , Total reward:  19124.0
Episode:  099 , Total reward:  19121.0
Episode:  100 , Total reward:  19118.0
Episode:  101 , Total reward:  19050.0
Episode:  102 , Total reward:  19004.0
Episode:  103 , Total reward:  19958.0
Episode:  104 , Total reward:  20941.0
Episode:  105 , Total reward:  20938.0
Episode:  106 , Total reward:  20927.0
Episode:  107 , Total reward:  20924.0
Episode:  108 , Total reward:  21889.0
Episode:  109 , Total reward:  22874.0
Episode:  110 , Total reward:  22871.0
Episode:  111 , Total reward:  23841.0
Episode:  112 , Total reward:  23838.0
Episode:  113 , Total reward:  23750.0
Episode:  114 , Total reward:  24708.0
Episode:  115 , Total reward:  24705.0
Episode:  116 , Total reward:  24678.0
Episode:  117 , Total reward:  24608.0
Episode:  118 , Total reward:  24583.0
Episode:  119 , Total reward:  25550.0
Episode:  120 , Total reward:  25547.0
Episode:  121 , Total reward:  26507.0
Episode:  122 , Total reward:  26504.0
Episode:  123 , Total reward:  26501.0
Episode:  124 , Total reward:  27430.0
Episode:  125 , Total reward:  27427.0
Episode:  126 , Total reward:  28365.0
Episode:  127 , Total reward:  29317.0
Episode:  128 , Total reward:  30282.0
Episode:  129 , Total reward:  30279.0
Episode:  130 , Total reward:  31253.0
Episode:  131 , Total reward:  31250.0
Episode:  132 , Total reward:  31247.0
Episode:  133 , Total reward:  31225.0
Episode:  134 , Total reward:  32203.0
Episode:  135 , Total reward:  32200.0
Episode:  136 , Total reward:  32189.0
Episode:  137 , Total reward:  33149.0
Episode:  138 , Total reward:  33138.0
Episode:  139 , Total reward:  33135.0
Episode:  140 , Total reward:  33132.0
Episode:  141 , Total reward:  33129.0
Episode:  142 , Total reward:  33118.0
Episode:  143 , Total reward:  33115.0
Episode:  144 , Total reward:  34080.0
Episode:  145 , Total reward:  34077.0
Episode:  146 , Total reward:  34066.0
Episode:  147 , Total reward:  35051.0
Episode:  148 , Total reward:  36011.0
Episode:  149 , Total reward:  36965.0
Episode:  150 , Total reward:  36948.0
Episode:  151 , Total reward:  37892.0
Episode:  152 , Total reward:  38875.0
Episode:  153 , Total reward:  38827.0
Episode:  154 , Total reward:  38757.0
Episode:  155 , Total reward:  38754.0
Episode:  156 , Total reward:  38716.0
Episode:  157 , Total reward:  38713.0
Episode:  158 , Total reward:  38702.0
Episode:  159 , Total reward:  38640.0
Episode:  160 , Total reward:  38594.0
Episode:  161 , Total reward:  38583.0
Episode:  162 , Total reward:  38521.0
Episode:  163 , Total reward:  38463.0
Episode:  164 , Total reward:  38407.0
Episode:  165 , Total reward:  38396.0
Episode:  166 , Total reward:  38393.0
Episode:  167 , Total reward:  39336.0
Episode:  168 , Total reward:  39333.0
Episode:  169 , Total reward:  39310.0
Episode:  170 , Total reward:  39299.0
Episode:  171 , Total reward:  39296.0
Episode:  172 , Total reward:  40253.0
Episode:  173 , Total reward:  40250.0
Episode:  174 , Total reward:  40247.0
Episode:  175 , Total reward:  40236.0
Episode:  176 , Total reward:  40233.0
Episode:  177 , Total reward:  41216.0
Episode:  178 , Total reward:  41205.0
Episode:  179 , Total reward:  41194.0
Episode:  180 , Total reward:  42167.0
Episode:  181 , Total reward:  43114.0
Episode:  182 , Total reward:  43103.0
Episode:  183 , Total reward:  43100.0
Episode:  184 , Total reward:  43048.0
Episode:  185 , Total reward:  43045.0
Episode:  186 , Total reward:  44015.0
Episode:  187 , Total reward:  44012.0
Episode:  188 , Total reward:  43986.0
Episode:  189 , Total reward:  43983.0
Episode:  190 , Total reward:  43980.0
Episode:  191 , Total reward:  43928.0
Episode:  192 , Total reward:  44898.0
Episode:  193 , Total reward:  44895.0
Episode:  194 , Total reward:  44892.0
Episode:  195 , Total reward:  44889.0
Episode:  196 , Total reward:  44878.0
Episode:  197 , Total reward:  44867.0
Episode:  198 , Total reward:  44864.0
Episode:  199 , Total reward:  44853.0
Episode:  200 , Total reward:  45836.0
Episode:  201 , Total reward:  45794.0
Episode:  202 , Total reward:  45783.0
Episode:  203 , Total reward:  45752.0
Episode:  204 , Total reward:  45749.0
Episode:  205 , Total reward:  45732.0
Episode:  206 , Total reward:  45678.0
Episode:  207 , Total reward:  45667.0
Episode:  208 , Total reward:  45664.0
Episode:  209 , Total reward:  45661.0
Episode:  210 , Total reward:  45658.0
Episode:  211 , Total reward:  46583.0
Episode:  212 , Total reward:  46572.0
Episode:  213 , Total reward:  47525.0
Episode:  214 , Total reward:  47495.0
Episode:  215 , Total reward:  47484.0
Episode:  216 , Total reward:  47481.0
Episode:  217 , Total reward:  47478.0
Episode:  218 , Total reward:  47467.0
Episode:  219 , Total reward:  48428.0
Episode:  220 , Total reward:  48425.0
Episode:  221 , Total reward:  48391.0
Episode:  222 , Total reward:  48388.0
Episode:  223 , Total reward:  49366.0
Episode:  224 , Total reward:  50318.0
Episode:  225 , Total reward:  50290.0
Episode:  226 , Total reward:  50268.0
Episode:  227 , Total reward:  51252.0
Episode:  228 , Total reward:  51202.0
Episode:  229 , Total reward:  51185.0
Episode:  230 , Total reward:  51182.0
Episode:  231 , Total reward:  51171.0
Episode:  232 , Total reward:  51156.0
Episode:  233 , Total reward:  51153.0
Episode:  234 , Total reward:  51150.0
Episode:  235 , Total reward:  51129.0
Episode:  236 , Total reward:  52065.0
Episode:  237 , Total reward:  53048.0
Episode:  238 , Total reward:  53037.0
Episode:  239 , Total reward:  52994.0
Episode:  240 , Total reward:  52952.0
Episode:  241 , Total reward:  52941.0
Episode:  242 , Total reward:  52889.0
Episode:  243 , Total reward:  52886.0
Episode:  244 , Total reward:  52883.0
Episode:  245 , Total reward:  52880.0
Episode:  246 , Total reward:  52877.0
Episode:  247 , Total reward:  52874.0
Episode:  248 , Total reward:  53846.0
Episode:  249 , Total reward:  53835.0
Episode:  250 , Total reward:  53832.0
Episode:  251 , Total reward:  53829.0
Episode:  252 , Total reward:  53779.0
Episode:  253 , Total reward:  54762.0
Episode:  254 , Total reward:  55725.0
Episode:  255 , Total reward:  55714.0
Episode:  256 , Total reward:  55711.0
Episode:  257 , Total reward:  55686.0
Episode:  258 , Total reward:  55683.0
Episode:  259 , Total reward:  55661.0
Episode:  260 , Total reward:  55650.0
Episode:  261 , Total reward:  56606.0
Episode:  262 , Total reward:  56603.0
Episode:  263 , Total reward:  56600.0
Episode:  264 , Total reward:  56597.0
Episode:  265 , Total reward:  56549.0
Episode:  266 , Total reward:  56522.0
Episode:  267 , Total reward:  56511.0
Episode:  268 , Total reward:  57483.0
Episode:  269 , Total reward:  57480.0
Episode:  270 , Total reward:  57454.0
Episode:  271 , Total reward:  57451.0
Episode:  272 , Total reward:  57448.0
Episode:  273 , Total reward:  57437.0
Episode:  274 , Total reward:  57426.0
Episode:  275 , Total reward:  57415.0
Episode:  276 , Total reward:  57404.0
Episode:  277 , Total reward:  57401.0
Episode:  278 , Total reward:  58385.0
Episode:  279 , Total reward:  59368.0
Episode:  280 , Total reward:  60332.0
Episode:  281 , Total reward:  60329.0
Episode:  282 , Total reward:  60326.0
Episode:  283 , Total reward:  60294.0
Episode:  284 , Total reward:  61252.0
Episode:  285 , Total reward:  62224.0
Episode:  286 , Total reward:  63179.0
Episode:  287 , Total reward:  64157.0
Episode:  288 , Total reward:  65142.0
Episode:  289 , Total reward:  65139.0
Episode:  290 , Total reward:  65128.0
Episode:  291 , Total reward:  65125.0
Episode:  292 , Total reward:  65122.0
Episode:  293 , Total reward:  65119.0
Episode:  294 , Total reward:  66056.0
Episode:  295 , Total reward:  67039.0
Episode:  296 , Total reward:  67969.0
Episode:  297 , Total reward:  67966.0
Episode:  298 , Total reward:  68925.0
Episode:  299 , Total reward:  68914.0
Episode:  300 , Total reward:  68911.0
Episode:  301 , Total reward:  69894.0
Episode:  302 , Total reward:  69868.0
Episode:  303 , Total reward:  70814.0
Episode:  304 , Total reward:  70803.0
Episode:  305 , Total reward:  70780.0
Episode:  306 , Total reward:  70752.0
Episode:  307 , Total reward:  70741.0
Episode:  308 , Total reward:  70718.0
Episode:  309 , Total reward:  70674.0
Episode:  310 , Total reward:  70671.0
Episode:  311 , Total reward:  71654.0
Episode:  312 , Total reward:  72639.0
Episode:  313 , Total reward:  72620.0
Episode:  314 , Total reward:  73580.0
Episode:  315 , Total reward:  74565.0
Episode:  316 , Total reward:  74542.0
Episode:  317 , Total reward:  75486.0
Episode:  318 , Total reward:  75483.0
Episode:  319 , Total reward:  75472.0
Episode:  320 , Total reward:  76443.0
Episode:  321 , Total reward:  76440.0
Episode:  322 , Total reward:  77425.0
Episode:  323 , Total reward:  78395.0
Episode:  324 , Total reward:  78392.0
Episode:  325 , Total reward:  79350.0
Episode:  326 , Total reward:  79302.0
Episode:  327 , Total reward:  79299.0
Episode:  328 , Total reward:  79296.0
Episode:  329 , Total reward:  79293.0
Episode:  330 , Total reward:  79282.0
Episode:  331 , Total reward:  79271.0
Episode:  332 , Total reward:  79225.0
Episode:  333 , Total reward:  80186.0
Episode:  334 , Total reward:  80183.0
Episode:  335 , Total reward:  81144.0
Episode:  336 , Total reward:  81141.0
Episode:  337 , Total reward:  81138.0
Episode:  338 , Total reward:  82092.0
Episode:  339 , Total reward:  83041.0
Episode:  340 , Total reward:  83038.0
Episode:  341 , Total reward:  83035.0
Episode:  342 , Total reward:  83971.0
Episode:  343 , Total reward:  83938.0
Episode:  344 , Total reward:  83935.0
Episode:  345 , Total reward:  84897.0
Episode:  346 , Total reward:  84894.0
Episode:  347 , Total reward:  85848.0
Episode:  348 , Total reward:  85845.0
Episode:  349 , Total reward:  85834.0
Episode:  350 , Total reward:  85823.0
Episode:  351 , Total reward:  85812.0
Episode:  352 , Total reward:  85809.0
Episode:  353 , Total reward:  86770.0
Episode:  354 , Total reward:  87733.0
Episode:  355 , Total reward:  88718.0
Episode:  356 , Total reward:  88682.0
Episode:  357 , Total reward:  88679.0
Episode:  358 , Total reward:  89663.0
Episode:  359 , Total reward:  89660.0
Episode:  360 , Total reward:  90630.0
Episode:  361 , Total reward:  90608.0
Episode:  362 , Total reward:  91561.0
Episode:  363 , Total reward:  91558.0
Episode:  364 , Total reward:  92536.0
Episode:  365 , Total reward:  92525.0
Episode:  366 , Total reward:  93503.0
Episode:  367 , Total reward:  93480.0
Episode:  368 , Total reward:  93477.0
Episode:  369 , Total reward:  93474.0
Episode:  370 , Total reward:  93463.0
Episode:  371 , Total reward:  93417.0
Episode:  372 , Total reward:  93414.0
Episode:  373 , Total reward:  93411.0
Episode:  374 , Total reward:  93408.0
Episode:  375 , Total reward:  93346.0
Episode:  376 , Total reward:  93343.0
Episode:  377 , Total reward:  93320.0
Episode:  378 , Total reward:  94305.0
Episode:  379 , Total reward:  94255.0
Episode:  380 , Total reward:  95237.0
Episode:  381 , Total reward:  96183.0
Episode:  382 , Total reward:  96172.0
Episode:  383 , Total reward:  96169.0
Episode:  384 , Total reward:  96166.0
Episode:  385 , Total reward:  96155.0
Episode:  386 , Total reward:  96152.0
Episode:  387 , Total reward:  96149.0
Episode:  388 , Total reward:  96138.0
Episode:  389 , Total reward:  96135.0
Episode:  390 , Total reward:  96095.0
Episode:  391 , Total reward:  96092.0
Episode:  392 , Total reward:  96089.0
Episode:  393 , Total reward:  96078.0
Episode:  394 , Total reward:  97011.0
Episode:  395 , Total reward:  96988.0
Episode:  396 , Total reward:  96977.0
Episode:  397 , Total reward:  96960.0
Episode:  398 , Total reward:  97899.0
Episode:  399 , Total reward:  97888.0
Episode:  400 , Total reward:  97877.0
Episode:  401 , Total reward:  97866.0
Episode:  402 , Total reward:  97806.0
Episode:  403 , Total reward:  98791.0
Episode:  404 , Total reward:  98788.0
Episode:  405 , Total reward:  99771.0
Episode:  406 , Total reward:  99756.0
Episode:  407 , Total reward:  99739.0
Episode:  408 , Total reward:  99736.0
Episode:  409 , Total reward:  100708.0
Episode:  410 , Total reward:  100705.0
Episode:  411 , Total reward:  101663.0
Episode:  412 , Total reward:  101611.0
Episode:  413 , Total reward:  101608.0
Episode:  414 , Total reward:  101566.0
Episode:  415 , Total reward:  101563.0
Episode:  416 , Total reward:  102536.0
Episode:  417 , Total reward:  102525.0
Episode:  418 , Total reward:  103486.0
Episode:  419 , Total reward:  104468.0
Episode:  420 , Total reward:  104465.0
Episode:  421 , Total reward:  104462.0
Episode:  422 , Total reward:  104414.0
Episode:  423 , Total reward:  105395.0
Episode:  424 , Total reward:  105347.0
Episode:  425 , Total reward:  105283.0
Episode:  426 , Total reward:  105227.0
Episode:  427 , Total reward:  105224.0
Episode:  428 , Total reward:  105221.0
Episode:  429 , Total reward:  105218.0
Episode:  430 , Total reward:  105207.0
Episode:  431 , Total reward:  105157.0
Episode:  432 , Total reward:  105146.0
Episode:  433 , Total reward:  106100.0
Episode:  434 , Total reward:  106062.0
Episode:  435 , Total reward:  107029.0
Episode:  436 , Total reward:  107994.0
Episode:  437 , Total reward:  107991.0
Episode:  438 , Total reward:  107988.0
Episode:  439 , Total reward:  107985.0
Episode:  440 , Total reward:  107982.0
Episode:  441 , Total reward:  108938.0
Episode:  442 , Total reward:  108935.0
Episode:  443 , Total reward:  108924.0
Episode:  444 , Total reward:  108921.0
Episode:  445 , Total reward:  108910.0
Episode:  446 , Total reward:  108854.0
Episode:  447 , Total reward:  109810.0
Episode:  448 , Total reward:  110756.0
Episode:  449 , Total reward:  110708.0
Episode:  450 , Total reward:  110705.0
Episode:  451 , Total reward:  110702.0
Episode:  452 , Total reward:  110646.0
Episode:  453 , Total reward:  110578.0
Episode:  454 , Total reward:  110500.0
Episode:  455 , Total reward:  110497.0
Episode:  456 , Total reward:  110486.0
Episode:  457 , Total reward:  110483.0
Episode:  458 , Total reward:  110472.0
Episode:  459 , Total reward:  110469.0
Episode:  460 , Total reward:  110466.0
Episode:  461 , Total reward:  110432.0
Episode:  462 , Total reward:  110429.0
Episode:  463 , Total reward:  110426.0
Episode:  464 , Total reward:  110423.0
Episode:  465 , Total reward:  110412.0
Episode:  466 , Total reward:  110409.0
Episode:  467 , Total reward:  110398.0
Episode:  468 , Total reward:  111361.0
Episode:  469 , Total reward:  112317.0
Episode:  470 , Total reward:  113260.0
Episode:  471 , Total reward:  113233.0
Episode:  472 , Total reward:  113230.0
Episode:  473 , Total reward:  113227.0
Episode:  474 , Total reward:  113216.0
Episode:  475 , Total reward:  113213.0
Episode:  476 , Total reward:  114171.0
Episode:  477 , Total reward:  115134.0
Episode:  478 , Total reward:  116117.0
Episode:  479 , Total reward:  116041.0
Episode:  480 , Total reward:  116038.0
Episode:  481 , Total reward:  117023.0
Episode:  482 , Total reward:  117020.0
Episode:  483 , Total reward:  117017.0
Episode:  484 , Total reward:  117989.0
Episode:  485 , Total reward:  117986.0
Episode:  486 , Total reward:  117983.0
Episode:  487 , Total reward:  117972.0
Episode:  488 , Total reward:  117918.0
Episode:  489 , Total reward:  117862.0
Episode:  490 , Total reward:  117859.0
Episode:  491 , Total reward:  118813.0
Episode:  492 , Total reward:  118791.0
Episode:  493 , Total reward:  119746.0
Episode:  494 , Total reward:  119692.0
Episode:  495 , Total reward:  119689.0
Episode:  496 , Total reward:  120672.0
Episode:  497 , Total reward:  121656.0
Episode:  498 , Total reward:  121610.0
Episode:  499 , Total reward:  122568.0
Episode:  500 , Total reward:  123523.0
Episode:  501 , Total reward:  123504.0
Episode:  502 , Total reward:  123501.0
Episode:  503 , Total reward:  123490.0
Episode:  504 , Total reward:  123479.0
Episode:  505 , Total reward:  123476.0
Episode:  506 , Total reward:  123459.0
Episode:  507 , Total reward:  124420.0
Episode:  508 , Total reward:  124417.0
Episode:  509 , Total reward:  124406.0
Episode:  510 , Total reward:  125373.0
Episode:  511 , Total reward:  125370.0
Episode:  512 , Total reward:  126355.0
Episode:  513 , Total reward:  126344.0
Episode:  514 , Total reward:  126322.0
Episode:  515 , Total reward:  126278.0
Episode:  516 , Total reward:  127204.0
Episode:  517 , Total reward:  127201.0
Episode:  518 , Total reward:  127198.0
Episode:  519 , Total reward:  127162.0
Episode:  520 , Total reward:  127159.0
Episode:  521 , Total reward:  128142.0
Episode:  522 , Total reward:  128131.0
Episode:  523 , Total reward:  129114.0
Episode:  524 , Total reward:  129084.0
Episode:  525 , Total reward:  130056.0
Episode:  526 , Total reward:  130053.0
Episode:  527 , Total reward:  130050.0
Episode:  528 , Total reward:  131021.0
Episode:  529 , Total reward:  131971.0
Episode:  530 , Total reward:  131968.0
Episode:  531 , Total reward:  131965.0
Episode:  532 , Total reward:  132943.0
Episode:  533 , Total reward:  132905.0
Episode:  534 , Total reward:  133868.0
Episode:  535 , Total reward:  133857.0
Episode:  536 , Total reward:  133854.0
Episode:  537 , Total reward:  133843.0
Episode:  538 , Total reward:  134826.0
Episode:  539 , Total reward:  134823.0
Episode:  540 , Total reward:  135772.0
Episode:  541 , Total reward:  136732.0
Episode:  542 , Total reward:  136729.0
Episode:  543 , Total reward:  136726.0
Episode:  544 , Total reward:  136709.0
Episode:  545 , Total reward:  136672.0
Episode:  546 , Total reward:  137639.0
Episode:  547 , Total reward:  137636.0
Episode:  548 , Total reward:  137633.0
Episode:  549 , Total reward:  138592.0
Episode:  550 , Total reward:  138589.0
Episode:  551 , Total reward:  138586.0
Episode:  552 , Total reward:  138583.0
Episode:  553 , Total reward:  139548.0
Episode:  554 , Total reward:  140508.0
Episode:  555 , Total reward:  141493.0
Episode:  556 , Total reward:  141447.0
Episode:  557 , Total reward:  141419.0
Episode:  558 , Total reward:  141416.0
Episode:  559 , Total reward:  142374.0
Episode:  560 , Total reward:  142371.0
Episode:  561 , Total reward:  143315.0
Episode:  562 , Total reward:  143304.0
Episode:  563 , Total reward:  143301.0
Episode:  564 , Total reward:  143298.0
Episode:  565 , Total reward:  143295.0
Episode:  566 , Total reward:  144279.0
Episode:  567 , Total reward:  144268.0
Episode:  568 , Total reward:  144265.0
Episode:  569 , Total reward:  145217.0
Episode:  570 , Total reward:  146173.0
Episode:  571 , Total reward:  146170.0
Episode:  572 , Total reward:  147153.0
Episode:  573 , Total reward:  148123.0
Episode:  574 , Total reward:  149060.0
Episode:  575 , Total reward:  150045.0
Episode:  576 , Total reward:  150042.0
Episode:  577 , Total reward:  150020.0
Episode:  578 , Total reward:  150017.0
Episode:  579 , Total reward:  150014.0
Episode:  580 , Total reward:  149983.0
Episode:  581 , Total reward:  149980.0
Episode:  582 , Total reward:  149938.0
Episode:  583 , Total reward:  149896.0
Episode:  584 , Total reward:  149893.0
Episode:  585 , Total reward:  149882.0
Episode:  586 , Total reward:  149879.0
Episode:  587 , Total reward:  149853.0
Episode:  588 , Total reward:  149850.0
Episode:  589 , Total reward:  149790.0
Episode:  590 , Total reward:  149742.0
Episode:  591 , Total reward:  149731.0
Episode:  592 , Total reward:  150703.0
Episode:  593 , Total reward:  150692.0
Episode:  594 , Total reward:  151659.0
Episode:  595 , Total reward:  151648.0
Episode:  596 , Total reward:  151637.0
Episode:  597 , Total reward:  151634.0
Episode:  598 , Total reward:  151619.0
Episode:  599 , Total reward:  151616.0
Episode:  600 , Total reward:  151586.0
Episode:  601 , Total reward:  151569.0
Episode:  602 , Total reward:  151521.0
Episode:  603 , Total reward:  152477.0
Episode:  604 , Total reward:  152474.0
Episode:  605 , Total reward:  153450.0
Episode:  606 , Total reward:  153447.0
Episode:  607 , Total reward:  154401.0
Episode:  608 , Total reward:  155386.0
Episode:  609 , Total reward:  155383.0
Episode:  610 , Total reward:  156348.0
Episode:  611 , Total reward:  156345.0
Episode:  612 , Total reward:  157323.0
Episode:  613 , Total reward:  158279.0
Episode:  614 , Total reward:  158276.0
Episode:  615 , Total reward:  158236.0
Episode:  616 , Total reward:  158198.0
Episode:  617 , Total reward:  158195.0
Episode:  618 , Total reward:  158184.0
Episode:  619 , Total reward:  158181.0
Episode:  620 , Total reward:  158170.0
Episode:  621 , Total reward:  158159.0
Episode:  622 , Total reward:  158156.0
Episode:  623 , Total reward:  159138.0
Episode:  624 , Total reward:  159127.0
Episode:  625 , Total reward:  160094.0
Episode:  626 , Total reward:  160091.0
Episode:  627 , Total reward:  160088.0
Episode:  628 , Total reward:  161071.0
Episode:  629 , Total reward:  162017.0
Episode:  630 , Total reward:  162987.0
Episode:  631 , Total reward:  162976.0
Episode:  632 , Total reward:  162973.0
Episode:  633 , Total reward:  162970.0
Episode:  634 , Total reward:  162967.0
Episode:  635 , Total reward:  162922.0
Episode:  636 , Total reward:  162919.0
Episode:  637 , Total reward:  163891.0
Episode:  638 , Total reward:  163888.0
Episode:  639 , Total reward:  163877.0
Episode:  640 , Total reward:  163866.0
Episode:  641 , Total reward:  163812.0
Episode:  642 , Total reward:  163782.0
Episode:  643 , Total reward:  164765.0
Episode:  644 , Total reward:  164748.0
Episode:  645 , Total reward:  164737.0
Episode:  646 , Total reward:  165704.0
Episode:  647 , Total reward:  165648.0
Episode:  648 , Total reward:  166613.0
Episode:  649 , Total reward:  167575.0
Episode:  650 , Total reward:  167572.0
Episode:  651 , Total reward:  167518.0
Episode:  652 , Total reward:  168475.0
Episode:  653 , Total reward:  168472.0
Episode:  654 , Total reward:  168450.0
Episode:  655 , Total reward:  168420.0
Episode:  656 , Total reward:  168417.0
Episode:  657 , Total reward:  168414.0
Episode:  658 , Total reward:  168411.0
Episode:  659 , Total reward:  168408.0
Episode:  660 , Total reward:  169393.0
Episode:  661 , Total reward:  169390.0
Episode:  662 , Total reward:  169373.0
Episode:  663 , Total reward:  169352.0
Episode:  664 , Total reward:  169349.0
Episode:  665 , Total reward:  169346.0
Episode:  666 , Total reward:  170299.0
Episode:  667 , Total reward:  170288.0
Episode:  668 , Total reward:  170285.0
Episode:  669 , Total reward:  170274.0
Episode:  670 , Total reward:  170271.0
Episode:  671 , Total reward:  171243.0
Episode:  672 , Total reward:  171232.0
Episode:  673 , Total reward:  171215.0
Episode:  674 , Total reward:  171204.0
Episode:  675 , Total reward:  171201.0
Episode:  676 , Total reward:  172138.0
Episode:  677 , Total reward:  172135.0
Episode:  678 , Total reward:  172113.0
Episode:  679 , Total reward:  172102.0
Episode:  680 , Total reward:  172091.0
Episode:  681 , Total reward:  173063.0
Episode:  682 , Total reward:  174036.0
Episode:  683 , Total reward:  174013.0
Episode:  684 , Total reward:  174982.0
Episode:  685 , Total reward:  174950.0
Episode:  686 , Total reward:  174947.0
Episode:  687 , Total reward:  174944.0
Episode:  688 , Total reward:  175909.0
Episode:  689 , Total reward:  175906.0
Episode:  690 , Total reward:  175870.0
Episode:  691 , Total reward:  175867.0
Episode:  692 , Total reward:  176793.0
Episode:  693 , Total reward:  177767.0
Episode:  694 , Total reward:  177756.0
Episode:  695 , Total reward:  177700.0
Episode:  696 , Total reward:  178643.0
Episode:  697 , Total reward:  178605.0
Episode:  698 , Total reward:  179561.0
Episode:  699 , Total reward:  179550.0
Episode:  700 , Total reward:  180524.0
Episode:  701 , Total reward:  181496.0
Episode:  702 , Total reward:  182440.0
Episode:  703 , Total reward:  182437.0
Episode:  704 , Total reward:  182434.0
Episode:  705 , Total reward:  183399.0
Episode:  706 , Total reward:  184350.0
Episode:  707 , Total reward:  185319.0
Episode:  708 , Total reward:  185289.0
Episode:  709 , Total reward:  186259.0
Episode:  710 , Total reward:  186256.0
Episode:  711 , Total reward:  187179.0
Episode:  712 , Total reward:  187157.0
Episode:  713 , Total reward:  188141.0
Episode:  714 , Total reward:  189099.0
Episode:  715 , Total reward:  189096.0
Episode:  716 , Total reward:  189093.0
Episode:  717 , Total reward:  189065.0
Episode:  718 , Total reward:  189062.0
Episode:  719 , Total reward:  190020.0
Episode:  720 , Total reward:  189997.0
Episode:  721 , Total reward:  190980.0
Episode:  722 , Total reward:  190977.0
Episode:  723 , Total reward:  190931.0
Episode:  724 , Total reward:  190928.0
Episode:  725 , Total reward:  190891.0
Episode:  726 , Total reward:  190888.0
Episode:  727 , Total reward:  190885.0
Episode:  728 , Total reward:  190874.0
Episode:  729 , Total reward:  190818.0
Episode:  730 , Total reward:  191803.0
Episode:  731 , Total reward:  191792.0
Episode:  732 , Total reward:  191777.0
Episode:  733 , Total reward:  191774.0
Episode:  734 , Total reward:  191763.0
Episode:  735 , Total reward:  192733.0
Episode:  736 , Total reward:  193718.0
Episode:  737 , Total reward:  193680.0
Episode:  738 , Total reward:  193677.0
Episode:  739 , Total reward:  193674.0
Episode:  740 , Total reward:  193671.0
Episode:  741 , Total reward:  193668.0
Episode:  742 , Total reward:  193622.0
Episode:  743 , Total reward:  194593.0
Episode:  744 , Total reward:  194582.0
Episode:  745 , Total reward:  194565.0
Episode:  746 , Total reward:  194554.0
Episode:  747 , Total reward:  194551.0
Episode:  748 , Total reward:  195535.0
Episode:  749 , Total reward:  195532.0
Episode:  750 , Total reward:  195529.0
Episode:  751 , Total reward:  195526.0
Episode:  752 , Total reward:  195454.0
Episode:  753 , Total reward:  195437.0
Episode:  754 , Total reward:  195385.0
Episode:  755 , Total reward:  196350.0
Episode:  756 , Total reward:  196328.0
Episode:  757 , Total reward:  196325.0
Episode:  758 , Total reward:  196322.0
Episode:  759 , Total reward:  196286.0
Episode:  760 , Total reward:  196283.0
Episode:  761 , Total reward:  197229.0
Episode:  762 , Total reward:  197214.0
Episode:  763 , Total reward:  197211.0
Episode:  764 , Total reward:  198194.0
Episode:  765 , Total reward:  198183.0
Episode:  766 , Total reward:  198121.0
Episode:  767 , Total reward:  199082.0
Episode:  768 , Total reward:  200048.0
Episode:  769 , Total reward:  201018.0
Episode:  770 , Total reward:  201007.0
Episode:  771 , Total reward:  201004.0
Episode:  772 , Total reward:  201954.0
Episode:  773 , Total reward:  201910.0
Episode:  774 , Total reward:  202868.0
Episode:  775 , Total reward:  202824.0
Episode:  776 , Total reward:  202821.0
Episode:  777 , Total reward:  203784.0
Episode:  778 , Total reward:  204746.0
Episode:  779 , Total reward:  205719.0
Episode:  780 , Total reward:  206665.0
Episode:  781 , Total reward:  206662.0
Episode:  782 , Total reward:  206651.0
Episode:  783 , Total reward:  206613.0
Episode:  784 , Total reward:  206610.0
Episode:  785 , Total reward:  206607.0
Episode:  786 , Total reward:  206590.0
Episode:  787 , Total reward:  206587.0
Episode:  788 , Total reward:  206584.0
Episode:  789 , Total reward:  206567.0
Episode:  790 , Total reward:  207550.0
Episode:  791 , Total reward:  207527.0
Episode:  792 , Total reward:  207516.0
Episode:  793 , Total reward:  207454.0
Episode:  794 , Total reward:  207443.0
Episode:  795 , Total reward:  207440.0
Episode:  796 , Total reward:  207390.0
Episode:  797 , Total reward:  207350.0
Episode:  798 , Total reward:  207314.0
Episode:  799 , Total reward:  207311.0
Episode:  800 , Total reward:  207308.0
Episode:  801 , Total reward:  207305.0
Episode:  802 , Total reward:  208233.0
Episode:  803 , Total reward:  208230.0
Episode:  804 , Total reward:  208219.0
Episode:  805 , Total reward:  208216.0
Episode:  806 , Total reward:  208162.0
Episode:  807 , Total reward:  208159.0
Episode:  808 , Total reward:  208148.0
Episode:  809 , Total reward:  209120.0
Episode:  810 , Total reward:  209064.0
Episode:  811 , Total reward:  209061.0
Episode:  812 , Total reward:  209044.0
Episode:  813 , Total reward:  209041.0
Episode:  814 , Total reward:  210007.0
Episode:  815 , Total reward:  209990.0
Episode:  816 , Total reward:  209944.0
Episode:  817 , Total reward:  210890.0
Episode:  818 , Total reward:  211875.0
Episode:  819 , Total reward:  211856.0
Episode:  820 , Total reward:  211845.0
Episode:  821 , Total reward:  212810.0
Episode:  822 , Total reward:  212788.0
Episode:  823 , Total reward:  213773.0
Episode:  824 , Total reward:  213770.0
Episode:  825 , Total reward:  213767.0
Episode:  826 , Total reward:  213752.0
Episode:  827 , Total reward:  213749.0
Episode:  828 , Total reward:  213746.0
Episode:  829 , Total reward:  213690.0
Episode:  830 , Total reward:  214673.0
Episode:  831 , Total reward:  214662.0
Episode:  832 , Total reward:  214647.0
Episode:  833 , Total reward:  214571.0
Episode:  834 , Total reward:  214568.0
Episode:  835 , Total reward:  215551.0
Episode:  836 , Total reward:  216493.0
Episode:  837 , Total reward:  216490.0
Episode:  838 , Total reward:  216487.0
Episode:  839 , Total reward:  216444.0
Episode:  840 , Total reward:  217407.0
Episode:  841 , Total reward:  217404.0
Episode:  842 , Total reward:  218376.0
Episode:  843 , Total reward:  218365.0
Episode:  844 , Total reward:  219314.0
Episode:  845 , Total reward:  220272.0
Episode:  846 , Total reward:  221255.0
Episode:  847 , Total reward:  222216.0
Episode:  848 , Total reward:  223181.0
Episode:  849 , Total reward:  223178.0
Episode:  850 , Total reward:  223104.0
Episode:  851 , Total reward:  223082.0
Episode:  852 , Total reward:  224067.0
Episode:  853 , Total reward:  224064.0
Episode:  854 , Total reward:  224053.0
Episode:  855 , Total reward:  224050.0
Episode:  856 , Total reward:  225013.0
Episode:  857 , Total reward:  225982.0
Episode:  858 , Total reward:  226965.0
Episode:  859 , Total reward:  226935.0
Episode:  860 , Total reward:  226895.0
Episode:  861 , Total reward:  227860.0
Episode:  862 , Total reward:  228818.0
Episode:  863 , Total reward:  228815.0
Episode:  864 , Total reward:  228775.0
Episode:  865 , Total reward:  228772.0
Episode:  866 , Total reward:  229742.0
Episode:  867 , Total reward:  230685.0
Episode:  868 , Total reward:  230682.0
Episode:  869 , Total reward:  230653.0
Episode:  870 , Total reward:  231625.0
Episode:  871 , Total reward:  231602.0
Episode:  872 , Total reward:  231591.0
Episode:  873 , Total reward:  231580.0
Episode:  874 , Total reward:  231577.0
Episode:  875 , Total reward:  231574.0
Episode:  876 , Total reward:  232544.0
Episode:  877 , Total reward:  232488.0
Episode:  878 , Total reward:  232477.0
Episode:  879 , Total reward:  232466.0
Episode:  880 , Total reward:  232443.0
Episode:  881 , Total reward:  232407.0
Episode:  882 , Total reward:  233365.0
Episode:  883 , Total reward:  233309.0
Episode:  884 , Total reward:  234293.0
Episode:  885 , Total reward:  234290.0
Episode:  886 , Total reward:  234234.0
Episode:  887 , Total reward:  234231.0
Episode:  888 , Total reward:  234228.0
Episode:  889 , Total reward:  234225.0
Episode:  890 , Total reward:  234222.0
Episode:  891 , Total reward:  235184.0
Episode:  892 , Total reward:  235173.0
Episode:  893 , Total reward:  235121.0
Episode:  894 , Total reward:  236099.0
Episode:  895 , Total reward:  237045.0
Episode:  896 , Total reward:  237034.0
Episode:  897 , Total reward:  237031.0
Episode:  898 , Total reward:  237020.0
Episode:  899 , Total reward:  237017.0
Episode:  900 , Total reward:  238002.0
Episode:  901 , Total reward:  237991.0
Episode:  902 , Total reward:  238976.0
Episode:  903 , Total reward:  238965.0
Episode:  904 , Total reward:  239914.0
Episode:  905 , Total reward:  239911.0
Episode:  906 , Total reward:  239908.0
Episode:  907 , Total reward:  239905.0
Episode:  908 , Total reward:  239815.0
Episode:  909 , Total reward:  239812.0
Episode:  910 , Total reward:  239801.0
Episode:  911 , Total reward:  239798.0
Episode:  912 , Total reward:  239787.0
Episode:  913 , Total reward:  239784.0
Episode:  914 , Total reward:  239781.0
Episode:  915 , Total reward:  239778.0
Episode:  916 , Total reward:  239767.0
Episode:  917 , Total reward:  240737.0
Episode:  918 , Total reward:  240734.0
Episode:  919 , Total reward:  241692.0
Episode:  920 , Total reward:  242675.0
Episode:  921 , Total reward:  242672.0
Episode:  922 , Total reward:  242637.0
Episode:  923 , Total reward:  242613.0
Episode:  924 , Total reward:  243576.0
Episode:  925 , Total reward:  244559.0
Episode:  926 , Total reward:  244511.0
Episode:  927 , Total reward:  244471.0
Episode:  928 , Total reward:  244468.0
Episode:  929 , Total reward:  244457.0
Episode:  930 , Total reward:  244446.0
Episode:  931 , Total reward:  245400.0
Episode:  932 , Total reward:  245397.0
Episode:  933 , Total reward:  245386.0
Episode:  934 , Total reward:  245383.0
Episode:  935 , Total reward:  245380.0
Episode:  936 , Total reward:  245377.0
Episode:  937 , Total reward:  245374.0
Episode:  938 , Total reward:  245318.0
Episode:  939 , Total reward:  245315.0
Episode:  940 , Total reward:  246270.0
Episode:  941 , Total reward:  247218.0
Episode:  942 , Total reward:  247170.0
Episode:  943 , Total reward:  248099.0
Episode:  944 , Total reward:  249035.0
Episode:  945 , Total reward:  249024.0
Episode:  946 , Total reward:  250002.0
Episode:  947 , Total reward:  250985.0
Episode:  948 , Total reward:  251968.0
Episode:  949 , Total reward:  251896.0
Episode:  950 , Total reward:  251885.0
Episode:  951 , Total reward:  251882.0
Episode:  952 , Total reward:  251879.0
Episode:  953 , Total reward:  251868.0
Episode:  954 , Total reward:  252822.0
Episode:  955 , Total reward:  252797.0
Episode:  956 , Total reward:  252780.0
Episode:  957 , Total reward:  252769.0
Episode:  958 , Total reward:  252758.0
Episode:  959 , Total reward:  253729.0
Episode:  960 , Total reward:  253685.0
Episode:  961 , Total reward:  253682.0
Episode:  962 , Total reward:  254644.0
Episode:  963 , Total reward:  254641.0
Episode:  964 , Total reward:  255626.0
Episode:  965 , Total reward:  255580.0
Episode:  966 , Total reward:  255569.0
Episode:  967 , Total reward:  255566.0
Episode:  968 , Total reward:  255563.0
Episode:  969 , Total reward:  255560.0
Episode:  970 , Total reward:  255496.0
Episode:  971 , Total reward:  255446.0
Episode:  972 , Total reward:  255402.0
Episode:  973 , Total reward:  255391.0
Episode:  974 , Total reward:  255388.0
Episode:  975 , Total reward:  256332.0
Episode:  976 , Total reward:  256329.0
Episode:  977 , Total reward:  257292.0
Episode:  978 , Total reward:  257289.0
Episode:  979 , Total reward:  258254.0
Episode:  980 , Total reward:  258206.0
Episode:  981 , Total reward:  259158.0
Episode:  982 , Total reward:  259155.0
Episode:  983 , Total reward:  260085.0
Episode:  984 , Total reward:  261056.0
Episode:  985 , Total reward:  261045.0
Episode:  986 , Total reward:  261028.0
Episode:  987 , Total reward:  261025.0
Episode:  988 , Total reward:  261988.0
Episode:  989 , Total reward:  261985.0
Episode:  990 , Total reward:  261982.0
Episode:  991 , Total reward:  261971.0
Episode:  992 , Total reward:  262943.0
Episode:  993 , Total reward:  262905.0
Episode:  994 , Total reward:  263883.0
Episode:  995 , Total reward:  263872.0
Episode:  996 , Total reward:  263869.0
Episode:  997 , Total reward:  264825.0
Episode:  998 , Total reward:  265781.0
Episode:  999 , Total reward:  266764.0
Episode:  1000 , Total reward:  266753.0
```

So the agent achieved a total reward of `266753` after `1000` episodes, for an average score of `266` per game. Since winning the game with the gold grabbed gives the agent a score of `~1000` (minus any moves), we can approximate that the agent is successful (in grabbing the gold) in about `266/1000`, or `~27%` of the games.

For comparison when the agent had a max risk threshold of `0.35` it would only achieve a total score of `188000` after `1000` episodes. 
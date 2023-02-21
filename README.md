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
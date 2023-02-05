from typing import List
from wumpus.src.environment.Environments import Environment
from wumpus.src.environment.Environments import Percept
from wumpus.src.agent.Agents import NaiveAgent


class WumpusWorld():
    
    def __init__(self) -> None:
        pass
    
    def main(args: List[str]):
        def run_episode(env: Environment,
                        agent: NaiveAgent,
                        percept: Percept) -> float:
            next_action = agent.next_action(percept)
            (next_environment, next_percept) = env.apply_action(next_action)
            print("Action: ", str(next_action.name), "| Agent Orientation: ", next_environment.agent.orientation.state.name)
            print('---------------------')
            print(next_environment.visualize())
            print('---------------------')
            print(next_percept.show())
            total_reward = next_percept.reward + \
                (run_episode(next_environment, 
                            agent, 
                            next_percept) if not next_percept.is_terminated else 0.0)
            return total_reward
                
        (initial_env, initial_percept) = Environment.initialize(4, 4, 0.2, False)
        agent = NaiveAgent()
        total_reward = run_episode(initial_env, agent, initial_percept)
        print("Total reward: ", str(total_reward))
         
         
if __name__ == '__main__':
    w = WumpusWorld()
    w.main()
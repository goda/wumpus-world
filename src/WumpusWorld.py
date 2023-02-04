

from typing import List
from src.environment.Environments import Environment
from src.environment.Environments import Percept
from src.agent.Agents import NaiveAgent

class WumpusWorld():
    
    def __init__(self) -> None:
        pass
    
    def main(args: List[str]):
        
        def run_episode(env: Environment,
                        agent: NaiveAgent,
                        percept: Percept) -> float:
            next_action = agent.next_action()
            print("Action: ", str(next_action))
            
            (next_environment, next_percept) = env.apply_action(next_action)
            print(next_environment.visualize())
            print(next_percept.show())
            
            return next_percept.reward + \
                run_episode(next_environment, agent, next_percept) if not next_percept.is_terminated else 0
                
        initial_env = Environment(4, 4, 0.2, False)
        initial_percept = Percept()
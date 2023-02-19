from wumpus.src.environment.Environments import Environment
from wumpus.src.environment.Environments import Percept
from wumpus.src.agent.Agents import BeelineAgent, NaiveAgent


class WumpusWorld():
    grid_width: int = 4
    grid_height: int = 4
    pit_prob: float = 0.2
    allow_climb_without_gold = False
    
    def __init__(self, grid_width: int, grid_height: int, 
                 pit_prob: float,
                 allow_climb_without_gold: bool) -> None:
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.pit_prob = pit_prob
        self.allow_climb_without_gold = allow_climb_without_gold
    
    def main(self, visualize: bool = False):
        def run_episode(env: Environment,
                        agent: NaiveAgent,
                        percept: Percept) -> float:
            next_action = agent.next_action(percept)
            (next_environment, next_percept) = env.apply_action(next_action)
            if visualize:
                print("Action: ", str(next_action.name), "| Agent Orientation: ", next_environment.agent.orientation.state.name)
                print(next_environment.visualize())
                print(next_percept.show())

            total_reward = next_percept.reward + \
                (run_episode(next_environment, 
                            agent, 
                            next_percept) if not next_percept.is_terminated else 0.0)
            return total_reward
                
        (initial_env, initial_percept) = Environment.initialize(self.grid_width,
                                                                self.grid_height,
                                                                self.pit_prob,
                                                                self.allow_climb_without_gold)
        agent = BeelineAgent()
        total_reward = run_episode(initial_env, agent, initial_percept)
        print("Total reward: ", str(total_reward))     

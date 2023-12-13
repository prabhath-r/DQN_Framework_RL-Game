import argparse
from dqn_agent import DQNAgent
import config
from environment import ChromeDinoEnvironment, BreakoutEnvironment, PongEnvironment, SpaceInvadersEnvironment, MsPacmanEnvironment, FrostbiteEnvironment, QbertEnvironment, AssaultEnvironment, EnduroEnvironment, SeaquestEnvironment, RiverRaidEnvironment
from torch.utils.tensorboard import SummaryWriter

def train():
    writer = SummaryWriter(log_dir=f"runs/{config.GAME_ENV}")
    env_classes = {
        'ChromeDino': ChromeDinoEnvironment,
        'Breakout': BreakoutEnvironment,
        'Pong': PongEnvironment,
        'SpaceInvaders': SpaceInvadersEnvironment,
        'MsPacman': MsPacmanEnvironment,
        'Frostbite': FrostbiteEnvironment,
        'Qbert': QbertEnvironment,
        'Assault': AssaultEnvironment,
        'Enduro': EnduroEnvironment,
        'Seaquest': SeaquestEnvironment,
        'RiverRaid': RiverRaidEnvironment
    }
    env_class = env_classes.get(config.GAME_ENV)
    if not env_class:
        raise ValueError("Invalid game environment specified")
    
    env = env_class()
        # Handling different environment types
    if hasattr(env, 'env') and hasattr(env.env, 'action_space'):
        config.ACTION_SIZE = env.env.action_space.n
    else:
        # Directly use the action size defined for custom environments
        config.ACTION_SIZE = 2
    agent = DQNAgent()

    global_step = 0
    for episode in range(config.NUM_EPISODES):
        state = env.reset()
        total_reward = 0
        episode_loss = 0
        done = False
        while not done:
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            agent.remember(state, action, reward, next_state, done)

            total_reward += reward
            loss = agent.learn()
            if loss is not None:
                episode_loss += loss
                writer.add_scalar('Loss/train', loss, global_step)
                writer.add_scalar('Learning Rate', agent.scheduler.get_last_lr()[0], global_step)

            writer.add_scalar('Epsilon', agent.epsilon, global_step)
            global_step += 1

            state = next_state

            if done:
                break
        print(f"Episode: {episode}, Total Reward: {total_reward}")
        writer.add_scalar('Total Reward', total_reward, episode)
        writer.add_scalar('Average Loss', episode_loss / global_step, episode)
        agent.scheduler.step()  # Update the learning rate

    writer.close()
    env.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--game_env", type=str, required=True, choices=["Breakout", "ChromeDino", "Pong", "SpaceInvaders", "MsPacman", "Frostbite", "Qbert", "Assault", "Enduro", "Seaquest", "RiverRaid"], help="Specify the game environment")
    args = parser.parse_args()
    config.GAME_ENV = args.game_env
    train()

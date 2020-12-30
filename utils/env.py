from collections import deque

import cv2
import gym
import numpy as np
from gym import spaces
from retro import make

import utils


class ActionsDiscretizer(gym.ActionWrapper):
    def __init__(self, env, actions):
        super(ActionsDiscretizer, self).__init__(env)
        buttons = env.buttons
        self._actions = []
        for action in actions:
            arr = np.array([False]*len(buttons))
            for button in action:
                arr[buttons.index(button)] = True
            self._actions.append(arr)
        self.action_space = spaces.Discrete(len(self._actions))

    def action(self, action):
        return self._actions[action].copy()


class ProcessFrame(gym.ObservationWrapper):
    def __init__(self, env, width=84, height=84):
        super(ProcessFrame, self).__init__(env)
        self.observation_space = spaces.Box(low=0, high=255, shape=(1, width, height))
        self.shape = width, height

    def observation(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frame = cv2.resize(frame, self.shape, interpolation=cv2.INTER_AREA)
        frame = frame[None, :, :]
        return frame


class AllowBacktracking(gym.Wrapper):
    def __init__(self, env, skip=4):
        super(AllowBacktracking, self).__init__(env)
        self.skip, self.xscrollHi, self.xscrollLo = skip, 0, 0

    def step(self, action):
        total_reward = 0
        for _ in range(self.skip):
            state, reward, done, info = self.env.step(action)
            reward += self.xscrollLo and (info["xscrollLo"]-self.xscrollLo) * 40.0
            self.xscrollLo = info["xscrollLo"]
            reward += self.xscrollHi and (info["xscrollHi"]-self.xscrollHi) * 80.0
            self.xscrollHi = info["xscrollHi"]
            total_reward += reward
            if done: break
        return state, max(min(total_reward, 200), -200), done, info

    def reset(self, **kwargs):
        self.xscrollHi, self.xscrollLo = 0, 0
        return self.env.reset(**kwargs)


class RewardScaler(gym.RewardWrapper):
    def __init__(self, env, scale=0.00125):
        super(RewardScaler, self).__init__(env)
        self.scale = scale

    def reward(self, reward):
        return reward * self.scale


class MarioWinner(gym.Wrapper):
    def __init__(self, env):
        super(MarioWinner, self).__init__(env)
        self.levelLo, self.levelHi, self.lives, self.finish = 0, 0, 0, None

    def step(self, action):
        state, reward, done, info = self.env.step(action)
        if self.finish == None:
            self.lives, self.levelLo, self.levelHi = info["lives"], info["levelLo"], info["levelHi"]
            self.finish = lambda levelLo, levelHi: levelLo != self.levelLo or levelHi != self.levelHi
        self.lives = max(self.lives, info["lives"])
        info["finish"] = self.finish(info["levelHi"], info["levelLo"])
        done |= info["finish"] or info["lives"] < self.lives
        return state, reward, done, info

    def reset(self, **kwargs):
        self.levelLo, self.levelHI, self.lives, self.finish = 0, 0, 0, None
        return self.env.reset(**kwargs)


class FrameStack(gym.Wrapper):
    def __init__(self, env, width=84, height=84):
        super(FrameStack, self).__init__(env)
        self.observation_space = spaces.Box(low=0, high=255, shape=(4, width, height))
        self.states = deque(np.zeros((4, width, height), dtype=np.float32), maxlen=4)
        self.correct = deque(maxlen=30)
        self.assist, self.skip = 0, 4

    def step(self, action):
        total_reward, state_buffer = 0, deque(maxlen=2)
        for _ in range(self.skip):
            state, reward, done, info = self.env.step(action)
            done |= self.assist == 400 or self.correct.count((action, True)) == self.correct.maxlen
            if done:
                if info["finish"]:
                    total_reward += 100
                    self.states.append(np.concatenate(state, 0))
                else:
                    total_reward += -10
                break
            else:
                total_reward += reward
            state_buffer.append(state)
        else:
            self.states.append(np.max(np.concatenate(state_buffer, 0), 0))
        result = max(0, reward) == 0
        self.correct.append((action, result))
        self.assist += result
        del state_buffer
        return np.array(self.states)[None, :, :, :].astype(np.float32), total_reward, done, info

    def reset(self):
        self.correct.clear()
        self.assist, state = 0, self.env.reset()
        self.states.extend(np.concatenate([state for _ in range(self.skip)], 0))
        return np.array(self.states)[None, :, :, :].astype(np.float32)


def create_runtime_env(game, state, action_type, record=False):
    actions = utils.Actions.get(action_type)
    assert actions, "Invalid action type."
    env = make(game, state, record=record)
    env = ActionsDiscretizer(env, actions)
    env = ProcessFrame(env)
    env = AllowBacktracking(env)
    env = RewardScaler(env)
    env = MarioWinner(env)
    env = FrameStack(env)
    return env, env.observation_space.shape[0], len(actions)

import gym
import trec_questions
import stanza
from whoosh import index
from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.qparser import QueryParser
import json

CURRENT_SCORE = 0
first_step = True
tq = trec_questions.trec_questions()

class EscapeRoomEnvironment(gym.Env):
    def __init__(self):
        super().__init__()

        #range of possible rewards; this can change based on how the checking mechanism quantifies correctness
        self.reward_range = (-1, 1)

        #I am thinking we might define the action object as a string that contains doccument index
        self.action_space = gym.spaces.Discrete(1)

        #we need to think about this one
        self.observation_space = list
        tq.next_search()

    def step(self, action):
        reward = 0

        #only rate a search when it isn't first time (since no search will have been done before first time)
        if self.first_step:
            self.first_step = False
        else:
            reward = self.check(action)

        #observation is a list returned by a yet-to-be-integrated "search" function which returns hits from whoosh search
        obs = tq.next_search()

        #returns next observation, reward, and that the program is not finished (the {} represent a null information space
        # since we are not currently utilizing an information space)
        return obs, reward, False, {}
    def reset(self):
        score = 0
        self.first_step = True
        return self.next_search()
    def next_search(self):
      return 0



    def check(self, action):
      if action == tq.current_question()[1]:
        return 1
      return -1

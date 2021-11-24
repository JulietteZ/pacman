#%%
# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0
     
    "*** YOUR CODE HERE ***"
    def get_v(state, values):
      q_lst = []
      if self.mdp.isTerminal(state):
        return 0
      else:
        for action in self.mdp.getPossibleActions(state):
          q_lst.append(values[(state, action)])
        return max(q_lst)
    
    i = 0
    while i < self.iterations:
      value = self.values.copy()
      for state in self.mdp.getStates():
        for action in self.mdp.getPossibleActions(state):
          # q_lst = []
          for next_state in self.mdp.getTransitionStatesAndProbs(state, action):
            # q_value = next_state[1] * \
            #   (self.mdp.getReward(state, action, next_state) + \
            #     self.discount * getValue(self, next_state))
            # if self.mdp.isTerminal(next_state[0])
            print next_state
            self.values[(state, action)] += next_state[1] * \
              (self.mdp.getReward(state, action, next_state) + \
                self.discount * get_v(next_state[0], value))
      i += 1
      # self.values = value

    # i = 0
    # while i < self.iterations:
    #   value = self.values.copy()
    #   for state in self.mdp.getStates():
    #     for action in self.mdp.getPossibleActions(state):
    #       q_lst = []

    


  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"
    return self.values[(state, action)]

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    "*** YOUR CODE HERE ***"
    
    q_lst = util.Counter()

    if len(self.mdp.getPossibleActions(state)) == 0: return None
    for action in self.mdp.getPossibleActions(state):
      q_lst[action] = self.getQValue(state, action)
    print "#################"
    print state
    print q_lst
    return q_lst.argMax()

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
# %%

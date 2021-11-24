# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util
import searchAgents
import search

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"
    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    # print "New start:"
    # print "current: ", currentGameState
    # print "action: ", action
    # print "state: ", successorGameState
    # print "newPos: ", newPos
    # print "newFood: ", newFood
    # print "newGhostStates: ", newGhostStates
    # print "newScaredTimes: ", newScaredTimes

    "*** YOUR CODE HERE ***"
    
    ans = 0
    foodDistance = []
    for food in newFood.asList():
        foodDistance.append(util.manhattanDistance(newPos, food))
    
    if len(foodDistance) == 0:
        ans = float("inf")
    else:
        ans += 1./(min(foodDistance))
    
    for ghost in successorGameState.getGhostPositions():
        if util.manhattanDistance(newPos, ghost) <= 1:
            ans -= float("inf")
    
    return successorGameState.getScore() + ans
#    return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    
    def max_value(gameState, agent, depth, evalFn, actions):
        v = -float("inf")

        legalMoves = gameState.getLegalActions(agent)
        if len(legalMoves) != 0:
            for successor in legalMoves:
                current_actions = []
                if len(actions) == 0:
                    current_actions = [successor]
                else:
                    current_actions = actions[:]
                    current_actions.append(successor)
                next_v, next_actions = min_value(gameState.generateSuccessor(agent, successor), agent+1, depth, evalFn, current_actions)
                if v < next_v:
                    v = next_v
                    ans_actions = next_actions
        else:
            ans_actions = actions
        return v, ans_actions

    def min_value(gameState, agent, depth, evalFn, actions):
        v = float("inf")
        legalMoves = gameState.getLegalActions(agent)
        if (agent == gameState.getNumAgents()-1 and depth <= 1) or len(legalMoves) == 0 or gameState.isLose() or gameState.isWin() :
            v = evalFn(gameState)
        elif agent == gameState.getNumAgents()-1:
            for successor in legalMoves:
                next_v, next_actions = max_value(gameState.generateSuccessor(agent, successor), 0, depth-1, evalFn, actions)
                if v > next_v:
                    v = next_v
                    actions = next_actions
        else:
            for successor in legalMoves:
                next_v, next_actions = min_value(gameState.generateSuccessor(agent, successor), agent+1, depth, evalFn, actions)
                if v > next_v:
                    v = next_v
                    actions = next_actions
        return v, actions
    
    numDepth = self.depth
    evalFn = self. evaluationFunction
    agent = 0
    actions = []
    while numDepth != 0:
        if agent == 0:
            next_v, next_action = max_value(gameState, agent, numDepth, evalFn, actions)
            return next_action[0]
        else:
            return min_value(gameState, agent, numDepth, evalFn, actions)[1][0]
        
class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """
  
  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    
    def max_value(gameState, a, b, agent, depth, evalFn, actions):
        v = -float("inf")

        legalMoves = gameState.getLegalActions(agent)
        if len(legalMoves) != 0:
            for successor in legalMoves:
                current_actions = []
                if len(actions) == 0:
                    current_actions = [successor]
                else:
                    current_actions = actions[:]
                    current_actions.append(successor)
                next_v, next_actions = min_value(gameState.generateSuccessor(agent, successor), a, b, agent+1, depth, evalFn, current_actions)
                if v < next_v:
                    v = next_v
                    ans_actions = next_actions
                a = max(a, v)
                if a >= b:
                    return v, ans_actions
        else:
            ans_actions = actions
        return v, ans_actions

    def min_value(gameState, a, b, agent, depth, evalFn, actions):
        v = float("inf")
        legalMoves = gameState.getLegalActions(agent)
        if (agent == gameState.getNumAgents()-1 and depth <= 1) or len(legalMoves) == 0 or gameState.isLose() or gameState.isWin() :
            v = evalFn(gameState)
        elif agent == gameState.getNumAgents()-1:
            for successor in legalMoves:
                next_v, next_actions = max_value(gameState.generateSuccessor(agent, successor), a, b, 0, depth-1, evalFn, actions)
                if v > next_v:
                    v = next_v
                    actions = next_actions
                b = min (b, v)
                if a >= b:
                    return v, actions
        else:
            for successor in legalMoves:
                next_v, next_actions = min_value(gameState.generateSuccessor(agent, successor), a, b, agent+1, depth, evalFn, actions)
                if v > next_v:
                    v = next_v
                    actions = next_actions
                b = min (b, v)
                if a >= b:
                    return v, actions
        return v, actions
    
    numDepth = self.depth
    evalFn = self. evaluationFunction
    agent = 0
    actions = []
    a = -float("inf")
    b = float("inf")
    while numDepth != 0:
        if agent == 0:
            next_v, next_action = max_value(gameState, a, b, agent, numDepth, evalFn, actions)
            return next_action[0]
        else:
            return min_value(gameState, a, b, agent, numDepth, evalFn, actions)[1][0]

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"

    def max_value(gameState, agent, depth, evalFn, actions):
        v = -float("inf")
        legalMoves = gameState.getLegalActions(agent)
        if len(legalMoves) != 0:
            for successor in legalMoves:
                current_actions = []
                if len(actions) == 0:
                    current_actions = [successor]
                else:
                    current_actions = actions[:]
                    current_actions.append(successor)
                next_v, next_actions = min_value(gameState.generateSuccessor(agent, successor), agent+1, depth, evalFn, current_actions)
                if v < next_v:
                    v = next_v
                    ans_actions = next_actions
        else:
            ans_actions = actions
            v = evalFn(gameState)
        return v, ans_actions

    def min_value(gameState, agent, depth, evalFn, actions):
        v = float("inf")
        legalMoves = gameState.getLegalActions(agent)
        if (agent == gameState.getNumAgents()-1 and depth <= 1) or len(legalMoves) == 0 or gameState.isLose() or gameState.isWin() :
            v = evalFn(gameState)
        elif agent == gameState.getNumAgents()-1:
            v_sum = 0
            for successor in legalMoves:
                next_v, next_actions = max_value(gameState.generateSuccessor(agent, successor), 0, depth-1, evalFn, actions)
                v_sum += next_v
            v = float(v_sum)/len(legalMoves)
        else:
            v_sum = 0
            for successor in legalMoves:
                next_v, next_actions = min_value(gameState.generateSuccessor(agent, successor), agent+1, depth, evalFn, actions)
                v_sum += next_v
            v = float(v_sum)/len(legalMoves)
        return v, actions
    
    numDepth = self.depth
    evalFn = self. evaluationFunction
    agent = 0
    actions = []
    while numDepth != 0:
        if agent == 0:
            next_v, next_action = max_value(gameState, agent, numDepth, evalFn, actions)
            return next_action[0]
        else:
            return min_value(gameState, agent, numDepth, evalFn, actions)[1][0]

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    For the current state, calculate the distance to the closest food, 
    the remaining food, and the distance to the ghost to find the evaluation function.
  """
  "*** YOUR CODE HERE ***"
  
  pos = currentGameState.getPacmanPosition()
  food = currentGameState.getFood()
  
  ans = 0
  foodDistance = []
  for pellet in food.asList():
      foodDistance.append(util.manhattanDistance(pos, pellet))

  if len(foodDistance) != 0:
      ans += 100./(min(foodDistance)+1)
      
  ans += 100000./(len(foodDistance)+1)  
  ans += 1000./(len(currentGameState.getCapsules())+1)
      
  ghostDistance = []
  for ghost in currentGameState.getGhostPositions():
      ghost_dis = util.manhattanDistance(pos, ghost)
      if ghost_dis < 2:
          return -9999999
      else:
          ghostDistance.append(ghost_dis)
          
  if len(ghostDistance) != 0:
      ans += min(ghostDistance)
      
  if currentGameState.isLose():
      ans -= 5000.
  elif currentGameState.isWin():
      ans += 5000.

  return ans 

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def mazeDistance(point1, point2, gameState):
    """
    Returns the maze distance between any two points, using the search functions
    you have already built.  The gameState can be any game state -- Pacman's position
    in that state is ignored.

    Example usage: mazeDistance( (2,4), (5,6), gameState)

    This might be a useful helper function for your ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + point1
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = searchAgents.PositionSearchProblem(gameState, start=point1, goal=point2, warn=False)
    return len(search.bfs(prob))
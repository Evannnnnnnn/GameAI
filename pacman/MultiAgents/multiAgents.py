# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #get information about the current state - position
        currentPosition = currentGameState.getPacmanPosition()

        #check for best or worst cases
        #highest score for a winning state
        if successorGameState.isWin():
            return 99999

        #worst case if pacman and ghost position are the same
        #but ghost is not scared
        for state in newGhostStates:
            if state.getPosition() == currentPosition and state.scaredTimer == 0:
                return -99999
        score = 0
        #for an action that causes pacman to stop negative score to avoid stopping
        if action == 'Stop':
            score -= 100
        #better score for state with food near and ghosts far
        #check distance of food from the Pacman
        foodDistance = [util.manhattanDistance(newPos, food) \
        for food in newFood]
        nearestFood = min(foodDistance)
        #nearer food should have more weightage - take inverse
        score += float(1/nearestFood)
        #subtract the no of food left and proportional weight to this as we want to Pick
        #state with less food leftover
        score -= len(newFood)

        #check distance of food of ghost in current and new states
        #if worse then deduct score else add score
        #for the current game state
        currentGhostDistances = [util.manhattanDistance(newPos, ghost.getPosition()) \
        for ghost in currentGameState.getGhostStates()]
        nearestCurrentGhost = min(currentGhostDistances)
        #for new GameStates
        newGhostDistances = [util.manhattanDistance(newPos, ghost.getPosition()) \
        for ghost in newGhostStates]
        nearestNewGhost = min(newGhostDistances)

        ##farther ghosts are better
        if nearestNewGhost < nearestCurrentGhost:
            score -= 100
        else:
            score += 200

        return successorGameState.getScore() + score


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

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #for minmax
        #minimum value function
        def minValue(state, agentIndex, depth):
            #information about the agent count and the legal actions for the index
            agentCount = gameState.getNumAgents()
            legalActions = state.getLegalActions(agentIndex)

            #if no legal actions then return the evaluation function
            if not legalActions:
                return self.evaluationFunction(state)

            # pacman is the last to move after all ghost movement
            if agentIndex == agentCount - 1:
                minimumValue =  min(maxValue(state.generateSuccessor(agentIndex, action), \
                agentIndex,  depth) for action in legalActions)
            else:
                minimumValue = min(minValue(state.generateSuccessor(agentIndex, action), \
                agentIndex + 1, depth) for action in legalActions)

            return minimumValue

        #maximum value function used for only pacman and hence setting index to 0
        def maxValue(state, agentIndex, depth):
            #information about the agent index and the legal actions for the index
            agentIndex = 0
            legalActions = state.getLegalActions(agentIndex)

            #if no legal actions or depth reached(prevent maximum depth
            #exceeded in recursion)then return the evaluation function
            if not legalActions  or depth == self.depth:
                return self.evaluationFunction(state)

            maximumValue =  max(minValue(state.generateSuccessor(agentIndex, action), \
            agentIndex + 1, depth + 1) for action in legalActions)

            return maximumValue

        #maximizing the best possible moves for the rootnode i.e.
        #the pacman thus agent index 0
        actions = gameState.getLegalActions(0)
        #find all actions and the corresponding value and then return action
        #corresponding to the maximum value
        allActions = {}
        for action in actions:
            allActions[action] = minValue(gameState.generateSuccessor(0, action), 1, 1)

        return max(allActions, key=allActions.get)

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #minimum value function
        def minValue(state, agentIndex, depth, alpha, beta):
            #information about the agent count and the legal actions for the index
            agentCount = gameState.getNumAgents()
            legalActions = state.getLegalActions(agentIndex)

            #if no legal actions then return the evaluation function
            if not legalActions:
                return self.evaluationFunction(state)

            #value track
            minimumValue = 99999
            currentBeta = beta
            # pacman is the last to move after all ghost movement
            if agentIndex == agentCount - 1:
                for action in legalActions:
                    minimumValue =  min(minimumValue, maxValue(state.generateSuccessor(agentIndex, action), \
                    agentIndex,  depth, alpha, currentBeta))
                    if minimumValue < alpha:
                        return minimumValue
                    currentBeta = min(currentBeta, minimumValue)

            else:
                for action in legalActions:
                    minimumValue =  min(minimumValue,minValue(state.generateSuccessor(agentIndex, action), \
                    agentIndex + 1, depth, alpha, currentBeta))
                    if minimumValue < alpha:
                        return minimumValue
                    currentBeta = min(currentBeta, minimumValue)

            return minimumValue

        #maximum value function used for only pacman and hence setting index to 0
        def maxValue(state, agentIndex, depth, alpha, beta):
            #information about the agent index and the legal actions for the index
            agentIndex = 0
            legalActions = state.getLegalActions(agentIndex)

            #if no legal actions or depth reached(prevent maximum depth
            #exceeded in recursion)then return the evaluation function
            if not legalActions  or depth == self.depth:
                return self.evaluationFunction(state)

            #value track
            maximumValue = -99999
            currentAlpha = alpha

            for action in legalActions:
                maximumValue = max(maximumValue, minValue(state.generateSuccessor(agentIndex, action), \
                agentIndex + 1, depth + 1, currentAlpha, beta) )
                if maximumValue > beta:
                    return maximumValue
                currentAlpha = max(currentAlpha, maximumValue)
            return maximumValue

        #maximizing the best possible moves for the rootnode i.e.
        #the pacman thus agent index 0
        #get state informatin and initialize alpha and beta
        actions = gameState.getLegalActions(0)
        alpha = -99999
        beta = 99999
        #find all actions and the corresponding value and then return action
        #corresponding to the maximum value
        allActions = {}
        for action in actions:
            value = minValue(gameState.generateSuccessor(0, action), 1, 1, alpha, beta)
            allActions[action] = value

            #update alpha
            if value > beta:
                return action
            alpha = max(value, alpha)

        return max(allActions, key=allActions.get)

        util.raiseNotDefined()

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

        #expected value function
        def expValue(state, agentIndex, depth):
            #information about the agent count and the legal actions for the index
            agentCount = gameState.getNumAgents()
            legalActions = state.getLegalActions(agentIndex)

            #if no legal actions then return the evaluation function
            if not legalActions:
                return self.evaluationFunction(state)

            #expected value and the probabilyt
            expectedValue = 0
            probabilty = 1.0 / len(legalActions) #probability of each action
            # pacman is the last to move after all ghost movement
            for action in legalActions:
                if agentIndex == agentCount - 1:
                    currentExpValue =  maxValue(state.generateSuccessor(agentIndex, action), \
                    agentIndex,  depth)
                else:
                    currentExpValue = expValue(state.generateSuccessor(agentIndex, action), \
                    agentIndex + 1, depth)
                expectedValue += currentExpValue * probabilty

            return expectedValue


        #maximum value function used for only pacman and hence setting index to 0
        def maxValue(state, agentIndex, depth):
            #information about the agent index and the legal actions for the index
            agentIndex = 0
            legalActions = state.getLegalActions(agentIndex)

            #if no legal actions or depth reached(prevent maximum depth
            #exceeded in recursion)then return the evaluation function
            if not legalActions  or depth == self.depth:
                return self.evaluationFunction(state)

            maximumValue =  max(expValue(state.generateSuccessor(agentIndex, action), \
            agentIndex + 1, depth + 1) for action in legalActions)

            return maximumValue

        #maximizing the best possible moves for the rootnode i.e.
        #the pacman thus agent index 0
        actions = gameState.getLegalActions(0)
        #find all actions and the corresponding value and then return action
        #corresponding to the maximum value
        allActions = {}
        for action in actions:
            allActions[action] = expValue(gameState.generateSuccessor(0, action), 1, 1)

        #returning action with best expectimax value
        return max(allActions, key=allActions.get)

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: For the purpose of building a better evaluation function, I
    have repurposed the initial evaluation function and improved it. For the
    current state the best and the worst cases are identified i.e. winning and
    being in the same state as a not-scared-ghost the score of 99999 and -99999
    respectively.

    For food gobbling, nearer the food the better and lesser food pellets left
    is a plus.

    For pellet-nabbing, nearer the pellets better the score.

    For ghost-hunting, I utilized the sum of the scared times to find if scared
    time is remainign and if yes then closer the ghost the better else the score
    is bad.

    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    currentPos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood().asList()
    currentGhostStates = currentGameState.getGhostStates()
    currentScaredTimes = [ghostState.scaredTimer for ghostState in currentGhostStates]
    currentCapsule = currentGameState.getCapsules()
    #highest score for a winning state
    if currentGameState.isWin():
        return 99999

    #worst case if pacman and ghost position are the same
    #but ghost is not scared
    for state in currentGhostStates:
        if state.getPosition() == currentPos and state.scaredTimer == 1:
            return -99999

    score = 0

    #chase food - food gobbling
    #better score for state with food near and ghosts far
    #check distance of food from the Pacman
    foodDistance = [util.manhattanDistance(currentPos, food) \
    for food in currentFood]
    nearestFood = min(foodDistance)
    #nearer food should have more weightage - take inverse
    score += float(1/nearestFood)
    #subtract the no of food left and proportional weight to this as we want to Pick
    #state with less food leftover
    score -= len(currentFood)

    #chase capsule - pellet nabbing
    #score for capsules
    if currentCapsule:
        capsuleDistance = [util.manhattanDistance(currentPos, capsule) \
        for capsule in currentCapsule]
        nearestCapsule = min(capsuleDistance)
        #near capsule better
        score += float(1/nearestCapsule)

    #chase ghost when ghost is scared else avoid - ghost hunting
    currentGhostDistances = [util.manhattanDistance(currentPos, ghost.getPosition()) \
    for ghost in currentGameState.getGhostStates()]
    nearestCurrentGhost = min(currentGhostDistances)
    scaredTime = sum(currentScaredTimes)
    ##farther ghosts are better
    if nearestCurrentGhost >= 1:
        if scaredTime < 0:
            score -= 1/nearestCurrentGhost
        else:
            score += 1/nearestCurrentGhost

    return currentGameState.getScore() + score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

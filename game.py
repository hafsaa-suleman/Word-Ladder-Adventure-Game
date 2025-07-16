from node import Node
from collections import deque
from queue import PriorityQueue
import math
import random
import time

#To Check if the word exists in the dictionary
def ValidWord(input,wordsList):
    for word in wordsList:
        if(input == word):
            return True
    
    return False
        
#To check if the new word is made by 1 letter transformation
def compare(input,similar):
    if len(input) != len(similar):
        return False
    
    transformationCount = 0 
    for i in range(len(input)):
        if(input[i] != similar[i]):
            transformationCount+=1
    
    if transformationCount==1:
        return True
    return False

# To add all the possible transformations from a word
def addAllTransformations(currentWord,endWord,wordsList,graph):
    for word in wordsList:
        if compare(currentWord,word):
            
            cost = 1
            heuristicCost = getHeuristic(word,endWord)
            # print("Current Word: ", word, "Heuristic: ",heuristicCost)
            #Adding word if it does not exist
            if word not in graph:
                graph[word] = Node(word,currentWord,[],heuristicCost)
            
            if word not in graph[currentWord].actions:
                graph[currentWord].actions.append((word, cost)) 
            # or
            # if not any(action[0] == word for action in graph[currentWord].actions):
            #     graph[currentWord].actions.append((word, cost))

def buildGraph(startWord,endWord, wordsList, depthLimit): 
    heuristicCost = getHeuristic(startWord,endWord)
    graph = {startWord : Node(startWord,None,[],heuristicCost,0)}
    queue = deque([(startWord,0)]) 
    explored = []

    while queue:
        currentWord, currentDepth = queue.popleft()
        
        if currentDepth > depthLimit:
            return None
        
        if currentWord not in explored:
            if currentWord not in graph:
                graph[currentWord] = Node(currentWord,None)
                
            addAllTransformations(currentWord,endWord,wordsList,graph)
        
            for action,cost  in graph[currentWord].actions:
                if action not in explored:
                    queue.append((action, currentDepth + 1))
                
            explored.append(currentWord)
            
        if endWord in explored:
            return graph
            
    return graph

def pathExists(startWord,endWord,graph):
    explored = set()
    queue = deque([startWord])
    while queue:
        word = queue.popleft()
        if word == endWord:
            return True
        explored.add(word)
        
        for action,cost in graph[word].actions:
            if action not in explored:
                explored.add(action)
                queue.append(action)
                
    return False

def actionSequence(graph, goalState,initialState):
    solution = [goalState]
    currentParent = graph[goalState].parent
    while currentParent is not initialState:
        # print("ParentNode", currentParent)
        solution.append(currentParent)
        currentParent = graph[currentParent].parent
    solution.reverse()
    return solution

def findMin(frontier):
    minPathCost = math.inf
    node = ''
    for i in frontier:
        if minPathCost > frontier[i][1]:
            minPathCost = frontier[i][1]
            node = i
    # print("Returning ",node," from FindMin")
    return node

def UCS(startWord,endWord,graph):

    if startWord in graph and endWord in graph:
        initialState = startWord
        goalState = endWord

        frontier = {}
        explored = []

        frontier[initialState] = (None,0)

        while frontier:
            currentNode = findMin(frontier)
            del frontier[currentNode]

            if graph[currentNode].word == goalState:
                return actionSequence(graph,goalState,initialState)

            explored.append(currentNode)
            for action in graph[currentNode].actions:
                currentCost = action[1] + graph[currentNode].path_cost

                if action[0] not in frontier and action[0] not in explored:
                    graph[action[0]].parent = currentNode
                    graph[action[0]].path_cost = currentCost
                    frontier[action[0]]=(graph[action[0]].parent, graph[action[0]].path_cost)
                elif action[0] in frontier:
                    if frontier[action[0]][1]<currentCost:
                        graph[action[0]].parent = frontier[action[0]][0]
                        graph[action[0]].path_cost = frontier[action[0]][1]
                    else:
                        frontier[action[0]] = (currentNode, currentCost)
                        graph[action[0]].parent=currentNode
                        graph[action[0]].path_cost = currentCost

def Astar(startWord,endWord,graph):
    if startWord in graph and endWord in graph:
        initialState = startWord
        goalState = endWord

        frontier = {}
        explored = {}

        frontier[initialState]=(None, graph[initialState].heuristic_cost)

        while frontier:
            currentNode = findMin(frontier)
            del frontier[currentNode]

            if graph[currentNode].word == goalState:
                return actionSequence(graph, goalState, initialState)

            # calculating total cost
            currentCost = graph[currentNode].path_cost
            heuristicCost = graph[currentNode].heuristic_cost
            explored[currentNode]=(graph[currentNode].parent, heuristicCost+currentCost)

            # Explore child nodes for cost
            for child in graph[currentNode].actions:
                currentCost=child[1] + graph[currentNode].path_cost
                heuristicCost = graph[child[0]].heuristic_cost


                # if already looked at or initial state or cost lesser than current, continue
                if child[0] in explored:
                    if graph[child[0]].parent == currentNode or child[0] == initialState or \
                        explored[child[0]][1] <= currentCost + heuristicCost:
                        continue

                # if not in frontier - add to it
                if child[0] not in frontier:
                    graph[child[0]].parent = currentNode
                    graph[child[0]].path_cost = currentCost
                    frontier[child[0]] = (graph[child[0]].parent, currentCost + heuristicCost)

                # if in frontier - check cost
                else:
                    #if cost is lesser - update graph with frontier
                    if frontier[child[0]][1] < currentCost + heuristicCost:
                        graph[child[0]].parent=frontier[child[0]][0]
                        graph[child[0]].path_cost=frontier[child[0]][1] - heuristicCost

                    # if cost is higher - update graph with current cost
                    else:
                        frontier[child[0]]=(currentNode, currentCost + heuristicCost)
                        graph[child[0]].parent=frontier[child[0]][0]
                        graph[child[0]].path_cost=currentCost

def getHeuristic(word,goalWord):
    transformationCount = 0 
    
    for i in range(len(word)):
        if(word[i] != goalWord[i]):
            transformationCount+=1
    
    # transformationCount = len(word) - sum(1 for a, b in zip(word, goalWord) if a == b)
            
    return transformationCount

def GBFS(startWord,endWord,graph):

    currentNode = graph[startWord]
    queue = PriorityQueue()
    explored = set()
    queue.put((currentNode.heuristic_cost, currentNode.word, []))
    
    
    while not queue.empty():
        heuristic, currentWord, path = queue.get()
        
        if currentWord == endWord:
            # print(path)
            return path
        
        if currentWord in explored:
            continue
        
        explored.add(currentWord)
        
        # print(f"Current Word: {currentWord}, Actions: {graph[currentWord].actions}, Heuristic_Cost: {graph[currentWord].heuristic_cost}")
        
        for action, _ in graph[currentWord].actions:
            if action not in explored:
                queue.put((graph[action].heuristic_cost, action, path + [action]))
                    
    return None

def printGraph(graph):
    for word, node in graph.items():
        print(f"Word: {word}, Parent: {node.parent}, Actions: {node.actions}")

def instructions():
    print("\033[1;34m\n\t\t======================== WELCOME TO THE WORD LADDER ADVENTURE GAME ========================\033[0m")

    instructions = [
        "Transform the start word into the target word. Sounds easy? Ha! We'll see.\n",
        "Rules of engagement: \n",
        "1. You may change **one** letter at a time. No sneaky business!",
        "2. Each step **must** be a real English word. No 'XQZT' nonsense, please.",
        "3. The word length stays the same—no stretching, no shrinking, no magic tricks.\n",
        "\033[1;32mCan you find the shortest path? Or will you wander endlessly in word limbo?\033[0m",
        "\033[1;32mGood luck, brave linguist! May your dictionary guide you well.\033[0m"
    ]

    for instruction in instructions:
        print("\t\t\t", instruction)

    input("\n\t\t\t\t\033[1;36mPress Enter to prove you're ready...\033[0m")  
    print("\n\t\t" + "\033[34m=\033[0m" * 92 + "\n")  



# Game Type Manual or Auto
def gameType():
    print()
    print("\t\t\t\t1. Wanna enter your own words🥱")
    print("\t\t\t\t2. Or Let us challenge you😼")
    print()
    choice = input("\033[1;36m\t\t\t\tWhat do you think? Enter 1 or 2: \033[0m")
    
    while True:
        if choice == "1" or choice == "2":
            break
        else:
            choice = input("\t\t\t\t\033[31mInvalid Choice! Enter again 😒: \033[0m")

    if choice == "1":
        print("\t\t\t\tYou chose to enter your own words")
    else:
        print("\t\t\t\tLet us find the perfect words for you")
    return choice

# Choose Game Mode - Beginner, Intermediate, Advanced
def chooseMode():
    print("\n\t\t\t\t\033[4;32mChoose Your Game Mode\033[0m")
    print("\n\t\t\t\t1. Beginner - Baby steps. Training wheels included.")
    print("\t\t\t\t2. Intermediate - For those who think they know words.")
    print("\t\t\t\t3. Advanced - Only enter if you're ready to suffer.")
    
    movesLimit = 0
    
    mode = input("\n\t\t\t\t\033[1;36mEnter your choice (1, 2, or 3): \033[0m")
    while True:
        if mode == "1" or mode == "2" or mode == "3":
            break
        else:
            mode = input("\t\t\t\t\033[31mInvalid Choice! Enter again 😒: \033[0m")
        
    if mode == "1":
        print("\n\t\t\t\tBeginner Mode Selected - Easy Peasy")
        print("\t\t\t\tYou will have 5 moves to reach the end word")
        movesLimit = 5

    elif mode == "2":
        print("\n\t\t\t\tIntermediate Mode Selected - Let's see how good you are")
        print("\t\t\t\tYou will have 7 moves to reach the end word")
        movesLimit = 7

    elif mode == "3":
        print("\n\t\t\t\tAdvanced Mode Selected - You are a pro")
        print("\t\t\t\tYou will have 10 moves to reach the end word")
        movesLimit = 10
            
    return mode, movesLimit

def beginner():
    words = [("cat", "dog"), ("lead", "gold"), ("ruby", "code"), ("warm", "cold"), ("cap", "mop"),("line","cake"),("head","tail"),("star","moon"),("book","read"),("pen","ink"),("sail","ruin"),("wolf","gown"),("side","walk")]
    wordTuple = random.choice(words)
    return wordTuple[0],wordTuple[1]

def intermediate():
    words = [("stone","money"),("ladder","better"),("cross","river"),("wheat","bread"),("apple","mango"),("blue","pink"),("work","team")]
    wordTuple = random.choice(words)
    return wordTuple[0],wordTuple[1]

def advanced():
    print("advanced")
    #todo
 
 #For user custom words
def ownWords(wordsList):
    print("\n\t\t" + "\033[34m=\033[0m" * 92 + "\n")
    print("\n\t\t\033[1;36mTime to pick your words! Choose wisely...\033[0m")

    startWord = input("\033[1;36m\n\t\t\t\tEnter start word: \033[0m")
    while True:
        if ValidWord(startWord,wordsList) != True:
            print("\t\t\t\tWord does not exist in Dictionary :(")
            startWord = input("\033[1;36m\t\t\t\tEnter a valid start word: \033[0m")
        else:
            break

    endWord = input("\033[1;36m\t\t\t\tEnter end word: \033[0m")
    while True:
        if startWord == endWord:
            print("\n\t\t\t\033[1;31mReally? The same word? This isn't a loop simulator. Try again!\033[0m 🤦‍♂️")
            endWord = input("\033[1;36m\t\t\t\tEnter a valid end word: \033[0m")
        elif len(startWord) != len(endWord):
            print("\n\t\t\tStart and End word must be of same length.")
            endWord = input("\033[1;36m\t\t\t\tEnter a valid end word: \033[0m")
        elif ValidWord(endWord,wordsList) == False:
            print("\n\t\t\tWord does not exist in Dictionary")
            endWord = input("\033[1;36m\t\t\t\tEnter a valid end word: \033[0m")
        else:
            break
    
    print("\n\t\t" + "\033[34m=\033[0m" * 92 + "\n")
    return startWord,endWord

def playGame(startWord, endWord, graph, moveLimit):
    
    currentNode = graph[startWord]
    moves = 0
    path = []

    while currentNode.word != endWord:
        # Add transformations if no actions exist
        if moves == moveLimit:
            print("You have reached the move limit. Game Over!😔")
            print("Path:", path)
            return False
        
        if not currentNode.actions:
            addAllTransformations(currentNode.word, endWord, graph.keys(), graph)
            currentNode = graph[currentNode.word]

        if moves > moveLimit/2:
            print("\n\t\t\t\tKeep count of moves, you have ",moveLimit-moves," moves left ☹️⌛")
        
        nextWord = input("\033[1;36m\n\t\t\t\t\tEnter the next word or type '1' to get a hint: \033[0m").strip()
        
        valid_words = {word for word, _ in currentNode.actions}
        while True:
            if nextWord == '1':
                break
            elif nextWord in valid_words:
                break
            else:
                nextWord = input("\n\t\t\t\t\t\033[31mInvalid Word, Enter another word or type '1' to get a hint: \033[0m").strip()

        while nextWord.lower() == '1':
            print("\n\t\t\t\t\t\033[4;32mChoose an algorithm to get hint\033[0m")
            print("\n\t\t\t\t\t1. UCS")
            print("\t\t\t\t\t2. GBFS")
            print("\t\t\t\t\t3. A*")
            algo = input("\033[1;36m\n\t\t\t\t\tEnter Algorithm No.: \033[0m").strip()

            hintPath = []
            if algo == "1":
                hintPath = UCS(currentNode.word, endWord, graph)
            elif algo == "2":
                hintPath = GBFS(currentNode.word, endWord, graph)
            elif algo == "3":
                hintPath = Astar(currentNode.word, endWord, graph)
            else:
                print("\t\t\t\t\033[31mInvalid algorithm choice! Try again.\033[0m")
                continue

            if hintPath:
                print("\t\t\t\t\t\033[32mHint: \033[0m", hintPath[0])
            else:
                print("\t\t\t\t\033[31mNo valid path found!\033[0m")
            
            nextWord = input("\033[1;36m\n\t\t\t\t\tEnter the next word: \033[0m")
            valid_words = {word for word, _ in currentNode.actions}
            while nextWord not in valid_words:
                nextWord = input("\n\t\t\t\t\t\033[31mInvalid Word, Enter another word: \033[0m").strip()
            
        # Move to the next word
        path.append(nextWord)
        moves += 1
        currentNode = graph[nextWord]

    print("\n\t\t" + "\033[34m=\033[0m" * 92 + "\n")  
    print("\n\t\t\t\t\tCONGRAATUULATIONSS, YOUU WONNN! 🎉 SCORE: ", moves)
    print("\n\t\t\t\t\tPath: ", path)
    print("\n\t\t" + "\033[34m=\033[0m" * 92 + "\n")  
    
    return moves

def optimalMoves(startWord, endWord,graph):
    optimalPath = Astar(startWord,endWord,graph)
    return len(optimalPath)

def calculateScore(movesTaken,optimalMoves):
    maxScore = 100
    penaltyPerExtraMove = 10
    extraMoves = max(0,movesTaken - optimalMoves)
    score = max(0,maxScore - (extraMoves * penaltyPerExtraMove))
    
    return score

def startGame():
    file = open("words_alpha.txt", "r" )
    wordsList = file.read().split("\n")
    file.close()
    depthLimit = 5
    moveLimit = 0
    startWord = ""
    endWord = ""
    moveLimit = 0
    score = 0
    
    instructions()
    
    while True:
        type = gameType()
        if type == "1":
            startWord,endWord = ownWords(wordsList)
            moveLimit = 10
            print("\n\t\t\t\tYou chose your own path. 🤷")
            print("\n\t\t\t\tso you have 10 moves to reach the end word 🏃")
            
        elif type == "2":
            mode, moveLimit = chooseMode()
            if mode == "1":
                startWord,endWord = beginner()
            elif mode == "2":
                startWord,endWord = intermediate()
            elif mode == "3":
                startWord,endWord = advanced()
        
        
        dictionary = [word for word in wordsList if len(word) == len(startWord)]

        print("\n\t\t\t\t\033[5mPreparing Game for you...\033[0m")
        graph = buildGraph(startWord,endWord,dictionary,depthLimit)
    
        #Depth and path existence only to check if user enter words
        if gameType == "1":
            if graph is None:
                print("\t\t\t\tDepth limit reached and still end word not found.")
                continue

            if pathExists(startWord,endWord,graph) == False :
                print("\t\t\t\tNo path exists between these words")
                continue
        
        # clear screen
        print("\033[H\033[2J", end="")  
        print("\n\t\t" + "\033[34m=\033[0m" * 92 + "\n")  
        
        # game ready
        print("\t\t\t\t\t\t\033[1;34m🎉 Game Ready! Let's Do This! 🚀\033[0m")
        time.sleep(1)  
        print("\n\t\t\t\t\t\t\033[1;34mYour starting point: \033[0m", f"\033[1;32m{startWord.upper()}\033[0m 🏁")
        time.sleep(0.5)
        print("\t\t\t\t\t\t\033[1;34mYour ultimate goal: \033[0m", f"\033[1;31m{endWord.upper()}\033[0m 🎯")
        
        print("\n\t\t\033[1;36mGet ready to flex those brain muscles! 🧠💪\033[0m")
        print("\t\t\033[1;36mRemember: One letter at a time... unless you have magical powers. 🪄\033[0m")

        print("\n\t\t" + "\033[34m=\033[0m" * 92 + "\n")

        optimalmoves = optimalMoves(startWord,endWord,graph)
        print("\n\t\t\t\toptimal moves", optimalmoves)
        moves = playGame(startWord,endWord,graph,moveLimit)
        if moves != False:
            score = calculateScore(moves,optimalmoves)
        
        print("\n\t\t\t\tYour Score is: ", score)
        playAgain = input("\n\t\t\t\tDo you want to play again?(1/0): ")
        if playAgain == "1":
            startGame()
        else:
            print("\n\t\t\t\tThanks for playing!👋🙋‍♂️")
            break
  
startGame()

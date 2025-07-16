class Node:
    def __init__(self,word,parent=None,actions=[], heuristic_cost=0,path_cost=0):
        self.word = word
        self.parent = parent
        self.actions = actions
        self.heuristic_cost = heuristic_cost
        self.path_cost = path_cost
        
    def __str__(self):
        return f"Node(word={self.word}, parent={self.parent}, actions={self.actions})"

    def __repr__(self):
        return self.__str__()
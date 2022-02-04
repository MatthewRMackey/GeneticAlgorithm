'''
    Author: Matthew Mackey
    Overview: Simple graph data structure built on a dictionary to test my genetic algorithm
    Requires the maximally allowed degree of the nodes in the graph to contruct
'''
class Graph:
    def __init__(self, degree):
        self.graph = {}
        self.degree = degree
        self.current = None
        self.head = None
        
    def addNode(self, obj, edge):
        if obj in self.graph.keys(): 
            self.graph[self.current][edge] = obj
            self.current = obj
        else:
            if self.current == None:
                self.current = obj
                self.head = obj
                self.graph[obj] = [None for i in range(self.degree)]
            else:
                self.graph[self.current][edge%self.degree] = obj
                self.graph[obj] = [None for i in range(self.degree)]
                self.current = obj

    def resetCurrentNode(self):
        self.current = self.head
        
    def traverseGraph(self, edge):
        self.current = self.graph[self.current][edge]

    def printGraph(self):
        for k in self.graph.keys():
            print(k, self.graph[k])

    # This evaluates a path through the graph by the number of steps it takes to reach the end
    # Path is a list edges representing the next node for each step from start to end
    # Paths with no solution are defaulted to a value of -999
    def evaluatePath(self, path, start, end):
        self.current = start
        steps = 0
        solution = [self.current]
        for step in path:
            if self.graph[self.current][step] == None:
                return -999
            if step > len(self.graph[self.current]):
                return -999
            if self.current == end:
                return steps
            if self.current != self.graph[self.current][step]:
                self.traverseGraph(step)
                steps += 1
                solution.append(step)
        if self.current == end:
            return steps
        return -999

    # This is a helper function for traversing a path in the graph.
    # Returns an empty path if there is no connection (in the case of None), 
    # or the start and end are the same node.
    # It will trim paths that have steps beyond the end node.
    def trimPath(self, path, start, end):
        self.current = start
        solution = []
        for step in path:
            if self.graph[self.current][step] == None:
                return []
            if step > len(self.graph[self.current]):
                return []
            if self.current == end:
                self.current = start
                return solution
            if self.current != self.graph[self.current][step]:
                self.traverseGraph(step)
                solution.append(step)
        if self.current == end:
            return solution
        return []
    
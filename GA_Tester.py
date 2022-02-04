from GeneticAlgorithm import GeneticAlgorithm
from Graph import Graph
import random
from numpy import average

if __name__ == "__main__":
    lengths = []
    for k in range(100):
        graph = Graph(20)
        for i in range(100):
            for j in range(40):
                graph.addNode(random.randint(0,59), random.randint(0,19))
        start = random.randint(0,59)
        end = random.randint(0,59)
        eval_path = lambda e: graph.evaluatePath(e, start, end)
        ga = GeneticAlgorithm(10, 20, 20, eval_path, (0,19))
        solution = ga.generate()
        lengths.append(graph.evaluatePath(solution, start, end))
    
    print("Average length for GA solutions:", average(lengths))
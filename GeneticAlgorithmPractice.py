import random
'''
    Author: Matthew Mackey
    References: https://arxiv.org/ftp/arxiv/papers/1308/1308.4675.pdf, https://www.geeksforgeeks.org/python-lambda-anonymous-functions-filter-map-reduce/
    Objective: Explore the concept of Genetic Algorithms making use of map and lambda functions for self-education.
    Construct with:
    - a n-tuple of numerical genes to be optimize
    - number of generations to run
    - a eval_function should be provided that will take the tuple containing the 
        chromosome's genes and return a corresponding value.
'''

class GeneticAlgorithm:
    def __init__(self, genes, generations, chromosomes, eval_function, gene_range=(-100,100)):
        self.genes = genes
        self.generations = generations
        self.chromosomes = chromosomes
        self.eval_function = eval_function
        self.gene_range = gene_range
        #dict{i:[random genes] for i < 10}
        self.population = {j:[random.randint(self.gene_range[0], self.gene_range[1]) for i in range(self.genes)] for j in range(self.chromosomes)}
        #self.population = {j:[j,j,j,j] for j in range(11)}
        #dict{i:evaluation of ith genes in puplation}
        self.evaluations = {i:abs(self.eval_function(self.population[i])) for i in self.population.keys()}

    #Runs the genetic algorithm which generates the optimized parameters     
    def generate(self):
        for gen in range(0, self.generations, 1):            
            self.selection()
            self.crossover()
            self.mutation()  
            self.evaluations = {i:abs(self.eval_function(self.population[i])) for i in self.population.keys()}
        
        winner = self.evaluations[0]
        w_index = 0
        for i in self.evaluations:
            if self.evaluations[i] < winner:
                winner = self.evaluations[i]
                w_index = i
        return self.population[w_index]
    #Determine the probability that each chromosome is selected for the next 
    #generation based on the fitness of its evaluation. Fitness = 1/(1+eval(gene)) for each gene. 
    #We want to minimize, so inverting the value will increase its fitness as the value gets closer to 0. 
    #The +1 in the denomenator is to avoid division by 0.
    def selection(self):
        fitness = dict(map(lambda e:(e,1/(1+self.evaluations[e])), self.evaluations.keys()))
        total_fit = sum(fitness.values())
        probabilities = dict(map(lambda e:(e,fitness[e]/total_fit), fitness.keys()))
        cumulative = {}
        for i, p in enumerate(probabilities.keys()):
            if i == 0:
                cumulative[p] = probabilities[p]
            else:
                cumulative[p] = probabilities[p]+cumulative[p-1] 
        
        rand_nums = [random.random() for i in range(len(cumulative.keys()))]
        for i, r in enumerate(rand_nums):
            index = 0
            while index < len(cumulative):
                if r < cumulative[index]:
                    #Copy will assign the values rather than reference 
                    #so manipulating the lists won't carry over to the copied objects
                    self.population[i] = self.population[index].copy() 
                    break
                index += 1

    def crossover(self):
        random_nums = [random.random() for i in self.population.keys()]
        pc = .25
        selected = []
        for i, s in enumerate(random_nums):
            if s < pc:
                selected.append(i)
        #Needs to be a deepcopy instead of reference because the referenced 
        #value changes before the original value is finished being used in the if below
        try:
            selected_buffer = [i for i in self.population[selected[0]]] 
            for i in range(len(selected)):
                cutoff = random.randint(1,self.genes-1)
                gene = 0
                while gene < cutoff:
                    if i == len(selected)-1:
                        self.population[selected[i]][gene] = selected_buffer[gene]
                        gene += 1
                    else:
                        self.population[selected[i]][gene] = self.population[selected[i+1]][gene]
                        gene += 1
        except IndexError:
            pass

    def mutation(self):
        pm = .1
        total_genes = (len(self.population.keys())-1) * self.genes
        num_mutations = pm * total_genes
        mutations = [random.randint(0, total_genes) for i in range(int(num_mutations))]
        for m in mutations:
            self.population[int(m/self.genes)][m%self.genes] = random.randint(self.gene_range[0], self.gene_range[1])

#Using lambdas for eval_function because:
# 1. it's only one line and this saves space.
# 2. lambdas allow for definition without defined parameters
# 3. the class is designed for lambdas to increase user control andfelxibility
#if __name__ == "__main__":
#    start_time = time.time()
#    genes = 2
#    eval_function = lambda vars: (vars[0]**2 + vars[1]**2) - 50 # -> x^2 + y^2 = 50 
#    vals = []
#    for i in range(100):
#        vals.append(eval_function(GeneticAlgorithm(genes, 100, 40, eval_function, (-50,50)).generate()))
#    print('time:', time.time()-start_time)
#    print('avg error:', sum(vals)/len(vals))
#    print(GeneticAlgorithm(genes, 50, 20, eval_function, (-50,50)).generate())

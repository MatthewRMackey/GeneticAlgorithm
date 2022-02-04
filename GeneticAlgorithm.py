import random

'''
    Author: Matthew Mackey
    
    Objective: Exploratory program to utilize my previously written GA code to work on graphs
    in an attempt to find a shortest path from one node to another.
    
    Usage: The constructor requires:
    -the number of genes in each chromosome 
    -the number of generations to run
    -the number of chromosomes in a population per generation
    -the evaluation function, which should be designed to take the list of genes as input
    -and the desired gene value range; defaulted to (-100,100)
    
    Applications:
    I have used this GA to find solutions to equations and in finding optimal paths through graphs.
    
    References:
    References: https://arxiv.org/ftp/arxiv/papers/1308/1308.4675.pdf, https://www.geeksforgeeks.org/python-lambda-anonymous-functions-filter-map-reduce/
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
        #dict{i:evaluation of ith genes in puplation}
        self.evaluations = {i:abs(self.eval_function(self.population[i])) for i in self.population.keys()}

    #Method to generate the solution of the genetic algorithm 
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
                    #Copy will assign the values rather than reference, 
                    #so manipulating the lists won't carry over to the copied objects
                    self.population[i] = self.population[index].copy() 
                    break
                index += 1

    #Randomly select individuals to crossover genes with a probablility of .25
    #Each individual selected will take a random number of between (1,n-1) genes from the subsequent chromosome
    #The final chromosome chosen will crossover with the original set of genes from the first chromosome (via selected_buffer)
    def crossover(self):
        random_nums = [random.random() for i in self.population.keys()]
        pc = .25
        selected = []
        for i, s in enumerate(random_nums):
            if s < pc:
                selected.append(i)
        try:
            selected_buffer = self.population[selected[0]].copy()
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

    #Randomly choose .1 * total_genes in population to mutate 
    #The mutated genes will be randomly re-generate within the given gene range.
    def mutation(self):
        pm = .1
        total_genes = (len(self.population.keys())-1) * self.genes
        num_mutations = pm * total_genes
        mutations = [random.randint(0, total_genes) for i in range(int(num_mutations))]
        for m in mutations:
            # select the m/(#genes) chromosome and its m%(#genes) gene to mutate 
            self.population[int(m/self.genes)][m%self.genes] = random.randint(self.gene_range[0], self.gene_range[1])


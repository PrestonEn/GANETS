from igraph import Graph, VertexClustering
import numpy as np
from collections import Counter

class Individual(object):
    def __init__(self, graph, genes=[]):
        if not isinstance(graph, Graph):
            print 'Individual must take a graph as a parameter'
            raise Exception

        self.graph = graph

        self.genes = genes

        self.fitness = -1

        if genes == []:
            self.initalizeGenes()


    def initalizeGenes(self, bias=0.3):
        self.genes = [np.random.randint(0, self.graph.vcount() - 1) \
                      for i in range(0, self.graph.vcount())]


        # Bias the initialization by selecting a subset of nodes, and assigning their
        # cluster id to their neighbours
        b = self.graph.vcount() * bias

        for c in range(int(b)):
            i = np.random.randint(0, len(self.genes))
            cid = self.genes[i]
            for n in self.graph.neighbors(i):
                self.genes[n] = cid


    @staticmethod
    def oneWayCross(g1, g2):
        """
        Select a cluster from g1, and assign the same cluster membership in g2
        :param g1:
        :param g2:
        :return:
        """
        if not isinstance(g1, Individual) or not isinstance(g2,Individual):
            print 'Must pass individual to crossover'
            raise Exception

        c = np.random.choice(g1.genes)
        cgenes = [i for i in g2.genes]
        for index, val in enumerate(g1.genes):
            if val == c:
                cgenes[index] = val

        return Individual(g1.graph, cgenes)


    def mutate(self, prob):
        """
        Assign a random gene to a new cluster
        We limit clusters to the neighbours of the selected node
        :return:
        """
        if np.random.uniform(0,1) < prob:
            i = np.random.randint(0, len(self.genes))
            ngh = np.random.choice(self.graph.neighbors(i))
            self.genes[i] = self.genes[ngh]



    def setFitness(self):
        self.fitness = VertexClustering(self.graph, self.genes).modularity

    def getVertexCluster(self):
        return VertexClustering(self.graph, self.genes)

    def getComVariance(self, n, neighs):
        non_com = 0.0
        c = self.genes[n]
        for i in neighs:
            if self.genes[i] != c:
                non_com += 1.0
        return non_com/self.graph.degree(n)



    def cleanUp(self, portion=0.3, thold=0.49):
        index_set = list(set([i for i in range(0, len(self.genes))]))
        b = int(self.graph.vcount() * portion)
        for i in range(b):
            i = np.random.randint(0, len(index_set))
            n = index_set[i]
            neigs = self.graph.neighbors(n)
            if self.getComVariance(n, neigs) > thold:
                clusts = [self.genes[t] for t in neigs]
                self.genes[n] = Counter(clusts).most_common(1)[0][1]
            del index_set[i]

import numpy as np
from igraph import Graph
from igraph import VertexClustering
from tqdm import *

class Individual(object):
    """A member of the GA-NET population
    """
    def __init__(self, graph, genes=[]):
        if not isinstance(graph, Graph):
            print 'Individual must take a graph as a parameter'
            raise Exception

        self.graph = graph

        self.genes = genes

        self.fitness = -1

        if genes == []:
            self.initalizeGenes()

    @staticmethod
    def UniformCrossOver(g1, g2, prob=0.5):
        if not isinstance(g1, Individual) or not isinstance(g2,Individual):
            print 'Must pass individual to crossover'
            raise Exception
        binstr = [False if i >= prob else True for i in \
                  [np.random.uniform(0,1) for j in range(len(g1.genes))]]
        childGenes = []
        for index, val in enumerate(binstr):
            childGenes.append(g1.genes[index]) if val else \
                childGenes.append(g2.genes[index])
        child = Individual(g1.graph, childGenes)
        # child.makeSafe()
        return child


    def decode(self):
        """
        Given a locus representation, decode to a string of groups list
        :return: cluster membership list
        """
        newestGroup = 1
        membership = [-1 for item in self.genes]

        for index, val in enumerate(self.genes):
            fromNode = index
            toNode = val
            if membership[toNode] == -1:
                if membership[fromNode] == -1:
                    membership[fromNode] = newestGroup
                    membership[toNode] = newestGroup
                    newestGroup += 1
                else:
                    membership[toNode] = membership[fromNode]
            else:
                if membership[toNode] != membership[fromNode]:
                    mergeingFrom = membership[fromNode]
                    mergingTo = membership[toNode]
                    #try to merge up to and including current node
                    for j_index in range(index+1):
                        if membership[j_index] == mergeingFrom:
                            membership[j_index] = mergingTo
        return membership

    def initalizeGenes(self):
        self.genes = [np.random.randint(0,self.graph.vcount()-1) \
                        for i in range(0,self.graph.vcount())]
        self.makeSafe()
        # print "done"

    def makeSafe(self):
        """Parse through the locus representation of the indiviual checking
        that all connections exist.

        If a connection does not exist, repair
        """
        adjMat = self.graph.get_adjacency()

        for i in range(len(self.genes)):
            if adjMat[i][self.genes[i]] is not 1:
                try:
                    self.genes[i] = np.random.choice(self.graph.neighbors(i))
                except IndexError:
                    self.genes[i] = i

    def setComscore(self, r=0.9):
        sum = np.sum
        pow = np.power
        div = np.divide
        mul = np.multiply

        comscore = 0.0
        c = self.decode()
        clustering = VertexClustering(self.graph, c)

        # igraph doesnt put cluster IDs in lowest terms
        # filter to avoid empty subgraphs
        sgs = [i for i in clustering.subgraphs() if len(i.vs) != 0]
        for sg in sgs:

            d = sg.get_adjacency().data
            meanSum = 0.0
            volume = 0.0
            for row in d:
                rowSum = float(sum(row))
                meanSum += pow(rowSum/float(len(d)),r)
                volume += rowSum

            powerMean = meanSum/len(d)
            comscore += powerMean * volume
        # print comscore
        self.fitness = comscore

    def setModularity(self):
        c = self.decode()
        self.fitness = VertexClustering(self.graph, c).modularity


    def mutate(self, prob):
        if np.random.uniform(0,1) < prob:
            i = np.random.randint(0, len(self.genes)-1)
            self.genes[i] = np.random.choice(self.graph.neighbors(self.genes[i]))
            # self.makeSafe()


    def getVertexCluster(self):
        return VertexClustering(self.graph, self.decode())



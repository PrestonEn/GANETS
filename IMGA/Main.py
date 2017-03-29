import argparse
import time
import numpy as np
from igraph import Graph, VertexClustering




def ga_loop(pop, pop_size, gens, crossover_rate, mutation_rate, elite_portion):
    pass



if __name__ == "__main__":
    # GA params
    pop = []
    population_size = -1
    generations = -1
    crossover_rate = -1
    mutate_rate = -1
    elite = -1
    seed = 0
    g = None

    # record keeping for graphs
    best = []
    avg = []

    FLAGS = None

    parser = argparse.ArgumentParser()
    parser.register("type", "bool", lambda v: v.lower() == "true");
    parser.add_argument("--graph_path", type=str, default="", help="Path to graph file")
    parser.add_argument("--population", type=int, default=300, help="Individuals in the population")
    parser.add_argument("--elite_portion", type=float, default=0.1, help="Portion of best individuals to save next gen")
    parser.add_argument("--generations", type=int, default=30, help="Max Cycles of GA to run")
    parser.add_argument("--crossover_rate", type=float, default=0.8, help="The crossover rate")
    parser.add_argument("--mutation_rate", type=float, default=0.3, help="The mutation rate")
    parser.add_argument("--seed", type=long, default=int(time.time()), help="Random seed to use")

    FLAGS, unparsed = parser.parse_known_args()
    crossover_rate = FLAGS.crossover_rate
    population_size = FLAGS.population
    generations = FLAGS.generations
    mutate_rate = FLAGS.mutation_rate
    elite = FLAGS.elite_portion
    seed = FLAGS.seed
    graph_path = ""

    np.random.seed(seed)

    if FLAGS.graph_path == "":
        g, graph_path = Graph.Famous('Zachary'), "../gml_files/karate.gml"
        g.write_gml("../gml_files/karate.gml")
    else:
        g, graph_path = Graph.Read_GML(FLAGS.graph_path), FLAGS.graph_path



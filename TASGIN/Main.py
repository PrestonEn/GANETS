import sqlite3
import time
from tqdm import *
import argparse, json
import numpy as np
from igraph import Graph
from PlotFunction import plot
from Individual import Individual
import ntpath

def roulette_select():
    global pop
    total_fit = sum([i.fitness for i in pop])
    index_list = [i.fitness / total_fit for i in pop]
    roll = np.random.uniform(0, 1) * total_fit
    for index, val in enumerate(index_list):
        roll -= pop[index].fitness
        if roll <= 0:
            return pop[index]
    return pop[-1]


def sort_popstats():
    global pop
    pop.sort(key=lambda x: x.fitness)
    best.append(pop[-1].fitness)
    avg.append(sum([i.fitness for i in pop]) / population_size)


def write_results(vals):
    assert len(vals) == 9

    conn = sqlite3.connect('../ClusterResults.db')
    # seed, algo, params, clstr_mbrship, grph_fl_nm, bst_fit_lst, avg_fit_lst, bst_ft
    conn.execute("INSERT INTO ClusterOutputs Values (?, ?, ?, ?, ?, ?, ?, ?, ?)", vals)
    conn.commit()
    conn.close()


def main():
    global pop
    global generations
    global elite

    # initalize population
    print population_size

    pop = [Individual(g) for i in range(population_size)]
    map(lambda ind: ind.setFitness(), pop)
    # sort in increasing order of fitness

    sort_popstats()

    pbar = tqdm(total=generations)
    for gen in xrange(generations):
        new_pop = []
        # move the slice of elites to the new population
        for item in pop[int(-(population_size * elite)):]:
            new_pop.append(item)

        while len(new_pop) < population_size:
            # do your selection of parents and crossover
            p1 = roulette_select()
            p2 = roulette_select()
            child = Individual.oneWayCross(p1, p2)

            # try for mutation
            child.mutate(mutate_rate)
            child.cleanUp()
            child.setFitness()

            # add to new population
            new_pop.append(child)

        pop = new_pop

        sort_popstats()
        pbar.update(1)
    pbar.close()


    filename = "../imgs/tasgin"+str(time.time())+ ntpath.basename(graph_path) + ".png"
    print filename
    vals = (seed,
            "tasgin",
            json.dumps(vars(FLAGS)),
            json.dumps(pop[-1].getVertexCluster().membership),
            graph_path,
            json.dumps(best),
            json.dumps(avg),
            pop[-1].fitness,
            filename)
    plot(g,  filename, pop[-1].getVertexCluster().membership)
    write_results(vals)



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
    r = 1

    # record keeping for graphs
    best = []
    avg = []

    FLAGS = None

    parser = argparse.ArgumentParser()
    parser.register("type", "bool", lambda v: v.lower() == "true")
    parser.add_argument(
        "--graph_path",
        type=str,
        default="",
        help="Path to graph file"
    )
    parser.add_argument(
        "--population",
        type=int,
        default=300,
        help="Individuals in the population"
    )
    parser.add_argument(
        "--elite_portion",
        type=float,
        default=0.1,
        help="Portion of best individuals to copy to the next generation"
    )
    parser.add_argument(
        "--generations",
        type=int,
        default=30,
        help="Max Cycles of GA to run"
    )
    parser.add_argument(
        "--mutation_rate",
        type=float,
        default=0.3,
        help="The mutation rate"
    )
    parser.add_argument(
        "--seed",
        type=long,
        default=int(time.time()),
        help="Random seed to use"
    )


    FLAGS, unparsed = parser.parse_known_args()
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



    main()

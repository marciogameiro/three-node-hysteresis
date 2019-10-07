# QueryDescending.py
# Shaun Harker
# 2017-04-02
# MIT LICENSE

# This file is meant to analyze a specific network
# for queries indicated in the "Query" paper

import DSGRN
from memoize import memoize
import time
import sys

class PQNetworkAnalyzer:
    def __init__(self, network, P):
        self.network = network
        self.P_index = network.index(P)
        self.parametergraph = DSGRN.ParameterGraph(network)

    def AnalyzeParameter(self, parameterindex):
        parameter = self.parametergraph.parameter(parameterindex)
        dg = DSGRN.DomainGraph(parameter)
        md = DSGRN.MorseDecomposition(dg.digraph())
        mg = DSGRN.MorseGraph(dg, md)
        return mg

    def is_FP(self, annotation):
        return annotation.startswith("FP")

    def is_quiescent_FP(self, annotation):
        if self.is_FP(annotation):
            digits = [int(s) for s in annotation.replace(",", "").split() if s.isdigit()]
            if digits[self.P_index] > 0:  # reversed (descending)
                return True
        return False

    def is_proliferative_FP(self, annotation):
        if self.is_FP(annotation):
            digits = [int(s) for s in annotation.replace(",", "").split() if s.isdigit()]
            if digits[self.P_index] == 0:  # reversed (descending)
                return True
        return False

    def AnalyzeMorseGraph(self, mg):
        mg_poset = mg.poset()
        stable_annotations = [ mg.annotation(i)[0] for i in range(0,mg.poset().size()) if len(mg.poset().children(i)) == 0]
        monostable = len(stable_annotations) == 1
        quiescent = any( self.is_quiescent_FP(annotation) for annotation in stable_annotations )
        proliferative = any( self.is_proliferative_FP(annotation) for annotation in stable_annotations )
        if monostable and quiescent:
            return 'Q'
        if monostable and proliferative:
            return 'P'
        if quiescent and proliferative:
            return 'B'
        if quiescent:
            return 'q'
        if proliferative:
            return 'p'
        return 'O'

    @memoize
    def Classify(self, parameterindex):
        return self.AnalyzeMorseGraph(self.AnalyzeParameter(parameterindex))

def topological_sort(graph):
    """
    Return list of vertices in (reverse) topologically sorted order
    """
    result = []
    explored = set()
    dfs_stack = [ (v,0) for v in graph.vertices]
    while dfs_stack:
        (v,i) = dfs_stack.pop()
        if (v,i) in explored: continue
        explored.add((v,i))
        if i == 0: # preordering visit
            dfs_stack.extend([(v,1)] + [ (u,0) for u in graph.adjacencies(v) ])
        elif i == 1: # postordering visit
            result.append(v)
    return result

def count_paths(graph, source = None, target = None, allowed = None):
    """
    returns card{ (u,v) : source(u) & target(v) & there is an allowed path from u to v}
    """
    if source == None: source = lambda v : True
    if target == None: target = lambda v : True
    if allowed == None: allowed = lambda x : True
    ts = topological_sort(graph)
    # trivial_paths = {} # trivial paths with zero edges
    unit_paths = {} # paths with only one edge
    paths = {} # paths with more than one edge
    # result_trivial = 0
    result_unit = 0
    result = 0
    for v in ts:
        if not allowed(v): continue
        # trivial_paths[v] = (1 if target(v) else 0)
        unit_paths[v] = sum([1 for u in graph.adjacencies(v) if target(u) and allowed(u)])
        paths[v] = sum([paths[u] + unit_paths[u] for u in graph.adjacencies(v) if allowed(u)])
        # # paths[v] = sum([ paths[u] for u in graph.adjacencies(v) if allowed(u)]) + ( 1 if target(v) else 0)
        # # if source(v): result += paths[v]
        if source(v):
            # result_trivial += trivial_paths[v]
            result_unit += unit_paths[v]
            result += paths[v]
    return result

class ComputeHysteresisQueryPartialPath:
    def __init__(self, network, S, P):
        self.network = network 
        self.analyzer = PQNetworkAnalyzer(self.network, P)
        self.query = DSGRN.ComputeSingleGeneQuery(network,S,self.analyzer.Classify)
        self.patterngraph = DSGRN.Graph(set([0,1,2,3,4]), [(0,0),(1,1),(0,1),(1,0),(0,2),(1,2),(2,2),(2,3),(2,4),(3,3),(3,4),(4,4),(4,3)])
        self.patterngraph.matching_label = lambda v : { 0:'Q', 1:'q', 2:'B', 3:'p', 4:'P' }[v]
        self.matching_relation = lambda label1, label2 : label1 == label2
        self.memoization_cache = {}

    def __call__(self,reduced_parameter_index):
        searchgraph = self.query(reduced_parameter_index)
        searchgraphstring = ''.join([ searchgraph.matching_label(v) for v in searchgraph.vertices ])
        if searchgraphstring not in self.memoization_cache:
            alignment_graph = DSGRN.AlignmentGraph(searchgraph, self.patterngraph, self.matching_relation)
            source = lambda x: x[1] == 0
            target = lambda x: x[1] == 4
            num_paths = count_paths(alignment_graph, source, target)
            self.memoization_cache[searchgraphstring] = num_paths
        return self.memoization_cache[searchgraphstring]

    def num_paths(self):
        return count_paths(self.query(0))

class ComputeResettableBistabilityQueryPartialPath:
    def __init__(self, network, S, P):
        self.network = network 
        self.analyzer = PQNetworkAnalyzer(self.network, P)
        self.query = DSGRN.ComputeSingleGeneQuery(network,S,self.analyzer.Classify)
        self.patterngraph = DSGRN.Graph(set([0,1,2]), [(0,0),(1,1),(0,1),(1,0),(0,2),(1,2),(2,2)])
        self.patterngraph.matching_label = lambda v : { 0:'Q', 1:'q', 2:'B'}[v]
        self.matching_relation = lambda label1, label2 : label1 == label2
        self.memoization_cache = {}

    def __call__(self,reduced_parameter_index):
        searchgraph = self.query(reduced_parameter_index)
        searchgraphstring = ''.join([ searchgraph.matching_label(v) for v in searchgraph.vertices ])
        if searchgraphstring not in self.memoization_cache:
            alignment_graph = DSGRN.AlignmentGraph(searchgraph, self.patterngraph, self.matching_relation)
            source = lambda x: x[1] == 0
            target = lambda x: x[1] == 2
            num_paths = count_paths(alignment_graph, source, target)
            self.memoization_cache[searchgraphstring] = num_paths
        return self.memoization_cache[searchgraphstring]

    def num_paths(self):
        return count_paths(self.query(0))

class ComputeHysteresisQueryFullPath:
    def __init__(self, network, S, P):
        self.network = network 
        self.analyzer = PQNetworkAnalyzer(self.network, P)
        self.query = DSGRN.ComputeSingleGeneQuery(network,S,self.analyzer.Classify)
        self.patterngraph = DSGRN.Graph(set([0,1,2,3,4]), [(0,0),(1,1),(0,1),(1,0),(0,2),(1,2),(2,2),(2,3),(2,4),(3,3),(3,4),(4,4),(4,3)])
        self.patterngraph.matching_label = lambda v : { 0:'Q', 1:'q', 2:'B', 3:'p', 4:'P' }[v]
        self.matching_relation = lambda label1, label2 : label1 == label2
        self.memoization_cache = {}
        self.root = 0
        self.leaf = self.query.number_of_gene_parameters()-1

    def __call__(self,reduced_parameter_index):
        searchgraph = self.query(reduced_parameter_index)
        searchgraphstring = ''.join([ searchgraph.matching_label(v) for v in searchgraph.vertices ])
        if searchgraphstring not in self.memoization_cache:
            alignment_graph = DSGRN.AlignmentGraph(searchgraph, self.patterngraph, self.matching_relation)
            source = lambda x: x[0] == self.root and x[1] == 0
            target = lambda x: x[0] == self.leaf and x[1] == 4
            num_paths = count_paths(alignment_graph, source, target)
            self.memoization_cache[searchgraphstring] = num_paths
        return self.memoization_cache[searchgraphstring]

    def num_paths(self):
        source = lambda x: x == self.root
        target = lambda x: x == self.leaf
        return count_paths(self.query(0), source, target)

class ComputeResettableBistabilityQueryFullPath:
    def __init__(self, network, S, P):
        self.network = network 
        self.analyzer = PQNetworkAnalyzer(self.network, P)
        self.query = DSGRN.ComputeSingleGeneQuery(network,S,self.analyzer.Classify)
        self.patterngraph = DSGRN.Graph(set([0,1,2]), [(0,0),(1,1),(0,1),(1,0),(0,2),(1,2),(2,2)])
        self.patterngraph.matching_label = lambda v : { 0:'Q', 1:'q', 2:'B'}[v]
        self.matching_relation = lambda label1, label2 : label1 == label2
        self.memoization_cache = {}
        self.root = 0
        self.leaf = self.query.number_of_gene_parameters()-1

    def __call__(self,reduced_parameter_index):
        searchgraph = self.query(reduced_parameter_index)
        searchgraphstring = ''.join([ searchgraph.matching_label(v) for v in searchgraph.vertices ])
        if searchgraphstring not in self.memoization_cache:
            alignment_graph = DSGRN.AlignmentGraph(searchgraph, self.patterngraph, self.matching_relation)
            source = lambda x: x[0] == self.root and x[1] == 0
            target = lambda x: x[0] == self.leaf and x[1] == 2
            num_paths = count_paths(alignment_graph, source, target)
            self.memoization_cache[searchgraphstring] = num_paths
        return self.memoization_cache[searchgraphstring]

    def num_paths(self):
        source = lambda x: x == self.root
        target = lambda x: x == self.leaf
        return count_paths(self.query(0), source, target)

if __name__ == "__main__":
    # Read command line arguments
    if len(sys.argv) < 8:
    # if len(sys.argv) < 10:
        print("./QueryDescending network_specification_file.txt partial_hysteresis_output_file.txt full_hysteresis_output_file.txt starting_rpi ending_rpi S_gene P_gene")
        # print("./QueryDescending network_specification_file.txt partial_hysteresis_output_file.txt partial_resettable_output_file.txt full_hysteresis_output_file.txt full_resettable_output_file.txt starting_rpi ending_rpi S_gene P_gene")
        exit(1)
    network_specification_file = str(sys.argv[1])
    network = DSGRN.Network(network_specification_file)
    partial_hysteresis_output_file = str(sys.argv[2])
    full_hysteresis_output_file = str(sys.argv[3])
    starting_rpi = int(sys.argv[4])
    ending_rpi = int(sys.argv[5])
    S = sys.argv[6]
    P = sys.argv[7]
    # partial_hysteresis_output_file = str(sys.argv[2])
    # partial_resettable_output_file = str(sys.argv[3])
    # full_hysteresis_output_file = str(sys.argv[4])
    # full_resettable_output_file = str(sys.argv[5])
    # starting_rpi = int(sys.argv[6])
    # ending_rpi = int(sys.argv[7])
    # S = sys.argv[8]
    # P = sys.argv[9]

    # Routine to run queries
    def RunQueries(Query, filename):
        start_time = time.time()
        query = Query(network, S, P)
        result = 0    
        for rpi in range(starting_rpi, ending_rpi):
            result += query(rpi)
            if (rpi - starting_rpi) % 10000 == 0:
                DSGRN.LogToSTDOUT("Processed from " + str(starting_rpi) + " to " + str(rpi) + " out of " + str(ending_rpi))
        normalization = (ending_rpi - starting_rpi)*query.num_paths() 
        with open(filename, 'w') as outfile:
            outfile.write(str(result) + " " + str(normalization) + "\n")
        with open(filename + ".log", 'w') as outfile:
            outfile.write(str(time.time() - start_time) + '\n')

    # Queries to run
    RunQueries(ComputeHysteresisQueryPartialPath, partial_hysteresis_output_file)
    # RunQueries(ComputeResettableBistabilityQueryPartialPath, partial_resettable_output_file)
    RunQueries(ComputeHysteresisQueryFullPath, full_hysteresis_output_file)
    # RunQueries(ComputeResettableBistabilityQueryFullPath, full_resettable_output_file)

    exit(0)

# EnqueueDescending.py
# Shaun Harker
# 2017-04-02
# MIT LICENSE

# Enqueue jobs for Query paper on a cluster

import subprocess
import DSGRN
import sys, os

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("./EnqueueDescending.py output_folder network_specification_file S_gene_name P_gene_name [command]")
        exit(1)
    if len(sys.argv) == 6:
        command = sys.argv[5]
    else:
        command = ""
    output_folder = sys.argv[1]
    network_specification_file = sys.argv[2]
    S = sys.argv[3]
    P = sys.argv[4]
    network = DSGRN.Network(network_specification_file);
    print(network.graphviz())
    parametergraph = DSGRN.ParameterGraph(network)
    S_index = network.index(S)
    N = parametergraph.size()
    M = len(parametergraph.factorgraph(S_index))
    L = N // M  # number of reduced parameter index
    Jmax = 2000 # maximum number of jobs to split into
    Kmin = 10000 # minimum number of reduced parameters per job
    K = max(Kmin, int(L/2000))  # number of reduced parameter indices per job
    # K = L # hack: just a single job (c.f. Enqueue.py)
    shard_script = str(os.path.dirname(os.path.realpath(__file__))) + "/Shard.sh"
    query_script = str(os.path.dirname(os.path.realpath(__file__))) + "/QueryDescending.py"
    jobs = [ (command + ' ' + shard_script + ' ' + query_script + ' ' + output_folder + ' ' + network_specification_file + ' ' + str(i) + ' ' + str(min(i+K,L)) + ' ' + S + ' ' + P) for i in range(0, L, K) ]
    print(jobs)
    for job in jobs:
        subprocess.call(job, shell=True)

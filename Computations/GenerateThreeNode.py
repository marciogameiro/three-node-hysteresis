# Generate Three Node Networks

import itertools

three = [-1, 0, 1]
somelists = [three, three, three]

input_combinations = [ element for element in itertools.product(*somelists) ]
threelists = [input_combinations, input_combinations, input_combinations]
possibilities = [ element for element in itertools.product(*threelists) ]

def NodeSymbol(triple, i):
  # triple is 3-tuple, e.g. (-1, 0, 1)
  # triple[i] is self edge
  if i == 0:
    j = 1
    k = 2
  if i == 1:
    j = 0
    k = 2
  if i == 2:
    j = 0
    k = 1
  # i is self edge, j and k are other edges
  return (triple[i], min(triple[j], triple[k]), max(triple[j], triple[k]))

def NumberEdges(network):
    num_edges = 0
    for i in range(3):
        for j in range(3):
            if not network[i][j] == 0:
                num_edges = num_edges + 1
    return num_edges

def NetworkHeuristic(network):
  # "network" is triple of triples, e.g. ((1, 1, 1), (1, 1, 1), (1, 1, -1))
  return tuple(sorted([NodeSymbol(network[i], i) for i in range(0,3)]))

table = {}

def CheckNetworkIsomorphism(network1, network2):
  for pi in itertools.permutations([0, 1, 2]):
    if all( [ network1[i][j] == network2[pi[i]][pi[j]] for i in range(0,3) for j in range(0,3) ]):
      return True 
  return False

def CheckIfNetworkNontrivial(network):
  aa = network[0][0]
  bb = network[1][1]
  cc = network[2][2]
  # Return 0 if has self repressor
  if (aa == -1) or (bb == -1) or (cc == -1):
    return 0

  ab = network[1][0]
  ac = network[2][0]
  ba = network[0][1]
  bc = network[2][1]
  ca = network[0][2]
  cb = network[1][2]

  # Make sure it is connected
  # Return 0 if a is isolated
  if (ab == 0) and (ba == 0) and (ac == 0) and (ca == 0):
    return 0
  # Return 0 if b is isolated
  if (ba == 0) and (ab == 0) and (bc == 0) and (cb == 0):
    return 0
  # Return 0 if c is isolated
  if (ca == 0) and (ac == 0) and (cb == 0) and (bc == 0):
    return 0

  # Return 0 if no edge from a or b to c
  # if (ac == 0) and (bc == 0):
  #   return 0

  # Return 0 if a does not regulate c
  # if (ab == 0 or bc == 0) and (ac == 0):
  #   return 0

  # Return 0 if a has no out edge
  if (aa == 0) and (ab == 0) and (ac == 0):
    return 0
  # Return 0 if b has no out edge
  if (ba == 0) and (bb == 0) and (bc == 0):
    return 0
  # Return 0 if c has no out edge
  if (ca == 0) and (cb == 0) and (cc == 0):
    return 0

  return 1

def NetworkFileString(network):
  symbol = { -1 : "R", 0 : "0", 1 : "A" }
  return ''.join([symbol[network[i][j]] for i in range(0,3) for j in range(0,3) ])

def NetworkSpecFile(network):
  spec = ''
  for i in range(0,3):
    spec += 'X' + str(i) + ' : '
    activators = '+'.join([ 'X' + str(j) for j in range(0,3) if network[i][j] == 1])
    repressors = ')('.join([ '~X' + str(j) for j in range(0,3) if network[i][j] == -1])
    if activators:
      activators = '(' + activators + ')'
    if repressors:
      repressors = '(' + repressors + ')'
    spec += activators + repressors + ( " : E\n" if i > 0 else "\n")
  return spec

for network in possibilities:
  if not CheckIfNetworkNontrivial(network):
    continue
  if not NumberEdges(network) < 9:
    continue
  heuristic = NetworkHeuristic(network)
  if heuristic not in table:
    table[heuristic] = []
  # didn't need to check symmetry because input and output node break symmetry
  # if not any( CheckNetworkIsomorphism(network, tabled_network) for tabled_network in table[heuristic]):
  #   table[heuristic].append(network)
  table[heuristic].append(network)

number_of_networks = sum([ len(table[key]) for key in table ])

print("Number of networks: " + str(number_of_networks))

for key in table:
  for network in table[key]:
    filename = NetworkFileString(network) + '.txt'
    content = NetworkSpecFile(network)
    with open('Networks/' + filename, 'w') as file:
      file.write(content)

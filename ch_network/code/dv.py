from pprint import pprint as pp
from collections import defaultdict



initial_routing_tables = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: float('inf'))))

link_cost = dict()

initial_routing_tables['A']['B']['B']  = 3
initial_routing_tables['A']['F']['F']  = 75
initial_routing_tables['A']['Z']['Z']  = 150


initial_routing_tables['B']['A']['A']  = 3
initial_routing_tables['B']['C']['C']  = 5
initial_routing_tables['B']['D']['D']  = 20
initial_routing_tables['B']['F']['F']  = 4

initial_routing_tables['C']['B']['B']  = 5
initial_routing_tables['C']['D']['D']  = 10
initial_routing_tables['C']['F']['F']  = 8

initial_routing_tables['D']['B']['B']  = 20
initial_routing_tables['D']['C']['C']  = 10
initial_routing_tables['D']['Z']['Z']  = 2


initial_routing_tables['F']['A']['A']  = 75
initial_routing_tables['F']['B']['B']  = 4
initial_routing_tables['F']['C']['C']  = 8
initial_routing_tables['F']['Z']['Z']  = 60

initial_routing_tables['Z']['A']['A']  = 150
initial_routing_tables['Z']['D']['D']  = 5
initial_routing_tables['Z']['F']['F']  = 60

# initial_routing_tables['']['']['']  = 



# initial_routing_tables = {
#     'A': {'B': {'B': 3},
#           'F': {'F': 75},
#           'Z': {'Z': 150}
#           },
#     'B': {'A': {'A': 3},
#           'C': {'C': 5},
#           'D': {'D': 20},
#           'F': {'F': 4},
#           },
#     'C': {'B': {'B': 5},
#           'D': {'D': 10},
#           'F': {'F': 8},        
#           },
#     'D': {'B': {'B': 20},
#           'C': {'C': 10},
#           'Z': {'Z': 2},
#           },
#     'F': {'A': {'A': 75},
#           'B': {'B': 4},
#           'C': {'C': 8},
#           'Z': {'Z': 60}, 
#           },
#     'Z': {'A': {'A': 150},
#           'D': {'D': 2},
#           'F': {'F': 60},
#           },
# }

nodes = list(initial_routing_tables.keys())
links = [(n, m, initial_routing_tables[n][m][m])
         for n in nodes
         for m in list(initial_routing_tables[n].keys())
]


# link_cost[(n,m)] = initial_routing_tables[n][m][m]

link_cost = dict( ((n, m), initial_routing_tables[n][m][m])
         for n in nodes
         for m in list(initial_routing_tables[n].keys())
         )



pp(nodes)
pp(links)

routing_tables = initial_routing_tables


def compute_dv (tab, node):
    """Compute distance vector of node in table tab"""
    neighbors = list(tab[node].keys())
    pp(tab[node][neighbors[0]].values())
    known_nodes = list(set(x 
        for n in neighbors
        for x in tab[node][n].keys()
                       ))
    # pp(neighbors)
    # pp(known_nodes)
    
    # pp(tab[node][neighbors[0]][known_nodes[3]])
    # pp(tab[node][neighbors[0]])

    dv = dict(
        (kn, min(tab[node][n][kn] for n in neighbors))
        for kn in known_nodes 
        ) 

    return dv
    # for kn in known_nodes:
        
    
def update_node_with_dv(tab, node, dv, neighbor):
    """assume DV arrives at link from neighbor neigh. Compute next state"""

    cost_to_neighbor = link_cost[(node,neighbor)]
    local_dv = compute_dv (tab, node)

    changed = False
    
    for n in dv:
        if n == node:
            continue 
        try: 
            current_cost = local_dv[n]

            if current_cost > cost_to_neighbor + dv[n]:
                # we learned about a cheaper route via this neighbor
                print("Updating at {} via neighbor {} to node {}".format(node, neighbor, n))
                tab[node][neighbor][n] = cost_to_neighbor + dv[n]
                changed = True 
        except KeyError:
            # we learned about a new node n!
            tab[node][neighbor][n] = cost_to_neighbor + dv[n]
            changed = True 
            print("Learned new node {} at {} from  neighbor {}; cost: {}, {} ".format(n, node, neighbor, cost_to_neighbor, dv[n]))
    pass

# test code:

# dv_at_f = compute_dv(initial_routing_tables, 'F')
# pp ( dv_at_f)

# update_node_with_dv (routing_tables, 'A', dv_at_f, 'F')
# pp(routing_tables['A'])

print("==============")

pp(routing_tables['C'])
dv_at_d = compute_dv(initial_routing_tables, 'D')
pp(dv_at_d)
update_node_with_dv (routing_tables, 'C', dv_at_d, 'D')
pp(routing_tables['C'])



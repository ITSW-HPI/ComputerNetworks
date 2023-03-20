from pprint import pprint as pp
from collections import defaultdict
import random 


initial_routing_tables = defaultdict(lambda: defaultdict(lambda: float('inf')))

link_cost = dict()

initial_routing_tables['A']['A']  = (0, 'A')
initial_routing_tables['A']['B']  = (3, 'A')
initial_routing_tables['A']['F']  = (75, 'A')
initial_routing_tables['A']['Z']  = (150, 'A')


initial_routing_tables['B']['B']  = (0, 'B')
initial_routing_tables['B']['A']  = (3, 'B')
initial_routing_tables['B']['C']  = (5, 'B')
initial_routing_tables['B']['D']  = (20, 'B')
initial_routing_tables['B']['F']  = (4, 'B')

initial_routing_tables['C']['C']  = (0, 'C')
initial_routing_tables['C']['B']  = (5, 'C')
initial_routing_tables['C']['D']  = (10, 'C')
initial_routing_tables['C']['F']  = (8, 'C')

initial_routing_tables['D']['D']  = (0, 'D')
initial_routing_tables['D']['B']  = (20, 'D')
initial_routing_tables['D']['C']  = (10, 'D')
initial_routing_tables['D']['Z']  = (2, 'D')


initial_routing_tables['F']['F']  = (0, 'F')
initial_routing_tables['F']['A']  = (75, 'F')
initial_routing_tables['F']['B']  = (4, 'F')
initial_routing_tables['F']['C']  = (8, 'F')
initial_routing_tables['F']['Z']  = (60, 'F')

initial_routing_tables['Z']['Z']  = (0, 'Z')
initial_routing_tables['Z']['A']  = (150, 'Z')
initial_routing_tables['Z']['D']  = (5, 'Z')
initial_routing_tables['Z']['F']  = (60, 'Z')


nodes = list(initial_routing_tables.keys())
links = [(n, m, initial_routing_tables[n][m])
         for n in nodes
         for m in list(initial_routing_tables[n].keys())
]

link_cost = dict( ((n, m), initial_routing_tables[n][m][0])
         for n in nodes
         for m in list(initial_routing_tables[n].keys())
         )
# pp(nodes)
# pp(links)
# pp(link_cost)

routing_tables = initial_routing_tables
     
    
def update_node_with_dv(tab, node, neighbor):
    """assume DV arrives at link from neighbor neigh. Compute next state.
    Note: This is simplified; e.g., in a real implementation, the outgoing
    interface would not be part of the DV sent to a neighbor."""

    cost_to_neighbor = link_cost[(node,neighbor)]
    dv = tab[neighbor]
    local_dv = tab[node]

    # print("local dv: ", local_dv)
    # print("remote dv:", dv)
    
    for n in dv:
        if n == node:
            continue
        if dv[n] == float('inf'):
            continue
        
        try:
            current_cost = local_dv[n][0]

            if current_cost > cost_to_neighbor + dv[n][0]:
                # we learned about a cheaper route via this neighbor
                # print("Updating at {} via neighbor {} to node {}, {}, {}, {}".format(
                #     node, neighbor, n, current_cost, cost_to_neighbor, dv[n]))
                tab[node][n] = (cost_to_neighbor + dv[n][0], neighbor)
        except TypeError:
            # print ("new entry found: at {} via  {} to  {}, cost {}".format(node, neighbor, n, cost_to_neighbor + dv[n][0]))
            tab[node][n] = (cost_to_neighbor + dv[n][0], neighbor)
            


def latex_output(tab, i, used_link=""):
    """return a LaTeX string represenation of a routing table"""

    column_heads = '|'.join('cc'*len(nodes))

    neighborlist = "&".join(
        "{}&{}".format("via", "Cost")
        for n in nodes
    )

    host_list = " & " + "&".join("\\multicolumn{{2}}{{c|}}{{{}}}".format(n) for n in nodes)

    rows = '\n \\\\'.join(
        destination + " & " + '&'.join(
            # "{} & {}".format(tab[source][destination][1], tab[source][destination][0])
            "--- & ---" if tab[source][destination] == float('inf') else 
            "{} & {} ".format(str(tab[source][destination][1]), tab[source][destination][0])            
            # for source in initial_routing_tables[destination]
            # columns: 
            for source in nodes 
        )
        # rows: 
        for destination in nodes
        )
    
    template = f"""
\\begin{{table}}
    \caption{{Distance vector  routing example, step {i}{used_link} }}
    \label{{tab:dv:step:{i}}}
\\begin{{tabular}}{{l|{column_heads}}}
    \\toprule
     {host_list} \\\\
    Destination & {neighborlist} \\\\ 
    \\midrule
    {rows}
    \\\\ \\bottomrule 
\\end{{tabular}}
\\end{{table}}
    """

    return template 


print(latex_output(routing_tables, 0, ", initial setup"))


ii = 1 
for i in range(50):
    link_to_update = random.choice(links)
    if link_to_update[0] == link_to_update[1]:
        continue

    update_node_with_dv (routing_tables, link_to_update[0], link_to_update[1])

    print(latex_output(routing_tables, ii,
                       ", update from {} to {}".format(link_to_update[1], link_to_update[0], )))
    ii = ii+1

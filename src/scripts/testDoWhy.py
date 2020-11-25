import pandas as pd
import networkx as nx

from data import flexibo
from dowhy import CausalModel



# we assume:
#   - the markov blanket is that of a performance metric
#   - performance metrics have no causal effect on configuration options
#   - configuration options are independent of each other
# we conclude that the members of the markov blanket are the parents of the performance metric
#
def mb_as_networkx_graph():
  G = nx.Graph()
  G.add_nodes_from()

if __name__ == '__main__':
  configurations, responses = flexibo.get_processed()
  # restrict experiment to one response for now
  responses = [responses[0]]
  # get markov blankets for each response
  mbs = flexibo.markov_blankets((configurations, responses))
  # get power sets for markov blankets for each response
  mbs_power_set = flexibo.power_set_of_mbs(mbs)


  # graph

  # create casual graph
  # model = CausalModel(
  #   data = flexibo_data,
  #   graph=

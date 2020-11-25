from utils.plot import dot_to_matplotlib

from ananke.graphs import ADMG
from ananke.identification import OneLineID
from ananke.estimation import CausalEffect
from ananke.datasets import load_afixable_data
from ananke.estimation import AutomatedIF

# create a casual graph from a markov blanket, where we know the target
# variable has no children. This allows us to assume the MB consists
# of parents of the target variable.
def childless_mb_to_causal_graph(target, mb):
  vertices = [target] + mb
  di_edges = [(x, target) for x in mb]
  bi_edges = []
  G = ADMG(vertices, di_edges, bi_edges)
  return G


if __name__ == '__main__':

  #####
  # Create a causal graph
  vertices = ['Income', 'Insurance', 'ViralLoad', 'Education', 'T', 'Toxicity', 'CD4']
  di_edges = [('ViralLoad', 'Income'), ('ViralLoad', 'T'), ('ViralLoad', 'Toxicity'),
              ('Education', 'Income'), ('Education', 'T'), ('Education', 'Toxicity'),
              ('Income', 'Insurance'), ('Insurance', 'T'), ('T', 'Toxicity'), ('Toxicity', 'CD4'), ('T', 'CD4')]
  bi_edges = [('Income', 'T'), ('Insurance', 'ViralLoad'), ('Education', 'CD4')]
  G = ADMG(vertices, di_edges, bi_edges)
  dot_to_matplotlib(G.draw(direction="LR"))

  # Identification of the Causal Effect (ask whether treatment on outcome is identified)
  one_id = OneLineID(graph=G, treatments=['T'], outcomes=['CD4'])
  print(one_id.id())

  # Estimation of the Causal Effect
  # cannot supply multiple treatments
  ace_obj = CausalEffect(graph=G, treatment='T', outcome='CD4')  # setting up the CausalEffect object

  data = load_afixable_data()  # load some pre-simulated data
  ace_ipw = ace_obj.compute_effect(data, "ipw")
  ace_gformula = ace_obj.compute_effect(data, "gformula")
  ace_aipw = ace_obj.compute_effect(data, "aipw")
  ace_eff = ace_obj.compute_effect(data, "eff-aipw")
  print("ace using IPW = ", ace_ipw)
  print("ace using g-formula = ", ace_gformula)
  print("ace using AIPW = ", ace_aipw)
  print("ace using efficient AIPW = ", ace_eff)
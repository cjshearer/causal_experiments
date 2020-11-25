from itertools import chain, combinations
import pandas as pd


# returns a dataframe containing rows as target variables, columns as algorithms for MB discover, and entries as MBs
def get_markov_blankets(configurations, responses, algorithms, pvalue=0.05):
  # list of dataframes
  mbs = []
  algorithm_names = [a.__name__ for a in algorithms]
  for response in responses:
    response_mbs = []
    for algorithm in algorithms:
      # join configurations with current response
      conf_and_resp = pd.concat([configurations, response], axis='columns')
      response_idx = conf_and_resp.shape[1]-1
      # find MB for current response and algorithm
      mb, _ = algorithm(conf_and_resp, response_idx, pvalue, False)
      response_mbs.append([mb])
    mbs.append(pd.DataFrame(response_mbs, index=algorithm_names, columns=response.columns.values))
  return mbs


# https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
def _power_set(mb_as_series):
  """non-empty powerset([1,2,3]) --> (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
  s = mb_as_series.values[0]
  # don't include empty set by starting range at 1
  subsets_as_tuples = chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))
  subsets_as_lists = [list(c) for c in list(subsets_as_tuples)]
  return subsets_as_lists


# returns a dataframe which contained MBs of target variable with the subsets of the MBs
# without repeating
def get_power_set_of_mbs(list_of_dfs_of_mbs):
  list_of_dfs_of_subsets_of_mbs = []
  for df_of_mbs in list_of_dfs_of_mbs:
    df_of_mbs.iloc[:, 0] = df_of_mbs.apply(_power_set, axis=1)
    list_of_dfs_of_subsets_of_mbs.append(df_of_mbs)
  return list_of_dfs_of_subsets_of_mbs


  # df_subsets = pd.DataFrame()
  # for row in range(len(df.index)):
  #   unique_subsets = []
  #   for mb_col in mb_idxs:
  #     mb = df.iloc[row,mb_col]
  #     unique_subsets = unique_subsets + [x for x in _powerset(mb) if x not in unique_subsets]
  #   for subset in unique_subsets:
  #     df[subset] = ""
  # return df
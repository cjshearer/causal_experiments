from utils.markovBlankets import get_markov_blankets
from utils.markovBlankets import get_power_set_of_mbs

from pyCausalFS.CBD.MBs.GSMB import GSMB
from pyCausalFS.CBD.MBs.IAMB import IAMB
from pyCausalFS.CBD.MBs.inter_IAMB import inter_IAMB
from pyCausalFS.CBD.MBs.HITON.HITON_MB import HITON_MB

from pathlib import Path
import pandas as pd
from re import search


data_path = Path(__file__).parent.parent.parent/'data/raw/flexibo'
data_files = ["tx2_sampled_output_inceptionv3_200x200.csv",  # [s1,w1]
              "tx2_sampled_output_inceptionv3_400x400.csv",  # [s1,w2]
              "tx2_sampled_output_inceptionv3_600x600.csv",  # [s1,w3]
              "tx2_sampled_output_inceptionv3_800x800.csv",  # [s1,w4]
              "tx2_sampled_output_xception_200x200.csv",  # [s2,w1]
              "tx2_sampled_output_xception_400x400.csv",  # [s2,w2]
              "tx2_sampled_output_xception_600x600.csv",  # [s2,w3]
              "tx2_sampled_output_xception_800x800.csv"  # [s2,w4]
              ]
# indices from which to extract configuration options and responses from raw data
conf_raw_idxs = slice(6,15)
resp_raw_idxs = slice(15,17)


def select_configurations_from_raw(df):
  return df.iloc[:, conf_raw_idxs]


def select_responses_from_raw(df):
  return df.iloc[:, resp_raw_idxs]


def get_processed():
  responses = []
  configurations = None
  for file in data_files:
    df = pd.read_csv((data_path/file).resolve())
    # get configurations from first file (confs should be identical across files)
    if configurations is None:
      configurations = select_configurations_from_raw(df)
    # rename response columns to include their filenames
    try:
      # get substring between 'output_' and '.csv'
      name_from_file = search('output_(.+?).csv', file).group(1)
    except AttributeError:
      print("Could not find substring between 'output_' and '.csv' in file name")

    df = df.rename(columns={'inference_time': 'inference_time_'+name_from_file,
                            'power_consumption': 'power_consumption_'+name_from_file})
    df_responses = select_responses_from_raw(df)
    for response_name in df_responses:
      responses.append(df_responses[[response_name]])
  return configurations, responses


# given a dataframe of configurations and a list of 1 column dataframes as responses, returns list of
# dataframes containing markov blankets for each markov blanket algorithm supplied
def markov_blankets(configurations_and_responses=get_processed(),
                    algorithms=[GSMB, IAMB, inter_IAMB, HITON_MB],
                    pvalue=0.05):
  configurations, responses = configurations_and_responses
  return get_markov_blankets(configurations, responses, algorithms, pvalue)


# given a list of 1 column dataframes containing markov blankets in each row/for each MB algorithm, returns
# a list of 1 column dataframes containing a list of non-empty subsets of the markov blankets
def power_set_of_mbs(list_of_dfs_of_mbs=markov_blankets()):
  return get_power_set_of_mbs(list_of_dfs_of_mbs)


if __name__ == '__main__':
  # load and process raw flexibo data
  configurations, responses = get_processed()
  # get markov blankets for each response
  mbs = markov_blankets((configurations, responses))
  # get power sets for markov blankets for each response
  mbs_power_set = power_set_of_mbs(mbs)
  print(mbs_power_set)
  # print(configurations.add(responses[0], axis='rows').columns.values)
  # process and load raw flexibo data
  # data = get_processed()
  # print(data.head(5))
  # algorithms = [GSMB, IAMB, inter_IAMB, HITON_MB]
  # target_idxs = list(range(9, 25))
  #
  # MBs = get_markov_blankets(data, algorithms, target_idxs)
  #
  # # convert MB functions to their names
  # algorithms = list(map(lambda x: x.__name__, algorithms))
  #
  # pd.set_option('display.max_columns', None)
  # # print(MBs.head(10))
  #
  # print(get_unique_subsets_of_mbs(MBs, [2, 3, 4, 5]))
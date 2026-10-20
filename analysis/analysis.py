"""

Calculation and analytical visualizations for the
Kyoto Penguin Network

"""

# Importing and loading network data
import networkx as nx
import pandas as pd
import sys
from pathlib import Path
import pprint as pp
import seaborn as sns
from pyvis.network import Network
from urllib.parse import quote
import matplotlib.pyplot as plt

# Setting up the loading of the network
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "data"))

from import_network import load_data


penguin_network = load_data()


def printer(centrality_dict,centrality_type):

    """
    Receipt of centrality measures
    
    """

    centrality_dict = {penguin:centrality for penguin,centrality in sorted(centrality_dict.items(),
                                                          key = lambda item: item[1],
                                                          reverse = True)}

    print(f"=========== {centrality_type} CENTRALITY================")
    for penguin,centrality in centrality_dict.items():

        print(f"Penguin: {penguin}")
        print(f"{centrality_type} Centrality: {centrality}")
        print()


######################## Centrality Measures ##########################
### Degree Centrality
degree_centrality = nx.degree_centrality(penguin_network)
# printer(degree_centrality,"DEGREE")

### Betweeness Centrality
between_centrality = nx.betweenness_centrality(penguin_network)
# printer(between_centrality,"BETWEENESS")

# ### PageRank Centrality
# pagerank_centrality = nx.pagerank(penguin_network,alpha = 0.5)

# eigenvector_dist = []

# for _,centrality in pagerank_centrality.items():

#     eigenvector_dist.append(centrality)

# sns.set_theme(style = "dark")
# sns.histplot(x = eigenvector_dist, bins = 20, kde = True, color = "skyblue")
# plt.show()



# printer(pagerank_centrality,"EIGENVECTOR")

# ######################## Degree Definition ##########################
# degree_distribution = nx.degree_histogram(penguin_network)
# sns.set_theme(style = "darkgrid")
# sns.histplot(x = degree_distribution, bins = 10, kde = True, color = "skyblue")
# plt.show()

for u,v data in G
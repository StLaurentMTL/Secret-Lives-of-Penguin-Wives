import networkx as nx
import pandas as pd
from pathlib import Path

# Setting filepath
data_path = Path(__file__).parent / "kyoto_penguins.xlsx"
print(data_path)

def load_data():

    # Loading edgelist and attribute Data
    penguins_edges = pd.read_excel(data_path, sheet_name = "edges")
    penguins_nodes = pd.read_excel(data_path, sheet_name = "nodes")

    # Setting the Penguin Network
    penguin_network = nx.from_pandas_edgelist(penguins_edges,
                                              source = "source_id",
                                              target = "target_id",
                                              edge_attr = "type")


    # Setting node attributes
    node_attributes = penguins_nodes.set_index("id").to_dict(orient = "index")
    nx.set_node_attributes(penguin_network,node_attributes)

    return penguin_network
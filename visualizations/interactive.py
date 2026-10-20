import networkx as nx
import pandas as pd
import sys
from pathlib import Path
import pprint as pp
from pyvis.network import Network
from urllib.parse import quote

# Setting up the loading of the network
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "data"))

from import_network import load_data

penguin_network = load_data()

############# Visualization settings
# Node color by species
NODE_ATTR = "species"
node_colors = {"human": "#E4572E",    # orange-red
               "penguin": "#17BEBB",  # teal
}
default_node_color = "#999999"

# Simple SVG icons, embedded as data URIs
PENGUIN_SVG = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>
<ellipse cx='20' cy='60' rx='6' ry='20' fill='#1B2A3A' transform='rotate(15 20 60)'/>
<ellipse cx='80' cy='60' rx='6' ry='20' fill='#1B2A3A' transform='rotate(-15 80 60)'/>
<ellipse cx='50' cy='56' rx='30' ry='38' fill='#1B2A3A'/>
<ellipse cx='50' cy='65' rx='20' ry='27' fill='#FFFFFF'/>
<circle cx='41' cy='34' r='5' fill='#FFFFFF'/><circle cx='59' cy='34' r='5' fill='#FFFFFF'/>
<circle cx='41' cy='35' r='2.2' fill='#000000'/><circle cx='59' cy='35' r='2.2' fill='#000000'/>
<polygon points='43,42 57,42 50,52' fill='#F6A21E'/>
<ellipse cx='38' cy='95' rx='10' ry='4' fill='#F6A21E'/>
<ellipse cx='62' cy='95' rx='10' ry='4' fill='#F6A21E'/>
</svg>"""

HUMAN_SVG = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>
<path d='M12 98 Q12 56 50 56 Q88 56 88 98 Z' fill='#E4572E'/>
<circle cx='50' cy='30' r='19' fill='#F2C9A0'/>
<path d='M30 28 Q50 0 70 28 Q50 14 30 28 Z' fill='#4A3426'/>
<circle cx='43' cy='32' r='2' fill='#222'/><circle cx='57' cy='32' r='2' fill='#222'/>
<path d='M44 40 Q50 45 56 40' stroke='#222' stroke-width='1.6' fill='none'/>
</svg>"""

def to_data_uri(svg):
    return "data:image/svg+xml;charset=utf-8," + quote(svg)

node_images = {"penguin": to_data_uri(PENGUIN_SVG),
               "human": to_data_uri(HUMAN_SVG)}

# Edge color by relationship type
edge_colors = {"friend": "#2E86AB",
               "romantic_interest": "#F6AE2D",
               "spouse": "#D7263D",
               "enemy": "#00419D",
               "parent":"#018E14",
               "love":"#850505",
               "ex":"#F292FF",
               "sibling":"#9DE79A"}

default_edge_color = "#BBBBBB"

# Setting node size by degree
degrees = dict(penguin_network.degree())
min_deg, max_deg = min(degrees.values()), max(degrees.values())
min_size, max_size = 10, 50

def scale_size(d):
    if max_deg == min_deg:
        return (min_size + max_size) / 2
    return min_size + (d - min_deg) / (max_deg - min_deg) * (max_size - min_size)

# Apply node styling
for node, data in penguin_network.nodes(data=True):
    category = str(data.get(NODE_ATTR, "")).strip().lower()
    data["color"] = node_colors.get(category, default_node_color)
    data["size"] = scale_size(degrees[node])
    data["label"] = str(data.get("name", node))  # uses "name" column if present
    data["title"] = f"""{data['label']} 
                        {NODE_ATTR}: {category} 
                        degree: {degrees[node]}"""

    # Species icon (unknown species fall back to a plain colored dot)
    if category in node_images:
        data["shape"] = "image"
        data["image"] = node_images[category]

# Apply edge styling
for u, v, data in penguin_network.edges(data=True):
    edge_type = str(data.get("type", "")).strip().lower()
    data["color"] = edge_colors.get(edge_type, default_edge_color)
    data["title"] = f"Relationship Type: {edge_type}"

"""
Visualizing with Pyvis, which creates an html

"""

# Initializing a "net" object
net = Network(height = "1200px",
              width = "100%",
              directed = True,
              cdn_resources = "remote")

net.from_nx(penguin_network)
# Build the legend from the types that actually appear in the graph
used_types = sorted({str(d.get("type", "")).strip().lower()
                     for _, _, d in penguin_network.edges(data=True)})

edge_rows = "".join(
    f'<div style="display:flex;align-items:center;margin:4px 0;">'
    f'<span style="display:inline-block;width:28px;height:4px;'
    f'background:{edge_colors.get(t, default_edge_color)};margin-right:8px;"></span>'
    f'{t if t else "unknown"}</div>'
    for t in used_types
)

node_rows = "".join(
    f'<div style="display:flex;align-items:center;margin:4px 0;">'
    f'<img src="{node_images[label]}" style="width:22px;height:22px;margin-right:8px;">'
    f'{label}</div>'
    for label in node_colors
    if label in node_images
)

legend_html = f"""
<div style="position:fixed;top:15px;left:15px;z-index:1000;background:rgba(255,255,255,0.92);
            border:1px solid #ccc;border-radius:6px;padding:10px 14px;
            font-family:sans-serif;font-size:13px;color:#222;">
  <div style="font-weight:bold;margin-bottom:4px;">Edges</div>
  {edge_rows}
  <div style="font-weight:bold;margin:10px 0 4px;">Nodes</div>
  {node_rows}
</div>
"""

html = net.generate_html()
html = html.replace("</body>", legend_html + "</body>")

with open("kyoto_pengys.html", "w", encoding="utf-8") as f:
    f.write(html)
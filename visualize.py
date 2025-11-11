import os
import graphviz
from alpha_miner import  AlphaMinerFrequencies

# Manually set the path to the Graphviz "bin" directory
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

def visualize_model(miner: AlphaMinerFrequencies, output_path="model.dot"):
    """Generate a DOT file for the discovered Petri net model."""

    dot = graphviz.Digraph(format="png")

    # Add places
    for p in miner.P_w:
        dot.node(p, shape="circle")

    # Add transitions
    for t in miner.T_w:
        dot.node(t, shape="box")

    # Add arcs (flows)
    for src, tgt in miner.F_w:
        dot.edge(src, tgt)

    # Save the file
    dot.render(output_path, view=False)
    print(f"Model visualized and saved to {output_path}.png")

if __name__ == "__main__":

    miner = AlphaMinerFrequencies(abs_threshold=1, rel_threshold=0.4)
    miner.run("data/BPI_Challenge_2012.xes")

    visualize_model(miner)
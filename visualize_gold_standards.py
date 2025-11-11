import os
import graphviz
from utils.gold_standards import standards

# Optional: Add Graphviz to PATH (for Windows compatibility)
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

def visualize_gold_standard(model, output_dir="outputs/gold_standards"):
    """Visualize a gold standard Petri net using Graphviz."""
    os.makedirs(output_dir, exist_ok=True)

    dot = graphviz.Digraph(format="png")
    dataset_name = model.dataset_name.replace(".xes", "")

    # Add transitions (activities) as boxes
    for t in model.activities:
        dot.node(t, shape="box", style="filled", fillcolor="#f0f0f0")

    # Add places (circles)
    for i, (inputs, outputs) in enumerate(model.places, start=1):
        place_name = f"p{i}"
        dot.node(place_name, shape="circle")

        # Connect transitions → place
        for a in inputs:
            dot.edge(a, place_name)
        # Connect place → transitions
        for b in outputs:
            dot.edge(place_name, b)

    # Add start and end place indicators
    dot.node("i_L", shape="circle", style="filled", fillcolor="#b2fab4")
    for a in model.start_activities:
        dot.edge("i_L", a)

    dot.node("o_L", shape="circle", style="filled", fillcolor="#ffb2b2")
    for a in model.end_activities:
        dot.edge(a, "o_L")

    # Render the diagram
    output_path = os.path.join(output_dir, f"{dataset_name}_gold_standard")
    dot.render(output_path, view=False)
    print(f"Gold standard for {dataset_name} saved to {output_path}.png")

def visualize_all_gold_standards():
    """Generate visualizations for all gold standards."""
    for name, model in standards.items():
        visualize_gold_standard(model)

if __name__ == "__main__":
    visualize_all_gold_standards()

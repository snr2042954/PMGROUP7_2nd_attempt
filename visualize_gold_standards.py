"""
Visualize Gold Standard Petri Nets
Converts gold standard models to PM4Py Petri nets for professional visualization.
"""

import os
from utils.gold_standards import standards, GoldStandardModel

try:
    import pm4py
    from pm4py.objects.petri_net.obj import PetriNet as PM4PyPetriNet, Marking
    from pm4py.objects.petri_net.utils import petri_utils
    from pm4py.visualization.petri_net import visualizer as pn_visualizer
    PM4PY_AVAILABLE = True
except ImportError:
    PM4PY_AVAILABLE = False
    print("⚠️  PM4Py not available. Install with: pip install pm4py")


def gold_standard_to_pm4py_petri_net(gold_standard):
    """
    Convert a GoldStandardModel to a PM4Py Petri net for professional visualization.
    
    Args:
        gold_standard: GoldStandardModel instance
        
    Returns:
        Tuple of (PM4PyPetriNet, initial_marking, final_marking)
    """
    if not PM4PY_AVAILABLE:
        raise ImportError("PM4Py is required for visualization")
    
    # Create PM4Py Petri net
    net = PM4PyPetriNet(name=gold_standard.dataset_name)
    
    # Add all transitions (activities)
    transitions = {}
    for activity in gold_standard.activities:
        trans = petri_utils.add_transition(net, name=activity, label=activity)
        transitions[activity] = trans
    
    # Add start place (source)
    source_place = petri_utils.add_place(net, name="source")
    
    # Add end place (sink)
    sink_place = petri_utils.add_place(net, name="sink")
    
    # Add arcs from start place to start activities
    for activity in gold_standard.start_activities:
        petri_utils.add_arc_from_to(source_place, transitions[activity], net)
    
    # Add arcs from end activities to end place
    for activity in gold_standard.end_activities:
        petri_utils.add_arc_from_to(transitions[activity], sink_place, net)
    
    # Add internal places and their arcs
    for idx, (input_acts, output_acts) in enumerate(gold_standard.places):
        place_name = f"p{idx+1}"
        place = petri_utils.add_place(net, name=place_name)
        
        # Add arcs from input activities to this place
        for activity in input_acts:
            petri_utils.add_arc_from_to(transitions[activity], place, net)
        
        # Add arcs from this place to output activities
        for activity in output_acts:
            petri_utils.add_arc_from_to(place, transitions[activity], net)
    
    # Create initial and final markings
    initial_marking = Marking()
    initial_marking[source_place] = 1
    
    final_marking = Marking()
    final_marking[sink_place] = 1
    
    return net, initial_marking, final_marking


# Removed gold_standard_to_petri_net function as it depends on non-existent PetriNet class
# Using only PM4Py visualization


def visualize_all_gold_standards(output_dir: str = "results/gold_standard_visualizations", format: str = "png"):
    """
    Generate visualizations for all gold standard models using PM4Py.
    
    Args:
        output_dir: Directory to save visualization files
        format: Output format ('png', 'svg', 'pdf')
    """
    if not PM4PY_AVAILABLE:
        print("❌ PM4Py is required for visualization. Install with: pip install pm4py")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 80)
    print(f"GOLD STANDARD PETRI NET VISUALIZATION (PM4Py - {format.upper()})")
    print("=" * 80)
    print()
    
    for dataset_name, gold_standard in standards.items():
        
        print(f"📊 {dataset_name}")
        print(f"   Figure: {gold_standard.textbook_figure}")
        print(f"   Description: {gold_standard.description}")
        
        try:
            # Convert to PM4Py Petri net
            pm4py_net, initial_marking, final_marking = gold_standard_to_pm4py_petri_net(gold_standard)
            
            # Get statistics
            print(f"   Structure: {len(pm4py_net.places)} places, {len(pm4py_net.transitions)} transitions, {len(pm4py_net.arcs)} arcs")
            
            # Save visualization
            safe_name = dataset_name.replace(".xes", "")
            output_filename = os.path.join(output_dir, f"{safe_name}_gold_standard.{format}")
            
            # Use PM4Py's visualizer with transparent background
            parameters = {
                "bgcolor": "transparent"  # Remove background
            }
            gviz = pn_visualizer.apply(pm4py_net, initial_marking, final_marking, parameters=parameters)
            gviz.format = format  # Set output format
            pn_visualizer.save(gviz, output_filename)
            
            print(f"   ✅ Saved: {output_filename}")
            print()
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print()
    
    print("=" * 80)
    print(f"All {format.upper()} files saved to: {output_dir}")
    print(f"Open {format.upper()} files in a browser or image viewer to see the visualizations")
    print()


def visualize_single_gold_standard(dataset_name: str, output_dir: str = "results/gold_standard_visualizations", format: str = "png"):
    """
    Generate visualization for a single gold standard model using PM4Py.
    
    Args:
        dataset_name: Name of the dataset (e.g., "L1.xes")
        output_dir: Directory to save visualization file
        format: Output format ('png', 'svg', 'pdf')
    """
    if not PM4PY_AVAILABLE:
        print("❌ PM4Py is required for visualization. Install with: pip install pm4py")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get gold standard
    if dataset_name not in standards:
        print(f"❌ No gold standard found for {dataset_name}")
        print(f"Available datasets: {', '.join(standards.keys())}")
        return
    
    gold_standard = standards[dataset_name]
    
    print(f"📊 Visualizing: {dataset_name}")
    print(f"   Figure: {gold_standard.textbook_figure}")
    print(f"   Description: {gold_standard.description}")
    print()
    
    try:
        # Convert to PM4Py Petri net
        pm4py_net, initial_marking, final_marking = gold_standard_to_pm4py_petri_net(gold_standard)
        
        # Get statistics
        print(f"   Structure: {len(pm4py_net.places)} places, {len(pm4py_net.transitions)} transitions, {len(pm4py_net.arcs)} arcs")
        print()
        
        # Save visualization
        safe_name = dataset_name.replace(".xes", "")
        output_filename = os.path.join(output_dir, f"{safe_name}_gold_standard.{format}")
        
        # Use PM4Py's visualizer with transparent background
        parameters = {
            "bgcolor": "transparent"  # Remove background
        }
        gviz = pn_visualizer.apply(pm4py_net, initial_marking, final_marking, parameters=parameters)
        gviz.format = format  # Set output format
        pn_visualizer.save(gviz, output_filename)
        
        print(f"✅ {format.upper()} file saved: {output_filename}")
        print(f"📸 Open in browser or image viewer to see the visualization")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Visualize specific dataset
        dataset_name = sys.argv[1]
        if not dataset_name.endswith(".xes"):
            dataset_name += ".xes"
        visualize_single_gold_standard(dataset_name)
    else:
        # Visualize all gold standards
        visualize_all_gold_standards()


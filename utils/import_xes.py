"""
Two separate import functions because our method and the PM4PY method both expect different formats
Both clean the names to have spaces replaced by underscores, i.e.: "this place" would become "this_place"
"""

import xml.etree.ElementTree as ET
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.util import sorting
from pm4py.objects.log.obj import EventLog, Event, Trace

def read_xes(path, only_complete=True):
    """Parse XES log into {case_id: [activities]}."""
    tree = ET.parse(path)
    root = tree.getroot()

    ns = root.tag.split("}")[0] + "}" if "}" in root.tag else ""
    log = {}

    for trace in root.findall(f"{ns}trace"):
        case_id = None
        events = []

        for s in trace.findall(f"{ns}string"):
            if s.attrib.get("key") == "concept:name":
                case_id = s.attrib.get("value")
                break
        if case_id is None:
            case_id = f"case_{len(log)+1}"

        for e in trace.findall(f"{ns}event"):
            name, lifecycle = None, None
            for s in e.findall(f"{ns}string"):
                key, val = s.attrib["key"], s.attrib["value"]
                if key == "concept:name":
                    name = val
                elif key == "lifecycle:transition":
                    lifecycle = val.lower()

            if not only_complete or lifecycle is None or lifecycle == "complete":
                if name:
                    events.append(name)

        if events:
            log[case_id] = events

    # Clean activity names
    cleaned_log = {}
    for case_id, activities in log.items():
        cleaned_activities = [activity.replace(" ", "_") for activity in activities]
        cleaned_log[case_id] = cleaned_activities

    return log




def read_xes_pm4py(path: str, only_complete: bool = True) -> EventLog:
    """Import a XES log with PM4Py and clean activity names."""

    # Import XES file
    log = xes_importer.apply(path)

    cleaned_log = EventLog()

    for trace in log:
        new_trace = Trace()
        # Copy trace attributes (case ID, etc.)
        new_trace.attributes.update(trace.attributes)

        for event in trace:
            # Lifecycle and activity filtering
            lifecycle = event.get("lifecycle:transition", "").lower()
            if only_complete and lifecycle not in ("", "complete"):
                continue

            new_event = Event(dict(event))  # copy original event

            # Clean activity name
            if "concept:name" in new_event:
                new_event["concept:name"] = new_event["concept:name"].replace(" ", "_")

            new_trace.append(new_event)

        if len(new_trace) > 0:
            cleaned_log.append(new_trace)

    # Sort events by timestamp (PM4Py best practice)
    cleaned_log = sorting.sort_timestamp(cleaned_log)

    return cleaned_log



if __name__ == "__main__":

    FOLDER = "../data/"
    DATASET = "L1.xes"

    log_our_method = read_xes(FOLDER+DATASET, only_complete=True)
    log_pm4py_method = read_xes_pm4py(FOLDER+DATASET, only_complete=True)
    print(f"{log_our_method=}")
    print(f"{log_pm4py_method=}")
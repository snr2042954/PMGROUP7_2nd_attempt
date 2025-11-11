import xml.etree.ElementTree as ET

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

    return log
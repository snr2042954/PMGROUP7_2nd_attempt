"""
Creates a GoldStandardModel class and fills it in 'standards' which is a dictionary of such objects
"""


from typing import Set, List, Tuple
from dataclasses import dataclass

@dataclass
class GoldStandardModel:
    """Represents a gold standard Petri net model from textbook."""
    dataset_name: str
    textbook_figure: str
    description: str

    # Expected model structure
    activities: Set[str]
    start_activities: Set[str]
    end_activities: Set[str]
    places: List[Tuple[Set[str], Set[str]]]  # (input_activities, output_activities)
    direct_succession: Set[Tuple[str, str]]

    # Model statistics for comparison
    expected_places_count: int
    expected_transitions_count: int
    expected_arcs_count: int

standards = {}

standards["L1.xes"] = GoldStandardModel(
    dataset_name="L1.xes",
    textbook_figure="Fig. 6.1",
    description="After a: p1→{b,e}, p2→{c,e}; {b,e}→p3→d, {c,e}→p4→d",
    activities={"a", "b", "c", "d", "e"},
    start_activities={"a"},
    end_activities={"d"},
    places=[
        # p1: After a, enables both b and e (upper branch)
        ({"a"}, {"b", "e"}),
        # p2: After a, enables both c and e (lower branch)
        ({"a"}, {"c", "e"}),
        # p3: After b and e (both required), enables d
        ({"b", "e"}, {"d"}),
        # p4: After c and e (both required), enables d
        ({"c", "e"}, {"d"}),
    ],
    direct_succession={
        ("a", "b"), ("a", "c"), ("a", "e"),  # a enables b, c, and e through places
        ("b", "d"), ("e", "d"), ("c", "d"),  # b, e, c all lead to d through places
    },
    expected_places_count=6,  # 4 internal + i_L + o_L
    expected_transitions_count=5,
    expected_arcs_count=16  # based on textbook figure
)


standards["L2.xes"] = GoldStandardModel(
    dataset_name="L2.xes",
    textbook_figure="Fig. 6.2",
    description="a→{p1,p2}; p1→b→p3→{e,d}; p2→c→p4→{e,d}; e→p5→f→{p1,p2} (loop)",
    activities={"a", "b", "c", "d", "e", "f"},
    start_activities={"a"},
    end_activities={"d"},
    places=[
        ({"a", "f"}, {"b"}),
        ({"a", "f"}, {"c"}),
        ({"b"}, {"e", "d"}),
        ({"c"}, {"e", "d"}),
        ({"e"}, {"f"}),
    ],
    direct_succession={
        ("a", "b"), ("a", "c"),
        ("b", "e"), ("b", "d"),
        ("c", "e"), ("c", "d"),
        ("e", "f"),
        ("f", "b"), ("f", "c"),
    },
    expected_places_count=7,  # 5 internal + i_L + o_L
    expected_transitions_count=6,
    expected_arcs_count=18
)

standards["L3.xes"] = GoldStandardModel(
    dataset_name="L3.xes",
    textbook_figure="Fig. 6.5",
    description="a→p1→b→{p2,p3}→{c,d}→{p4,p5}→e→p6→{f,g}; f loops to p1",
    activities={"a", "b", "c", "d", "e", "f", "g"},
    start_activities={"a"},
    end_activities={"g"},
    places=[
        ({"a", "f"}, {"b"}),
        ({"b"}, {"c"}),
        ({"b"}, {"d"}),
        ({"c"}, {"e"}),
        ({"d"}, {"e"}),
        ({"e"}, {"f", "g"}),
    ],
    direct_succession={
        ("a", "b"),
        ("b", "c"), ("b", "d"),
        ("c", "e"), ("d", "e"),
        ("e", "f"), ("e", "g"),
        ("f", "b"),  # loop back
    },
    expected_places_count=8,  # 6 internal + i_L + o_L
    expected_transitions_count=7,
    expected_arcs_count=16
)

standards["L4.xes"] = GoldStandardModel(
    dataset_name="L4.xes",
    textbook_figure="Fig. 6.6",
    description="Start→{a,b}→p1→c→p2→{d,e}→End",
    activities={"a", "b", "c", "d", "e"},
    start_activities={"a", "b"},
    end_activities={"d", "e"},
    places=[
        ({"a", "b"}, {"c"}),
        ({"c"}, {"d", "e"}),
    ],
    direct_succession={
        ("a", "c"), ("b", "c"),
        ("c", "d"), ("c", "e"),
    },
    expected_places_count=4,  # 2 internal + i_L + o_L
    expected_transitions_count=5,
    expected_arcs_count=10
)

standards["L5.xes"] = GoldStandardModel(
    dataset_name="L5.xes",
    textbook_figure="Fig. 6.8",
    description="a→{p1,p2}; p1→e→p5→f; p2→b→p4→{c,f}; c→p3→d→p2 (loop)",
    activities={"a", "b", "c", "d", "e", "f"},
    start_activities={"a"},
    end_activities={"f"},
    places=[
        ({"a"}, {"e"}),
        ({"a", "d"}, {"b"}),
        ({"c"}, {"d"}),
        ({"b"}, {"c", "f"}),
        ({"e"}, {"f"}),
    ],
    direct_succession={
        ("a", "e"), ("a", "b"),
        ("e", "f"),
        ("b", "c"), ("b", "f"),
        ("c", "d"),
        ("d", "b"),  # loop back
    },
    expected_places_count=7,  # 5 internal + i_L + o_L
    expected_transitions_count=6,
    expected_arcs_count=14
)


standards["L6.xes"] = GoldStandardModel(
    dataset_name="L6.xes",
    textbook_figure="Fig. 6.9",
    description="Complete WF-net WITH redundant places p6 and p7 as shown in textbook",
    activities={"a", "b", "c", "d", "e", "f", "g"},
    start_activities={"a", "b"},
    end_activities={"g"},
    places=[
        ({"a"}, {"c"}),
        ({"a"}, {"e"}),
        ({"b"}, {"d"}),
        ({"b"}, {"f"}),
        ({"c", "d"}, {"g"}),
        ({"d", "e"}, {"g"}),
        ({"c", "f"}, {"g"}),
        ({"e", "f"}, {"g"}),
    ],
    direct_succession={
        ("a", "c"), ("a", "e"),
        ("b", "d"), ("b", "f"),
        ("c", "g"), ("d", "g"), ("e", "g"), ("f", "g"),  # all can reach g
    },
    expected_places_count=10,  # 8 internal + i_L + o_L
    expected_transitions_count=7,  # a,b,c,d,e,f,g
    expected_arcs_count=28  # includes all connections with redundant places
)

standards["L7.xes"] = GoldStandardModel(
    dataset_name="L7.xes",
    textbook_figure="Fig. 6.10-6.11",
    description="Short loop: a→{b,c}, b can loop to itself (b*), then c",
    activities={"a", "b", "c"},
    start_activities={"a"},
    end_activities={"c"},
    places=[
        ({"a", "b"}, {"b", "c"}),
    ],
    direct_succession={
        ("a", "b"), ("a", "c"),  # a can go to b or c
        ("b", "b"),  # b can loop to itself (short loop)
        ("b", "c"),  # b can proceed to c
    },
    expected_places_count=3,  # 1 internal + i_L + o_L
    expected_transitions_count=3,
    expected_arcs_count=8  # includes self-loop arcs
)

standards["running-example.xes"] = GoldStandardModel(
    dataset_name="running-example.xes",
    textbook_figure="Fig. 2.6",
    description="Insurance claim: register→{b||c}+d→(AND-join)→decide→{pay|reject|reinitiate}",
    activities={
        "register request", "examine thoroughly", "examine casually", "check ticket",
        "decide", "pay compensation", "reinitiate request", "reject request"
    },
    start_activities={"register request"},
    end_activities={"pay compensation", "reject request"},
    places=[
        ({"register request"}, {"examine thoroughly", "examine casually"}),
        ({"register request", "reinitiate request"}, {"check ticket"}),
        ({"examine thoroughly", "examine casually"}, {"decide"}),
        ({"check ticket"}, {"decide"}),
        ({"decide"}, {"pay compensation", "reject request", "reinitiate request"}),
    ],
    direct_succession={
        ("register request", "examine thoroughly"),
        ("register request", "examine casually"),
        ("register request", "check ticket"),
        ("examine thoroughly", "decide"), ("examine casually", "decide"),  # through c3
        ("check ticket", "decide"),  # through c4
        ("decide", "pay compensation"),
        ("decide", "reject request"),
        ("decide", "reinitiate request"),
        ("reinitiate request", "check ticket"),  # loop back to c2
    },
    expected_places_count=7,  # 5 internal (c1, c2, c3, c4, c5) + start + end
    expected_transitions_count=8,
    expected_arcs_count=22
)


standards["billinstances.xes"] = GoldStandardModel(
    dataset_name="billinstances.xes",
    textbook_figure="Fig.11",
    description="Process P2: write bill -> print bill -> deliver bill (with shared printer)",
    activities={"write bill", "print bill", "deliver bill"},
    start_activities={"write bill"},
    end_activities={"deliver bill"},
    places=[
        ({"write bill"}, {"print bill"}),
        ({"print bill"}, {"deliver bill"}),
    ],
    direct_succession={
        ("write bill", "print bill"), ("print bill", "deliver bill")
    },
    expected_places_count=4,  # 2 + start + end
    expected_transitions_count=3,
    expected_arcs_count=6
)

standards["posterinstances.xes"] = GoldStandardModel(
    dataset_name="posterinstances.xes",
    textbook_figure="Fig.11",
    description="Process P3: receive order and photo -> design photo poster -> print poster -> deliver poster",
    activities={"receive order and photo", "design photo poster", "print poster", "deliver poster"},
    start_activities={"receive order and photo"},
    end_activities={"deliver poster"},
    places=[
        ({"receive order and photo"}, {"design photo poster"}),
        ({"design photo poster"}, {"print poster"}),
        ({"print poster"}, {"deliver poster"}),
    ],
    direct_succession={
        ("receive order and photo", "design photo poster"),
        ("design photo poster", "print poster"),
        ("print poster", "deliver poster")
    },
    expected_places_count=5,  # 3 + start + end
    expected_transitions_count=4,
    expected_arcs_count=8
)

standards["flyerinstances.xes"] = GoldStandardModel(
    dataset_name="flyerinstances.xes",
    textbook_figure="Fig.11",
    description="Process P1: Flyer with customer revision loop (send draft can loop back to design)",
    activities={"receive flyer order", "design flyer", "send draft to customer",
                "print flyer", "deliver flyer"},
    start_activities={"receive flyer order"},
    end_activities={"deliver flyer"},
    places=[
        ({"receive flyer order", "send draft to customer"}, {"design flyer"}),
        ({"design flyer"}, {"send draft to customer"}),
        ({"send draft to customer"}, {"print flyer"}),
        ({"print flyer"}, {"deliver flyer"}),
    ],
    direct_succession={
        ("receive flyer order", "design flyer"),
        ("design flyer", "send draft to customer"),
        ("send draft to customer", "design flyer"),  # Loop back for revisions
        ("send draft to customer", "print flyer"),  # Approved, proceed
        ("print flyer", "deliver flyer")
    },
    expected_places_count=6,  # 4 + start + end
    expected_transitions_count=5,
    expected_arcs_count=12
)


standards["BPI_Challenge_2012.xes"] = GoldStandardModel(
    dataset_name="BPI_Challenge_2012.xes",
    textbook_figure="Empirical-BPI2012",
    description="Real-world loan application process - complete gold standard from discovered model",
    activities={
        "A_SUBMITTED", "A_PARTLYSUBMITTED", "A_PREACCEPTED", "A_ACCEPTED",
        "A_FINALIZED", "A_REGISTERED", "A_CANCELLED", "A_DECLINED",
        "A_APPROVED", "A_ACTIVATED",
        "O_SELECTED", "O_CREATED", "O_SENT", "O_SENT_BACK",
        "O_ACCEPTED", "O_CANCELLED", "O_DECLINED",
        "W_Completeren aanvraag", "W_Valideren aanvraag", "W_Nabellen offertes",
        "W_Nabellen incomplete dossiers", "W_Afhandelen leads",
        "W_Beoordelen fraude", "W_Wijzigen contractgegevens"
    },
    start_activities={"A_SUBMITTED"},
    end_activities={
        "W_Nabellen incomplete dossiers", "O_DECLINED", "O_CANCELLED", "O_ACCEPTED",
        "W_Beoordelen fraude", "A_REGISTERED", "W_Afhandelen leads",
        "W_Nabellen offertes", "A_CANCELLED", "W_Wijzigen contractgegevens",
        "W_Completeren aanvraag", "W_Valideren aanvraag", "A_DECLINED"
    },
    places=[
        ({"A_SUBMITTED"}, {"A_PARTLYSUBMITTED"}),
        ({"A_PARTLYSUBMITTED"}, {"A_PREACCEPTED"}),
        ({"A_PARTLYSUBMITTED"}, {"A_DECLINED"}),
        ({"A_PARTLYSUBMITTED"}, {"W_Valideren aanvraag"}),
        ({"A_PARTLYSUBMITTED"}, {"W_Nabellen incomplete dossiers"}),
        ({"A_PREACCEPTED"}, {"W_Completeren aanvraag"}),
        ({"A_ACCEPTED"}, {"O_SELECTED"}),
        ({"A_ACCEPTED"}, {"A_FINALIZED"}),
        ({"A_ACCEPTED"}, {"O_CANCELLED"}),
        ({"A_ACCEPTED"}, {"A_CANCELLED"}),
        ({"A_ACCEPTED"}, {"W_Wijzigen contractgegevens"}),
        ({"A_ACCEPTED"}, {"A_REGISTERED"}),
        ({"A_ACCEPTED"}, {"W_Afhandelen leads"}),
        ({"O_SELECTED", "A_FINALIZED"}, {"O_CREATED"}),
        ({"O_CREATED"}, {"O_SENT"}),
    ],
    direct_succession={
        ("A_SUBMITTED", "A_PARTLYSUBMITTED"),
        ("A_PARTLYSUBMITTED", "A_PREACCEPTED"),
        ("A_PARTLYSUBMITTED", "A_DECLINED"),
        ("A_PARTLYSUBMITTED", "W_Valideren aanvraag"),
        ("A_PARTLYSUBMITTED", "W_Nabellen incomplete dossiers"),
        ("A_PREACCEPTED", "W_Completeren aanvraag"),
        ("W_Completeren aanvraag", "A_ACCEPTED"),
        ("A_ACCEPTED", "O_SELECTED"),
        ("A_ACCEPTED", "A_FINALIZED"),
        ("A_ACCEPTED", "O_CANCELLED"),
        ("A_ACCEPTED", "A_CANCELLED"),
        ("A_ACCEPTED", "W_Wijzigen contractgegevens"),
        ("A_ACCEPTED", "A_REGISTERED"),
        ("A_ACCEPTED", "W_Afhandelen leads"),
        ("A_ACCEPTED", "W_Nabellen offertes"),
        ("A_ACCEPTED", "W_Beoordelen fraude"),
        ("A_ACCEPTED", "W_Completeren aanvraag"),
        ("O_SELECTED", "O_CREATED"),
        ("A_FINALIZED", "O_CREATED"),
        ("O_CREATED", "O_SENT"),
    },
    expected_places_count=20,  # Based on visible structure
    expected_transitions_count=24,
    expected_arcs_count=60  # Estimated from complex structure
)
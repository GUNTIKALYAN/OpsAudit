from langgraph.graph import StateGraph, END

from app.graph.state import AuditState
from app.graph.nodes import create_node

# Import agents
from app.agents.data_ingestion_agent import run as ingestion_agent
from app.agents.duplicate_agent import run as duplicate_agent
from app.agents.missing_data_agent import run as missing_agent
from app.agents.logic_validation_agent import run as logic_agent
from app.agents.anomaly_agent import run as anomaly_agent
from app.agents.reasoning_agent import run as reasoning_agent
from app.agents.reporting_agent import run as reporting_agent


def build_graph():

    graph = StateGraph(AuditState)

    
    # Register Nodes
    graph.add_node("ingestion", create_node(ingestion_agent))
    graph.add_node("duplicate", create_node(duplicate_agent))
    graph.add_node("missing", create_node(missing_agent))
    graph.add_node("logic", create_node(logic_agent))
    graph.add_node("anomaly", create_node(anomaly_agent))
    graph.add_node("reasoning", create_node(reasoning_agent))
    graph.add_node("reporting", create_node(reporting_agent))

    # Define Flow

    # Entry
    graph.set_entry_point("ingestion")

    # After ingestion → parallel detection agents
    graph.add_edge("ingestion", "duplicate")
    graph.add_edge("ingestion", "missing")
    graph.add_edge("ingestion", "logic")
    graph.add_edge("ingestion", "anomaly")

    # All detection agents → reasoning
    graph.add_edge("duplicate", "reasoning")
    graph.add_edge("missing", "reasoning")
    graph.add_edge("logic", "reasoning")
    graph.add_edge("anomaly", "reasoning")

    # Reasoning → reporting
    graph.add_edge("reasoning", "reporting")

    # End
    graph.add_edge("reporting", END)

    # Compile graph
    return graph.compile()
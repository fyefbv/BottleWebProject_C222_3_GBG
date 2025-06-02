import os
import json
from graph_operations.graph_builder import GraphBuilder

# Пути к JSON с вводом пользователя
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_DATA_FILE = os.path.join(BASE_DIR, "data", "input_data.json")


def _load_json_list(filepath):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []

def get_adjacency_matrix():
    user_entries = _load_json_list(USER_DATA_FILE)

    last = user_entries[-1]
    adjacency_matrix = last.get("adjacency_matrix", [])

    return adjacency_matrix

def get_graph_json(adjacency_matrix):
    builder = GraphBuilder(adjacency_matrix)
    graph_data = builder.to_d3_json()
    graph_json = json.dumps(graph_data)

    return graph_json

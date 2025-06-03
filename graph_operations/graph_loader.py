import json
from graph_operations.graph_builder import GraphBuilder

USER_DATA_FILE = 'data/input_data.json'

# Загружает список из JSON-файла.
def load_json_list(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Сохраняет список в JSON-файл, перезаписывая его.
def save_json_list(filepath, lst):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(lst, f, ensure_ascii=False, indent=2)

# Возвращает матрицу смежности последнего сохранённого графа из input_data.json.
def get_adjacency_matrix():
    user_entries = load_json_list(USER_DATA_FILE)

    last = user_entries[-1]
    adjacency_matrix = last.get("adjacency_matrix", [])

    return adjacency_matrix

# Преобразует матрицу смежности в JSON-строку для D3.js.
def get_graph_json(adjacency_matrix):
    builder = GraphBuilder(adjacency_matrix)
    graph_data = builder.to_d3_json()
    graph_json = json.dumps(graph_data)

    return graph_json

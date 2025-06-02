import os
import json
import datetime
from bottle import request, template, post
from graph_operations.graph_builder import GraphBuilder

# Пути к JSON-файлам
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_DATA_FILE = os.path.join(BASE_DIR, "data", "input_data.json")
ALGORITHM_LOGS = os.path.join(BASE_DIR, "data", "logs.json")

def _load_json_list(filepath):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []

def _save_json_list(filepath, lst):
    folder = os.path.dirname(filepath)
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(lst, f, ensure_ascii=False, indent=2)

@post('/build_graph')
def build_graph_handler():
    """Обрабатывает POST-запрос для построения графа"""
    year = datetime.datetime.now().year

    # 1. Читаем количество вершин
    try:
        vertex_count = int(request.forms.get('vertex-count', 0))
    except (TypeError, ValueError):
        return template('index',
                        title='Главная страница',
                        year=year,
                        graph_json=''
        )

    if vertex_count < 1 or vertex_count > 15:
        return template('index',
                        title='Главная страница',
                        year=year,
                        graph_json=''
        )

    # 2. Собираем матрицу смежности
    adjacency_matrix = []
    for i in range(vertex_count):
        row = []
        for j in range(vertex_count):
            field_name = f"cell-{i}-{j}"
            raw_val = request.forms.get(field_name, '0')
            val = int(raw_val) if raw_val.isdigit() else 0
            val = 1 if val == 1 else 0  # Только 0 или 1
            row.append(val)
        adjacency_matrix.append(row)

    # 3. Сохраняем данные в JSON
    user_entries = _load_json_list(USER_DATA_FILE)
    user_record = {
        "timestamp": datetime.datetime.now().isoformat(),
        "vertex_count": vertex_count,
        "adjacency_matrix": adjacency_matrix
    }
    user_entries.append(user_record)
    _save_json_list(USER_DATA_FILE, user_entries)

    # 4. Строим граф
    try:
        builder = GraphBuilder(adjacency_matrix)
        G = builder.build_graph()
        graph_json = json.dumps(builder.to_d3_json())
    except ValueError:
        return template('index',
                        title='Главная страница',
                        year=year,
                        graph_json=''
        )

    # 5. Логируем рёбра
    log_entries = _load_json_list(ALGORITHM_LOGS)
    run_log = {
        "run_timestamp": datetime.datetime.now().isoformat(),
        "vertex_count": vertex_count,
        "edges_added": [
            {"timestamp": datetime.datetime.now().isoformat(), "action": "add_edge", "from": i, "to": j}
            for i in range(vertex_count) for j in range(vertex_count) if adjacency_matrix[i][j] == 1
        ]
    }
    log_entries.append(run_log)
    _save_json_list(ALGORITHM_LOGS, log_entries)

    # 6. Возвращаем данные для шаблона
    return template('index',
                    title='Главная страница',
                    year=year,
                    graph_json=graph_json)
import json
import datetime
from bottle import request, template, post
from graph_operations.graph_builder import GraphBuilder
from graph_operations.graph_loader import load_json_list, save_json_list

USER_DATA_FILE = 'data/input_data.json'
ALGORITHM_LOGS = 'data/logs.json'

@post('/build_graph')
def index_handler():
    year = datetime.datetime.now().year

    vertex_count = int(request.forms.get('vertex-count', 0))

    # Собираем матрицу смежности
    adjacency_matrix = []
    for i in range(vertex_count):
        row = []
        for j in range(vertex_count):
            raw_val = request.forms.get(f'cell-{i}-{j}', '0')
            try:
                val = int(raw_val)
            except ValueError:
                val = 0
            row.append(1 if val == 1 else 0)
        adjacency_matrix.append(row)

    # Сохраняем введённую матрицу в input_data.json
    user_entries = load_json_list(USER_DATA_FILE)
    user_entries.append({
        "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "vertex_count": vertex_count,
        "adjacency_matrix": adjacency_matrix
    })
    save_json_list(USER_DATA_FILE, user_entries)

    # Строим граф и готовим JSON для D3.js
    try:
        builder = GraphBuilder(adjacency_matrix)
        G = builder.build_graph()
        graph_json = json.dumps(builder.to_d3_json())
    except ValueError:
        return template('index',
                        title='Главная страница',
                        year=year,
                        graph_json='')

    # Логируем добавление рёбер в logs.json
    log_entries = load_json_list(ALGORITHM_LOGS)
    log_entries.append({
        "run_timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "vertex_count": vertex_count,
        "edges_added": [
            {"timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
             "action": "add_edge", "from": i, "to": j}
            for i in range(vertex_count)
            for j in range(vertex_count)
            if adjacency_matrix[i][j] == 1
        ]
    })
    save_json_list(ALGORITHM_LOGS, log_entries)
    print(graph_json)
    # Отдаём шаблон с graph_json
    return template('index',
                    title='Главная страница',
                    year=year,
                    graph_json=graph_json)

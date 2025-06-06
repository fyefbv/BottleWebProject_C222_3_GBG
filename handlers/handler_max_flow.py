import random
import json
import datetime 
from graph_operations.flow_optimizer import MaxFlowFinder 
import networkx as nx
from bottle import request, template, post, response
from graph_operations.graph_builder import GraphBuilder
from graph_operations.graph_loader import get_adjacency_matrix, get_graph_json
USER_DATA_FILE = 'data/input_data.json'

@post('/generate_graph')
def generate_graph():
    """Обрабатывает POST-запрос для построения графа для задачи максимального потока"""
    year = datetime.datetime.now().year

    # 1. Читаем количество вершин
    try:
        vertex_count = int(request.forms.get('vertex-count', 0))
    except (TypeError, ValueError):
        return template('max_flow',
                        title='Поиск максимального потока',
                        year=year,
                        graph_json=''
        )

    if vertex_count < 1 or vertex_count > 15:
        return template('max_flow',
                        title='Поиск максимального потока',
                        year=year,
                        graph_json=''

        )

    # 2. Генерация ориентированного графа с «двунаправленными» дугами, затем удаляем одно направление
    def generate_flow_graph(n, cap_min=2, cap_max=10):
        """Генерирует случайный ориентированный граф с истоком (0) и стоком (n-1)"""
        G = nx.DiGraph()
        G.add_nodes_from(range(n))
        
        # 1. Гарантируем, что исток (0) не имеет входящих ребер
        #    и сток (n-1) не имеет исходящих ребер
        
        # 2. Строим случайный DAG (Directed Acyclic Graph) между истоком и стоком
        for i in range(n - 1):
            # Каждая вершина (кроме стока) имеет хотя бы одно исходящее ребро
            if not list(G.successors(i)):  # Если нет исходящих ребер
                j = random.choice(range(i + 1, n))
                G.add_edge(i, j, capacity=random.randint(cap_min, cap_max))
            
            # Добавляем случайные ребра
            for j in range(i + 1, n):
                if random.random() < 0.5:  # 50% вероятность ребра
                    G.add_edge(i, j, capacity=random.randint(cap_min, cap_max))
        
        # 3. Удаляем все входящие в исток (на случай если добавились)
        for u in list(G.predecessors(0)):
            G.remove_edge(u, 0)
        
        # 4. Удаляем все исходящие из стока (на случай если добавились)
        for v in list(G.successors(n - 1)):
            G.remove_edge(n - 1, v)
        
        # 5. Гарантируем связность - находим путь от истока к стоку
        if not nx.has_path(G, 0, n - 1):
            # Если пути нет, добавляем случайный путь
            path = random.sample(range(1, n - 1), random.randint(1, n - 2))
            path = [0] + sorted(path) + [n - 1]
            for u, v in zip(path[:-1], path[1:]):
                G.add_edge(u, v, capacity=random.randint(cap_min, cap_max))
        
        return G

    G = generate_flow_graph(vertex_count, cap_min=2, cap_max=10)

    # 3. Преобразуем в матрицу смежности capacities
    matrix = nx.to_numpy_array(G, weight='capacity', dtype=int).tolist()

    # 4. Возвращаем JSON с матрицей
    response.content_type = 'application/json'
    return json.dumps({
        "matrix": matrix,
        "info": "Граф для задачи максимального потока (исток=0, сток=n-1)"
    })




# @post('/build_graph_max_flow')
# def build_graph_handler():
#     # --response.content_type = 'application/json'
    
#     try:
#         vertex_count = int(request.forms.get('vertex-count', 0))
#     except (TypeError, ValueError):
#         return json.dumps({"error": "Invalid vertex count"})
    
#     if vertex_count < 1 or vertex_count > 15:
#         return json.dumps({"error": "Vertex count out of range (1–15)"})

#     # --Собираем матрицу
#     adjacency_matrix = []
#     for i in range(vertex_count):
#         row = []
#         for j in range(vertex_count):
#             field_name = f"cell-{i}-{j}"
#             raw_val = request.forms.get(field_name, '0')
#             row.append(int(raw_val) if raw_val.isdigit() else 0)
#         adjacency_matrix.append(row)
    
#     print("Матрица для построения:", adjacency_matrix)  # --Для отладки

#     # --Строим граф напрямую
#     try:
#         G = nx.DiGraph()
#         for i in range(vertex_count):
#             G.add_node(i)
        
#         for i in range(vertex_count):
#             for j in range(vertex_count):
#                 if adjacency_matrix[i][j] > 0:
#                     G.add_edge(i, j, weight=adjacency_matrix[i][j])
        
#         graph_json = {
#             "nodes": [{"id": i} for i in range(vertex_count)],
#             "links": [
#                 {"source": u, "target": v, "value": d['weight']}
#                 for u, v, d in G.edges(data=True)
#             ]
#         }
        
#     except Exception as e:
#         return json.dumps({"error": f"Graph build error: {str(e)}"})

#     # --return json.dumps({
#     # --    "timestamp": datetime.datetime.now().isoformat(),
#     # --    "vertex_count": vertex_count,
#     # --    "graph": graph_json
#     # --})

#         # --Строим граф и готовим JSON для D3.js
#     try:
#         builder = GraphBuilder(adjacency_matrix)
#         G = builder.build_graph()
#         graph_json = json.dumps(builder.to_d3_json())


#     except ValueError:
#         return template('index',
#                         title='Главная страница',
#                         year=datetime.datetime.now().year,
#                         graph_json='')


#     graph_json = json.dumps(builder.to_d3_json())
#     print(graph_json)
#     # --Отдаём шаблон с graph_json
#     return template('max_flow',
#                     title='Поиск максимального потока',
#                     year=datetime.datetime.now().year,
#                     graph_json=graph_json,
#                     adjacency_matrix=adjacency_matrix)




# @post('/max_flow')
# def max_flow_detection_handler():
#     year = datetime.datetime.now().year

#     adjacency_matrix = get_adjacency_matrix()
#     graph_json = get_graph_json(adjacency_matrix)

#     # --detector = CycleDetector(adjacency_matrix)
#     # --cycles = detector.find_cycles()





#     # --Возвращаем шаблон с данными
#     return template('max_flow',
#                     title='Поиск максимального потока',
#                     year=year,
#                     graph_json=graph_json,
#                     adjacency_matrix=adjacency_matrix)


#     # --graph_json=graph_json graph_json = ''














@post('/build_graph_max_flow')
def build_graph_handler():
    try:
        vertex_count = int(request.forms.get('vertex-count', 0))
    except (TypeError, ValueError):
        return json.dumps({"error": "Invalid vertex count"})
    
    if vertex_count < 1 or vertex_count > 15:
        return json.dumps({"error": "Vertex count out of range (1–15)"})

    # Собираем матрицу
    adjacency_matrix = []
    for i in range(vertex_count):
        row = []
        for j in range(vertex_count):
            field_name = f"cell-{i}-{j}"
            raw_val = request.forms.get(field_name, '0')
            row.append(int(raw_val) if raw_val.isdigit() else 0)
        adjacency_matrix.append(row)

    # Строим граф для визуализации
    try:
        builder = GraphBuilder(adjacency_matrix)
        graph_json = builder.to_d3_json()
        
        # Вычисляем максимальный поток
        flow_finder = MaxFlowFinder(adjacency_matrix)
        flow_data = flow_finder.calculate_max_flow()
        
        # Добавляем информацию о потоке
        graph_json['flow'] = flow_data

    except Exception as e:
        return json.dumps({"error": str(e)})

    return template('max_flow',
                   title='Поиск максимального потока',
                   year=datetime.datetime.now().year,
                   graph_json=json.dumps(graph_json),
                   adjacency_matrix=adjacency_matrix,
                   max_flow_value=flow_data['value'],
                   flow=flow_data)

@post('/max_flow')
def max_flow_detection_handler():
    adjacency_matrix = get_adjacency_matrix()
    
    try:
        builder = GraphBuilder(adjacency_matrix)
        graph_json = builder.to_d3_json()
        
        flow_finder = MaxFlowFinder(adjacency_matrix)
        flow_data = flow_finder.calculate_max_flow()
        
        graph_json['flow'] = flow_data

    except Exception as e:
        return json.dumps({"error": str(e)})

    return template('max_flow',
                   title='Поиск максимального потока',
                   year=datetime.datetime.now().year,
                   graph_json=json.dumps(graph_json),
                   adjacency_matrix=adjacency_matrix,
                   max_flow_value=flow_data['value'],
                   flow=flow_data)
























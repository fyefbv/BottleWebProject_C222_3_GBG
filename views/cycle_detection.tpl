% rebase('layout.tpl', title=title, year=year, adjacency_matrix=adjacency_matrix, graph_json=graph_json, cycles=cycles)

<head>
    <link rel="stylesheet" href="/static/content/pages/cycle_detection.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>

<body>
    <div class="container">
        <header>
            <h1>Поиск циклов в ориентированном графе</h1>
        </header>

        <main class="content">
            <!-- Блок теории -->
            <section class="card">
                <button class="theory-toggle" onclick="toggleTheory()">
                    <span>Теоретический материал</span>
                    <i class="fas fa-chevron-down"></i>
                </button>
                <div id="theory-block" style="display: none; margin-top: 1.5rem;">
                    <h2>Что такое цикл в графе?</h2>
                    <div class="theory-content">
                        <div class="theory-left">
                            <div class="matrix-container">
                                <p class="matrix-label">Матрица смежности:</p>
                                <pre>0 1 0
0 0 1
1 0 0</pre>
                            </div>
                            <img src="/static/images/cyclic_graph.png" alt="Пример графа с циклом" class="example-image">
                        </div>
                        <div class="theory-right">
                            <p><strong>Цикл</strong> — это путь, начинающийся и заканчивающийся в одной и той же вершине, при этом не повторяя рёбра или вершины (кроме начальной и конечной).</p>
                            
                            <div class="property-explanation">
                                <h3><i class="fas fa-redo"></i> Обнаружение цикла</h3>
                                <p>Для поиска циклов в графе можно использовать алгоритмы поиска в глубину (DFS), ведя учёт посещённых вершин и пути обхода.</p>
                            </div>

                            <div class="property-explanation">
                                <h3><i class="fas fa-random"></i> Признаки цикла</h3>
                                <p>Если при обходе графа по DFS происходит возврат к вершине, которая уже находится в стеке рекурсии, это указывает на наличие цикла.</p>
                            </div>

                            <p class="conclusion"><strong>Примечание:</strong> в ориентированном графе цикл считается ориентированным; в неориентированном графе обратные рёбра требуют дополнительной обработки.</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Горизонтальные блоки: входные данные и граф -->
            <div class="data-graph-container">
                <!-- Блок с входными данными -->
                <section class="card input-data">
                    <h2>Входные данные</h2>
                    % if adjacency_matrix:
                        <div class="info-block">
                            <p><strong>Количество вершин:</strong> {{ len(adjacency_matrix) }}</p>
                        </div>
                        <div class="info-block">
                            <p><strong>Матрица смежности:</strong></p>

                            <table class="matrix-table static-matrix">
                                % for row in adjacency_matrix:
                                    <tr>
                                        % for val in row:
                                            <td>{{ val }}</td>
                                        % end
                                    </tr>
                                % end
                            </table>
                        </div>
                    % else:
                        <div class="info-block">
                            <p>Матрица смежности не задана.</p>
                        </div>
                    % end
                </section>

                <!-- Блок с графом -->
                <section class="card graph-area" id="graph-area">
                    <h2>Визуализация графа</h2>
                    % if graph_json:
                        <div id="d3-graph" style="width:100%; height:400px;"></div>
                    % else:
                        <div id="graph-container">
                            <div class="graph-placeholder">
                                <i class="fas fa-project-diagram"></i>
                                <p>Граф будет отображен после анализа</p>
                            </div>
                        </div>
                    % end
                </section>
            </div>


            <!-- Результат поиска циклов -->
            <section class="card result-section">
                <h2>Результат поиска</h2>
                <div class="properties-grid">
                    <div class="property-card">
                        <h3>Количество найденных циклов</h3>
                        <div class="property-result" id="cycle-detected">
                            % if cycles is not None:
                                {{ len(cycles) }}
                            % else:
                                0
                            % end
                        </div>
                        <div class="property-description">
                            Всего циклов
                        </div>
                    </div>

                    <div class="property-card-cycles-list">
                        <h3>Список найденных циклов</h3>
                        <div class="property-result" id="cycle-example">
                            % if cycles:
                                <ul class="cycle-list">
                                    % for c in cycles:
                                        <li>{{ c }}</li>
                                    % end
                                </ul>
                            % else:
                                <p>Циклов не найдено.</p>
                            % end
                        </div>
                        <div class="property-description">
                            Каждая строка – последовательность вершин
                        </div>
                    </div>
                </div>
            </section>
        </main>
    </div>

    <script src="/static/scripts/collapse-block.js"></script>
    <script src="https://d3js.org/d3.v7.min.js"></script>

    % if graph_json:
        <script>
            var graphData = {{!graph_json}};
        </script>
        <script src="/static/scripts/graph.js"></script>
    % end
</body>
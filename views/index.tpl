% rebase('layout.tpl', title='Анализ свойств графа', year=year, graph_json=graph_json)

<head>
    <link rel="stylesheet" href="/static/content/pages/index.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>

<body>
    <div class="container">
        <div class="page-header">
            <h1>Анализ ориентированных графов</h1>
            <button class="scroll-btn" id="scrollToMethods" aria-label="Методы анализа графа">
                <i class="fas fa-diagram-project"></i>
                <span class="tooltip">
                    <span class="tooltip-arrow"></span>
                    Перейти к методам анализа графа
                </span>
            </button>
        </div>

        <div class="layout">
            <!-- Список шаблонов слева -->
            <div class="content-left">
                <aside class="template-aside">
                    <h2>Готовые шаблоны</h2>
                    <ul id="template-list"></ul>
                </aside>

                <aside class="template-aside">
                    <h2>Сохраненные шаблоны</h2>
                    <ul id="save-template-list"></ul>
                </aside>
            </div>

            <!-- Основной контент справа -->
            <main class="content-right">
                <!-- Блок ввода данных графа -->
                <section>
                    <form method="POST" action="/build_graph" class="main-card">
                        <h2>Ввод данных графа</h2>
                        <div class="form-group">
                            <label for="vertex-count">Количество вершин:</label>
                            <input type="number" id="vertex-count" name="vertex-count" min="1" max="15" value="4">
                        </div>
                        <div class="form-group">
                            <label>Матрица смежности:</label>
                            <div id="matrix-container" class="main-matrix-container"></div>
                        </div>
                        <button class="btn action-btn" id="build-graph" type="submit">Построить граф</button>
                        <button class="btn action-btn" id="generate-matrix" type="button">Сгенерировать матрицу</button>
                    </form>
                </section>

                <!-- Блок для построения графа -->
                <section class="main-card graph-area" id="graph-area">
                    <div class="graph-placeholder">
                        <i class="fas fa-diagram-project"></i>
                        <p>Граф будет отображён здесь после построения</p>
                    </div>
                </section>

                <!-- Блок с кнопками перехода к методам -->
                <section id="methods" class="main-card">
                    <h2>Методы анализа графа</h2>
                        <ul class="method-list">
                            <li>
                                <form method="POST" action="/cycle_detection">
                                    <button type="submit" class="btn method-btn">
                                        <span class="method-icon">↻</span>
                                        <span class="method-text">Поиск циклов в графе</span>
                                    </button>
                                </form>
                            </li>
                            <li><a href="/max_flow" class="btn method-btn"><span class="method-icon">⇄</span><span class="method-text">Расчет максимального потока</span></a></li>
                            <li><a href="/equivalence" class="btn method-btn"><span class="method-icon">✓</span><span class="method-text">Анализ отношений эквивалентности</span></a></li>
                        </ul>
                </section>
            </main>
        </div>
    </div>

    <script src="/static/scripts/matrix.js"></script>
    <script src="/static/scripts/scroll.js"></script>
    <script src="/static/scripts/check_graph.js"></script>
    <script src="/static/scripts/templates.js"></script>
    <script src="https://d3js.org/d3.v7.min.js"></script>

    % if graph_json:
        <script>
            var graphData = {{!graph_json}};
        </script>
        <script src="/static/scripts/graph.js"></script>
    % end
</body>
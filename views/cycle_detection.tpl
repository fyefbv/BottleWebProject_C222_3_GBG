% rebase('layout.tpl', title=title, year=year)

<head>
    <link rel="stylesheet" href="/static/content/pages/cycle_detection.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>

<body>
    <div class="container">
        <header>
            <h1>Поиск циклов в графе</h1>
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
                    <div class="info-block">
                        <p><strong>Количество вершин:</strong> <span id="vertex-count-display">–</span></p>
                    </div>
                    <div class="info-block">
                        <p><strong>Матрица смежности:</strong></p>
                        <pre id="adjacency-matrix-display">–</pre>
                    </div>
                </section>

                <!-- Блок с графом -->
                <section class="card graph-area" id="graph-area">
                    <h2>Визуализация графа</h2>
                    <div id="graph-container">
                        <div class="graph-placeholder">
                            <i class="fas fa-project-diagram"></i>
                            <p>Граф будет отображен после анализа</p>
                        </div>
                    </div>
                </section>
            </div>


            <!-- Результат поиска циклов -->
            <section class="card result-section">
                <h2>Результат поиска</h2>
                <div class="properties-grid">
                    <div class="property-card">
                        <h3>Количество найденных циклов</h3>
                        <div class="property-result" id="cycle-detected">
                            –
                        </div>
                        <div class="property-description">
                            Будет отображено, сколько циклов найдено
                        </div>
                    </div>

                    <div class="property-card">
                        <h3>Список найденных циклов</h3>
                        <div class="property-result" id="cycle-example">
                            –
                        </div>
                        <div class="property-description">
                            Будет отображен список циклов в виде последовательностей вершин
                        </div>
                    </div>
                </div>
            </section>
        </main>
    </div>

    <script src="/static/scripts/collapse-block.js"></script>
</body>
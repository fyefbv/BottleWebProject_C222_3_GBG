% rebase('layout.tpl', title=title, year=year, graph_json=graph_json)

<head>
    <link rel="stylesheet" href="/static/content/pages/equivalence.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
                                                                   
<body>
    <div class="container">
        <header>
            <h1>Эквивалентность</h1>
        </header>

        <main class="content">

<!-- Теоретический блок -->
<section class="card">
    <button class="btn theory-toggle" onclick="toggleTheory()">
        <span>Теоретический материал</span>
        <i class="fas fa-chevron-down"></i>
    </button>
    <div id="theory-block" style="display: none; margin-top: 1.5rem;">
        <h2>Что такое эквивалентность?</h2>
        <div class="theory-content">
            <div class="theory-left">
                <div class="matrix-container">
                    <p class="matrix-label">Матрица смежности:</p>
                    <pre>1 1 0
1 1 1
0 1 1</pre>
                </div>
                <img src="/static/images/equivalence-example.jpg" alt="Пример графа" class="example-image">
            </div>
            <div class="theory-right">
                <p><strong>Эквивалентное отношение</strong> — это бинарное отношение, обладающее тремя свойствами:</p>
                
                <div class="property-explanation">
                    <h3><i class="fas fa-arrow-circle-right"></i> Рефлексивность</h3>
                    <p>Каждый элемент соотносится с самим собой. В матрице смежности это означает, что все диагональные элементы (a, a) должны быть равны 1.</p>
                </div>
                
                <div class="property-explanation">
                    <h3><i class="fas fa-exchange-alt"></i> Симметричность</h3>
                    <p>Если элемент A соотносится с B, то и B с A. В матрице это означает, что если M[i][j] = 1, то обязательно M[j][i] = 1. Матрица должна быть симметрична относительно главной диагонали.</p>
                </div>
                
                <div class="property-explanation">
                    <h3><i class="fas fa-share-alt"></i> Транзитивность</h3>
                    <p>Если A связано с B, а B с C, то A связано с C. Формально: если (a, b) ∈ R и (b, c) ∈ R, то (a, c) ∈ R. В матрице это проверяется через алгоритм Уоршалла.</p>
                </div>

                <h3>Анализ примера</h3>
                <div class="analysis-grid">
                    <div class="analysis-point">
                        <i class="fas fa-check-circle valid-icon"></i>
                        <span>Рефлексивность</span>
                        <p>Диагональ: 1, 1, 1</p>
                    </div>
                    <div class="analysis-point">
                        <i class="fas fa-check-circle valid-icon"></i>
                        <span>Симметричность</span>
                        <p>M[0][1]=M[1][0], M[1][2]=M[2][1]</p>
                    </div>
                    <div class="analysis-point">
                        <i class="fas fa-times-circle invalid-icon"></i>
                        <span>Транзитивность</span>
                        <p>Нарушение: (0,1) и (1,2) есть, но (0,2) отсутствует</p>
                    </div>
                </div>

                <p class="conclusion"><strong>Вывод:</strong> отношение не является эквивалентным, так как нарушено свойство транзитивности. Требуется транзитивное замыкание.</p>
            </div>
        </div>
    </div>
</section>

            <!-- Блоки данных и графа -->
           <div class="data-graph-container">
                <!-- Входные данные -->
                <section class="card input-data">
                    <h2>Входные данные</h2>
                    % if results:
                        <div class="info-block">
                            <p><strong>Количество вершин:</strong> {{ results['vertex_count'] }}</p>
                        </div>
                        <div class="matrix-container">
                            <p><strong>Матрица смежности:</strong></p>
                            <pre>{{ results['adjacency_matrix'] }}</pre>
                        </div>
                    % else:
                        <div class="info-block">
                            <p><i class="fas fa-exclamation-triangle"></i> Данные графа не загружены</p>
                            <a href="/" class="btn btn-primary">
                                <i class="fas fa-project-diagram"></i> Построить граф
                            </a>
                        </div>
                    % end
                </section>

                <!-- Визуализация графа -->
   <section class="card graph-area" id="graph-area">
    <h2>Визуализация графа</h2>
    % if graph_json:
        <div id="d3-graph"></div>
    % else:
        <div class="graph-placeholder">
            <i class="fas fa-project-diagram"></i>
            <p>Граф будет отображен после анализа</p>
        </div>
    % end
</section>
            </div>

            <!-- Результаты анализа -->
            <section class="card result-section">
                <h2>Свойства отношения</h2>
                <div class="properties-grid">
                    <div class="property-card">
                        <h3>Рефлексивность</h3>
                        <div class="property-result">
                            % if results:
                                <span class="{{ 'valid' if results['is_reflexive'] else 'invalid' }}">
                                    {{ 'Да' if results['is_reflexive'] else 'Нет' }}
                                </span>
                            % else:
                                <span>–</span>
                            % end
                        </div>
                        <div class="property-description">
                            Все диагональные элементы равны 1
                        </div>
                    </div>
                    
                    <div class="property-card">
                        <h3>Симметричность</h3>
                        <div class="property-result">
                            % if results:
                                <span class="{{ 'valid' if results['is_symmetric'] else 'invalid' }}">
                                    {{ 'Да' if results['is_symmetric'] else 'Нет' }}
                                </span>
                            % else:
                                <span>–</span>
                            % end
                        </div>
                        <div class="property-description">
                            Матрица совпадает со своей транспонированной версией
                        </div>
                    </div>
                    
                    <div class="property-card">
                        <h3>Транзитивность</h3>
                        <div class="property-result">
                            % if results:
                                <span class="{{ 'valid' if results['is_transitive'] else 'invalid' }}">
                                    {{ 'Да' if results['is_transitive'] else 'Нет' }}
                                </span>
                            % else:
                                <span>–</span>
                            % end
                        </div>
                        <div class="property-description">
                            Если A→B и B→C, то обязательно A→C
                        </div>
                    </div>
                </div>
            </section>

            <!-- Замыкания -->
            <section class="card closure-section">
                <h2>Замыкания</h2>
                <div class="closures-grid">
                    <div class="matrix-container">
                        <h3>Рефлексивное</h3>
                        % if results:
                            <pre>{{ results['reflexive_closure'] }}</pre>
                        % else:
                            <pre>–</pre>
                        % end
                    </div>
                    
                    <div class="matrix-container">
                        <h3>Симметричное</h3>
                        % if results:
                            <pre>{{ results['symmetric_closure'] }}</pre>
                        % else:
                            <pre>–</pre>
                        % end
                    </div>
                    
                    <div class="matrix-container">
                        <h3>Транзитивное</h3>
                        % if results:
                            <pre>{{ results['transitive_closure'] }}</pre>
                        % else:
                            <pre>–</pre>
                        % end
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
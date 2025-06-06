% rebase('layout.tpl', title='Максимальный поток', year=year, graph_json=graph_json, adjacency_matrix=adjacency_matrix)

<head>
    <link rel="stylesheet" href="/static/content/pages/max_flow.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
   <!-- <link rel="stylesheet" href="/static/content/site.css"> -->
</head>






<body>
    <div class="container">
        <header>
            <h1>Максимальный поток в графе</h1>
        </header>

        <main class="content">
            <!-- Теория -->
            <section class="card">
    <button class="theory-toggle" onclick="toggleTheory()">
        <span>Теоретический материал</span>
        <i class="fas fa-chevron-down"></i>
    </button>
    <div id="theory-block" style="display: none; margin-top: 1.5rem;">
        <h2>Что такое максимальный поток?</h2>
        <div class="theory-content">
            <div class="theory-left">
                <div class="matrix-container">
                    <p class="matrix-label">Матрица пропускных способностей:</p>
                    <pre>0  3  2  0  0
0  0  5  2  0
0  0  0  3  4
0  0  0  0  2
0  0  0  0  0</pre>
                </div>
                <img src="/static/images/max-flow-example.jpg" alt="Пример графа с потоком" class="example-image">
            </div>
            <div class="theory-right">
                <p><strong>Максимальный поток</strong> — это наибольшее количество "вещества" (например, воды, тока, данных), которое можно передать от <strong>истока</strong> к <strong>стоку</strong> по сети, не превышая пропускную способность рёбер.</p>

                <div class="property-explanation">
                    <h3><i class="fas fa-water"></i> Основные понятия</h3>
                    <ul>
                        <li><strong>Исток (source)</strong> — начальная вершина, из которой поступает поток.</li>
                        <li><strong>Сток (sink)</strong> — конечная вершина, куда поток должен прибыть.</li>
                        <li><strong>Пропускная способность ребра</strong> — максимальный поток, который может пройти по ребру между двумя вершинами.</li>
                        <li><strong>Остаточная сеть</strong> — модифицированный граф, отражающий, сколько ещё потока можно отправить по рёбрам на данном этапе.</li>
                    </ul>
                </div>

                <div class="property-explanation">
                    <h3><i class="fas fa-project-diagram"></i> Алгоритмы</h3>
                    <ul>
                        <li><strong>Форда-Фалкерсона</strong> — итеративно находит увеличивающие пути в остаточной сети и наращивает поток. Простой, но может быть медленным на графах с дробными значениями.</li>
                        <li><strong>Эдмондса-Карпа</strong> — реализация алгоритма Форда-Фалкерсона, в которой увеличивающий путь ищется с помощью поиска в ширину (BFS), что даёт полиномиальную сложность.</li>
                        <li><strong>Push-Relabel</strong> — работает не с путями, а с локальными операциями "перекачки" (push) потока и "подъёма" (relabel) узлов. Эффективен для плотных графов.</li>
                    </ul>
                </div>

                <p class="conclusion"><strong>Примечание:</strong> Величина максимального потока равна пропускной способности минимального разреза (теорема Форда-Фалкерсона).</p>
            </div>
        </div>
    </div>
</section>

            <!-- Горизонтальные блоки: входные данные и граф method="POST" action="/build_graph_max_flow"-->
            <div class="data-graph-container">
                <!-- Блок с входными данными -->
                <section class="card input-data">
                    <h2>Входные данные</h2>
                    <form id="build-graph-form" method="POST" action="/build_graph_max_flow" >
                         <div class="form-group">
                            <label for="vertex-count">Количество вершин:</label>
                            <input type="number" id="vertex-count" name="vertex-count" min="1" max="15" value="${adjacency_matrix and initialVertexCount or '4'}">
                        </div>

                        <div style="margin-bottom: 20px; class="button-row">
                            <button  class="btn primary" type="submit" title="Функция не реализована">
                                <i class="fas fa-eye"></i> Отобразить граф
                            </button>
                        </div>


                        <div class="form-group">
                            <label>Матрица пропускных способностей:</label>
                        <div id="matrix-container" class="main-matrix-container"></div>


                    </div>
                    </form>



                    <form method="POST" action="/generate_graph" id="generate-graph-form">
                        <div class="button-row">
                            <button id="generate-matrix" class="btn primary" type="submit" title="Сгенерировать случайную матрицу">
                                <i class="fas fa-random"></i> Сгенерировать случайно
                            </button>
                        </div>
                    </form>
             
                    </form>
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

            <!-- Результат поиска максимального потока -->
            <section class="card result-section">
                <h2>Результат расчёта</h2>
                <div class="properties-grid">
                    <div class="property-card">
                        <h3>Максимальный поток</h3>

                        <div class="property-result" id="max-flow-value">
                            % if max_flow_value is not None:
                                {{max_flow_value}} (из {{flow['source']}} в {{flow['sink']}})
                            % else:
                                –
                            % end
                        </div>

                        <div class="property-description">
                            Величина максимального потока от истока к стоку
                        </div>
                    </div>
                </div>
            </section>






















        </main>
    </div>


   <!-- <script src="/static/scripts/matrix.js"></script> -->
    <script src="/static/scripts/collapse-block.js"></script>




   % if adjacency_matrix:
   <script>
       const initialMatrix = {{!adjacency_matrix}};
       const initialVertexCount = initialMatrix.length;
   </script>
   % end
   <script src="/static/scripts/matrix_max_flow.js"></script>


   <script src="https://d3js.org/d3.v7.min.js"></script>
  <!--  <script src="/static/scripts/templates.js"></script> -->


  % if graph_json:
      <script>
          var graphData = {{!graph_json}};
          console.log('graph dla otobrazheniya1:', graphData);
      </script>
      <script src="/static/scripts/graph.js"></script>
  % end


</body>
% rebase('layout.tpl', title='Определение свойств графа', year=year)

<head>
    <link rel="stylesheet" href="/static/content/pages/equivalence.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        function toggleTheory() {
            const theoryBlock = document.getElementById("theory-block");
            const toggleIcon = document.querySelector(".theory-toggle i");
            
            if (theoryBlock.style.display === "none") {
                theoryBlock.style.display = "block";
                toggleIcon.classList.remove("fa-chevron-down");
                toggleIcon.classList.add("fa-chevron-up");
            } else {
                theoryBlock.style.display = "none";
                toggleIcon.classList.remove("fa-chevron-up");
                toggleIcon.classList.add("fa-chevron-down");
            }
        }
    </script>
</head>

<body>
    <div class="container">
        <header>
            <h1>Эквивалентность</h1>
        </header>

        <main class="content">

<!-- Обновленный теоретический блок -->
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

            <!-- Блок с результатами анализа -->
            <section class="card result-section">
                <h2>Свойства отношения</h2>
                <div class="properties-grid">
                    <div class="property-card">
                        <h3>Рефлексивность</h3>
                        <div class="property-result">
                            <span id="reflexivity-result">–</span>
                        </div>
                        <div class="property-description">
                            Все диагональные элементы равны 1
                        </div>
                    </div>
                    
                    <div class="property-card">
                        <h3>Симметричность</h3>
                        <div class="property-result">
                            <span id="symmetry-result">–</span>
                        </div>
                        <div class="property-description">
                            Матрица совпадает со своей транспонированной версией
                        </div>
                    </div>
                    
                    <div class="property-card">
                        <h3>Транзитивность</h3>
                        <div class="property-result">
                            <span id="transitivity-result">–</span>
                        </div>
                        <div class="property-description">
                            Если A→B и B→C, то обязательно A→C
                        </div>
                    </div>
                </div>
            </section>

            <!-- Блок с замыканиями -->
            <section class="card closure-section">
                <h2>Замыкания</h2>
                <div class="closures-grid">
                    <div class="closure-card">
                        <h3>Рефлексивное</h3>
                        <pre id="reflexive-closure">–</pre>
                    </div>
                    
                    <div class="closure-card">
                        <h3>Симметричное</h3>
                        <pre id="symmetric-closure">–</pre>
                    </div>
                    
                    <div class="closure-card">
                        <h3>Транзитивное</h3>
                        <pre id="transitive-closure">–</pre>
                    </div>
                </div>
            </section>

        </main>
    </div>
</body>
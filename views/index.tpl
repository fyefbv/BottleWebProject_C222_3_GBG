% rebase('layout.tpl', title='Главная страница', year=year)

<head>
    <link rel="stylesheet" href="/static/content/pages/index.css">
</head>

<body>
    <div class="container">
        <header>
            <h1>Главная страница</h1>
        </header>

        <div class="layout">
            <!-- Список шаблонов слева -->
            <aside class="template-aside">
                <h2>Шаблоны</h2>
                <ul id="template-list">
                    <!-- Список шаблонов загружаемых графов -->
                </ul>
                <button class="btn load-btn" id="load-template">Загрузить шаблон</button>
            </aside>

            <!-- Основной контент справа -->
            <main class="content">
                <section class="card input-section">
                    <h2>Ввод данных графа</h2>
                    <label for="vertex-count">Количество вершин:</label>
                    <input type="number" id="vertex-count" class="input-field" name="vertex-count" min="1">

                    <label for="adj-matrix">Матрица смежности:</label>
                    <textarea id="adj-matrix" class="textarea-field" name="adj-matrix" rows="5" placeholder="Введите матрицу через пробелы и переносы строк"></textarea>

                    <button class="btn action-btn" id="build-graph">Построить граф</button>
                </section>

                <section class="card graph-area" id="graph-area">
                    <!-- Здесь будет отрисован ориентированный граф -->
                </section>

                <section class="card methods">
                    <h2>Методы анализа</h2>
                    <div class="btn-group">
                        <a href="/equivalence" class="btn method-btn">Эквивалентность</a>
                        <a href="/cycles" class="btn method-btn">Поиск циклов</a>
                        <a href="/maxflow" class="btn method-btn">Максимальный поток</a>
                    </div>
                </section>
            </main>
        </div>
    </div>
</body>
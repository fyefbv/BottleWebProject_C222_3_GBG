document.addEventListener('DOMContentLoaded', function () {
    // Загружаем шаблоны из JSON
    fetch('/static/data/templates.json')
        .then(response => response.json())
        .then(templates => {
            const templateList = document.getElementById('template-list');

            templates.forEach(template => {
                const li = document.createElement('li');
                li.textContent = template.name;
                li.addEventListener('click', () => {
                    updateForm(
                        template.adjacency_matrix.length,
                        template.adjacency_matrix
                    );
                });
                templateList.appendChild(li);
            });
        });

    // Функция для обновления формы на основе выбранного шаблона
    function updateForm(vertexCount, matrix) {
        const vertexCountInput = document.getElementById('vertex-count');
        const matrixContainer = document.getElementById('matrix-container');

        // Обновляем количество вершин
        vertexCountInput.value = vertexCount;

        // Генерируем матрицу
        matrixContainer.innerHTML = '';
        const table = document.createElement('table');
        table.className = 'matrix-table';

        // Заголовок столбцов
        const headerRow = document.createElement('tr');
        headerRow.appendChild(document.createElement('th')); // Пустой уголок
        for (let i = 1; i <= vertexCount; i++) {
            const th = document.createElement('th');
            th.textContent = i;
            headerRow.appendChild(th);
        }
        table.appendChild(headerRow);

        // Строки матрицы
        for (let i = 1; i <= vertexCount; i++) {
            const row = document.createElement('tr');
            const rowHeader = document.createElement('th');
            rowHeader.textContent = i;
            row.appendChild(rowHeader);

            for (let j = 1; j <= vertexCount; j++) {
                const cell = document.createElement('td');
                const input = document.createElement('input');
                input.type = 'number';
                input.min = '0';
                input.max = '1';
                input.value = matrix[i - 1][j - 1]; // Подставляем значения из шаблона
                input.className = 'matrix-input';
                input.name = `cell-${i - 1}-${j - 1}`;
                input.dataset.row = i - 1;
                input.dataset.col = j - 1;

                input.addEventListener('input', function () {
                    if (this.value !== '0' && this.value !== '1') {
                        this.classList.add('invalid');
                        this.value = this.value.slice(0, -1);
                    } else {
                        this.classList.remove('invalid');
                    }
                });

                cell.appendChild(input);
                row.appendChild(cell);
            }
            table.appendChild(row);
        }

        matrixContainer.appendChild(table);
    }
});

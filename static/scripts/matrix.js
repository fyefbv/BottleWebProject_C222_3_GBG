document.addEventListener('DOMContentLoaded', function () {
    const vertexCountInput = document.getElementById('vertex-count');
    const matrixContainer = document.getElementById('matrix-container');
    const generateBtn = document.getElementById('generate-matrix');

    // При загрузке создаём матрицу по умолчанию
    generateAdjacencyMatrix(parseInt(vertexCountInput.value));

    // Перестраиваем таблицу, когда меняется количество вершин
    vertexCountInput.addEventListener('input', function () {
        const count = parseInt(this.value) || 0;
        if (count > 0 && count <= 15) {
            generateAdjacencyMatrix(count);
        }
    });

    // Генерация ориентированной матрицы: для каждой пары (i<j) 0 или 1, а обратная ячейка ставится в 0.
    // Диагональ всегда 0.
    generateBtn.addEventListener('click', function (e) {
        e.preventDefault();

        const n = parseInt(vertexCountInput.value) || 0;
        if (n <= 0 || n > 15) return;

        // Функция-помощник: получить элемент input по его координатам
        function getInput(i, j) {
            return matrixContainer.querySelector(`input[name="cell-${i}-${j}"]`);
        }

        // Для всех i<j генерируем случайную грань, обратную ставим 0
        for (let i = 0; i < n; i++) {
            // Ставим 0 на диагонали
            const diagInput = getInput(i, i);
            if (diagInput) {
                diagInput.value = '0';
                diagInput.classList.remove('invalid');
            }

            for (let j = i + 1; j < n; j++) {
                const bit = Math.random() < 0.5 ? '1' : '0';
                const inpIJ = getInput(i, j);
                const inpJI = getInput(j, i);

                if (inpIJ) {
                    inpIJ.value = bit;
                    inpIJ.classList.remove('invalid');
                }
                if (inpJI) {
                    // чтобы матрица оставалась ориентированной, противоположную ячейку сбрасываем в 0
                    inpJI.value = '0';
                    inpJI.classList.remove('invalid');
                }
            }
        }
    });

    // При ручном вводе: если пользователь ставит "1" в [i,j], то [j,i] обнуляем.
    function attachInputListener(input) {
        input.addEventListener('input', function () {
            if (this.value !== '0' && this.value !== '1') {
                this.classList.add('invalid');
                this.value = this.value.slice(0, -1);
                return;
            }
            this.classList.remove('invalid');

            const i = parseInt(this.dataset.row);
            const j = parseInt(this.dataset.col);
            if (this.value === '1' && i !== j) {
                // Обнуляем зеркальную ячейку
                const opposite = matrixContainer.querySelector(`input[name="cell-${j}-${i}"]`);
                if (opposite) {
                    opposite.value = '0';
                    opposite.classList.remove('invalid');
                }
            }
            if (i === j && this.value === '1') {
                // на диагонали всегда 0
                this.value = '0';
            }
        });
    }

    // После создания таблицы присоединяем слушатели к каждому input
    function generateAdjacencyMatrix(vertexCount) {
        matrixContainer.innerHTML = '';
        const table = document.createElement('table');
        table.className = 'matrix-table';

        // Заголовок столбцов
        const headerRow = document.createElement('tr');
        headerRow.appendChild(document.createElement('th')); // пустая ячейка
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
                input.value = '0';
                input.className = 'matrix-input';
                input.name = `cell-${i - 1}-${j - 1}`;
                input.dataset.row = i - 1;
                input.dataset.col = j - 1;

                // Присоединяем слушатель, гарантирующий ориентированность
                attachInputListener(input);

                cell.appendChild(input);
                row.appendChild(cell);
            }
            table.appendChild(row);
        }

        matrixContainer.appendChild(table);
    }
});

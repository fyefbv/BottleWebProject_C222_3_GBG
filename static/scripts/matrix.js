document.addEventListener('DOMContentLoaded', function () {
    const vertexCountInput = document.getElementById('vertex-count');
    const matrixContainer = document.getElementById('matrix-container');
    const generateBtn = document.getElementById('generate-matrix');

    // При загрузке создаём матрицу по умолчанию
    generateAdjacencyMatrix(parseInt(vertexCountInput.value));

    vertexCountInput.addEventListener('input', function () {
        const count = parseInt(this.value) || 0;
        if (count > 0 && count <= 15) {
            generateAdjacencyMatrix(count);
        }
    });

    generateBtn.addEventListener('click', function (e) {
        e.preventDefault();

        const n = parseInt(vertexCountInput.value) || 0;
        if (n <= 0 || n > 15) return;

        function getInput(i, j) {
            return matrixContainer.querySelector(`input[name="cell-${i}-${j}"]`);
        }

        // Обнуляем все значения
        for (let i = 0; i < n; i++) {
            for (let j = 0; j < n; j++) {
                const inp = getInput(i, j);
                if (inp) {
                    inp.value = '0';
                    inp.classList.remove('invalid');
                }
            }
        }

        // Генерация случайных значений (кроме диагонали)
        for (let i = 0; i < n; i++) {
            for (let j = 0; j < n; j++) {
                if (i === j) continue;

                const inp = getInput(i, j);
                const random = Math.random() < 0.5 ? '0' : '1';
                if (inp) inp.value = random;
            }
        }
    });

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

            // Диагональ всегда должна оставаться 0
            if (i === j && this.value === '1') {
                this.value = '0';
            }

            // Удалена логика зеркального обнуления
        });
    }

    function generateAdjacencyMatrix(vertexCount) {
        matrixContainer.innerHTML = '';
        const table = document.createElement('table');
        table.className = 'matrix-table';

        const headerRow = document.createElement('tr');
        headerRow.appendChild(document.createElement('th'));
        for (let i = 1; i <= vertexCount; i++) {
            const th = document.createElement('th');
            th.textContent = i;
            headerRow.appendChild(th);
        }
        table.appendChild(headerRow);

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

                attachInputListener(input);

                cell.appendChild(input);
                row.appendChild(cell);
            }
            table.appendChild(row);
        }

        matrixContainer.appendChild(table);
    }
});

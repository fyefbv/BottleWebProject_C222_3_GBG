document.addEventListener('DOMContentLoaded', function () {
    //console.log("matrix_max_flow.js загружен");
    const vertexCountInput = document.getElementById('vertex-count');
    const matrixContainer = document.getElementById('matrix-container');
    const generateBtn = document.getElementById('generate-matrix');
    //const drawBtn = document.getElementById('generate-graph');

    //drawBtn.addEventListener('click', async (e) => {
    //    e.preventDefault();

    //    const formData = new FormData();
    //    formData.append('vertex-count', document.getElementById('vertex-count').value);

    //    document.querySelectorAll('#matrix-container input').forEach(input => {
    //        formData.append(input.name, input.value || 0);
    //    });

    //    try {
    //        const response = await fetch('/build_graph_max_flow', {
    //            method: 'POST',
    //            body: formData
    //        });
    //        //const graphData = await response.json();
    //        //console.log('Граф получен:', graphData);
    //        // Здесь можно добавить отрисовку графа
    //    } catch (err) {
    //        console.error('Ошибка:', err);
    //    }
    //});




    // Инициализация матрицы
    let vertexCount = parseInt(vertexCountInput.value) || 4;

    // Если есть начальная матрица - используем её
    if (typeof initialMatrix !== 'undefined') {
        vertexCount = initialVertexCount;
        vertexCountInput.value = vertexCount;
        populateMatrixInputs(initialMatrix);
    } else {
        generateAdjacencyMatrix(vertexCount);
    }







    // Инициализация пустой матрицы
    // generateAdjacencyMatrix(parseInt(vertexCountInput.value));

    vertexCountInput.addEventListener('input', function () {
        const count = parseInt(this.value) || 0;
        if (count > 0) {
            generateAdjacencyMatrix(count);
        }
    });

    // Обработчик генерации случайной матрицы через сервер
    generateBtn.addEventListener('click', function (e) {
        e.preventDefault();

        const vertexCount = parseInt(vertexCountInput.value) || 0;
        if (vertexCount < 1 || vertexCount > 15) return;

        fetch('/generate_graph', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `vertex-count=${vertexCount}`
        })
            .then(res => res.json())
            .then(data => {
                const matrix = data.matrix;
                populateMatrixInputs(matrix);
            })
            .catch(err => {
                console.error('Ошибка при получении матрицы с сервера:', err);
            });
        console.log("Kod tut")
    });

    // Заполнение таблицы матрицы значениями
    function populateMatrixInputs(matrix) {
        const size = matrix.length;
        generateAdjacencyMatrix(size);
        for (let i = 0; i < size; i++) {
            for (let j = 0; j < size; j++) {
                const input = matrixContainer.querySelector(`input[name="cell-${i}-${j}"]`);
                if (input) {
                    input.value = matrix[i][j];
                    input.classList.remove('invalid');
                }
            }
        }
    }

    function attachInputListener(input) {
        input.addEventListener('input', function () {
            const i = parseInt(this.dataset.row);
            const j = parseInt(this.dataset.col);
            let value = parseInt(this.value);
            if (isNaN(value) || value < 0) value = 0;
            if (i === j) value = 0;
            this.value = value;
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

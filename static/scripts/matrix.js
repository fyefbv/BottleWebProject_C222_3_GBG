document.addEventListener('DOMContentLoaded', function () {
    const vertexCountInput = document.getElementById('vertex-count');
    const matrixContainer = document.getElementById('matrix-container');

    // ������������� �������
    generateAdjacencyMatrix(parseInt(vertexCountInput.value));

    // ���������� ��������� ���������� ������
    vertexCountInput.addEventListener('input', function () {
        const count = parseInt(this.value) || 0;
        if (count > 0 && count <= 15) {
            generateAdjacencyMatrix(count);
        }
    });

    // ��������� ������� ������� ���������
    function generateAdjacencyMatrix(vertexCount) {
        matrixContainer.innerHTML = '';

        const table = document.createElement('table');
        table.className = 'matrix-table';

        // ������� ��������� �������
        const headerRow = document.createElement('tr');
        headerRow.appendChild(document.createElement('th')); // ������ ������ � ����

        for (let i = 1; i <= vertexCount; i++) {
            const th = document.createElement('th');
            th.textContent = i;
            headerRow.appendChild(th);
        }

        table.appendChild(headerRow);

        // ������� ������ �������
        for (let i = 1; i <= vertexCount; i++) {
            const row = document.createElement('tr');

            // ��������� ������
            const rowHeader = document.createElement('th');
            rowHeader.textContent = i;
            row.appendChild(rowHeader);

            // ������ �������
            for (let j = 1; j <= vertexCount; j++) {
                const cell = document.createElement('td');
                const input = document.createElement('input');
                input.type = 'number';
                input.min = '0';
                input.max = '1';
                input.value = '0';
                input.className = 'matrix-input';
                input.dataset.row = i - 1;
                input.dataset.col = j - 1;

                // ���������� ����� - ��������� ������ 0 � 1
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

        // ��������� ������ ����������
        const controls = document.createElement('div');
        controls.className = 'matrix-controls';

        matrixContainer.appendChild(controls);
    }
})
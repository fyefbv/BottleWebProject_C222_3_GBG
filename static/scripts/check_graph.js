document.addEventListener('DOMContentLoaded', function () {
    // Проверка на наличие графа
    const isGraphEmpty = () =>
        typeof graphData === 'undefined' || !graphData.nodes || graphData.nodes.length === 0;

    // Обработка ссылок
    const methodLinks = document.querySelectorAll('#methods a.method-btn');
    methodLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            if (isGraphEmpty()) {
                event.preventDefault();
                alert('Сначала постройте граф!');
            }
        });
    });

    // Обработка форм с кнопками (например, «Поиск циклов»)
    const methodForms = document.querySelectorAll('#methods form');
    methodForms.forEach(form => {
        form.addEventListener('submit', function (event) {
            if (isGraphEmpty()) {
                event.preventDefault();
                alert('Сначала постройте граф!');
            }
        });
    });
});

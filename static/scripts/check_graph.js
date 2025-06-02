document.addEventListener('DOMContentLoaded', function () {
    // Находим все ссылки внутри блока #methods
    var methodLinks = document.querySelectorAll('#methods a.method-btn');
    methodLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            // Если граф ещё не построен (graphData не определена или пустая):
            if (typeof graphData === 'undefined' || !graphData.nodes || graphData.nodes.length === 0) {
                event.preventDefault();
                alert('Сначала постройте граф!');
            }
            // Иначе — пускаем переход по ссылке.
        });
    });
});

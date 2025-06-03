document.addEventListener('DOMContentLoaded', function () {
    if (typeof graphData !== 'undefined') {
        renderGraph(graphData);
    }
});

function renderGraph(data) {
    const container = document.getElementById("graph-area");
    container.innerHTML = ''; // Очищаем placeholder
    const width = container.clientWidth;
    const height = 600; // Фиксированная высота

    const svg = d3.select("#graph-area")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    // Определяем стрелки для ориентированных рёбер
    svg.append("defs").append("marker")
        .attr("id", "arrow")
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 15)
        .attr("refY", 0)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,-5L10,0L0,5")
        .attr("fill", "#999");

    // Настраиваем симуляцию силового расположения
    const simulation = d3.forceSimulation(data.nodes)
        .force("link", d3.forceLink(data.links).id(d => d.id))
        .force("charge", d3.forceManyBody().strength(-300))
        .force("center", d3.forceCenter(width / 2, height / 2));

    // Отрисовываем рёбра
    const link = svg.append("g")
        .selectAll("line")
        .data(data.links)
        .enter().append("line")
        .attr("stroke", "#999")
        .attr("stroke-width", 1)
        .attr("marker-end", "url(#arrow)");

    // Отрисовываем вершины
    const node = svg.append("g")
        .selectAll("circle")
        .data(data.nodes)
        .enter().append("circle")
        .attr("r", 5)
        .attr("fill", "#1f77b4")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    // Добавляем метки вершин
    const label = svg.append("g")
        .selectAll("text")
        .data(data.nodes)
        .enter().append("text")
        .attr("dx", 8)
        .attr("dy", ".35em")
        .text(d => d.id);

    // Обновляем позиции на каждом тике симуляции
    simulation.on("tick", () => {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node
            .attr("cx", d => d.x)
            .attr("cy", d => d.y);

        label
            .attr("x", d => d.x)
            .attr("y", d => d.y);
    });

    // Функции для перетаскивания
    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
}

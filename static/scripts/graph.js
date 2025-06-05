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
        .attr("viewBox", "0 -5 20 20")
        .attr("refX", 20) //было 15
        .attr("refY", 0)
        .attr("markerWidth", 15)
        .attr("markerHeight", 15) //было по 6
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,-5L15,0L0,5") //было -5L10
        .attr("markerUnits", "userSpaceOnUse")
        .attr("fill", "#999");

    // Настраиваем симуляцию силового расположения
    const simulation = d3.forceSimulation(data.nodes)
        .force("link", d3.forceLink(data.links).id(d => d.id).distance(150))
        .force("charge", d3.forceManyBody().strength(-500))
        .force("center", d3.forceCenter(width / 2, height / 2));

    // Отрисовываем рёбра
    const link = svg.append("g")
        .selectAll("line")
        .data(data.links)
        .enter().append("line")
        .attr("stroke", "#999")
        .attr("stroke-width", 1)
        .attr("marker-end", "url(#arrow)");



    //....................................................................................
    const edgeLabels = svg.append("g")
        .selectAll(".edge-label")
        .data(data.links)
        .enter()
        .append("text")
        .attr("class", "edge-label")
        .attr("font-size", 12) // было 10
        .attr("fill", "#d32f2f") // Красный цвет для заметности
        .text(d => d.value || d.weight); // Используем value или weight из данных
        console.log("links example:", data.links);



    // Отрисовываем вершины
    const node = svg.append("g")
        .selectAll("circle")
        .data(data.nodes)
        .enter().append("circle")
        .attr("r", 8) //было 5
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
        .attr("dx", 12) //было 8
        .attr("dy", ".45em") //было 35
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





        // Обновляем позиции подписей рёбер........................................................................
        edgeLabels
            .attr("x", d => (d.source.x + d.target.x) / 2)
            .attr("y", d => (d.source.y + d.target.y) / 2);
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

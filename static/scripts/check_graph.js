document.addEventListener('DOMContentLoaded', function () {
    // ������� ��� ������ ������ ����� #methods
    var methodLinks = document.querySelectorAll('#methods a.method-btn');
    methodLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            // ���� ���� ��� �� �������� (graphData �� ���������� ��� ������):
            if (typeof graphData === 'undefined' || !graphData.nodes || graphData.nodes.length === 0) {
                event.preventDefault();
                alert('������� ��������� ����!');
            }
            // ����� � ������� ������� �� ������.
        });
    });
});

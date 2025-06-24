# interface/components/bar_chart_widget.py

from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt

class BarChartWidget(QWidget):
    def __init__(self, title: str, data: list[tuple[str, any]]):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Processa os dados aplicando as regras
        names = []
        values = []

        for name, value in data:
            # Sanitize o nome
            name_str = str(name)

            # Sanitize o valor
            try:
                value_int = int(value)
            except:
                value_int = 0

            if value_int < 0:
                value_int = 0

            names.append(name_str)
            values.append(value_int)

        # Determina o máximo de escala (maior valor + 1/3, truncado)
        max_value = max(values) if values else 10
        axis_max = int(max_value + (max_value / 3))

        # Cria o dataset de barras
        bar_set = QBarSet(title)
        for val in values:
            bar_set.append(val)

        series = QBarSeries()
        series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(title)
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        # Configura o eixo X com os nomes
        axis_x = QBarCategoryAxis()
        axis_x.append(names)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        # Configura o eixo Y
        axis_y = QValueAxis()
        axis_y.setRange(0, axis_max)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        # Torna bonito
        chart.legend().setVisible(False)

        # Cria o chart view e adiciona ao layout
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        layout.addWidget(chart_view)

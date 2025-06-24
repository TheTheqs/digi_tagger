# interface/screens/data_screen.py

from PySide6.QtWidgets import QWidget, QVBoxLayout
from interface.components.title import Title
from interface.components.back_button import BackButton
from interface.components.bar_chart_widget import BarChartWidget
from services.application_services import ApplicationService


class DataScreen(QWidget):
    def __init__(self, navigate_callback, app_service: ApplicationService):
        super().__init__()
        self.navi = navigate_callback
        self.app_service: ApplicationService = app_service
        self.setStyleSheet("padding: 20px;")

        self.layout = QVBoxLayout()

        # Botão de voltar
        back_button = BackButton(lambda: self.navi("home"))
        self.layout.addWidget(back_button)

        # Título
        title = Title("Painel de Dados")
        self.layout.addWidget(title)

        self.chart_widget = None

        self.setLayout(self.layout)

        self.update_screen()

    def update_screen(self):
        if self.chart_widget:
            self.layout.removeWidget(self.chart_widget)
            self.chart_widget.deleteLater()
            self.chart_widget = None

        # Consulta real ao banco via application service
        total, editados, nao_editados = self.app_service.db.get_sprite_statistics()

        # Monta os dados no formato de tuplas para o gráfico
        data = [
            ("Total de Sprites", total),
            ("Editados", editados),
            ("Não Editados", nao_editados)
        ]

        self.chart_widget = BarChartWidget("Estatísticas de Sprites", data)
        self.layout.addWidget(self.chart_widget)

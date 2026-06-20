import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QProgressBar,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QFileDialog,
)

from consulta_cnpj.utils.excel_reader import ExcelReader
from consulta_cnpj.ui.ui_worker import CnpjWorker

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Estado da aplicação
        self.input_file: str | None = None
        self.cnpjs: list[str] = []

        self.setWindowTitle("App - Consulta CNPJ")
        self.setWindowIcon(QIcon(str(self.resource_path("assets/app_icon.png"))))
        self.setFixedSize(700, 650)

        self.title_label = QLabel("Consulta CNPJ")
        self.title_label.setObjectName("title")

        self.subtitle_label = QLabel("Consulta automática de empresas via ReceitaWS")
        self.subtitle_label.setObjectName("subtitle")

        self.setStyleSheet("""
            QWidget {
                font-size: 12px;
            }

            QLabel#title {
                font-size: 24px;
                font-weight: bold;
            }

            QLabel#subtitle {
                color: #666666;
                font-size: 12px;
            }

            QLineEdit {
                padding: 8px;
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                background-color: #FAFAFA;
                color: #333333; 
            }

            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 14px;
                min-height: 25px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1565C0;
            }

            QPushButton:disabled {
                background-color: #AAAAAA;
            }

            QProgressBar {
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                text-align: center;
                min-height: 24px;
            }

            QProgressBar::chunk {
                background-color: #2E7D32;
                border-radius: 5px;
            }

            QTextEdit {
                font-family: Consolas;
                font-size: 11px;
                border-radius: 6px;
                border: 1px solid #CCCCCC;
            }
        """)


        # ==========================
        # Arquivo de entrada
        # ==========================
        self.file_input = QLineEdit()
        self.file_input.setReadOnly(True)
        self.file_input.setPlaceholderText("Selecione a planilha com os CNPJs (formato .xlsx)")

        self.btn_select = QPushButton("📂 Selecionar planilha")
        self.btn_select.setStyleSheet("""
            QPushButton {
                min-height: 20px;
                padding: 4px 14px;
            }
        """)


        # ==========================
        # Informações
        # ==========================
        self.info_label = QLabel("Nenhum arquivo carregado")


        # ==========================
        # Progresso
        # ==========================
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.status_label = QLabel("Aguardando início da consulta")


        # ==========================
        # Log
        # ==========================
        self.log = QTextEdit()
        self.log.setReadOnly(True)

        
        # ==========================
        # Ações principais
        # ==========================
        self.btn_run = QPushButton("▶ Iniciar consulta")
        self.btn_run.setEnabled(False)
        self.btn_run.setFixedWidth(200)
        self.btn_run.setFixedHeight(20)

        self.btn_cancel = QPushButton("❌ Cancelar")
        self.btn_cancel.setEnabled(False)
        self.btn_cancel.setFixedWidth(200)
        self.btn_cancel.setFixedHeight(20)
        
        self.btn_cancel.setStyleSheet("""
            QPushButton { background-color: #D32F2F; }
            QPushButton:hover { background-color: #B71C1C; }
        """)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.btn_run)
        buttons_layout.addWidget(self.btn_cancel)
        buttons_layout.addStretch()

        
        # ==========================
        # Cabeçalho
        # ==========================
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)

        title_layout = QVBoxLayout()

        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.subtitle_label)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()        


        # ==========================
        # Arquivo de entrada
        # ==========================
        file_group = QGroupBox("Arquivo de entrada")

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.btn_select)
        file_group.setLayout(file_layout)        


        # ==========================
        # Progresso
        # ==========================
        progress_group = QGroupBox("Progresso da consulta")

        progress_layout = QVBoxLayout()
        progress_layout.addWidget(self.progress)
        progress_layout.addWidget(self.status_label)

        progress_group.setLayout(progress_layout)


        # ==========================
        # Log
        # ==========================
        log_group = QGroupBox("Log de execução")

        log_layout = QVBoxLayout()
        log_layout.addWidget(self.log)

        log_group.setLayout(log_layout)
        

        # ==========================
        # Layout principal
        # ==========================
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        main_layout.addLayout(header_layout)
        main_layout.addWidget(file_group)
        main_layout.addWidget(self.info_label)
        main_layout.addWidget(progress_group)
        main_layout.addWidget(log_group)
        main_layout.addLayout(buttons_layout)

        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)

        # ==========================
        # Eventos
        # ==========================

        self.btn_select.clicked.connect(self.select_file)
        self.btn_run.clicked.connect(self.run_process)
        self.btn_cancel.clicked.connect(self.cancel_process)

    
    
    # ==========================================
    # AÇÕES DA INTERFACE
    # ==========================================
    def select_file(self):
        self.cnpjs = []

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar arquivo Excel",
            "",
            "Excel (*.xlsx)"
        )

        if not file_path:
            return

        self.input_file = file_path

        file_name = Path(file_path).name
        self.file_input.setText(file_name)

        reader = ExcelReader()

        try:
            self.cnpjs = reader.ler_cnpjs(file_path)

            self.info_label.setText(f"{len(self.cnpjs)} CNPJs encontrados")
            
            self.add_log(f"O Arquivo '{file_name}' foi carregado com sucesso.")

            self.status_label.setText("Arquivo pronto para processamento")
            
            if hasattr(self, 'btn_cancel'):
                self.btn_cancel.setEnabled(False)
            
            self.progress.setValue(0)

            self.btn_run.setEnabled(True)

        except Exception as e:
            self.btn_run.setEnabled(False)
            self.btn_cancel.setEnabled(False)
            self.cnpjs = []
            self.info_label.setText("Nenhum arquivo carregado")
            self.add_log(f"O Arquivo '{file_name}' é inválido.")
            self.add_log(f"{e}")

    # ==========================================

    def run_process(self):
        if not self.input_file or not self.cnpjs:
            self.add_log("Nenhum arquivo válido carregado.")
            return

        self.btn_run.setEnabled(False)
        self.btn_select.setEnabled(False)
        
        if hasattr(self, 'btn_cancel'):
            self.btn_cancel.setEnabled(True)

        self.add_log("Iniciando processamento em background.")

        self.worker = CnpjWorker(self.cnpjs, self.input_file)
        
        self.worker.progress_updated.connect(self.progress.setValue)
        self.worker.status_updated.connect(self.status_label.setText)
        self.worker.log_updated.connect(self.add_log)
        self.worker.finished_success.connect(self.on_process_finished)
        self.worker.finished_cancelled.connect(self.on_process_cancelled)
        
        self.worker.start()

    # ==========================================

    def cancel_process(self):
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.is_cancelled = True
            
            self.btn_cancel.setEnabled(False)
            self.status_label.setText("Cancelando, aguarde a finalização da requisição atual...")
            self.add_log("Solicitação de cancelamento enviada. Aguardando conclusão.")
            
            from PySide6.QtWidgets import QApplication
            QApplication.processEvents()

    # ==========================================

    def on_process_cancelled(self):
        self.status_label.setText("Cancelamento concluído. Pronto para recomeçar.")
        
        self.btn_run.setEnabled(True)
        self.btn_select.setEnabled(True)
        self.progress.setValue(0)

    # ==========================================

    def on_process_finished(self, output_path: str):
        self.status_label.setText("Processamento concluído!")
        self.add_log(f"Arquivo gerado: {output_path}")

        self.input_file = None
        self.cnpjs = []
        self.info_label.setText("Nenhum arquivo carregado")
        self.status_label.setText("Processamento concluído! Pronto para nova consulta.")
        
        self.btn_run.setEnabled(True)
        self.btn_select.setEnabled(True)
        if hasattr(self, 'btn_cancel'):
            self.btn_cancel.setEnabled(False)
        
        self.progress.setValue(100)

    # ==========================================
    # HELPERS
    # ==========================================
    def add_log(self, message: str):
        self.log.append(message)
    
    def resource_path(self, relative_path: str | Path) -> Path:
        base_path = Path(getattr(sys, "_MEIPASS", Path.cwd()))
        return base_path / Path(relative_path)
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QFormLayout, QLabel, QLineEdit, QTextEdit,
                             QRadioButton, QCheckBox, QPushButton, QButtonGroup,
                             QComboBox, QListWidget, QListWidgetItem, QMessageBox)
from PyQt6.QtCore import Qt
from task import Task


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.setWindowTitle("Task Manager 2.0")
        self.resize(650, 750)

        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название задачи...")
        form_layout.addRow("Task:", self.name_input)

        self.name_input.textChanged.connect(self._on_name_changed)

        self.char_count_label = QLabel("Название: 0 символов")
        form_layout.addRow("", self.char_count_label)

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Введите описание...")
        self.desc_input.setMaximumHeight(80)
        form_layout.addRow("Description:", self.desc_input)

        priority_layout = QHBoxLayout()
        self.priority_group = QButtonGroup(self)
        self.rb_low = QRadioButton("Low")
        self.rb_medium = QRadioButton("Medium")
        self.rb_high = QRadioButton("High")
        self.rb_low.setChecked(True)

        self.priority_group.addButton(self.rb_low)
        self.priority_group.addButton(self.rb_medium)
        self.priority_group.addButton(self.rb_high)

        priority_layout.addWidget(self.rb_low)
        priority_layout.addWidget(self.rb_medium)
        priority_layout.addWidget(self.rb_high)
        form_layout.addRow("Priority:", priority_layout)

        options_layout = QHBoxLayout()
        self.cb_important = QCheckBox("Important")
        self.cb_notify = QCheckBox("Send notification")
        options_layout.addWidget(self.cb_important)
        options_layout.addWidget(self.cb_notify)
        form_layout.addRow("Options:", options_layout)

        main_layout.addLayout(form_layout)

        buttons_layout = QHBoxLayout()
        self.btn_add = QPushButton("Добавить задачу")
        self.btn_add.clicked.connect(self._on_add_task)

        self.btn_clear = QPushButton("Очистить список")
        self.btn_clear.setObjectName("btnClear")
        self.btn_clear.clicked.connect(self._on_clear_tasks)

        buttons_layout.addWidget(self.btn_add)
        buttons_layout.addWidget(self.btn_clear)
        main_layout.addLayout(buttons_layout)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Фильтр по приоритету:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Low", "Medium", "High"])
        self.filter_combo.currentTextChanged.connect(self._on_filter_changed)
        filter_layout.addWidget(self.filter_combo)
        main_layout.addLayout(filter_layout)

        main_layout.addWidget(QLabel("Список задач:"))
        self.task_list = QListWidget()
        main_layout.addWidget(self.task_list)

        self.status_label = QLabel("Задач: 0")
        main_layout.addWidget(self.status_label)

    def _on_name_changed(self, text):
        count = len(text)
        self.char_count_label.setText(f"Название: {count} символов")

    def _on_add_task(self):
        name = self.name_input.text().strip()
        description = self.desc_input.toPlainText().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Название задачи не может быть пустым или состоять из пробелов!")
            return

        priority = "Low"
        if self.rb_medium.isChecked():
            priority = "Medium"
        elif self.rb_high.isChecked():
            priority = "High"

        options = []
        if self.cb_important.isChecked():
            options.append("Important")
        if self.cb_notify.isChecked():
            options.append("Notification")

        new_task = Task(name, description, priority, options)
        self.tasks.append(new_task)

        print(f"=== Новая задача ===")
        print(f"Название: {new_task.name}")
        print(f"Описание: {new_task.description}")
        print(f"Приоритет: {new_task.priority}")
        print(f"Опции: {new_task.options}")
        print(f"=====================")

        item = QListWidgetItem(str(new_task))
        item.setData(Qt.ItemDataRole.UserRole, priority)
        self.task_list.addItem(item)

        self._clear_form()
        self._update_status()
        self._on_filter_changed(self.filter_combo.currentText())

    def _on_clear_tasks(self):
        if self.task_list.count() == 0:
            QMessageBox.information(self, "Информация", "Список задач уже пуст.")
            return

        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены, что хотите удалить все задачи?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.task_list.clear()
            self.tasks.clear()
            self._update_status()

    def _on_filter_changed(self, filter_text):
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            item_priority = item.data(Qt.ItemDataRole.UserRole)
            if filter_text == "All" or item_priority == filter_text:
                item.setHidden(False)
            else:
                item.setHidden(True)

    def _clear_form(self):
        self.name_input.clear()
        self.desc_input.clear()
        self.rb_low.setChecked(True)
        self.cb_important.setChecked(False)
        self.cb_notify.setChecked(False)

    def _update_status(self):
        count = self.task_list.count()
        self.status_label.setText(f"Задач: {count}")

    def _apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QLineEdit, QTextEdit, QComboBox {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton#btnClear {
                background-color: #f44336;
            }
            QPushButton#btnClear:hover {
                background-color: #d32f2f;
            }
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                font-size: 14px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e0e0e0;
                color: black;
            }
            QRadioButton, QCheckBox {
                font-size: 14px;
            }
        """)
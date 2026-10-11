import sys
import os
import math
import random
import tempfile
import wave
import struct

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextBrowser, QFileDialog,
    QMessageBox, QRadioButton, QButtonGroup, QSlider, QInputDialog,
    QColorDialog, QTabWidget, QGroupBox, QSpinBox
)
from PyQt5.QtCore import Qt, QUrl, QRectF, QPointF
from PyQt5.QtGui import QImage, QPixmap, QColor, QPainter, QPen, QBrush, QTransform
from PyQt5.QtMultimedia import QSoundEffect


# ==============================================================================
# ЗАДАНИЕ №1: Статистика из текстового файла (1 балл)
# ==============================================================================
class Task1Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.max_val = None
        self.min_val = None
        self.avg_val = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        group = QGroupBox("Задание №1: Поиск мин, макс и среднего из .txt")
        g_layout = QVBoxLayout(group)

        self.btn_load = QPushButton("Загрузить файл")
        self.btn_load.clicked.connect(self.load_file)
        g_layout.addWidget(self.btn_load)

        self.lbl_max = QLabel("Максимальное значение: —")
        self.lbl_min = QLabel("Минимальное значение: —")
        self.lbl_avg = QLabel("Среднее значение: —")

        g_layout.addWidget(self.lbl_max)
        g_layout.addWidget(self.lbl_min)
        g_layout.addWidget(self.lbl_avg)

        self.btn_save = QPushButton("Сохранить результат")
        self.btn_save.clicked.connect(self.save_file)
        g_layout.addWidget(self.btn_save)

        layout.addWidget(group)
        layout.addStretch()

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите текстовый файл", "", "Text Files (*.txt);;All Files (*)"
        )
        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tokens = content.split()
            if not tokens:
                raise ValueError("Файл пуст.")

            # Преобразование в целые числа
            numbers = [int(token) for token in tokens]

            self.max_val = max(numbers)
            self.min_val = min(numbers)
            self.avg_val = sum(numbers) / len(numbers)

            self.lbl_max.setText(f"Максимальное значение: {self.max_val}")
            self.lbl_min.setText(f"Минимальное значение: {self.min_val}")
            self.lbl_avg.setText(f"Среднее значение: {self.avg_val:.2f}")

        except ValueError:
            QMessageBox.critical(
                self, "Ошибка формата",
                "Файл содержит неверный формат данных (содержит некорректные символы или пуст)!"
            )
            self.reset_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось прочитать файл:\n{e}")
            self.reset_data()

    def reset_data(self):
        self.max_val = None
        self.min_val = None
        self.avg_val = None
        self.lbl_max.setText("Максимальное значение: —")
        self.lbl_min.setText("Минимальное значение: —")
        self.lbl_avg.setText("Среднее значение: —")

    def save_file(self):
        if self.max_val is None:
            QMessageBox.warning(self, "Предупреждение", "Сначала загрузите корректный файл с данными.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить файл", "stats_result.txt", "Text Files (*.txt);;All Files (*)"
        )
        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"Максимальное значение: {self.max_val}\n")
                f.write(f"Минимальное значение: {self.min_val}\n")
                f.write(f"Среднее значение: {self.avg_val:.2f}\n")
            QMessageBox.information(self, "Успех", "Данные успешно сохранены.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{e}")


# ==============================================================================
# ЗАДАНИЕ №2: Простой текстовый редактор (1 балл)
# ==============================================================================
class Task2Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        btn_layout = QHBoxLayout()
        self.btn_new = QPushButton("Создать новый файл")
        self.btn_open = QPushButton("Открыть файл")
        self.btn_save = QPushButton("Сохранить файл")

        self.btn_new.clicked.connect(self.new_file)
        self.btn_open.clicked.connect(self.open_file)
        self.btn_save.clicked.connect(self.save_file)

        btn_layout.addWidget(self.btn_new)
        btn_layout.addWidget(self.btn_open)
        btn_layout.addWidget(self.btn_save)

        layout.addLayout(btn_layout)

        # По условию используется QTextBrowser
        self.text_browser = QTextBrowser()
        self.text_browser.setReadOnly(False)  # Включаем редактирование
        layout.addWidget(self.text_browser)

    def new_file(self):
        self.text_browser.clear()
        self.current_file = None

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть текстовый файл", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.text_browser.setPlainText(f.read())
                self.current_file = file_path
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл:\n{e}")

    def save_file(self):
        if not self.current_file:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Сохранить файл", "", "Text Files (*.txt);;All Files (*)"
            )
            if not file_path:
                return
            self.current_file = file_path

        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(self.text_browser.toPlainText())
            QMessageBox.information(self, "Успех", "Файл сохранен.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{e}")


# ==============================================================================
# ЗАДАНИЕ №3: Квадратная картинка, каналы и повороты (1 балл)
# ==============================================================================
class Task3Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.original_image = None
        self.current_image = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        btn_load = QPushButton("Загрузить квадратное изображение")
        btn_load.clicked.connect(self.load_image)
        layout.addWidget(btn_load)

        controls_layout = QHBoxLayout()

        self.group_channels = QGroupBox("Цветовой канал")
        chan_layout = QVBoxLayout(self.group_channels)
        self.rb_all = QRadioButton("Все каналы (RGB)")
        self.rb_red = QRadioButton("Красный канал (R)")
        self.rb_green = QRadioButton("Зеленый канал (G)")
        self.rb_blue = QRadioButton("Синий канал (B)")
        self.rb_all.setChecked(True)

        for rb in (self.rb_all, self.rb_red, self.rb_green, self.rb_blue):
            chan_layout.addWidget(rb)
            rb.toggled.connect(self.update_view)

        controls_layout.addWidget(self.group_channels)

        rot_layout = QVBoxLayout()
        self.btn_rot_left = QPushButton("Повернуть влево (90°)")
        self.btn_rot_right = QPushButton("Повернуть вправо (90°)")
        self.btn_rot_left.clicked.connect(lambda: self.rotate_image(-90))
        self.btn_rot_right.clicked.connect(lambda: self.rotate_image(90))

        rot_layout.addWidget(self.btn_rot_left)
        rot_layout.addWidget(self.btn_rot_right)
        rot_layout.addStretch()

        controls_layout.addLayout(rot_layout)
        layout.addLayout(controls_layout)

        self.lbl_image = QLabel("Изображение не загружено")
        self.lbl_image.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_image, stretch=1)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите квадратную картинку", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            img = QImage(file_path)
            if img.isNull():
                QMessageBox.critical(self, "Ошибка", "Не удалось загрузить изображение.")
                return

            if img.width() != img.height():
                QMessageBox.warning(self, "Предупреждение", "Изображение не квадратное! Оно будет обрезано до квадрата.")
                side = min(img.width(), img.height())
                img = img.copy(0, 0, side, side)

            self.original_image = img.convertToFormat(QImage.Format_RGB32)
            self.current_image = QImage(self.original_image)
            self.update_view()

    def rotate_image(self, angle):
        if self.current_image is None:
            return
        transform = QTransform().rotate(angle)
        self.current_image = self.current_image.transformed(transform)
        self.update_view()

    def update_view(self):
        if self.current_image is None:
            return

        processed = QImage(self.current_image)

        if not self.rb_all.isChecked():
            for x in range(processed.width()):
                for y in range(processed.height()):
                    col = QColor(processed.pixel(x, y))
                    r, g, b = col.red(), col.green(), col.blue()

                    if self.rb_red.isChecked():
                        processed.setPixel(x, y, QColor(r, 0, 0).rgb())
                    elif self.rb_green.isChecked():
                        processed.setPixel(x, y, QColor(0, g, 0).rgb())
                    elif self.rb_blue.isChecked():
                        processed.setPixel(x, y, QColor(0, 0, b).rgb())

        pix = QPixmap.fromImage(processed)
        self.lbl_image.setPixmap(pix.scaled(350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation))


# ==============================================================================
# ЗАДАНИЕ №4: Прозрачность изображения (alpha-канал) (1 балл)
# ==============================================================================
class Task4Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.base_image = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        btn_load = QPushButton("Загрузить изображение")
        btn_load.clicked.connect(self.load_image)
        layout.addWidget(btn_load)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("Прозрачность (Alpha):"))

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(255)
        self.slider.setValue(255)
        self.slider.valueChanged.connect(self.update_alpha)

        self.lbl_val = QLabel("255")
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.lbl_val)

        layout.addLayout(slider_layout)

        self.lbl_image = QLabel("Изображение не загружено")
        self.lbl_image.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_image, stretch=1)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.base_image = QImage(file_path).convertToFormat(QImage.Format_ARGB32)
            self.update_alpha()

    def update_alpha(self):
        val = self.slider.value()
        self.lbl_val.setText(str(val))

        if self.base_image is None:
            return

        result_img = QImage(self.base_image.size(), QImage.Format_ARGB32)
        result_img.fill(Qt.transparent)

        painter = QPainter(result_img)
        painter.setOpacity(val / 255.0)
        painter.drawImage(0, 0, self.base_image)
        painter.end()

        pix = QPixmap.fromImage(result_img)
        self.lbl_image.setPixmap(pix.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))


# ==============================================================================
# ЗАДАНИЕ №5: Генерация полосатого флага (1 балл)
# ==============================================================================
class Task5Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.btn_gen = QPushButton("Сгенерировать полосатый флаг")
        self.btn_gen.clicked.connect(self.generate_flag)
        layout.addWidget(self.btn_gen)

        self.lbl_flag = QLabel()
        self.lbl_flag.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_flag, stretch=1)

    def generate_flag(self):
        count, ok = QInputDialog.getInt(
            self, "Выбор количества цветов",
            "Введите количество полос (от 1 до 30):",
            value=5, min=1, max=30
        )
        if not ok:
            return

        w, h = 500, 300
        image = QImage(w, h, QImage.Format_RGB32)
        painter = QPainter(image)

        stripe_h = h / count
        for i in range(count):
            color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            painter.fillRect(0, int(i * stripe_h), w, int(stripe_h) + 1, color)

        painter.end()
        self.lbl_flag.setPixmap(QPixmap.fromImage(image))


# ==============================================================================
# ЗАДАНИЕ №6: Рисование смайлика средствами QPainter (2 балла)
# ==============================================================================
class SmileyCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.face_color = QColor(255, 220, 0)
        self.scale_factor = 1.0

    def set_color(self, color):
        if color.isValid():
            self.face_color = color
            self.update()

    def set_scale(self, value):
        self.scale_factor = value / 100.0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        center_x, center_y = w // 2, h // 2

        base_size = min(w, h) * 0.7
        size = int(base_size * self.scale_factor)
        r = size // 2

        # Лицо
        painter.setBrush(QBrush(self.face_color))
        painter.setPen(QPen(Qt.black, 3))
        painter.drawEllipse(center_x - r, center_y - r, size, size)

        # Глаза
        eye_w = int(size * 0.12)
        eye_h = int(size * 0.18)
        eye_dx = int(size * 0.2)
        eye_dy = int(size * 0.15)

        painter.setBrush(QBrush(Qt.black))
        painter.drawEllipse(center_x - eye_dx - eye_w // 2, center_y - eye_dy - eye_h // 2, eye_w, eye_h)
        painter.drawEllipse(center_x + eye_dx - eye_w // 2, center_y - eye_dy - eye_h // 2, eye_w, eye_h)

        # Улыбка
        mouth_w = int(size * 0.5)
        mouth_h = int(size * 0.3)
        mouth_y = center_y - int(size * 0.05)
        painter.drawArc(center_x - mouth_w // 2, mouth_y, mouth_w, mouth_h, 0 * 16, -180 * 16)


class Task6Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.canvas = SmileyCanvas()
        layout.addWidget(self.canvas, stretch=1)

        ctrl_layout = QHBoxLayout()
        self.btn_color = QPushButton("Выбрать цвет смайлика")
        self.btn_color.clicked.connect(self.choose_color)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(20)
        self.slider.setMaximum(150)
        self.slider.setValue(100)
        self.slider.valueChanged.connect(self.canvas.set_scale)

        ctrl_layout.addWidget(self.btn_color)
        ctrl_layout.addWidget(QLabel("Масштаб:"))
        ctrl_layout.addWidget(self.slider)

        layout.addLayout(ctrl_layout)

    def choose_color(self):
        color = QColorDialog.getColor(self.canvas.face_color, self, "Выберите цвет смайлика")
        if color.isValid():
            self.canvas.set_color(color)


# ==============================================================================
# ЗАДАНИЕ №7: Программа «Фортепиано» (2 балла)
# ==============================================================================
class Task7Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.sounds = {}
        self.temp_dir = tempfile.mkdtemp()
        self.init_sounds()
        self.init_ui()

    def init_sounds(self):
        # Автоматическая генерация WAV файлов для нот (чистый синтез звука)
        notes = {
            'До': 261.63,
            'Ре': 293.66,
            'Ми': 329.63,
            'Фа': 349.23,
            'Соль': 392.00,
            'Ля': 440.00,
            'Си': 493.88,
            'До (2)': 523.25
        }
        for name, freq in notes.items():
            path = os.path.join(self.temp_dir, f"{name}.wav")
            self.generate_note_wav(path, freq)
            effect = QSoundEffect()
            effect.setSource(QUrl.fromLocalFile(path))
            self.sounds[name] = effect

    def generate_note_wav(self, file_path, freq, duration=0.8, sample_rate=22050):
        num_samples = int(sample_rate * duration)
        with wave.open(file_path, 'w') as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(sample_rate)
            for i in range(num_samples):
                t = float(i) / sample_rate
                env = max(0.0, 1.0 - (t / duration))
                val = int(32767.0 * 0.5 * math.sin(2.0 * math.pi * freq * t) * env)
                f.writeframesraw(struct.pack('<h', val))

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Клавиши фортепиано:"), alignment=Qt.AlignCenter)

        keys_layout = QHBoxLayout()
        for note in self.sounds.keys():
            btn = QPushButton(note)
            btn.setMinimumHeight(150)
            btn.setStyleSheet(
                "QPushButton { background-color: white; color: black; font-weight: bold; border: 2px solid black; border-radius: 4px; }"
                "QPushButton:pressed { background-color: #dddddd; }"
            )
            btn.clicked.connect(lambda checked, n=note: self.play_note(n))
            keys_layout.addWidget(btn)

        layout.addLayout(keys_layout)

    def play_note(self, note):
        if note in self.sounds:
            self.sounds[note].stop()
            self.sounds[note].play()


# ==============================================================================
# ЗАДАНИЕ №8: Построение L-систем (3 балла)
# ==============================================================================
class LSystemCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.lines = []

    def set_lines(self, lines):
        self.lines = lines
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.white)

        if not self.lines:
            return

        min_x = min(min(p1[0], p2[0]) for p1, p2 in self.lines)
        max_x = max(max(p1[0], p2[0]) for p1, p2 in self.lines)
        min_y = min(min(p1[1], p2[1]) for p1, p2 in self.lines)
        max_y = max(max(p1[1], p2[1]) for p1, p2 in self.lines)

        dx = max_x - min_x or 1.0
        dy = max_y - min_y or 1.0

        margin = 30
        w = self.width() - 2 * margin
        h = self.height() - 2 * margin

        scale = min(w / dx, h / dy)

        painter.setPen(QPen(QColor(0, 100, 200), 2))

        for (x1, y1), (x2, y2) in self.lines:
            px1 = margin + (x1 - min_x) * scale
            py1 = margin + (y1 - min_y) * scale
            px2 = margin + (x2 - min_x) * scale
            py2 = margin + (y2 - min_y) * scale
            painter.drawLine(QPointF(px1, py1), QPointF(px2, py2))


class Task8Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.angle_deg = 0.0
        self.axiom = ""
        self.rules = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()
        self.btn_load = QPushButton("Загрузить L-систему из файла")
        self.btn_load.clicked.connect(self.load_lsystem_file)
        top_layout.addWidget(self.btn_load)

        self.lbl_info = QLabel("Система не загружена")
        top_layout.addWidget(self.lbl_info)

        layout.addLayout(top_layout)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("Шаг эволюции:"))
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(5)
        self.slider.setValue(1)
        self.slider.setEnabled(False)
        self.slider.valueChanged.connect(self.render_system)

        self.lbl_step = QLabel("1")
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.lbl_step)

        layout.addLayout(slider_layout)

        self.canvas = LSystemCanvas()
        layout.addWidget(self.canvas, stretch=1)

    def load_lsystem_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл L-системы", "", "Text Files (*.txt);;All Files (*)"
        )
        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]

            if len(lines) < 4:
                raise ValueError("Файл должен содержать минимум 4 строки (Название, Угол, Аксиома, Правила).")

            self.title = lines[0]
            divisor = int(lines[1])
            self.angle_deg = 360.0 / divisor
            self.axiom = lines[2]

            self.rules = {}
            for line in lines[3:]:
                if '=' in line:
                    k, v = line.split('=', 1)
                    self.rules[k.strip()] = v.strip()
                elif '->' in line:
                    k, v = line.split('->', 1)
                    self.rules[k.strip()] = v.strip()
                elif ' ' in line:
                    parts = line.split(None, 1)
                    self.rules[parts[0]] = parts[1]
                else:
                    self.rules['F'] = line.strip()

            self.lbl_info.setText(f"Система: {self.title} | Угол: {self.angle_deg:.1f}°")
            self.slider.setEnabled(True)
            self.slider.setValue(1)
            self.render_system()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка чтения L-системы", f"Не удалось распарсить файл:\n{e}")

    def generate_string(self, step):
        current = self.axiom
        for _ in range(step):
            nxt = []
            for ch in current:
                nxt.append(self.rules.get(ch, ch))
            current = "".join(nxt)
        return current

    def render_system(self):
        step = self.slider.value()
        self.lbl_step.setText(str(step))

        if not self.axiom:
            return

        l_str = self.generate_string(step)

        # Интерпретация строки Черепахой (Turtle)
        x, y = 0.0, 0.0
        angle = 0.0
        step_len = 10.0

        stack = []
        lines = []

        for ch in l_str:
            if ch in ('F', 'G'):
                rad = math.radians(angle)
                nx = x + step_len * math.cos(rad)
                ny = y + step_len * math.sin(rad)
                lines.append(((x, y), (nx, ny)))
                x, y = nx, ny
            elif ch == 'f':
                rad = math.radians(angle)
                x += step_len * math.cos(rad)
                y += step_len * math.sin(rad)
            elif ch == '+':
                angle += self.angle_deg
            elif ch == '-':
                angle -= self.angle_deg
            elif ch == '[':
                stack.append((x, y, angle))
            elif ch == ']':
                if stack:
                    x, y, angle = stack.pop()

        self.canvas.set_lines(lines)


# ==============================================================================
# ГЛАВНОЕ ОКНО ПРИЛОЖЕНИЯ
# ==============================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа №3 (Задания 1-8)")
        self.resize(850, 650)

        tabs = QTabWidget()
        tabs.addTab(Task1Widget(), "№1 Текст. статистика")
        tabs.addTab(Task2Widget(), "№2 Текстовый редактор")
        tabs.addTab(Task3Widget(), "№3 Каналы / Поворот")
        tabs.addTab(Task4Widget(), "№4 Прозрачность")
        tabs.addTab(Task5Widget(), "№5 Полосатый флаг")
        tabs.addTab(Task6Widget(), "№6 Смайлик QPainter")
        tabs.addTab(Task7Widget(), "№7 Фортепиано")
        tabs.addTab(Task8Widget(), "№8 L-системы")

        self.setCentralWidget(tabs)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
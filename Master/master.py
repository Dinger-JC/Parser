# Parser Industry-Hardstyle-Sex
# Copyright 2026 t.me/Dinger_JC
# Master GUI



# Сторонние библиотеки
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

# Локальные модули
from core import *



class GUI():
    '''Интерфейс'''
    def __init__(self):
        '''Хз что тут написать'''
        self.core = Core()
        self.text1: str = 'Доступные пресеты'
        self.text2: str = '1 (Strip2), 2 (XGroovy), 3 (AnalMedia), 4 (NoodleMagazine), 5 (PornHub)'

        self.Window()

        # Центральный виджет
        self.central_widget = QWidget()
        self.window.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Вывод на окно
        self.layout.addStretch(1)
        self.Text('Industry-Hardstyle-Sex', 'white', 30, 242, 100, Qt.AlignHCenter)
        self.InputField('Введите ссылку на видео...', 600, 40)
        #if download:
        #self.Text(self.window, self.text1, 'yellow', 15, 140, 185)
        #self.Text(self.window, self.text2, 'yellow', 15, 140, 205)
        self.layout.addStretch(5)

        # Показ окна
        self.window.show()

    def Window(self):
        '''Главное окно'''
        self.window = QMainWindow()
        self.window.setWindowTitle('Industry-Hardstyle-Sex - парсер порно контента')
        self.window.setWindowIcon(QIcon('icon.png'))
        self.window.setFixedSize(800, 600)
        self.window.setStyleSheet(
            '''
                QMainWindow {
                    background-color: qlineargradient(
                        spread:pad, x1:0, y1:0, x2:1, y2:1,
                        stop:0 #00081E, stop:0.25 #002A66, stop:0.50 #0661AE, stop:0.75 #3CC5F2, stop:1 #B5F4FA
                    );
                }
                QLabel {
                    color: white;
                    font-family: "Century Gothic";
                    font-size: 24px;
                }
            '''
        )

    def InputField(self, text: str = '', width: int = 0, height: int = 0):
        '''Поле ввода'''
        self.input_field = QLineEdit(self.window)
        self.input_field.setStyleSheet(
            '''
                /* Основное */
                QLineEdit {
                    background-color: #ADADAD;
                    border: 2px solid rgba(255, 255, 255, 255);
                    border-radius: 10px;
                    color: #ADADAD;
                    padding: 5px;
                    font-family: "Century Gothic";
                    font-size: 16px;
                }
                
                /* Активность */
                QLineEdit:focus {
                    border: 2px solid #FFFFFF;
                    background-color: #707070;
                }
                
                /* Наведение */
                QLineEdit:hover {
                    border: 2px solid rgba(60, 197, 242, 150);
                    background-color: rgba(255, 255, 255, 30);
                }
            '''
        )
        self.input_field.setPlaceholderText(text)
        self.input_field.setFixedWidth(width)
        self.input_field.setFixedHeight(height)
        self.input_field.returnPressed.connect(self.Logic)
        self.layout.addWidget(self.input_field, alignment = Qt.AlignHCenter)

    def Logic(self):
        '''Запуск ядра после активации'''
        def Thread(url: str):
            self.core.GetData(self.core.Link(url))
            self.core.GetInfo()
            self.core.GetVideo()

        url = self.input_field.text()
        self.input_field.clear()
        thread = threading.Thread(
            target = Thread,
            args = (url,),
            daemon = True
        )
        thread.start()

    def Text(self, text: str, color: str = 'white', size: int = 20, x: int = 0, y: int = 0, align: str = None):
        '''Блок текста'''
        label = QLabel(text, self.window)
        label.setStyleSheet(
            f'''
                color: {color};
                font-size: {size}px;
                margin: 10px;
            '''
        )
        if align is not None:
            self.layout.addWidget(label, alignment = align)
        else:
            label.move(x, y)
        label.adjustSize()

    def Button(self):
        '''Кнопка'''
        button = QPushButton('Настройки', self.window)
        button.setFixedSize(120, 40)
        button.move(660, 20)



if __name__ == '__main__':
    try:
        other = QApplication(sys.argv)
        master = GUI()
        sys.exit(other.exec())

    except Exception as error:
        log.error(f'Непредвиденная ошибка: {error}')

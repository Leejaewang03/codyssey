import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.current_value = '0'
        self.stored_value = 0.0
        self.operator = ''
        self.is_new_input = True
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Mars Survival Calculator')
        self.setFixedSize(320, 480)
        self.setStyleSheet('background-color: black;')
        
        main_layout = QVBoxLayout()
        
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(100)
        self.display.setStyleSheet('color: white; background-color: black; border: none; font-size: 60px;')
        main_layout.addWidget(self.display)
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        
        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]
        
        for row_idx, row in enumerate(buttons):
            for col_idx, text in enumerate(row):
                button = QPushButton(text)
                
                if text == '0':
                    button.setFixedSize(150, 70)
                    grid_layout.addWidget(button, row_idx, 0, 1, 2)
                else:
                    button.setFixedSize(70, 70)
                    if text == '.':
                        grid_layout.addWidget(button, row_idx, 2)
                    elif text == '=':
                        grid_layout.addWidget(button, row_idx, 3)
                    else:
                        grid_layout.addWidget(button, row_idx, col_idx)
                
                button.clicked.connect(lambda checked, t=text: self.button_clicked(t))
                
                if text in ['÷', '×', '-', '+', '=']:
                    button.setStyleSheet('''
                        QPushButton { background-color: #FF9F0A; color: white; border-radius: 35px; font-size: 30px; }
                        QPushButton:pressed { background-color: #CC7A00; }
                    ''')
                elif text in ['AC', '+/-', '%']:
                    button.setStyleSheet('''
                        QPushButton { background-color: #A5A5A5; color: black; border-radius: 35px; font-size: 24px; }
                        QPushButton:pressed { background-color: #D4D4D2; }
                    ''')
                else:
                    padding = 'padding-left: -50px;' if text == '0' else ''
                    button.setStyleSheet(f'''
                        QPushButton {{ background-color: #333333; color: white; border-radius: 35px; font-size: 30px; {padding} }}
                        QPushButton:pressed {{ background-color: #737373; }}
                    ''')
                    
        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)
        self.show()

    # ---------------------------------------------------------
    # [1] 코어 로직: 사칙연산 메소드 구현
    # ---------------------------------------------------------
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        # 수학적 예외처리: 0으로 나눌 경우 명시적으로 에러를 발생시킵니다.
        if b == 0:
            raise ZeroDivisionError
        return a / b

    # ---------------------------------------------------------
    # [2] 코어 로직: 특수 기능 메소드 구현
    # ---------------------------------------------------------
    def reset(self):
        self.current_value = '0'
        self.stored_value = 0.0
        self.operator = ''
        self.is_new_input = True
        self.update_display()

    # (주의: 파이썬 함수명에는 '-'를 쓸 수 없어 언더바 '_'로 대체했습니다)
    def negative_positive(self):
        if self.current_value != '0' and self.current_value != 'Error':
            if self.current_value.startswith('-'):
                self.current_value = self.current_value[1:]
            else:
                self.current_value = '-' + self.current_value
            self.update_display()

    def percent(self):
        if self.current_value != 'Error':
            try:
                val = float(self.current_value) / 100
                self.current_value = self.format_result(val)
                self.update_display()
                self.is_new_input = True
            except Exception:
                self.current_value = 'Error'
                self.update_display()

    def equal(self):
        if self.operator == '':
            return
            
        try:
            current = float(self.current_value)
            result = 0.0
            
            # operator 기호에 따라 분기하여 코어 사칙연산 메소드를 호출합니다.
            if self.operator == '+':
                result = self.add(self.stored_value, current)
            elif self.operator == '-':
                result = self.subtract(self.stored_value, current)
            elif self.operator == '×':
                result = self.multiply(self.stored_value, current)
            elif self.operator == '÷':
                result = self.divide(self.stored_value, current)
                
            # 계산 결과를 포맷팅(6자리 반올림 등)하여 화면에 반영합니다.
            self.current_value = self.format_result(result)
            
        except ZeroDivisionError:
            self.current_value = 'Error'
        except OverflowError:
            self.current_value = 'Error'
        except Exception:
            self.current_value = 'Error'
            
        self.operator = ''
        self.is_new_input = True
        self.update_display()

    # ---------------------------------------------------------
    # [3] 보너스 과제: 출력 포맷 및 다이내믹 폰트 사이즈 조정
    # ---------------------------------------------------------
    def format_result(self, value):
        # 소수점 6자리 이하의 경우 반올림 (예: 3.33333333... -> 3.333333)
        val = round(value, 6)
        if val.is_integer():
            return str(int(val))
        return str(val)

    def update_display(self):
        text_length = len(self.current_value)
        font_size = 60  # 기본 폰트 크기
        
        # 글자 수가 7자리를 넘어가면 길이에 비례하여 폰트 크기를 줄입니다 (최소 20px)
        if text_length > 7:
            font_size = max(20, 60 - (text_length - 7) * 4)
            
        # 계산된 폰트 크기를 스타일시트에 다시 덮어씌웁니다.
        self.display.setStyleSheet(f'color: white; background-color: black; border: none; font-size: {font_size}px;')
        self.display.setText(self.current_value)

    # ---------------------------------------------------------
    # [4] UI 이벤트 라우터 (버튼 클릭 감지)
    # ---------------------------------------------------------
    def button_clicked(self, text):
        if text in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if self.is_new_input:
                self.current_value = text
                self.is_new_input = False
            else:
                self.current_value += text
            self.update_display()
            
        elif text == 'AC':
            self.reset()
            
        elif text == '.':
            if '.' not in self.current_value:
                self.current_value += '.'
                self.update_display()
                self.is_new_input = False
                
        elif text in ['+', '-', '×', '÷']:
            if self.operator != '':
                self.equal()
            self.operator = text
            if self.current_value != 'Error':
                self.stored_value = float(self.current_value)
            self.is_new_input = True
            
        elif text == '=':
            self.equal()
            
        elif text == '+/-':
            self.negative_positive()
            
        elif text == '%':
            self.percent()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    sys.exit(app.exec_())
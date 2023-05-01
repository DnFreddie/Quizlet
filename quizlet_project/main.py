import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,QLineEdit,QMessageBox
from quizlet import Instance

class FirstWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        MAIN_DESCRIPTION = '''
        Welcome to Quizlet!
        What do you want to do?
        '''
        self.setWindowTitle('First Window')
        self.setGeometry(100, 100, 300, 200)
        self.label = QLabel()
        self.central_widget = QWidget()
        self.label.setText(MAIN_DESCRIPTION)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.central_widget.setLayout(self.layout)
        self.setLayout(self.layout)
        self.third_button = QPushButton("Revise")
        self.layout.addWidget(self.third_button)
        
        self.third_button.clicked.connect(self.go_to_third_window)

        button = QPushButton('Add new words', self)
        self.layout.addWidget(button)
        button.clicked.connect(self.go_to_second_window)

    def go_to_second_window(self):
        self.second_window = SecondWindow()
        self.second_window.show()
        self.hide()
    
    def go_to_third_window(self):
        self.third_window = ThirdWindow()
        self.third_window.show()
        self.hide()

class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('New Words')
        self.setGeometry(100, 100, 300, 200)
        self.label = QLabel()
        self.central_widget = QWidget()
        self.layout = QVBoxLayout ()
        self.label1 =  QLabel()
        self.label1.setText("Word")
        self.label2 =  QLabel()
        self.label2.setText("Translation")
        self.assuerence = QLabel()
        self.line_edit1 = QLineEdit()
        self.line_edit2 = QLineEdit()
        self.add_word_button = QPushButton("Add Word", self)
        self.button = QPushButton("HOME",self)
        self.close_button = QPushButton("Exit")
        self.central_widget.setLayout(self.layout)
        self.setLayout(self.layout)
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.line_edit1)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.line_edit2)
        self.layout.addWidget(self.assuerence)
        self.layout.addWidget(self.add_word_button)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.close_button)
        # Buttons 
        
        self.button.clicked.connect(self.go_to_first_window)
        self.add_word_button.clicked.connect(self.add_words)
        self.close_button.clicked.connect(self.exit)
    def go_to_first_window(self):
        self.first_window = FirstWindow()
        self.first_window.show()
        self.hide()
    
    def add_words(self):
        word_from_box = self.line_edit2.text()
        translation_from_box = self.line_edit1.text()
        insert = Instance(translation_from_box ,word_from_box )
        insert.create_table()
        insert.insert_word()
        self.line_edit1.clear()
        self.line_edit2.clear()
        self.assuerence.setText(f"The word {translation_from_box}has been added")
        
    def exit(self):
        reply = QMessageBox.warning(self, 'Exit', "Are you sure you want to quit?", QMessageBox.No | QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.close()
        else:
            pass


        
class ThirdWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.score = 0 
        self.setWindowTitle('Revise')
        self.setGeometry(100, 100, 300, 200)
        
        # Create layout and widget
        self.layout = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        # Create labels
        self.label1 = QLabel("Translation:")
        self.label2 = QLabel()
        # Create buttons
        self.check_button = QPushButton("Check")
        self.solution_button = QPushButton("Solution")
        self.home_button = QPushButton("Home")
        self.exit_button = QPushButton("Exit")

        # Load a new word
        self.instance = Instance("", "")
        if len(self.instance) == 0:
            self.label2.setText("NO WORDS in database!\n Add a word first!")
            self.check_button.setDisabled(True)
            self.solution_button.setDisabled(True)
            
                
        else:
            self.first_variable, self.second_variable = self.instance.load_word()
            self.label2.setText(self.first_variable) 
    # Create line edits

        # Create line edits
        self.line_edit1 = QLineEdit()
        self.hints  = QLabel("Hint",self)

        
        # Add widgets to layout
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.line_edit1)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.hints)
        self.layout.addWidget(self.check_button)
        self.layout.addWidget(self.solution_button)
        self.layout.addWidget(self.home_button)
        self.layout.addWidget(self.exit_button)

        # Connect button signals to slots
        self.check_button.clicked.connect(self.check)
        self.home_button.clicked.connect(self.go_to_first_window)
        self.exit_button.clicked.connect(self.exit)
        self.solution_button.clicked.connect(self.solution)

        # Set layout for the window
        self.setLayout(self.layout)
        
    def go_to_first_window(self):
        self.first_window = FirstWindow()
        self.first_window.show()
        self.hide()
    def show_letters(self,word): 

        name = ""

        for letter in range(self.score):
            if letter < len(word):

                name += word[letter]
            else: 
                break

                
        
        self.hints.setText(name)
 
        
    def check(self):
        user_input = self.line_edit1.text()
        translation = self.second_variable
        if user_input != translation:
            self.line_edit1.clear()
            self.score +=1
            self.show_letters(translation)
            
        else:
            # Clear input field
            self.line_edit1.clear()

            # Refresh window with new word
            self.score = 0
            self.hints.setText("Here we go again!")
            self.variables = Instance("", "").load_word()
            self.first_variable = self.variables[0]
            self.second_variable = self.variables[1]
            self.label2.setText(self.first_variable)
    def solution (self):
        print(self.second_variable)
        reply = QMessageBox.warning(self, 'The Solution ', f"The solution is: \n{self.second_variable}", QMessageBox.Yes)


   
    
    
    
    
    def exit(self):
        reply = QMessageBox.warning(self, 'Exit', "Are you sure you want to quit?", QMessageBox.No | QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.close()
        else:
            pass





if __name__ == '__main__':
    app = QApplication(sys.argv)
    first_window = FirstWindow()
    first_window.show()
    sys.exit(app.exec_())


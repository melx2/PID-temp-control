
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from QLed import QLed

class Widget(QWidget):
    def __init__(self ,parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        l=QVBoxLayout(self)
        self._led=QLed(self, onColour=QLed.Red, shape=QLed.Circle)
        self._led.value=True
        l.addWidget(self._led)
        
if __name__=="__main__":
    from sys import argv, exit
    
    a=QApplication(argv)
    w=Widget()
    w.show()
    exit(a.exec_())


    
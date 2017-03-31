import sys
from PyQt4.QtGui import QApplication, QWidget


def main():
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(450, 750)
    w.move(100, 100)
    w.setWindowTitle('Simple')
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

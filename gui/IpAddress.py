from PySide6 import QtWidgets

class IpAddress(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Initialize LineEdits for IPv4 address
        self.pos0 = QtWidgets.QLineEdit()
        self.pos1 = QtWidgets.QLineEdit()
        self.pos2 = QtWidgets.QLineEdit()
        self.pos3 = QtWidgets.QLineEdit()

        # Initialize labels for title and dots
        self.title = QtWidgets.QLabel('IP: ')
        self.dot0 = QtWidgets.QLabel('.')
        self.dot1 = QtWidgets.QLabel('.')
        self.dot2 = QtWidgets.QLabel('.')

        # Set parameters for LineEdits
        self.setParameters(self.pos0)
        self.setParameters(self.pos1)
        self.setParameters(self.pos2)
        self.setParameters(self.pos3)

        # Add everything to HBox
        self.box_array = QtWidgets.QHBoxLayout()
        self.box_array.setSpacing(1)
        self.box_array.addWidget(self.title)
        self.box_array.addWidget(self.pos0)
        self.box_array.addWidget(self.dot0)
        self.box_array.addWidget(self.pos1)
        self.box_array.addWidget(self.dot1)
        self.box_array.addWidget(self.pos2)
        self.box_array.addWidget(self.dot2)
        self.box_array.addWidget(self.pos3)

        # Connect textChanged to slots
        self.pos0.textChanged.connect(self.pos0Changed)
        self.pos1.textChanged.connect(self.pos1Changed)
        self.pos2.textChanged.connect(self.pos2Changed)
        self.pos3.textChanged.connect(self.pos3Changed)

        # Add grid to group
        self.setLayout(self.box_array)

    def pos0Changed(self,flags):
        if self.pos0.text().__len__() >= 3:
            self.pos1.setFocus()
            self.pos1.selectAll()

    def pos1Changed(self,flags):
        if self.pos1.text().__len__() >= 3:
            self.pos2.setFocus()
            self.pos2.selectAll()
        elif self.pos1.text().__len__() == 0:
            self.pos0.setFocus()
            self.pos0.selectAll()
            self.pos0.setCursorPosition(self.pos0.text().__len__())

    def pos2Changed(self,flags):
        if self.pos2.text().__len__() >= 3:
            self.pos3.setFocus()
            self.pos3.selectAll()
        elif self.pos2.text().__len__() == 0:
            self.pos1.setFocus()
            self.pos1.selectAll()
            self.pos1.setCursorPosition(self.pos1.text().__len__())

    def pos3Changed(self,flags):
        if self.pos3.text().__len__() == 0:
            self.pos2.setFocus()
            self.pos2.selectAll()
            self.pos2.setCursorPosition(self.pos2.text().__len__())

    def setParameters(self, object):
        object.setMinimumHeight(20)
        object.setMaximumWidth(38)
        object.setFrame(False)
        object.setInputMask('999')
        object.setText('')
    
    # Returns LineEdits' current IP address as a string
    def getIP(self):
        ip = ''
        ip =  self.pos0.text().replace(' ','') + '.'\
            + self.pos1.text().replace(' ','') + '.'\
            + self.pos2.text().replace(' ','') + '.'\
            + self.pos3.text().replace(' ','')
        return ip
    
    # Sets LineEdit boxes to a given IP address
    def setValue(self, ip):
        split = ip.split('.',4)
        self.pos0.setText(split[0])
        self.pos1.setText(split[1])
        self.pos2.setText(split[2])
        self.pos3.setText(split[3])
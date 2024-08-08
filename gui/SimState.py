from PySide6 import QtCore, QtWidgets

class SimState(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()

        # Define text for sim state
        self.state_txt = QtWidgets.QLabel(alignment = QtCore.Qt.AlignCenter)
        self.state_txt.setText("IDLE")
        self.state_txt.setFrameStyle(QtWidgets.QFrame.Shape.NoFrame | QtWidgets.QFrame.Shadow.Plain)
        self.idle_style = "QLabel { background-color : grey; border-radius : 5px; font : bold 15px; color : darkgrey}"
        self.loading_style = "QLabel { background-color : grey; border-radius : 5px; font : bold 15px; color : white}"
        self.paused_style = "QLabel { background-color : yellow; border-radius : 5px; font : bold 15px; color : black}"
        self.racing_style = "QLabel { background-color : green; border-radius : 5px; font : bold 15px; color : black}"
        self.state_txt.setStyleSheet(self.idle_style)
        self.state_txt.setMaximumHeight(30)
        self.state_txt.setMinimumHeight(30)
        self.state_txt.setMaximumWidth(180)
        self.state_txt.setMinimumWidth(180)

        # Define box to place text
        self.box = QtWidgets.QVBoxLayout(alignment = QtCore.Qt.AlignCenter)
        self.box.addWidget(self.state_txt)

        # Add grid to group
        self.setLayout(self.box)

    def update(self,flags):
        racing = (flags & 0x1)        # Bit 1 
        paused = (flags & 0x2) >> 1   # Bit 2
        loading = (flags & 0x4) >> 2  # Bit 3
        in_gear = (flags & 0x8) >> 3  # Bit 4

        # Piority: paused > racing > loading
        # Another possible scenario is replay mode when not racing, but in gear
        if paused:
            self.state_txt.setText("PAUSED")
            self.state_txt.setStyleSheet(self.paused_style)
        elif racing:
            self.state_txt.setText("RACING")
            self.state_txt.setStyleSheet(self.racing_style)
        elif loading:
            self.state_txt.setText("LOADING")
            self.state_txt.setStyleSheet(self.loading_style)
        elif not racing and in_gear:
            self.state_txt.setText("AUTO/REPLAY")
            self.state_txt.setStyleSheet(self.racing_style)
        else:
            self.state_txt.setText("IDLE")
            self.state_txt.setStyleSheet(self.idle_style)


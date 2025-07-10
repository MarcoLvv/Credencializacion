# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'modulo.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QLineEdit, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(480, 207)
        palette = QPalette()
        brush = QBrush(QColor(85, 170, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush)
        brush1 = QBrush(QColor(20, 85, 119, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush1)
        Dialog.setPalette(palette)
        Dialog.setAutoFillBackground(False)
        self.buttonBoxModulo = QDialogButtonBox(Dialog)
        self.buttonBoxModulo.setObjectName(u"buttonBoxModulo")
        self.buttonBoxModulo.setGeometry(QRect(320, 174, 156, 24))
        palette1 = QPalette()
        brush2 = QBrush(QColor(92, 176, 229, 255))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush2)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush2)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush2)
        self.buttonBoxModulo.setPalette(palette1)
        self.buttonBoxModulo.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBoxModulo.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.txtModulo = QLabel(Dialog)
        self.txtModulo.setObjectName(u"txtModulo")
        self.txtModulo.setGeometry(QRect(120, 60, 240, 19))
        font = QFont()
        font.setFamilies([u"Arial Rounded MT"])
        font.setPointSize(12)
        font.setBold(True)
        self.txtModulo.setFont(font)
        self.txtModulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineModulo = QLineEdit(Dialog)
        self.lineModulo.setObjectName(u"lineModulo")
        self.lineModulo.setGeometry(QRect(120, 90, 240, 31))
        palette2 = QPalette()
        brush3 = QBrush(QColor(0, 0, 0, 255))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush3)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush3)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush3)
        brush4 = QBrush(QColor(255, 255, 255, 255))
        brush4.setStyle(Qt.BrushStyle.SolidPattern)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush4)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush3)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush3)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush3)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush4)
        self.lineModulo.setPalette(palette2)

        self.retranslateUi(Dialog)
        self.buttonBoxModulo.accepted.connect(Dialog.accept)
        self.buttonBoxModulo.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.txtModulo.setText(QCoreApplication.translate("Dialog", u"Ingresa Numero De Modulo", None))
    # retranslateUi


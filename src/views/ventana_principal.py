# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'propuesta_principalv3.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QStatusBar, QTableView, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1218, 770)
        MainWindow.setMinimumSize(QSize(1218, 770))
        MainWindow.setStyleSheet(u"QMainWindow#MainWindow{\n"
"	background-color: qradialgradient(spread:reflect, cx:0.5, cy:0.499, radius:2, fx:0.512088, fy:1, stop:0.0549451 rgba(7, 49, 80, 255), stop:0.0989011 rgba(8, 48, 83, 255), stop:0.917582 rgba(6, 47, 78, 255));\n"
"	border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border-radius: 25px\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.mainWidget = QWidget(self.centralwidget)
        self.mainWidget.setObjectName(u"mainWidget")
        self.horizontalLayout_3 = QHBoxLayout(self.mainWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.buttonsBar = QWidget(self.mainWidget)
        self.buttonsBar.setObjectName(u"buttonsBar")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.buttonsBar.sizePolicy().hasHeightForWidth())
        self.buttonsBar.setSizePolicy(sizePolicy1)
        self.buttonsBar.setStyleSheet(u"QWidget#buttonsBar{\n"
"	background-color: qradialgradient(spread:pad, cx:0.5, cy:0.494, radius:0.694, fx:0.5, fy:0.5, stop:0.225275 rgba(10, 54, 84, 255), stop:0.236264 rgba(10, 54, 84, 255), stop:0.796703 rgba(10, 46, 70, 255), stop:0.835165 rgba(10, 46, 70, 255));\n"
"	border-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:2, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.401099 rgba(9, 54, 82, 255), stop:0.758242 rgba(14, 76, 118, 255));\n"
"\n"
"    border-top-left-radius: 10px;\n"
"    border-bottom-left-radius: 10px;\n"
"\n"
"\n"
"\n"
"}")
        self.verticalLayout = QVBoxLayout(self.buttonsBar)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.homeBtn = QPushButton(self.buttonsBar)
        self.homeBtn.setObjectName(u"homeBtn")
        self.homeBtn.setMinimumSize(QSize(160, 70))
        self.homeBtn.setMaximumSize(QSize(160, 70))
        font = QFont()
        font.setFamilies([u"Sans Serif Collection"])
        font.setPointSize(12)
        font.setBold(True)
        font.setStyleStrategy(QFont.PreferAntialias)
        self.homeBtn.setFont(font)
        self.homeBtn.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.homeBtn.setAutoFillBackground(False)
        self.homeBtn.setStyleSheet(u"text-align: left;   /* o: right, center */\n"
"padding-left: 10px;")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoHome))
        self.homeBtn.setIcon(icon)

        self.verticalLayout.addWidget(self.homeBtn)

        self.captureBtn = QPushButton(self.buttonsBar)
        self.captureBtn.setObjectName(u"captureBtn")
        self.captureBtn.setMinimumSize(QSize(160, 70))
        self.captureBtn.setMaximumSize(QSize(160, 70))
        font1 = QFont()
        font1.setFamilies([u"Sans Serif Collection"])
        font1.setPointSize(12)
        font1.setBold(True)
        self.captureBtn.setFont(font1)
        self.captureBtn.setStyleSheet(u"text-align: left;   /* o: right, center */\n"
"padding-left: 10px;")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentNew))
        self.captureBtn.setIcon(icon1)

        self.verticalLayout.addWidget(self.captureBtn)

        self.importBtn = QPushButton(self.buttonsBar)
        self.importBtn.setObjectName(u"importBtn")
        self.importBtn.setMinimumSize(QSize(160, 70))
        self.importBtn.setMaximumSize(QSize(160, 70))
        self.importBtn.setFont(font1)
        self.importBtn.setStyleSheet(u"text-align: left;   /* o: right, center */\n"
"padding-left: 10px;")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoDown))
        self.importBtn.setIcon(icon2)

        self.verticalLayout.addWidget(self.importBtn)

        self.verticalSpacer = QSpacerItem(160, 420, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.exportBtn = QPushButton(self.buttonsBar)
        self.exportBtn.setObjectName(u"exportBtn")
        self.exportBtn.setMinimumSize(QSize(160, 70))
        self.exportBtn.setMaximumSize(QSize(160, 70))
        self.exportBtn.setFont(font1)
        self.exportBtn.setStyleSheet(u"text-align: left;   /* o: right, center */\n"
"padding-left: 10px;")
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoUp))
        self.exportBtn.setIcon(icon3)

        self.verticalLayout.addWidget(self.exportBtn)


        self.horizontalLayout_3.addWidget(self.buttonsBar)

        self.stackedWidget = QStackedWidget(self.mainWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        self.stackedWidget.setPalette(palette)
        self.homeView = QWidget()
        self.homeView.setObjectName(u"homeView")
        sizePolicy.setHeightForWidth(self.homeView.sizePolicy().hasHeightForWidth())
        self.homeView.setSizePolicy(sizePolicy)
        self.verticalLayout_5 = QVBoxLayout(self.homeView)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.homeFrame = QFrame(self.homeView)
        self.homeFrame.setObjectName(u"homeFrame")
        self.homeFrame.setStyleSheet(u"QFrame#frameIndex{\n"
"	background-color:rgb(244, 246, 247);\n"
"    border-top-right-radius: 10px;\n"
"    border-bottom-right-radius: 10px;\n"
"\n"
"}")
        self.homeFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.homeFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.homeFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.infoWidget = QWidget(self.homeFrame)
        self.infoWidget.setObjectName(u"infoWidget")
        self.horizontalLayout_7 = QHBoxLayout(self.infoWidget)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.labelSistemaCuajimalpa = QLabel(self.infoWidget)
        self.labelSistemaCuajimalpa.setObjectName(u"labelSistemaCuajimalpa")
        self.labelSistemaCuajimalpa.setMinimumSize(QSize(400, 81))
        self.labelSistemaCuajimalpa.setMaximumSize(QSize(400, 81))
        font2 = QFont()
        font2.setFamilies([u"Sans Serif Collection"])
        font2.setPointSize(20)
        font2.setBold(False)
        self.labelSistemaCuajimalpa.setFont(font2)
        self.labelSistemaCuajimalpa.setStyleSheet(u"\n"
"color: rgb(0, 0, 0);")
        self.labelSistemaCuajimalpa.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.labelSistemaCuajimalpa, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)


        self.verticalLayout_3.addWidget(self.infoWidget)

        self.usersTableFrame = QFrame(self.homeFrame)
        self.usersTableFrame.setObjectName(u"usersTableFrame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.usersTableFrame.sizePolicy().hasHeightForWidth())
        self.usersTableFrame.setSizePolicy(sizePolicy2)
        self.usersTableFrame.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.usersTableFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.usersTableFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.usersTableFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.searchBar = QLineEdit(self.usersTableFrame)
        self.searchBar.setObjectName(u"searchBar")
        self.searchBar.setMinimumSize(QSize(435, 31))
        self.searchBar.setMaximumSize(QSize(435, 31))
        self.searchBar.setStyleSheet(u"background-color: rgb(245, 248, 247);")

        self.verticalLayout_2.addWidget(self.searchBar)

        self.usersTableView = QTableView(self.usersTableFrame)
        self.usersTableView.setObjectName(u"usersTableView")

        self.verticalLayout_2.addWidget(self.usersTableView)


        self.verticalLayout_3.addWidget(self.usersTableFrame)


        self.verticalLayout_5.addWidget(self.homeFrame)

        self.stackedWidget.addWidget(self.homeView)
        self.captureView = QWidget()
        self.captureView.setObjectName(u"captureView")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.captureView.sizePolicy().hasHeightForWidth())
        self.captureView.setSizePolicy(sizePolicy3)
        self.captureView.setMinimumSize(QSize(923, 666))
        self.horizontalLayout_2 = QHBoxLayout(self.captureView)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.actionsCaptureWidget = QWidget(self.captureView)
        self.actionsCaptureWidget.setObjectName(u"actionsCaptureWidget")
        sizePolicy.setHeightForWidth(self.actionsCaptureWidget.sizePolicy().hasHeightForWidth())
        self.actionsCaptureWidget.setSizePolicy(sizePolicy)
        self.actionsCaptureWidget.setMinimumSize(QSize(275, 645))
        self.actionsCaptureWidget.setMaximumSize(QSize(275, 16777215))
        self.verticalLayout_7 = QVBoxLayout(self.actionsCaptureWidget)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.widgetbuttonsBarPhoto = QWidget(self.actionsCaptureWidget)
        self.widgetbuttonsBarPhoto.setObjectName(u"widgetbuttonsBarPhoto")
        sizePolicy.setHeightForWidth(self.widgetbuttonsBarPhoto.sizePolicy().hasHeightForWidth())
        self.widgetbuttonsBarPhoto.setSizePolicy(sizePolicy)
        self.widgetbuttonsBarPhoto.setMaximumSize(QSize(257, 16777215))
        self.verticalLayout_6 = QVBoxLayout(self.widgetbuttonsBarPhoto)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.widgetPhoto = QWidget(self.widgetbuttonsBarPhoto)
        self.widgetPhoto.setObjectName(u"widgetPhoto")
        sizePolicy1.setHeightForWidth(self.widgetPhoto.sizePolicy().hasHeightForWidth())
        self.widgetPhoto.setSizePolicy(sizePolicy1)
        self.verticalLayout_9 = QVBoxLayout(self.widgetPhoto)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.comboBoxCamera = QComboBox(self.widgetPhoto)
        self.comboBoxCamera.setObjectName(u"comboBoxCamera")
        self.comboBoxCamera.setMinimumSize(QSize(217, 30))
        self.comboBoxCamera.setMaximumSize(QSize(217, 30))

        self.verticalLayout_9.addWidget(self.comboBoxCamera)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_6)

        self.labelPhoto = QLabel(self.widgetPhoto)
        self.labelPhoto.setObjectName(u"labelPhoto")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.labelPhoto.sizePolicy().hasHeightForWidth())
        self.labelPhoto.setSizePolicy(sizePolicy4)
        self.labelPhoto.setMinimumSize(QSize(170, 190))
        self.labelPhoto.setMaximumSize(QSize(170, 190))
        self.labelPhoto.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_9.addWidget(self.labelPhoto, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_5)

        self.startPhotoBtn = QPushButton(self.widgetPhoto)
        self.startPhotoBtn.setObjectName(u"startPhotoBtn")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.startPhotoBtn.sizePolicy().hasHeightForWidth())
        self.startPhotoBtn.setSizePolicy(sizePolicy5)
        self.startPhotoBtn.setMinimumSize(QSize(0, 35))
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.CameraPhoto))
        self.startPhotoBtn.setIcon(icon4)

        self.verticalLayout_9.addWidget(self.startPhotoBtn)

        self.uploadPhotoBtn = QPushButton(self.widgetPhoto)
        self.uploadPhotoBtn.setObjectName(u"uploadPhotoBtn")
        self.uploadPhotoBtn.setMinimumSize(QSize(0, 35))
        icon5 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen))
        self.uploadPhotoBtn.setIcon(icon5)

        self.verticalLayout_9.addWidget(self.uploadPhotoBtn)


        self.verticalLayout_6.addWidget(self.widgetPhoto)

        self.widgetBtn = QWidget(self.widgetbuttonsBarPhoto)
        self.widgetBtn.setObjectName(u"widgetBtn")
        self.widgetBtn.setMinimumSize(QSize(236, 190))
        self.widgetBtn.setMaximumSize(QSize(236, 210))
        self.verticalLayout_11 = QVBoxLayout(self.widgetBtn)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.labelSignature = QLabel(self.widgetBtn)
        self.labelSignature.setObjectName(u"labelSignature")
        sizePolicy4.setHeightForWidth(self.labelSignature.sizePolicy().hasHeightForWidth())
        self.labelSignature.setSizePolicy(sizePolicy4)
        self.labelSignature.setMinimumSize(QSize(200, 60))
        self.labelSignature.setMaximumSize(QSize(200, 60))
        font3 = QFont()
        font3.setBold(False)
        self.labelSignature.setFont(font3)
        self.labelSignature.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.labelSignature.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_11.addWidget(self.labelSignature, 0, Qt.AlignmentFlag.AlignHCenter)

        self.startSignatureBtn = QPushButton(self.widgetBtn)
        self.startSignatureBtn.setObjectName(u"startSignatureBtn")
        self.startSignatureBtn.setMinimumSize(QSize(0, 35))
        icon6 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MailMessageNew))
        self.startSignatureBtn.setIcon(icon6)

        self.verticalLayout_11.addWidget(self.startSignatureBtn)


        self.verticalLayout_6.addWidget(self.widgetBtn)

        self.saveDataBtn = QPushButton(self.widgetbuttonsBarPhoto)
        self.saveDataBtn.setObjectName(u"saveDataBtn")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.saveDataBtn.sizePolicy().hasHeightForWidth())
        self.saveDataBtn.setSizePolicy(sizePolicy6)
        self.saveDataBtn.setMinimumSize(QSize(0, 35))
        icon7 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.saveDataBtn.setIcon(icon7)

        self.verticalLayout_6.addWidget(self.saveDataBtn)


        self.verticalLayout_7.addWidget(self.widgetbuttonsBarPhoto)


        self.horizontalLayout_2.addWidget(self.actionsCaptureWidget, 0, Qt.AlignmentFlag.AlignHCenter)

        self.dataWidget = QWidget(self.captureView)
        self.dataWidget.setObjectName(u"dataWidget")
        self.horizontalLayout_4 = QHBoxLayout(self.dataWidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.dataWidgetL = QWidget(self.dataWidget)
        self.dataWidgetL.setObjectName(u"dataWidgetL")
        self.verticalLayout_4 = QVBoxLayout(self.dataWidgetL)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.txt_nombre = QLabel(self.dataWidgetL)
        self.txt_nombre.setObjectName(u"txt_nombre")

        self.verticalLayout_4.addWidget(self.txt_nombre)

        self.nombre = QLineEdit(self.dataWidgetL)
        self.nombre.setObjectName(u"nombre")

        self.verticalLayout_4.addWidget(self.nombre)

        self.txt_paterno = QLabel(self.dataWidgetL)
        self.txt_paterno.setObjectName(u"txt_paterno")

        self.verticalLayout_4.addWidget(self.txt_paterno)

        self.paterno = QLineEdit(self.dataWidgetL)
        self.paterno.setObjectName(u"paterno")

        self.verticalLayout_4.addWidget(self.paterno)

        self.txt_materno = QLabel(self.dataWidgetL)
        self.txt_materno.setObjectName(u"txt_materno")

        self.verticalLayout_4.addWidget(self.txt_materno)

        self.materno = QLineEdit(self.dataWidgetL)
        self.materno.setObjectName(u"materno")

        self.verticalLayout_4.addWidget(self.materno)

        self.txt_curp = QLabel(self.dataWidgetL)
        self.txt_curp.setObjectName(u"txt_curp")

        self.verticalLayout_4.addWidget(self.txt_curp)

        self.curp = QLineEdit(self.dataWidgetL)
        self.curp.setObjectName(u"curp")

        self.verticalLayout_4.addWidget(self.curp)

        self.txt_domicilio = QLabel(self.dataWidgetL)
        self.txt_domicilio.setObjectName(u"txt_domicilio")

        self.verticalLayout_4.addWidget(self.txt_domicilio)

        self.fechaNacimiento = QDateEdit(self.dataWidgetL)
        self.fechaNacimiento.setObjectName(u"fechaNacimiento")

        self.verticalLayout_4.addWidget(self.fechaNacimiento)

        self.txt_calle = QLabel(self.dataWidgetL)
        self.txt_calle.setObjectName(u"txt_calle")

        self.verticalLayout_4.addWidget(self.txt_calle)

        self.calle = QLineEdit(self.dataWidgetL)
        self.calle.setObjectName(u"calle")

        self.verticalLayout_4.addWidget(self.calle)

        self.txt_lote = QLabel(self.dataWidgetL)
        self.txt_lote.setObjectName(u"txt_lote")

        self.verticalLayout_4.addWidget(self.txt_lote)

        self.lote = QLineEdit(self.dataWidgetL)
        self.lote.setObjectName(u"lote")

        self.verticalLayout_4.addWidget(self.lote)

        self.txt_manzana = QLabel(self.dataWidgetL)
        self.txt_manzana.setObjectName(u"txt_manzana")

        self.verticalLayout_4.addWidget(self.txt_manzana)

        self.manzana = QLineEdit(self.dataWidgetL)
        self.manzana.setObjectName(u"manzana")

        self.verticalLayout_4.addWidget(self.manzana)

        self.txt_numext = QLabel(self.dataWidgetL)
        self.txt_numext.setObjectName(u"txt_numext")

        self.verticalLayout_4.addWidget(self.txt_numext)

        self.numExt = QLineEdit(self.dataWidgetL)
        self.numExt.setObjectName(u"numExt")

        self.verticalLayout_4.addWidget(self.numExt)


        self.horizontalLayout_4.addWidget(self.dataWidgetL)

        self.dataWidgetR = QWidget(self.dataWidget)
        self.dataWidgetR.setObjectName(u"dataWidgetR")
        self.verticalLayout_8 = QVBoxLayout(self.dataWidgetR)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.txt_numint = QLabel(self.dataWidgetR)
        self.txt_numint.setObjectName(u"txt_numint")

        self.verticalLayout_8.addWidget(self.txt_numint)

        self.numInt = QLineEdit(self.dataWidgetR)
        self.numInt.setObjectName(u"numInt")

        self.verticalLayout_8.addWidget(self.numInt)

        self.txt_cp = QLabel(self.dataWidgetR)
        self.txt_cp.setObjectName(u"txt_cp")

        self.verticalLayout_8.addWidget(self.txt_cp)

        self.codigoPostal = QLineEdit(self.dataWidgetR)
        self.codigoPostal.setObjectName(u"codigoPostal")

        self.verticalLayout_8.addWidget(self.codigoPostal)

        self.txt_colonia = QLabel(self.dataWidgetR)
        self.txt_colonia.setObjectName(u"txt_colonia")

        self.verticalLayout_8.addWidget(self.txt_colonia)

        self.colonia = QLineEdit(self.dataWidgetR)
        self.colonia.setObjectName(u"colonia")

        self.verticalLayout_8.addWidget(self.colonia)

        self.txt_municipio = QLabel(self.dataWidgetR)
        self.txt_municipio.setObjectName(u"txt_municipio")

        self.verticalLayout_8.addWidget(self.txt_municipio)

        self.municipio = QLineEdit(self.dataWidgetR)
        self.municipio.setObjectName(u"municipio")

        self.verticalLayout_8.addWidget(self.municipio)

        self.txt_entidad = QLabel(self.dataWidgetR)
        self.txt_entidad.setObjectName(u"txt_entidad")

        self.verticalLayout_8.addWidget(self.txt_entidad)

        self.entidad = QLineEdit(self.dataWidgetR)
        self.entidad.setObjectName(u"entidad")

        self.verticalLayout_8.addWidget(self.entidad)

        self.txt_seccion_electoral = QLabel(self.dataWidgetR)
        self.txt_seccion_electoral.setObjectName(u"txt_seccion_electoral")

        self.verticalLayout_8.addWidget(self.txt_seccion_electoral)

        self.seccionElectoral = QLineEdit(self.dataWidgetR)
        self.seccionElectoral.setObjectName(u"seccionElectoral")

        self.verticalLayout_8.addWidget(self.seccionElectoral)

        self.txt_genero = QLabel(self.dataWidgetR)
        self.txt_genero.setObjectName(u"txt_genero")

        self.verticalLayout_8.addWidget(self.txt_genero)

        self.genero = QComboBox(self.dataWidgetR)
        self.genero.setObjectName(u"genero")

        self.verticalLayout_8.addWidget(self.genero)

        self.txt_celular = QLabel(self.dataWidgetR)
        self.txt_celular.setObjectName(u"txt_celular")

        self.verticalLayout_8.addWidget(self.txt_celular)

        self.celular = QLineEdit(self.dataWidgetR)
        self.celular.setObjectName(u"celular")

        self.verticalLayout_8.addWidget(self.celular)

        self.txt_email = QLabel(self.dataWidgetR)
        self.txt_email.setObjectName(u"txt_email")

        self.verticalLayout_8.addWidget(self.txt_email)

        self.email = QLineEdit(self.dataWidgetR)
        self.email.setObjectName(u"email")

        self.verticalLayout_8.addWidget(self.email)


        self.horizontalLayout_4.addWidget(self.dataWidgetR)


        self.horizontalLayout_2.addWidget(self.dataWidget)

        self.stackedWidget.addWidget(self.captureView)
        self.credentialView = QWidget()
        self.credentialView.setObjectName(u"credentialView")
        sizePolicy.setHeightForWidth(self.credentialView.sizePolicy().hasHeightForWidth())
        self.credentialView.setSizePolicy(sizePolicy)
        self.horizontalLayout_5 = QHBoxLayout(self.credentialView)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.credentialPreview = QWidget(self.credentialView)
        self.credentialPreview.setObjectName(u"credentialPreview")
        sizePolicy.setHeightForWidth(self.credentialPreview.sizePolicy().hasHeightForWidth())
        self.credentialPreview.setSizePolicy(sizePolicy)
        self.credentialPreview.setMinimumSize(QSize(998, 680))
        self.horizontalLayout_6 = QHBoxLayout(self.credentialPreview)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.credentialBtns = QWidget(self.credentialPreview)
        self.credentialBtns.setObjectName(u"credentialBtns")
        self.credentialBtns.setMinimumSize(QSize(160, 662))
        self.credentialBtns.setMaximumSize(QSize(160, 662))
        self.verticalLayout_10 = QVBoxLayout(self.credentialBtns)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalSpacer_4 = QSpacerItem(20, 100, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_10.addItem(self.verticalSpacer_4)

        self.printBtn = QPushButton(self.credentialBtns)
        self.printBtn.setObjectName(u"printBtn")
        self.printBtn.setMinimumSize(QSize(140, 45))
        self.printBtn.setMaximumSize(QSize(140, 45))
        icon8 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentPrint))
        self.printBtn.setIcon(icon8)

        self.verticalLayout_10.addWidget(self.printBtn)

        self.verticalSpacer_3 = QSpacerItem(50, 550, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_10.addItem(self.verticalSpacer_3)


        self.horizontalLayout_6.addWidget(self.credentialBtns)

        self.credentialWidget = QWidget(self.credentialPreview)
        self.credentialWidget.setObjectName(u"credentialWidget")
        sizePolicy.setHeightForWidth(self.credentialWidget.sizePolicy().hasHeightForWidth())
        self.credentialWidget.setSizePolicy(sizePolicy)
        self.credentialWidget.setMinimumSize(QSize(780, 675))
        palette1 = QPalette()
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        self.credentialWidget.setPalette(palette1)
        self.verticalLayout_12 = QVBoxLayout(self.credentialWidget)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.frontWidgetCredential = QWidget(self.credentialWidget)
        self.frontWidgetCredential.setObjectName(u"frontWidgetCredential")
        self.frontWidgetCredential.setMinimumSize(QSize(500, 300))
        self.frontWidgetCredential.setMaximumSize(QSize(500, 300))
        self.frontWidgetCredential.setAutoFillBackground(False)
        self.frontWidgetCredential.setStyleSheet(u"QFrame#frameFrontal {\n"
"    border-radius: 25px;\n"
"}")
        self.labelCredentialCURP = QLabel(self.frontWidgetCredential)
        self.labelCredentialCURP.setObjectName(u"labelCredentialCURP")
        self.labelCredentialCURP.setGeometry(QRect(220, 200, 220, 31))
        self.labelCredentialCURP.setMinimumSize(QSize(220, 31))
        self.labelCredentialCURP.setMaximumSize(QSize(220, 16777215))
        palette2 = QPalette()
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        self.labelCredentialCURP.setPalette(palette2)
        font4 = QFont()
        font4.setFamilies([u"Arial Rounded MT"])
        font4.setPointSize(11)
        font4.setBold(True)
        self.labelCredentialCURP.setFont(font4)
        self.labelCredentialFolio = QLabel(self.frontWidgetCredential)
        self.labelCredentialFolio.setObjectName(u"labelCredentialFolio")
        self.labelCredentialFolio.setGeometry(QRect(220, 250, 220, 31))
        self.labelCredentialFolio.setMinimumSize(QSize(220, 31))
        self.labelCredentialFolio.setMaximumSize(QSize(260, 16777215))
        palette3 = QPalette()
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        self.labelCredentialFolio.setPalette(palette3)
        self.labelCredentialFolio.setFont(font4)
        self.labelUserPhotoCredencial = QLabel(self.frontWidgetCredential)
        self.labelUserPhotoCredencial.setObjectName(u"labelUserPhotoCredencial")
        self.labelUserPhotoCredencial.setGeometry(QRect(60, 100, 115, 150))
        self.labelUserPhotoCredencial.setMinimumSize(QSize(115, 150))
        self.labelCredentialName = QLabel(self.frontWidgetCredential)
        self.labelCredentialName.setObjectName(u"labelCredentialName")
        self.labelCredentialName.setGeometry(QRect(220, 27, 220, 70))
        self.labelCredentialName.setMinimumSize(QSize(220, 70))
        self.labelCredentialName.setMaximumSize(QSize(220, 70))
        palette4 = QPalette()
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        self.labelCredentialName.setPalette(palette4)
        font5 = QFont()
        font5.setFamilies([u"Arial Rounded MT"])
        font5.setPointSize(15)
        font5.setBold(True)
        self.labelCredentialName.setFont(font5)
        self.labelFrontBackgroundCredential = QLabel(self.frontWidgetCredential)
        self.labelFrontBackgroundCredential.setObjectName(u"labelFrontBackgroundCredential")
        self.labelFrontBackgroundCredential.setEnabled(True)
        self.labelFrontBackgroundCredential.setGeometry(QRect(0, 0, 501, 301))
        sizePolicy3.setHeightForWidth(self.labelFrontBackgroundCredential.sizePolicy().hasHeightForWidth())
        self.labelFrontBackgroundCredential.setSizePolicy(sizePolicy3)
        self.labelFrontBackgroundCredential.setMinimumSize(QSize(501, 301))
        self.labelFrontBackgroundCredential.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.labelCredentialAddress = QLabel(self.frontWidgetCredential)
        self.labelCredentialAddress.setObjectName(u"labelCredentialAddress")
        self.labelCredentialAddress.setGeometry(QRect(220, 120, 220, 51))
        self.labelCredentialAddress.setMinimumSize(QSize(220, 51))
        self.labelCredentialAddress.setMaximumSize(QSize(220, 16777215))
        palette5 = QPalette()
        palette5.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette5.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette5.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette5.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        self.labelCredentialAddress.setPalette(palette5)
        self.labelCredentialAddress.setFont(font4)
        self.labelFrontBackgroundCredential.raise_()
        self.labelCredentialCURP.raise_()
        self.labelCredentialFolio.raise_()
        self.labelUserPhotoCredencial.raise_()
        self.labelCredentialName.raise_()
        self.labelCredentialAddress.raise_()

        self.verticalLayout_12.addWidget(self.frontWidgetCredential, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.backWidgetCredential = QWidget(self.credentialWidget)
        self.backWidgetCredential.setObjectName(u"backWidgetCredential")
        self.backWidgetCredential.setMinimumSize(QSize(500, 300))
        self.backWidgetCredential.setMaximumSize(QSize(500, 300))
        self.labelReverseBackgroundCredential = QLabel(self.backWidgetCredential)
        self.labelReverseBackgroundCredential.setObjectName(u"labelReverseBackgroundCredential")
        self.labelReverseBackgroundCredential.setGeometry(QRect(0, -4, 501, 300))
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.labelReverseBackgroundCredential.sizePolicy().hasHeightForWidth())
        self.labelReverseBackgroundCredential.setSizePolicy(sizePolicy7)
        self.labelReverseBackgroundCredential.setMinimumSize(QSize(501, 300))
        self.labelReverseBackgroundCredential.setMaximumSize(QSize(500, 300))
        self.labelReverseBackgroundCredential.setStyleSheet(u"image: url(:/layout/back.png);")
        self.labelQrWhatsappCredential = QLabel(self.backWidgetCredential)
        self.labelQrWhatsappCredential.setObjectName(u"labelQrWhatsappCredential")
        self.labelQrWhatsappCredential.setGeometry(QRect(50, 100, 141, 141))
        self.labelQrWhatsappCredential.setMinimumSize(QSize(141, 141))
        self.labelQrWhatsappCredential.setMaximumSize(QSize(141, 141))
        self.labelQrWhatsappCredential.setStyleSheet(u"image: url(:/layout/qr/whatsapp.png);")
        self.labelCredentialFamCLogo = QLabel(self.backWidgetCredential)
        self.labelCredentialFamCLogo.setObjectName(u"labelCredentialFamCLogo")
        self.labelCredentialFamCLogo.setGeometry(QRect(250, 180, 191, 71))
        self.labelCredentialFamCLogo.setMaximumSize(QSize(191, 71))
        self.labelCredentialFamCLogo.setStyleSheet(u"image: url(:/layout/familia.png);")
        self.labelSignatureCredential = QLabel(self.backWidgetCredential)
        self.labelSignatureCredential.setObjectName(u"labelSignatureCredential")
        self.labelSignatureCredential.setGeometry(QRect(248, 65, 190, 70))
        self.labelSignatureCredential.setMinimumSize(QSize(190, 70))
        self.labelSignatureCredential.setMaximumSize(QSize(170, 60))
        palette6 = QPalette()
        palette6.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette6.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        self.labelSignatureCredential.setPalette(palette6)
        font6 = QFont()
        font6.setPointSize(15)
        font6.setBold(False)
        self.labelSignatureCredential.setFont(font6)
        self.labelSignatureCredential.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_12.addWidget(self.backWidgetCredential, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)


        self.horizontalLayout_6.addWidget(self.credentialWidget, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)


        self.horizontalLayout_5.addWidget(self.credentialPreview)

        self.stackedWidget.addWidget(self.credentialView)
        self.credentialGraphicView = QWidget()
        self.credentialGraphicView.setObjectName(u"credentialGraphicView")
        self.horizontalLayout_8 = QHBoxLayout(self.credentialGraphicView)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.stackedWidget.addWidget(self.credentialGraphicView)

        self.horizontalLayout_3.addWidget(self.stackedWidget)


        self.horizontalLayout.addWidget(self.mainWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.homeBtn.setText(QCoreApplication.translate("MainWindow", u" Inicio", None))
        self.captureBtn.setText(QCoreApplication.translate("MainWindow", u" Capturar", None))
        self.importBtn.setText(QCoreApplication.translate("MainWindow", u" Importar", None))
        self.exportBtn.setText(QCoreApplication.translate("MainWindow", u"Exportar", None))
        self.labelSistemaCuajimalpa.setText(QCoreApplication.translate("MainWindow", u"Sistema Familia Cuajimalpa", None))
        self.labelPhoto.setText(QCoreApplication.translate("MainWindow", u"Foto", None))
        self.startPhotoBtn.setText(QCoreApplication.translate("MainWindow", u" Iniciar Camara", None))
        self.uploadPhotoBtn.setText(QCoreApplication.translate("MainWindow", u" Subir Foto", None))
        self.labelSignature.setText(QCoreApplication.translate("MainWindow", u"Firma", None))
        self.startSignatureBtn.setText(QCoreApplication.translate("MainWindow", u" Iniciar Firma", None))
        self.saveDataBtn.setText(QCoreApplication.translate("MainWindow", u" Guardar", None))
        self.txt_nombre.setText(QCoreApplication.translate("MainWindow", u"Nombre", None))
        self.txt_paterno.setText(QCoreApplication.translate("MainWindow", u"Paterno", None))
        self.txt_materno.setText(QCoreApplication.translate("MainWindow", u"Materno", None))
        self.txt_curp.setText(QCoreApplication.translate("MainWindow", u"CURP", None))
        self.txt_domicilio.setText(QCoreApplication.translate("MainWindow", u"Fecha De Nacimiento", None))
        self.fechaNacimiento.setDisplayFormat(QCoreApplication.translate("MainWindow", u"yyyy/MM/dd", None))
        self.txt_calle.setText(QCoreApplication.translate("MainWindow", u"Calle", None))
        self.txt_lote.setText(QCoreApplication.translate("MainWindow", u"Lote", None))
        self.txt_manzana.setText(QCoreApplication.translate("MainWindow", u"Manzana", None))
        self.txt_numext.setText(QCoreApplication.translate("MainWindow", u"NumExt", None))
        self.txt_numint.setText(QCoreApplication.translate("MainWindow", u"NumInt", None))
        self.txt_cp.setText(QCoreApplication.translate("MainWindow", u"C\u00f3digo Postal", None))
        self.txt_colonia.setText(QCoreApplication.translate("MainWindow", u"Colonia", None))
        self.txt_municipio.setText(QCoreApplication.translate("MainWindow", u"Municipio", None))
        self.txt_entidad.setText(QCoreApplication.translate("MainWindow", u"Entidad", None))
        self.txt_seccion_electoral.setText(QCoreApplication.translate("MainWindow", u"Secci\u00f3n Electoral", None))
        self.txt_genero.setText(QCoreApplication.translate("MainWindow", u"G\u00e9nero", None))
        self.txt_celular.setText(QCoreApplication.translate("MainWindow", u"Celular", None))
        self.txt_email.setText(QCoreApplication.translate("MainWindow", u"Email", None))
        self.printBtn.setText(QCoreApplication.translate("MainWindow", u"Imprimir", None))
        self.labelCredentialCURP.setText(QCoreApplication.translate("MainWindow", u"Curp", None))
        self.labelCredentialFolio.setText(QCoreApplication.translate("MainWindow", u"Folio", None))
        self.labelUserPhotoCredencial.setText(QCoreApplication.translate("MainWindow", u"Foto", None))
        self.labelCredentialName.setText(QCoreApplication.translate("MainWindow", u"Nombre", None))
        self.labelFrontBackgroundCredential.setText("")
        self.labelCredentialAddress.setText(QCoreApplication.translate("MainWindow", u"Domicilio", None))
        self.labelQrWhatsappCredential.setText(QCoreApplication.translate("MainWindow", u"QrWhats", None))
        self.labelCredentialFamCLogo.setText("")
        self.labelSignatureCredential.setText(QCoreApplication.translate("MainWindow", u"Firma", None))
    # retranslateUi


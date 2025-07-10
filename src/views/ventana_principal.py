# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'propuesta_principal.ui'
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
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QDateEdit, QDateTimeEdit, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QStatusBar, QTableView, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1175, 725)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.buttonsBar = QWidget(self.centralwidget)
        self.buttonsBar.setObjectName(u"buttonsBar")
        self.verticalLayout = QVBoxLayout(self.buttonsBar)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btnInicio = QPushButton(self.buttonsBar)
        self.btnInicio.setObjectName(u"btnInicio")

        self.verticalLayout.addWidget(self.btnInicio)

        self.btnVer = QPushButton(self.buttonsBar)
        self.btnVer.setObjectName(u"btnVer")

        self.verticalLayout.addWidget(self.btnVer)

        self.btnCapturar = QPushButton(self.buttonsBar)
        self.btnCapturar.setObjectName(u"btnCapturar")

        self.verticalLayout.addWidget(self.btnCapturar)

        self.btnEditar = QPushButton(self.buttonsBar)
        self.btnEditar.setObjectName(u"btnEditar")

        self.verticalLayout.addWidget(self.btnEditar)

        self.verticalSpacer = QSpacerItem(160, 350, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.btnExportar = QPushButton(self.buttonsBar)
        self.btnExportar.setObjectName(u"btnExportar")

        self.verticalLayout.addWidget(self.btnExportar)


        self.horizontalLayout.addWidget(self.buttonsBar)

        self.index = QFrame(self.centralwidget)
        self.index.setObjectName(u"index")
        self.index.setFrameShape(QFrame.Shape.StyledPanel)
        self.index.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.index)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.stackedWidget = QStackedWidget(self.index)
        self.stackedWidget.setObjectName(u"stackedWidget")
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        self.stackedWidget.setPalette(palette)
        self.viewHome = QWidget()
        self.viewHome.setObjectName(u"viewHome")
        self.verticalLayout_5 = QVBoxLayout(self.viewHome)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.searchBar = QLineEdit(self.viewHome)
        self.searchBar.setObjectName(u"searchBar")

        self.verticalLayout_5.addWidget(self.searchBar)

        self.frameIndex = QFrame(self.viewHome)
        self.frameIndex.setObjectName(u"frameIndex")
        self.frameIndex.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameIndex.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frameIndex)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.usuariosVista = QTableView(self.frameIndex)
        self.usuariosVista.setObjectName(u"usuariosVista")

        self.verticalLayout_3.addWidget(self.usuariosVista)


        self.verticalLayout_5.addWidget(self.frameIndex)

        self.stackedWidget.addWidget(self.viewHome)
        self.viewCaptura = QWidget()
        self.viewCaptura.setObjectName(u"viewCaptura")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.viewCaptura.sizePolicy().hasHeightForWidth())
        self.viewCaptura.setSizePolicy(sizePolicy)
        self.viewCaptura.setMinimumSize(QSize(923, 666))
        self.horizontalLayout_2 = QHBoxLayout(self.viewCaptura)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.widgetFoto = QWidget(self.viewCaptura)
        self.widgetFoto.setObjectName(u"widgetFoto")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widgetFoto.sizePolicy().hasHeightForWidth())
        self.widgetFoto.setSizePolicy(sizePolicy1)
        self.widgetFoto.setMinimumSize(QSize(275, 0))
        self.widgetFoto.setMaximumSize(QSize(275, 648))
        self.verticalLayout_7 = QVBoxLayout(self.widgetFoto)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.frameFotoF = QFrame(self.widgetFoto)
        self.frameFotoF.setObjectName(u"frameFotoF")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frameFotoF.sizePolicy().hasHeightForWidth())
        self.frameFotoF.setSizePolicy(sizePolicy2)
        self.frameFotoF.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameFotoF.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frameFotoF)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.labelFoto = QLabel(self.frameFotoF)
        self.labelFoto.setObjectName(u"labelFoto")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.labelFoto.sizePolicy().hasHeightForWidth())
        self.labelFoto.setSizePolicy(sizePolicy3)
        self.labelFoto.setMaximumSize(QSize(16777215, 291))
        self.labelFoto.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.labelFoto)

        self.labelFirma = QLabel(self.frameFotoF)
        self.labelFirma.setObjectName(u"labelFirma")
        sizePolicy3.setHeightForWidth(self.labelFirma.sizePolicy().hasHeightForWidth())
        self.labelFirma.setSizePolicy(sizePolicy3)
        self.labelFirma.setMaximumSize(QSize(16777215, 97))
        font = QFont()
        font.setBold(False)
        self.labelFirma.setFont(font)
        self.labelFirma.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.labelFirma.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.labelFirma)


        self.verticalLayout_7.addWidget(self.frameFotoF)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_7.addItem(self.verticalSpacer_2)

        self.frameBtn = QFrame(self.widgetFoto)
        self.frameBtn.setObjectName(u"frameBtn")
        self.frameBtn.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameBtn.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.frameBtn)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.btnIniciarFoto = QPushButton(self.frameBtn)
        self.btnIniciarFoto.setObjectName(u"btnIniciarFoto")

        self.verticalLayout_11.addWidget(self.btnIniciarFoto)

        self.btnIniciarFirma = QPushButton(self.frameBtn)
        self.btnIniciarFirma.setObjectName(u"btnIniciarFirma")

        self.verticalLayout_11.addWidget(self.btnIniciarFirma)

        self.btnCapturarFoto = QPushButton(self.frameBtn)
        self.btnCapturarFoto.setObjectName(u"btnCapturarFoto")

        self.verticalLayout_11.addWidget(self.btnCapturarFoto)

        self.btnCapturarFirma = QPushButton(self.frameBtn)
        self.btnCapturarFirma.setObjectName(u"btnCapturarFirma")

        self.verticalLayout_11.addWidget(self.btnCapturarFirma)

        self.btnGuardarDatos = QPushButton(self.frameBtn)
        self.btnGuardarDatos.setObjectName(u"btnGuardarDatos")

        self.verticalLayout_11.addWidget(self.btnGuardarDatos)


        self.verticalLayout_7.addWidget(self.frameBtn)


        self.horizontalLayout_2.addWidget(self.widgetFoto)

        self.widgetDatos = QWidget(self.viewCaptura)
        self.widgetDatos.setObjectName(u"widgetDatos")
        self.horizontalLayout_4 = QHBoxLayout(self.widgetDatos)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.frameDatosL = QFrame(self.widgetDatos)
        self.frameDatosL.setObjectName(u"frameDatosL")
        self.frameDatosL.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameDatosL.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frameDatosL)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.txt_nombre = QLabel(self.frameDatosL)
        self.txt_nombre.setObjectName(u"txt_nombre")

        self.verticalLayout_4.addWidget(self.txt_nombre)

        self.nombre = QLineEdit(self.frameDatosL)
        self.nombre.setObjectName(u"nombre")

        self.verticalLayout_4.addWidget(self.nombre)

        self.txt_paterno = QLabel(self.frameDatosL)
        self.txt_paterno.setObjectName(u"txt_paterno")

        self.verticalLayout_4.addWidget(self.txt_paterno)

        self.paterno = QLineEdit(self.frameDatosL)
        self.paterno.setObjectName(u"paterno")

        self.verticalLayout_4.addWidget(self.paterno)

        self.txt_materno = QLabel(self.frameDatosL)
        self.txt_materno.setObjectName(u"txt_materno")

        self.verticalLayout_4.addWidget(self.txt_materno)

        self.materno = QLineEdit(self.frameDatosL)
        self.materno.setObjectName(u"materno")

        self.verticalLayout_4.addWidget(self.materno)

        self.txt_curp = QLabel(self.frameDatosL)
        self.txt_curp.setObjectName(u"txt_curp")

        self.verticalLayout_4.addWidget(self.txt_curp)

        self.curp = QLineEdit(self.frameDatosL)
        self.curp.setObjectName(u"curp")

        self.verticalLayout_4.addWidget(self.curp)

        self.txt_domicilio = QLabel(self.frameDatosL)
        self.txt_domicilio.setObjectName(u"txt_domicilio")

        self.verticalLayout_4.addWidget(self.txt_domicilio)

        self.fechaNacimiento = QDateEdit(self.frameDatosL)
        self.fechaNacimiento.setObjectName(u"fechaNacimiento")
        self.fechaNacimiento.setCurrentSection(QDateTimeEdit.Section.YearSection)

        self.verticalLayout_4.addWidget(self.fechaNacimiento)

        self.txt_calle = QLabel(self.frameDatosL)
        self.txt_calle.setObjectName(u"txt_calle")

        self.verticalLayout_4.addWidget(self.txt_calle)

        self.calle = QLineEdit(self.frameDatosL)
        self.calle.setObjectName(u"calle")

        self.verticalLayout_4.addWidget(self.calle)

        self.txt_lote = QLabel(self.frameDatosL)
        self.txt_lote.setObjectName(u"txt_lote")

        self.verticalLayout_4.addWidget(self.txt_lote)

        self.lote = QLineEdit(self.frameDatosL)
        self.lote.setObjectName(u"lote")

        self.verticalLayout_4.addWidget(self.lote)

        self.txt_manzana = QLabel(self.frameDatosL)
        self.txt_manzana.setObjectName(u"txt_manzana")

        self.verticalLayout_4.addWidget(self.txt_manzana)

        self.manzana = QLineEdit(self.frameDatosL)
        self.manzana.setObjectName(u"manzana")

        self.verticalLayout_4.addWidget(self.manzana)

        self.txt_numext = QLabel(self.frameDatosL)
        self.txt_numext.setObjectName(u"txt_numext")

        self.verticalLayout_4.addWidget(self.txt_numext)

        self.numExt = QLineEdit(self.frameDatosL)
        self.numExt.setObjectName(u"numExt")

        self.verticalLayout_4.addWidget(self.numExt)


        self.horizontalLayout_4.addWidget(self.frameDatosL)

        self.frameDatosR = QFrame(self.widgetDatos)
        self.frameDatosR.setObjectName(u"frameDatosR")
        self.frameDatosR.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameDatosR.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frameDatosR)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.txt_numint = QLabel(self.frameDatosR)
        self.txt_numint.setObjectName(u"txt_numint")

        self.verticalLayout_8.addWidget(self.txt_numint)

        self.numInt = QLineEdit(self.frameDatosR)
        self.numInt.setObjectName(u"numInt")

        self.verticalLayout_8.addWidget(self.numInt)

        self.txt_cp = QLabel(self.frameDatosR)
        self.txt_cp.setObjectName(u"txt_cp")

        self.verticalLayout_8.addWidget(self.txt_cp)

        self.codigoPostal = QLineEdit(self.frameDatosR)
        self.codigoPostal.setObjectName(u"codigoPostal")

        self.verticalLayout_8.addWidget(self.codigoPostal)

        self.txt_colonia = QLabel(self.frameDatosR)
        self.txt_colonia.setObjectName(u"txt_colonia")

        self.verticalLayout_8.addWidget(self.txt_colonia)

        self.colonia = QLineEdit(self.frameDatosR)
        self.colonia.setObjectName(u"colonia")

        self.verticalLayout_8.addWidget(self.colonia)

        self.txt_municipio = QLabel(self.frameDatosR)
        self.txt_municipio.setObjectName(u"txt_municipio")

        self.verticalLayout_8.addWidget(self.txt_municipio)

        self.municipio = QLineEdit(self.frameDatosR)
        self.municipio.setObjectName(u"municipio")

        self.verticalLayout_8.addWidget(self.municipio)

        self.txt_entidad = QLabel(self.frameDatosR)
        self.txt_entidad.setObjectName(u"txt_entidad")

        self.verticalLayout_8.addWidget(self.txt_entidad)

        self.entidad = QLineEdit(self.frameDatosR)
        self.entidad.setObjectName(u"entidad")

        self.verticalLayout_8.addWidget(self.entidad)

        self.txt_seccion_electoral = QLabel(self.frameDatosR)
        self.txt_seccion_electoral.setObjectName(u"txt_seccion_electoral")

        self.verticalLayout_8.addWidget(self.txt_seccion_electoral)

        self.seccionElectoral = QLineEdit(self.frameDatosR)
        self.seccionElectoral.setObjectName(u"seccionElectoral")

        self.verticalLayout_8.addWidget(self.seccionElectoral)

        self.txt_genero = QLabel(self.frameDatosR)
        self.txt_genero.setObjectName(u"txt_genero")

        self.verticalLayout_8.addWidget(self.txt_genero)

        self.genero = QLineEdit(self.frameDatosR)
        self.genero.setObjectName(u"genero")

        self.verticalLayout_8.addWidget(self.genero)

        self.txt_celular = QLabel(self.frameDatosR)
        self.txt_celular.setObjectName(u"txt_celular")

        self.verticalLayout_8.addWidget(self.txt_celular)

        self.celular = QLineEdit(self.frameDatosR)
        self.celular.setObjectName(u"celular")

        self.verticalLayout_8.addWidget(self.celular)

        self.txt_email = QLabel(self.frameDatosR)
        self.txt_email.setObjectName(u"txt_email")

        self.verticalLayout_8.addWidget(self.txt_email)

        self.email = QLineEdit(self.frameDatosR)
        self.email.setObjectName(u"email")

        self.verticalLayout_8.addWidget(self.email)


        self.horizontalLayout_4.addWidget(self.frameDatosR)


        self.horizontalLayout_2.addWidget(self.widgetDatos)

        self.stackedWidget.addWidget(self.viewCaptura)
        self.viewCredencial = QWidget()
        self.viewCredencial.setObjectName(u"viewCredencial")
        self.horizontalLayout_5 = QHBoxLayout(self.viewCredencial)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.btnCredencial = QFrame(self.viewCredencial)
        self.btnCredencial.setObjectName(u"btnCredencial")
        self.btnCredencial.setFrameShape(QFrame.Shape.StyledPanel)
        self.btnCredencial.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.btnCredencial)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.btnImprimir = QPushButton(self.btnCredencial)
        self.btnImprimir.setObjectName(u"btnImprimir")

        self.verticalLayout_10.addWidget(self.btnImprimir)

        self.pushButton_2 = QPushButton(self.btnCredencial)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout_10.addWidget(self.pushButton_2)

        self.verticalSpacer_3 = QSpacerItem(50, 350, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_10.addItem(self.verticalSpacer_3)


        self.horizontalLayout_5.addWidget(self.btnCredencial, 0, Qt.AlignmentFlag.AlignLeft)

        self.leftHorizontalCredencial = QSpacerItem(127, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.leftHorizontalCredencial)

        self.previewCredencial = QFrame(self.viewCredencial)
        self.previewCredencial.setObjectName(u"previewCredencial")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.previewCredencial.sizePolicy().hasHeightForWidth())
        self.previewCredencial.setSizePolicy(sizePolicy4)
        self.previewCredencial.setFrameShape(QFrame.Shape.StyledPanel)
        self.previewCredencial.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.previewCredencial)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.frameCredencial = QFrame(self.previewCredencial)
        self.frameCredencial.setObjectName(u"frameCredencial")
        palette1 = QPalette()
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        self.frameCredencial.setPalette(palette1)
        self.frameCredencial.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameCredencial.setFrameShadow(QFrame.Shadow.Raised)
        self.frameFrontal = QFrame(self.frameCredencial)
        self.frameFrontal.setObjectName(u"frameFrontal")
        self.frameFrontal.setGeometry(QRect(30, 10, 500, 300))
        self.frameFrontal.setAutoFillBackground(False)
        self.frameFrontal.setStyleSheet(u"QFrame#frameFrontal {\n"
"    border-radius: 25px;\n"
"}")
        self.frameFrontal.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameFrontal.setFrameShadow(QFrame.Shadow.Raised)
        self.labelCURPCredencial = QLabel(self.frameFrontal)
        self.labelCURPCredencial.setObjectName(u"labelCURPCredencial")
        self.labelCURPCredencial.setGeometry(QRect(220, 200, 220, 31))
        palette2 = QPalette()
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        self.labelCURPCredencial.setPalette(palette2)
        font1 = QFont()
        font1.setFamilies([u"Arial Rounded MT"])
        font1.setPointSize(11)
        font1.setBold(True)
        self.labelCURPCredencial.setFont(font1)
        self.labelFolioCredencial = QLabel(self.frameFrontal)
        self.labelFolioCredencial.setObjectName(u"labelFolioCredencial")
        self.labelFolioCredencial.setGeometry(QRect(220, 250, 220, 31))
        palette3 = QPalette()
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        self.labelFolioCredencial.setPalette(palette3)
        self.labelFolioCredencial.setFont(font1)
        self.labelFotoCredencial = QLabel(self.frameFrontal)
        self.labelFotoCredencial.setObjectName(u"labelFotoCredencial")
        self.labelFotoCredencial.setGeometry(QRect(40, 100, 141, 151))
        self.labelNombreCredencial = QLabel(self.frameFrontal)
        self.labelNombreCredencial.setObjectName(u"labelNombreCredencial")
        self.labelNombreCredencial.setGeometry(QRect(220, 30, 220, 60))
        palette4 = QPalette()
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        self.labelNombreCredencial.setPalette(palette4)
        font2 = QFont()
        font2.setFamilies([u"Arial Rounded MT"])
        font2.setPointSize(15)
        font2.setBold(True)
        self.labelNombreCredencial.setFont(font2)
        self.labelFondo = QLabel(self.frameFrontal)
        self.labelFondo.setObjectName(u"labelFondo")
        self.labelFondo.setGeometry(QRect(0, 0, 501, 301))
        self.labelFondo.setStyleSheet(u"image: url(:/layout/front.png);\n"
"")
        self.labelFondo.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.labelDomicilioCredencial = QLabel(self.frameFrontal)
        self.labelDomicilioCredencial.setObjectName(u"labelDomicilioCredencial")
        self.labelDomicilioCredencial.setGeometry(QRect(220, 120, 220, 51))
        palette5 = QPalette()
        palette5.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette5.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette5.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette5.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        self.labelDomicilioCredencial.setPalette(palette5)
        self.labelDomicilioCredencial.setFont(font1)
        self.labelFondo.raise_()
        self.labelCURPCredencial.raise_()
        self.labelFolioCredencial.raise_()
        self.labelFotoCredencial.raise_()
        self.labelNombreCredencial.raise_()
        self.labelDomicilioCredencial.raise_()
        self.framePosterior = QFrame(self.frameCredencial)
        self.framePosterior.setObjectName(u"framePosterior")
        self.framePosterior.setGeometry(QRect(30, 360, 500, 300))
        self.framePosterior.setFrameShape(QFrame.Shape.StyledPanel)
        self.framePosterior.setFrameShadow(QFrame.Shadow.Raised)
        self.labelFondoPosterior = QLabel(self.framePosterior)
        self.labelFondoPosterior.setObjectName(u"labelFondoPosterior")
        self.labelFondoPosterior.setGeometry(QRect(0, 0, 501, 301))
        self.labelFondoPosterior.setStyleSheet(u"image: url(:/layout/back.png);")
        self.labelQrWhatsapp = QLabel(self.framePosterior)
        self.labelQrWhatsapp.setObjectName(u"labelQrWhatsapp")
        self.labelQrWhatsapp.setGeometry(QRect(50, 100, 141, 141))
        self.labelQrWhatsapp.setStyleSheet(u"image: url(:/layout/qr/whatsapp.png);")
        self.labelFamC_2 = QLabel(self.framePosterior)
        self.labelFamC_2.setObjectName(u"labelFamC_2")
        self.labelFamC_2.setGeometry(QRect(250, 180, 191, 71))
        self.labelFamC_2.setStyleSheet(u"image: url(:/layout/familia.png);")
        self.labelFirmaCredencial = QLabel(self.framePosterior)
        self.labelFirmaCredencial.setObjectName(u"labelFirmaCredencial")
        self.labelFirmaCredencial.setGeometry(QRect(260, 90, 161, 31))
        palette6 = QPalette()
        palette6.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette6.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        self.labelFirmaCredencial.setPalette(palette6)
        font3 = QFont()
        font3.setPointSize(15)
        font3.setBold(False)
        self.labelFirmaCredencial.setFont(font3)
        self.labelFirmaCredencial.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_9.addWidget(self.frameCredencial)


        self.horizontalLayout_5.addWidget(self.previewCredencial)

        self.rightHorizontalCredencial = QSpacerItem(145, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.rightHorizontalCredencial)

        self.stackedWidget.addWidget(self.viewCredencial)
        self.pagePDF = QWidget()
        self.pagePDF.setObjectName(u"pagePDF")
        self.verticalLayout_12 = QVBoxLayout(self.pagePDF)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.previewPDF = QFrame(self.pagePDF)
        self.previewPDF.setObjectName(u"previewPDF")
        self.previewPDF.setFrameShape(QFrame.Shape.StyledPanel)
        self.previewPDF.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.previewPDF)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.webPreview = QWebEngineView(self.previewPDF)
        self.webPreview.setObjectName(u"webPreview")
        self.webPreview.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_14.addWidget(self.webPreview)


        self.verticalLayout_12.addWidget(self.previewPDF)

        self.stackedWidget.addWidget(self.pagePDF)

        self.verticalLayout_2.addWidget(self.stackedWidget)


        self.horizontalLayout.addWidget(self.index)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btnInicio.setText(QCoreApplication.translate("MainWindow", u"Inicio", None))
        self.btnVer.setText(QCoreApplication.translate("MainWindow", u"Ver", None))
        self.btnCapturar.setText(QCoreApplication.translate("MainWindow", u"Capturar", None))
        self.btnEditar.setText(QCoreApplication.translate("MainWindow", u"Editar", None))
        self.btnExportar.setText(QCoreApplication.translate("MainWindow", u"Exportar", None))
        self.labelFoto.setText(QCoreApplication.translate("MainWindow", u"Foto", None))
        self.labelFirma.setText(QCoreApplication.translate("MainWindow", u"Firma", None))
        self.btnIniciarFoto.setText(QCoreApplication.translate("MainWindow", u"Iniciar Camara", None))
        self.btnIniciarFirma.setText(QCoreApplication.translate("MainWindow", u"Iniciar Firma", None))
        self.btnCapturarFoto.setText(QCoreApplication.translate("MainWindow", u"Capturar Foto", None))
        self.btnCapturarFirma.setText(QCoreApplication.translate("MainWindow", u"Capturar Firma", None))
        self.btnGuardarDatos.setText(QCoreApplication.translate("MainWindow", u"Guardar", None))
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
        self.btnImprimir.setText(QCoreApplication.translate("MainWindow", u"Imprimir", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.labelCURPCredencial.setText(QCoreApplication.translate("MainWindow", u"Curp", None))
        self.labelFolioCredencial.setText(QCoreApplication.translate("MainWindow", u"Folio", None))
        self.labelFotoCredencial.setText(QCoreApplication.translate("MainWindow", u"Foto", None))
        self.labelNombreCredencial.setText(QCoreApplication.translate("MainWindow", u"Nombre", None))
        self.labelFondo.setText("")
        self.labelDomicilioCredencial.setText(QCoreApplication.translate("MainWindow", u"Domicilio", None))
        self.labelFondoPosterior.setText("")
        self.labelQrWhatsapp.setText(QCoreApplication.translate("MainWindow", u"QrWhats", None))
        self.labelFamC_2.setText("")
        self.labelFirmaCredencial.setText(QCoreApplication.translate("MainWindow", u"Firma", None))
    # retranslateUi


import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import re



class MyMainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MyMainWindow, self).__init__(*args, **kwargs)
        #self.setMouseTracking(True)
        self.draw_flag = False
        self.zoom_coefs = [0.27, 0.30, 0.33, 0.36, 0.40, 0.44, 0.49, 0.53,
                           0.59, 0.65, 0.71, 0.78, 0.86, 1.0, 1.1, 1.21,
                           1.33, 1.46, 1.61, 1.94, 2.14, 2.35, 2.59, 2.85,
                           3.13, 3.45, 3.79, 4.17, 4.59, 5.05, 5.55, 6.11,
                           6.72, 7.40, 8.14, 8.95, 9.84, 10.83, 11.91, 13.10,
                           14.42, 15.86, 17.44, 19.19, 20.00]

                          # 21.11, 23.22,
                          # 25.54, 28.10, 30.91, 34.00, 37.40, 41.14,
                          # 45.25, 49.78, 50.00]

        self.zoom_index = 0

        self.x_pos = 100
        self.y_pos = 100
        self.window_width = 800
        self.window_height = 600
        self.setMinimumSize(200, 200)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.full_screen = False

        self.path = os.path.join(os.getcwd(), 'test.jpeg')



        # set geometry
        self.setGeometry(self.x_pos, self.y_pos, self.window_width, self.window_height)
        self.UiComponents()
        self.customTitleBar.mouseMoveEvent = self.MoveWindow
        self.customTitleBar.mousePressEvent = self.PressWindow

        self.image_label.mouseMoveEvent = self.onImageMouseMoveEvent
        self.image_label.mousePressEvent = self.onImageMousePressEvent
        self.image_label.mouseReleaseEvent = self.onImageMouseReleaseEvent
        self.image_label.paintEvent = self.onImagePaintEvent

        # save original image
        self.image = QImage(self.path)
        self.display_image()


    def UiComponents(self):

        # create a main widget in order to make overlap of two images
        self.widget = QWidget()
        self.setCentralWidget(self.widget)


       # Label for Custom Title Bar
        self.customTitleBar = QLabel(self)
        self.customTitleBar.setGeometry(0, 0, self.window_width, 30)
        self.customTitleBar.setStyleSheet("background-color: #c3c3c3")
        self.customTitleBar.setMaximumHeight(30)



        # creating buttons for custom menu
        self.minimizeButton = QPushButton(self)
        self.fullButton = QPushButton(self)
        self.closeButton = QPushButton(self)
        # button for opening images
        self.open_image = QPushButton(self.customTitleBar)
        self.open_image.resize(35, 30)
        self.open_image.move(10, 0)
        # button for save a highlighted defect
        self.save_imageButton = QPushButton(self)
        self.save_imageButton.resize(35, 30)
        self.save_imageButton.move(45, 0)
        self.save_imageButton.hide()

        # Create layout for navigation buttons
        self.navigation_layout = QHBoxLayout(self.customTitleBar)

        self.navigation_layout.setContentsMargins(0, 0, 10, 0)
        self.navigation_layout.setSpacing(2)
        self.navigation_layout.setAlignment(Qt.AlignRight)


        self.navigation_layout.addWidget(self.minimizeButton)
        self.navigation_layout.addWidget(self.fullButton)
        self.navigation_layout.addWidget(self.closeButton)



        # setting radius and border
        self.minimizeButton.setStyleSheet("QPushButton::hover{background-color: #f8f9ff;}"
                                          "QPushButton {border-radius : 15;}")
        self.fullButton.setStyleSheet("QPushButton::hover{background-color: #f8f9ff;}"
                                          "QPushButton {border-radius : 15;}")
        self.closeButton.setStyleSheet("QPushButton::hover{background-color: #f8f9ff;}"
                                          "QPushButton {border-radius : 15;}")

        self.open_image.setStyleSheet("QPushButton::hover{background-color: #f8f9ff;}"
                                       "QPushButton {border-radius : 15;}")

        self.save_imageButton.setStyleSheet("QPushButton::hover{background-color: #f8f9ff;}"
                                      "QPushButton {border-radius : 15;}")

        # add an icon to a button
        self.minimizeButton.setIcon(QIcon("macOs_icons\minimize_30.png"))
        self.fullButton.setIcon(QIcon(r"macOs_icons\full_30.png"))
        self.closeButton.setIcon(QIcon("macOs_icons\close_30.png"))
        self.open_image.setIcon(QIcon(r"macOs_icons\folder_30.png"))
        self.save_imageButton.setIcon(QIcon(r"macOs_icons\save_30.png"))

        # change icon size
        self.minimizeButton.setIconSize(QSize(30, 30))
        self.fullButton.setIconSize(QSize(30, 30))
        self.closeButton.setIconSize(QSize(30, 30))
        self.open_image.setIconSize(QSize(25, 25))
        self.save_imageButton.setIconSize(QSize(27, 27))


        # signal - slot
        self.minimizeButton.clicked.connect(self.minimizeButton_clicked)
        self.fullButton.clicked.connect(self.fullButton_clicked)
        self.closeButton.clicked.connect(self.closeButton_clicked)
        self.open_image.clicked.connect(self.open_image_clicked)
        self.save_imageButton.clicked.connect(self.save_image)

        # set image label as a child of the central widget
        self.image_label = QLabel(self.widget)

        # grip to resize an image
        self.bottomRightGrip = QSizeGrip(self)
        self.bottomRightGrip.resize(16, 16)
        self.bottomRightGrip.move(self.rect().right() - 16, self.rect().bottom() - 16)


    def minimizeButton_clicked(self):
        self.showMinimized()

    def closeButton_clicked(self):
        self.close()

    def fullButton_clicked(self):

        if not self.full_screen:
            self.showFullScreen()
            self.customTitleBar.resize(self.width(), 30)
            self.full_screen = True

        elif self.full_screen:
            self.showNormal()
            self.customTitleBar.showNormal()
            self.customTitleBar.resize(self.width(), 30)
            self.full_screen = False

    def open_image_clicked(self):
        filename = QFileDialog.getOpenFileName(None, "Open Image", r"D:\projects\thesis_proposal\thesis_parts\extract_defects", "Image Files (*.png *.jpg *.bmp *.jpeg)")
        self.path = filename[0]

        # save original image
        self.image = QImage(self.path)
        self.display_image()

    def MoveWindow(self, event):
        if not self.isMaximized():
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()

    def PressWindow(self, event):
        self.clickPosition = event.globalPos()


    def resizeEvent(self, event):

        QMainWindow.resizeEvent(self, event)
        self.customTitleBar.setGeometry(0, 0, self.rect().right() + 1, 30)
        self.bottomRightGrip.move(self.rect().right() - 16, self.rect().bottom() - 16)
        self.image_label.move(int(self.rect().width() / 2 - self.scaled_pixmap.width() / 2),
                              int(self.rect().height() / 2 - self.scaled_pixmap.height() / 2) + 15)



    def display_image(self):

        self.resizeImage_toMainWindow()


    def resizeImage_toMainWindow(self):

        self.image_pixmap = QPixmap(self.image)
        size = self.image_pixmap.size()

        if size.height() > self.rect().height() - 30:
            coefficient = size.height() / (self.rect().height() - 30)
            coefficient = 1 / coefficient

            coeffs_list = self.zoom_coefs.copy()
            for index, value in enumerate(coeffs_list):
                if value > coefficient:
                    self.zoom_coefs.insert(index, coefficient)
                    self.zoom_index = index
                    break
        else:
            coefficient = 1
            self.zoom_index = self.zoom_coefs.index(coefficient)

        self.scaled_pixmap = self.image_pixmap.scaled(coefficient * size, Qt.KeepAspectRatio)


        self.image_label.setPixmap(self.scaled_pixmap)
        self.image_label.setGeometry(int(self.rect().width() / 2 - self.scaled_pixmap.width() / 2),
                                     int(self.rect().height() / 2 - self.scaled_pixmap.height() / 2) + 15,
                                     self.scaled_pixmap.width(), self.scaled_pixmap.height())

    def onImageMouseMoveEvent(self, event):
        if event.buttons() == Qt.RightButton:
            self.image_label.move(self.image_label.pos() + (event.globalPos() - self.img_clk))
            self.img_clk = event.globalPos()
        elif event.buttons() == Qt.LeftButton:
            self.draw_flag = True
            self.draw_end = event.pos()
            self.defect_rect = QRectF(self.draw_begin, self.draw_end)
            self.image_label.update()


    def onImageMousePressEvent(self, event):
        if event.buttons() == Qt.RightButton:
            self.img_clk = event.globalPos()
        elif event.button() == Qt.LeftButton:
            self.draw_begin = event.pos()

            self.init_coords = event.pos()
            self.init_coords /= self.zoom_coefs[self.zoom_index]

            self.draw_end = event.pos()



        elif event.button() == Qt.MiddleButton:
            self.draw_flag = False
            self.save_imageButton.hide()
            self.image_label.update()


    def onImageMouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.save_imageButton.show()


    def drawRect(self):

        painter = QPainter(self.image_label)
        painter.setPen(QColor(204, 102, 255, 180))
        brush = QBrush(QColor(100, 10, 10, 40))
        painter.setBrush(brush)

        painter.drawRect(self.defect_rect)


    def onImagePaintEvent(self, event):
        QMainWindow.paintEvent(self, event)
        QLabel.paintEvent(self.image_label, event)
        if self.draw_flag == True:
            self.drawRect()


    def zoom_image(self):

        self.image_pixmap = QPixmap(self.image)
        size = self.image_pixmap.size()
        self.scaled_pixmap = self.image_pixmap.scaled(self.zoom_coefs[self.zoom_index] * size, Qt.KeepAspectRatio)
        self.image_label.setPixmap(self.scaled_pixmap)
        self.image_label.resize(self.scaled_pixmap.width(), self.scaled_pixmap.height())

    def wheelEvent(self, event):
        # every scroll of a wheel generate 120 delta value (degrees * 8)
        numDegrees = event.angleDelta() / 8

        if numDegrees.y() > 0 and self.zoom_index < len(self.zoom_coefs) - 2:

            self.zoom_index += 1

            '''
            basic idea:
            firstly, we get the difference of the coordinates of zoomed image (for example 120% i.e coef = 1.2)
            then, we make it in 100% scale
            then, we make it to current coefficient (for example 140%)
            finally, we calculate a difference between dx_120% and dx_140%
            '''
            dx_initialCoef = event.pos().x() - self.image_label.x()
            dx_100 = dx_initialCoef / self.zoom_coefs[self.zoom_index - 1]
            dx_currentCoef = dx_100 * self.zoom_coefs[self.zoom_index]

            dy_initialCoef = event.pos().y() - self.image_label.y()
            dy_100 = dy_initialCoef / self.zoom_coefs[self.zoom_index - 1]
            dy_currentCoef = dy_100 * self.zoom_coefs[self.zoom_index]

            dx = dx_initialCoef - dx_currentCoef
            dy = dy_initialCoef - dy_currentCoef

            if self.draw_flag == True:


                self.defect_rect.moveTopLeft(self.init_coords * self.zoom_coefs[self.zoom_index])

                width_100 = self.defect_rect.width() / self.zoom_coefs[self.zoom_index - 1]
                self.defect_rect.setWidth(width_100 * self.zoom_coefs[self.zoom_index])

                height_100 = self.defect_rect.height() / self.zoom_coefs[self.zoom_index - 1]
                self.defect_rect.setHeight(height_100 * self.zoom_coefs[self.zoom_index])


        elif numDegrees.y() < 0 and self.zoom_index > 1:
            self.zoom_index -= 1

            dx_initialCoef = event.pos().x() - self.image_label.x()
            dx_100 = dx_initialCoef / self.zoom_coefs[self.zoom_index + 1]
            dx_currentCoef = dx_100 * self.zoom_coefs[self.zoom_index]

            dy_initialCoef = event.pos().y() - self.image_label.y()
            dy_100 = dy_initialCoef / self.zoom_coefs[self.zoom_index + 1]
            dy_currentCoef = dy_100 * self.zoom_coefs[self.zoom_index]

            dx = dx_initialCoef - dx_currentCoef
            dy = dy_initialCoef - dy_currentCoef

            if self.draw_flag == True:

                self.defect_rect.moveTopLeft(self.init_coords * self.zoom_coefs[self.zoom_index])

                width_100 = self.defect_rect.width() / self.zoom_coefs[self.zoom_index + 1]
                self.defect_rect.setWidth(width_100 * self.zoom_coefs[self.zoom_index])

                height_100 = self.defect_rect.height() / self.zoom_coefs[self.zoom_index + 1]
                self.defect_rect.setHeight(height_100 * self.zoom_coefs[self.zoom_index])

        else:
            dx = 0
            dy = 0

        self.image_label.move(int(round(self.image_label.x() + dx, 0)), int(round(self.image_label.y() + dy, 0)))
        self.zoom_image()
        # mark that event was handled
        event.accept()

    def change_scale_100(self, scale=1.0):

        self.defect_rect.moveTopLeft(self.init_coords * scale)

        width_100 = self.defect_rect.width() / self.zoom_coefs[self.zoom_index]
        self.defect_rect.setWidth(width_100 * scale)
        height_100 = self.defect_rect.height() / self.zoom_coefs[self.zoom_index]
        self.defect_rect.setHeight(height_100 * scale)

    def save_image(self):
        # TODO:
        # Ask supervisor about size requirements of the defect image
        self.save_imageButton.hide()
        self.draw_flag = False
        self.image_label.update()
        pixmap_100 = QPixmap(self.image)
        self.change_scale_100()
        # don't forget that copying implemented from image with 1.00 zoom coefficient
        defect = pixmap_100.copy(int(round(self.defect_rect.topLeft().x(), 0)),
                                 int(round(self.defect_rect.topLeft().y(), 0)),
                                 int(round(self.defect_rect.width(), 0)),
                                 int(round(self.defect_rect.height(), 0)))

        cwd = os.getcwd()

        try:
            os.mkdir(os.path.join(cwd, "images_defects"))
        except FileExistsError:
            cwd = os.path.join(cwd, "images_defects")
            defect_files = os.listdir(cwd)

            num = - 1
            if len(defect_files) > 0:
                for d in sorted(defect_files):
                    if re.search(r'^d\D+(\d+)\.png$', d):
                        num = int(re.search(r'^d\D+(\d+)\.png$', d).groups()[0])
                # if there are files with a different name that doesn't comply with the rules of a regex
                if num != -1:
                    num += 1
                else:
                    num = 0
            else:
                num = 0
            defect.save(os.path.join(cwd, 'def_' + str(num) + '.png'))

        else:
            cwd = os.path.join(cwd, "images_defects")
            num = 0
            defect.save(os.path.join(cwd, 'def_' + str(num) + '.png'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()

    app.exec_()

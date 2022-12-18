#!/usr/bin/env python

''' A basic GUi to use ImageViewer class to show its functionalities and use cases. '''

from PyQt5 import QtCore, QtWidgets, uic, QtWidgets
from actions import ImageViewer
import sys, os

gui = uic.loadUiType("main1.ui")[0]     # load UI file designed in Qt Designer
VALID_FORMAT = ('.BMP', '.GIF', '.JPG', '.JPEG', '.PNG', '.PBM', '.PGM', '.PPM', '.TIFF', '.XBM')  # Image formats supported by Qt

def getImages(folder):
    ''' Get the names and paths of all the images in a directory. '''
    image_list = []
    if os.path.isdir(folder):
        for file in os.listdir(folder):
            if file.upper().endswith(VALID_FORMAT):
                im_path = os.path.join(folder, file)
                image_obj = {'name': file, 'path': im_path }
                image_list.append(image_obj)
    return image_list

class Iwindow(QtWidgets.QMainWindow, gui):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.cntr, self.numImages = -1, -1  # self.cntr have the info of which image is selected/displayed

        self.image_viewer = ImageViewer(self.qlabel_image)
        self.__connectEvents()
        self.showMaximized()

    def __connectEvents(self):
        self.open_folder.clicked.connect(self.selectDir)
        self.next_im.clicked.connect(self.nextImg)
        self.prev_im.clicked.connect(self.prevImg)
        self.qlist_images.itemClicked.connect(self.item_click)
        # self.save_im.clicked.connect(self.saveImg)

        self.zoom_plus.clicked.connect(self.image_viewer.zoomPlus)
        self.zoom_minus.clicked.connect(self.image_viewer.zoomMinus)
        self.reset_zoom.clicked.connect(self.image_viewer.resetZoom)

        self.toggle_line.toggled.connect(self.action_line)
        self.toggle_rect.toggled.connect(self.action_rect)
        self.toggle_move.toggled.connect(self.action_move)


        ### Show results
        self.Bnt_Result.clicked.connect(self.show_results) # Unet
        self.Bnt_Result_UnetPlus.clicked.connect(self.Unet_show_results)  # Unet_show_results
        self.Bnt_Result_Resnet.clicked.connect(self.Resnet_show_results)  # Res_show_results


    def selectDir(self):
        ''' Select a directory, make list of images in it and display the first image in the list. '''
        # open 'select folder' dialog box
        print("Select Directory function")
        self.folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if not self.folder:
            QtWidgets.QMessageBox.warning(self, 'No Folder Selected', 'Please select a validate Folder')
            return
        
        self.logs = getImages(self.folder)
        self.numImages = len(self.logs)

        # make qitems of the image names
        self.items = [QtWidgets.QListWidgetItem(log['name']) for log in self.logs]
        for item in self.items:
            self.qlist_images.addItem(item)

        # display first image and enable Pan 
        self.cntr = 0
        self.image_viewer.enablePan(True)
        self.image_viewer.loadImage(self.logs[self.cntr]['path'])
        self.items[self.cntr].setSelected(True)
        #self.qlist_images.setItemSelected(self.items[self.cntr], True)

        # enable the next image button on the gui if multiple images are loaded
        if self.numImages > 1:
            self.next_im.setEnabled(True)

    def resizeEvent(self, evt):
        if self.cntr >= 0:
            self.image_viewer.onResize()

    def nextImg(self):
        print("Click next Image")
        if self.cntr < self.numImages -1:
            self.cntr += 1
            self.items[self.cntr].setSelected(True)
            self.image_viewer.loadImage(self.logs[self.cntr]['path'])

            #self.qlist_images.setItemSelected(self.items[self.cntr], True)
        else:
            QtWidgets.QMessageBox.warning(self, 'Sorry', 'No more Images!')

    def prevImg(self):
        print("Click next Image")
        if self.cntr > 0:
            self.cntr -= 1
            self.image_viewer.loadImage(self.logs[self.cntr]['path'])
            self.items[self.cntr].setSelected(True)

            #self.qlist_images.setItemSelected(self.items[self.cntr], True)
        else:
            QtWidgets.QMessageBox.warning(self, 'Sorry', 'No previous Image!')

    def item_click(self, item):
        self.cntr = self.items.index(item)
        self.image_viewer.loadImage(self.logs[self.cntr]['path'])

    def action_line(self):
        if self.toggle_line.isChecked():
            self.qlabel_image.setCursor(QtCore.Qt.CrossCursor)
            self.image_viewer.enablePan(False)

    def action_rect(self):
        if self.toggle_rect.isChecked():
            self.qlabel_image.setCursor(QtCore.Qt.CrossCursor)
            self.image_viewer.enablePan(False)

    def action_move(self):
        if self.toggle_move.isChecked():
            self.qlabel_image.setCursor(QtCore.Qt.OpenHandCursor)
            self.image_viewer.enablePan(True)

    # Unet
    def show_results(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(filter="Text files (1*.txt)")
        filename = filename[0]
        print("open file:", filename)
        if not filename:
            return
        with open(filename, "r") as f:
            text = f.read(10000)
            print(text)
            #self.qlist_results.setText(text)
            #self.qlist_results.setText("AAAAAAA")
            #self.qlabel_image.setText(text)
            self.textEdit.setText(text)


        # Unet plus
    def Unet_show_results(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(filter="Text files (2*.txt)")
        filename = filename[0]
        print("open file:", filename)
        if not filename:
            return
        with open(filename, "r") as f:
            text = f.read(10000)
            print(text)
            #self.qlabel_image.setText(text)
            self.textEdit.setText(text)

        # Resnet
    def Resnet_show_results(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(filter="Text files (3*.txt)")
        filename = filename[0]
        print("open file:", filename)
        if not filename:
            return
        with open(filename, "r") as f:
            text = f.read(10000)
            print(text)
            #self.qlabel_image.setText(text)
            self.textEdit.setText(text)

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create("Cleanlooks"))
    app.setPalette(QtWidgets.QApplication.style().standardPalette())
    parentWindow = Iwindow(None)
    sys.exit(app.exec_())

if __name__ == "__main__":
    #print __doc__
    main()
from Config import settings
import numpy as np
import cv2 as cv
import glob

class CalibratedCamera:
    ''' JINJIEAN B19 FPV Mini Camera '''
    chessboardSize = (8, 6)
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    ret = mtx = dist = rvecs = tvecs = None
    newcameramtx = roi = None
    cam_width, cam_height = settings.camera_scale[:2]

    def start(self):
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((self.chessboardSize[0] * self.chessboardSize[1] ,3), np.float32)
        objp[:,:2] = np.mgrid[0:self.chessboardSize[0], 0:self.chessboardSize[1]].T.reshape(-1,2)

        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.

        images = glob.glob('./calibration/*.jpg')

        for fname in images:
            img = cv.imread(fname)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret, corners = cv.findChessboardCornersSB(
                gray,
                self.chessboardSize,
                cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE
            )

            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)
                corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), self.criteria)
                imgpoints.append(corners2)

                # Draw and display the corners
                cv.drawChessboardCorners(img, self.chessboardSize, corners2, ret)
                # cv.imshow('img', img)
                # cv.waitKey(500)
        cv.destroyAllWindows()

        self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        self.newcameramtx, self.roi = cv.getOptimalNewCameraMatrix(self.mtx, self.dist, (self.cam_width,self.cam_height), 0, ((self.cam_width,self.cam_height)))

        return self
        
    def undistort(self, img):
        dst = cv.undistort(img, self.mtx, self.dist, None, self.newcameramtx)
        x, y, w, h = self.roi
        dst = dst[y:y+h, x:x+w]
        return dst


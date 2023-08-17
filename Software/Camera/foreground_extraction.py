import numpy as np
import cv2

class GrabCut:
    iterations = 5
    mask = []
    background_model = np.zeros((1, 65), np.float64)
    foreground_model = np.zeros((1, 65), np.float64)

    def begin(self, image, rect) -> np.ndarray:
        self.mask = np.zeros(image.shape[:2], np.uint8)

        cv2.grabCut(
            img = image,
            mask = self.mask,
            rect = rect,
            bgdModel = self.background_model,
            fgdModel = self.foreground_model,
            iterCount = self.iterations,
            mode = cv2.GC_INIT_WITH_RECT,
        )

        grabcut_mask = np.where((self.mask == cv2.GC_PR_BGD) | (self.mask == cv2.GC_BGD), 0, 1).astype("uint8")
        return image * grabcut_mask[:, :, np.newaxis]
# JINJIEAN B19 FPV Mini Camera

![jinjiean b19](https://github.com/xtnctx/Banana-Leaf-Classifier/assets/67821138/fadb10d4-2a45-4e8f-9a06-087fb7fbbfb3)


## B19 Product Manual

| <!-- -->                       | <!-- -->                                |
| ------------------------------ | ----------------------------------------|
| Model                          | MINI B19 FPV cameras                    |
| Image Sensor                   | 1/3' CMOS                               |
| Horizontal Resolution          | 1500TVL                                 |
| Lens                           | 2.1mm                                   |
| Signal System                  | PAL/NTSC (OSD internal adjustable)      |
| S/N Ratio                      | >60Db(AGC OFF)                          |
| Electronic Shutter Speed       | PAL: 1/50-100.000, NTSC: 1/60-100,000   |
| Auto Gain Control (AGC)        | LOW/MIDDLE/HIGH                         |
| Back light compensation (BLC)  | YES                                     |
| Min Illumination               | 0.001Lux/1.2F                           |
| WDR                            | D-WDR                                   |
| DNR                            | 3DNR                                    |
| Day/Night                      | Auto/Color/B*W                          |
| Power                          | DC 5V-30V                               |
| Net weight                     | 6.0g                                    |
| Dimensions                     | 19mm * 19mm * 19mm                      |

## On-Screen Display

| <!-- -->                       | <!-- -->                                                                              |
| ------------------------------ | ------------------------------------------------------------------------------------- |
| Exposure                       | Brightness/exposure mode/gain                                                         |
| The white balance              | Automatic tracking white balance                                                      |
| Day and night mode             | Internal automatic/color mode/black and white mode                                    |
| Video setings                  | Contrast/sharpness/saturation/digital noise/video format (N/P)/digital wide dynamic   |
| Language                       | Chinese/English/German/Italian/Russian                                                |
| Restore the factory settings   | OK                                                                                    |
| Save and exit                  | OK                                                                                    |



### Lens Distortion = Barrel
Appears in the middle of the lens's focal length range
 
![barrel distortion](https://github.com/xtnctx/Banana-Leaf-Classifier/assets/67821138/5c33ef7d-b686-4baa-be5b-f2968f8de38f)

## Camera Calibration
The goal of calibrating the camera is to remove the distortion to generate a normal flat image.
This is achieved using the `OpenCV Camera Calibration`

All of the camera's information (parameters or coefficients) necessary to calculate an accurate connection between a 3D point in the actual world and its corresponding 2D projection (pixel) in the picture acquired by that calibrated camera.


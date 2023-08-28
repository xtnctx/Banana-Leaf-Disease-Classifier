import winreg

# Only tested in Windows 10
def getAccentColor():
    ''' returns rgb values'''
    aReg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    aKey = winreg.OpenKey(aReg, 'SOFTWARE\Microsoft\Windows\DWM')
    value, _ = winreg.QueryValueEx(aKey, "AccentColor")
    value -= 0xff000000

    if aKey:
        winreg.CloseKey(aKey)

    bgr = '{:x}'.format(value)

    return [int(bgr[v:v+2], 16) for v in range(0, len(bgr), 2)][::-1] # rgb

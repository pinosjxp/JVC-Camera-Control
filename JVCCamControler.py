import requests
from requests.auth import HTTPDigestAuth
import json
import time
from threading import Thread


class JVCCam:
    def __init__(self, name, user, password, ip, debugFlag=False):
        self.debugFlag = debugFlag
        self.name = name
        self.pan = 0
        self.tilt = 0
        self.zoom = 0
        self.base_url = "http://" + ip
        R = requests.get(self.base_url+"/php/session_start.php", auth=HTTPDigestAuth(user, password))
        if R.status_code == 200:
            self.session_cookie = R.cookies
            print(self.session_cookie)
            self.t = Thread(target=self.keepAlive, args=[])
            self.t.start()
            print("Successful authentication.")
            requests.post(url=self.base_url + "/cgi-bin/cmd.cgi",
                              data=json.dumps({"Command":"CancelAvTransfer"}),
                              cookies=self.session_cookie,
                              headers={"Content-Type": "application/json"})
            requests.post(url=self.base_url + "/cgi-bin/cmd.cgi",
                              data=json.dumps({"Command": "SetCamCtrl", "Params": {"Ctrl": "ModeMonitor"}}),
                              cookies=self.session_cookie,
                              headers={"Content-Type": "application/json"})
            requests.get(self.base_url + "/cgi-bin/resource_release.cgi?param=mjpeg&" + str(round(time.time() * 1000)),
                             cookies=self.session_cookie)
            requests.get(self.base_url + "/cgi-bin/camera_status.cgi?" + str(round(time.time() * 1000)),
                             cookies=self.session_cookie)
            requests.get(self.base_url + "/cgi-bin/auto_status.cgi?" + str(round(time.time() * 1000)),
                             cookies=self.session_cookie)
            requests.get(self.base_url + "/cgi-bin/get_camera_setting.cgi?" + str(round(time.time() * 1000)),
                             cookies=self.session_cookie)
            requests.get(self.base_url + "/cgi-bin/hello.cgi?" + str(round(time.time() * 1000)),
                             cookies=self.session_cookie)
        elif R.status_code == 401:
            self.error(R, "Unauthorized - Invalid credentials supplied or session is invalid.", self.debugFlag)
        elif R.status_code == 403:
            self.error(R, "Access Forbidden - Camera is refusing connection. Check if session is still valid.", self.debugFlag)
        elif R.status_code == 404:
            self.error(R, "Not Found - API may be broken or camera connection issues.", self.debugFlag)
        else:
            self.error(R, "Unknown - Debug time!!!", True)

    def keepAlive(self):
        while True:
            time.sleep(1)
            requests.get(self.base_url+"/php/session_continue.php", auth=HTTPDigestAuth('root', 'password'),
                             cookies=self.session_cookie)
            requests.get(self.base_url+"/cgi-bin/ptz_position.cgi?"+str(round(time.time()*1000)),
                             cookies=self.session_cookie)
            requests.get(self.base_url + "/php/get_error_code.php", auth=HTTPDigestAuth('root', 'password'),
                             cookies=self.session_cookie)
            requests.get(self.base_url + "/cgi-bin/camera_status.cgi?" + str(round(time.time() * 1000)),
                             cookies=self.session_cookie)

    def zoom(self, z):
        request_data = {
            "Command": "SetZoomCtrl",
            "Params": {
                "Zoom": z
            }
        }
        R = requests.post(url=self.base_url + "/cgi-bin/cmd.cgi",
                          data=json.dumps(request_data),
                          cookies=self.session_cookie,
                          headers={"Content-Type": "application/json"})
        if R.status_code == 200:
            print(R.content)
            print("Successful action. Executed zoom {}".format(z))
            self.zoom = z
            # TODO: Check to make sure action completed in response data
        elif R.status_code == 401:
            self.error(R, "Unauthorized - Invalid credentials supplied or session is invalid.", self.debugFlag)
        elif R.status_code == 403:
            self.error(R, "Access Forbidden - Camera is refusing connection. Check if session is still valid.",
                       self.debugFlag)
        else:
            self.error(R, "Unknown - Debug Time", self.debugFlag)

    def getImage(self):
        R = requests.get(self.base_url + "/cgi-bin/get_jpeg.cgi?" + str(round(time.time() * 1000)),
                     cookies=self.session_cookie)
        if R.status_code == 200:
            return R.raw
        else:
            self.error(R,"Unknown - Retrieval of image data failed!!!")
            return None

    def move(self, p, t):
        if(p < -150 or p > 150) and (t < -30 or t > 40):
            print("Error: Incorrect move parameters")
        else:
            request_data = {
                "Command": "SetPTCtrl",
                "Params": {
                    "Cmd": 0,
                    "Pan": p,
                    "Tilt": t
                }
            }
            R = requests.post(url=self.base_url+"/cgi-bin/cmd.cgi",
                              data=json.dumps(request_data),
                              cookies=self.session_cookie,
                              headers={"Content-Type": "application/json"})
            if R.status_code == 200:
                print(R.content)
                print("Successful action. Executed pan {} tilt {}".format(p, t))
                self.pan = p
                self.tilt = t
                # TODO: Check to make sure action completed in response data
            elif R.status_code == 401:
                self.error(R, "Unauthorized - Invalid credentials supplied or session is invalid.", self.debugFlag)
            elif R.status_code == 403:
                self.error(R, "Access Forbidden - Camera is refusing connection. Check if session is still valid.", self.debugFlag)
            else:
                self.error(R, "Unknown - Debug Time", self.debugFlag)

    def logout(self):
        self.t.join()
        R = requests.get(self.base_url+"/php/session_finish.php",
                         auth=HTTPDigestAuth('root', 'password'),
                         cookies=self.session_cookie)
        if R.status_code == 200:
            print("Successfully logged out of {}".format(self.name))
        else:
            self.error(R, "Unknown - Future connections with {} may have issues!!!".format(self.name), self.debugFlag)

    def calibrate(self,quick=True):
        if quick:
            if self.debugFlag:
                print("Starting quick camera calibration for {}. Please stand by...".format(self.name))
            self.move(0, 0)
            time.sleep(3)
            self.move(150, 40)
            time.sleep(3)
            self.move(-150, 40)
            time.sleep(3)
            self.move(0, 0)
            time.sleep(3)
            if self.debugFlag:
                print("Completed quick camera calibration for {}.".format(self.name))
        else:
            if self.debugFlag:
                print("Starting full camera calibration for {}. Please stand by...".format(self.name))
            self.move(0, 0)
            time.sleep(3)
            self.move(0, 40)
            time.sleep(3)
            self.move(0, -30)
            time.sleep(3)
            self.move(0, 0)
            time.sleep(3)
            self.move(150, 0)
            time.sleep(3)
            self.move(150, 40)
            time.sleep(3)
            self.move(150, -30)
            time.sleep(3)
            self.move(150, 0)
            time.sleep(3)
            self.move(-150, 0)
            time.sleep(3)
            self.move(-150, 40)
            time.sleep(3)
            self.move(-150, -30)
            time.sleep(3)
            self.move(-150, 0)
            time.sleep(3)
            self.move(0, 0)
            time.sleep(3)
            if self.debugFlag:
                print("Completed full camera calibration for {}.".format(self.name))

    def error(self, request, message, detailsFlag):
        if detailsFlag:
            print("==============================")
            print("< " + self.name + " >")
            print("==============================")
            print("HTTP Error {}: ".format(request.status_code) + message)
            print("Headers:")
            print(request.headers)
            print("Response Data:")
            print(request.content)
            print("==============================")
        else:
            print("HTTP Error {}: ".format(request.status_code) + message)

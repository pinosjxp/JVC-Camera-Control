from JVCCamControler import JVCCam

if __name__ == "__main__":
    Cam_A = {}
    Cam_B = {
        "name": "JVC Camera B",
        "username": "root",
        "password": "password",
        "wifi": "192.168.1.1",
        "lan": "192.168.1.186",
        "wlan": "192.168.1.187"
    }
    Cam_C = {}

    B = JVCCam(Cam_B["name"], Cam_B["username"], Cam_B["password"], Cam_B["wifi"],True)
    B.calibrate(False)

    command = ""
    while True:
        command = input("> ")
        print(command)
        if command == "help" or command == "h":
            print("Enter two numbers corresponding to the pitch and tilt(I.e 10 10)")
        elif command != "end":
            commandArray = command.split(" ")
            B.move(int(commandArray[0]),int(commandArray[1]))
        else:
            print("Ending program")
            break
    B.logout()

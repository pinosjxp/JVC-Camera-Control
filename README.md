# JVC Camera Control Program

## Table of Contents
1. [Description](#Description)
2. [Developer Info](#Developer-Info)
    1. [Pre-Requisites](#Pre-Requisites)
    2. [API](#API)
3. [Future Work](#Future-Work)
4. [Miscellaneous](#Miscellaneous)

## Description

This program allow the user to control and receive information using a JVC GV-LS2 PTZ Camera. Current
## Developer Info

#### Pre-Requisites

Python Version:

* 3.5.x

Libraries used:

* Requests

Installation Instructions:

1. Create python virtual environment
    ```bash
    Linux-
    
    cd /path/to/your/Python/directory/Scripts/
    ./virtualenv /path/to/directory/the/virtual/environment/will/be/placed
    
    Windows-
    
    cd C:\Path\to\your\Python\Directory\Scripts\
    .\virtualenv C:\path\to\directory\the\virtual\environment\will\be\placed
    ```
2. Activate environment
    ```bash
    Linux-
    
    cd /path/to/directory/where/the/virtual/environment/is/
    cd ./Scripts
    ./activate
    
    Windows-
    
    cd C:\path\to\directory\where\the\virtual\environment\is\
    cd .\Scripts
    .\activate
    ```
3. Install requests library
    ```bash
    Linux-
 
    pip install requests
    
    Windows-
    
    pip install requests

    ```
4. Clone Gitlab repository
    * __HTTP -__ [https://github.com/pinosjxp/JVC-Camera-Control.git](https://github.com/pinosjxp/JVC-Camera-Control.git) - Requires Username/Password
    * __SSH -__ [git@toolsgit.labs.lenovo.com:jpinos/RedfishAutoPython.git](git@toolsgit.labs.lenovo.com:jpinos/RedfishAutoPython.git) - Requires SSH Keys

#### API

    WIP...
    
## Future Work
* Access full streaming capabilities (Camera supposed to stream at Full HD; Currently only reading image snapshots)

## Miscellaneous
Contact Joshua Pinos ([pinosjxp@gmail.com](pinosjxp@gmail.com)) for additional inquiries.

---

---

# Evaluation of Open-Source IIC-OSIC-TOOLS

There are numerous ways to install the open-source chip design tools. We will use a Windows machine and install
IIC-OSIC-TOOLS with the help of a docker. Now, installation can be performed by 2 methods, either using a docker desktop 
or by using wsl with docker. Let's explore each one by one.

## Method 1

1. Install Docker Desktop
   Go to the website https://www.docker.com/products/docker-desktop/ and download docker desktop. You can start without 
   signing in as well. 

2. Installation of IIC-OSIC-TOOLS on docker desktop
   * Open Docker Desktop
   * Go to images tab in docker
   * Search ***iic-osic-tools***
   * Install the ***hpretl/iic-osic-tools*** tool-kit
   * Run the docker container

3. Open Docker Image
   * Open the **iic-osic-tools** docker image.
   * Click on RUN symbol. As the image loads, it will display links to connect to a VNC server as well as a localhost.
   * Connect to the NoVNC html client link provided when the file runs.
   * Display should open on the browser.


## Method 2

1. Enable and install WSL

* Install **windows terminal** from microsoft store.

* Go to Control Panel -> Programs -> Programs and Features -> Turn Windows Features ON or OFF -> Turn ON Windows
  Subsystem for Linux feature. 

* Open command prompt as administrator and type the command `wsl --install` to install wsl (Windows Subsystem for Linux).

* It will display the available online distros to install. If it throws a kernel error, update wsl by typing `wsl --update`.

* Now, install your selected distro by `wsl --install -d <distro_name>`. 

* In case if you want to install more distros: `wsl --list -o`. 

* The default Linux distribution is Ubuntu but you can also install Debian or any other Linux distros by using the above two commands. 

* After installation, the shell that prompts you to set your UNIX user name and password. You can run your Linux commands from here.

2. Clone github repository

Now, open the installed Linux distro. Again, 2 ways to do this. 

* ***First***, open the installed **windows terminal** and select your Linux distro from there.

* ***Second***, search for the Linux distro directly from your Windows Search bar. 

* Now, clone the iic-osic-tools repository as shown below. This will clone the image to the home directory. 

* You can also install this to any other directory. Create a directory `mkdir AMCD`, move to the directory `cd AMCD`,
and clone the repository. The link for the repository is attached as a reference as well. 

```
git clone https://github.com/iic-jku/IIC-OSIC-TOOLS.git
```

3. Install docker in wsl

* Before running the docker container `./start_vnc.sh` script file, you need to install docker on wsl. 

* To do this, you can follow these steps :
  https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository. Test the installation using: `sudo docker
  run hello-world`. 
  
* Alternatively, you can install docker.io by typing `sudo apt install docker.io`.

4. Run docker with wsl

Now, you need to run the vnc script file. In order to do this, you are required to start the docker first. Then go the
working directory and run the vnc script file. 

```
sudo service docker start
cd IIC-OSIC-TOOLS
./start_vnc.sh
```

* The script file will ask you to start or remove the docker. Press 's' to start the docker. It will install the docker container.

* On first use, this will download and extract all the files (~17 GB or so), which will take time. This will be our initial setup.

* From second use, you just have to run the script file.

* You can also follow the post installation steps to manage the docker better. 
  Use: https://docs.docker.com/engine/install/linux-postinstall/. 
  You should now be able to run docker without sudo: `docker run hello-world`.

5. Running Docker Image

Now, we are done with the setup and can start the docker image.

* You can input the following command:

```
docker images/ docker image ls
docker run <image_id>
```

* Alternatively, you can run the vnc script file `./start_vnc.sh` and press 's' to start or stop the docker accordingly.


6. Open Docker Image

Connect to the NoVNC html client link provided when the file runs. Save or Bookmark the link for future use.
Display should open on a browser.


## Challenges faced

- Install ___Clash for Windows___ and enable system proxy if there is a server problem when installing wsl.

- If you choose to open docker image without vnc, you run the `./start_x.sh` script file. But it might fail displaying
'.Xauthority does not exist'. In order to solve this problem, create an empty file: `touch ~/.Xauthority`.

## Design and Simulation of Analog Circuits

1. Building a Circuit using Xschem

Xschem is the software which is particularly used in order to design analog circuits. When the NoVNC host displays a screen, open the terminal and type `Xschem &` to open Xschem.

Some useful shortcuts which may come handy while using Xschem are:

+ W : Draw wire
+ I : Draw line
+ C : Copy
+ M : Move
+ P : Pins 
+ Shift + I : Insert Symbols

Let's understand the design procedure to build a circuit.
 
2. Create a new circuit schematic file. Right click on mouse and click on Insert Symbols or use the above given shortcut
   to open the symbol window. In this window, there will be a set of libraries which an be used. We will use **Analog
   Lib** and **Sky130A** libraries to design our circuit. 

3. To select components such as voltage source, resistors, capacitors, ground, etc. go to **Analog Lib** library, click
   on `devices` directory and select the appropriate components. Place the compoments on the schematic. 

3. To select MosFETs, use the **Sky130A** library, click on `sky130_fd_pr` directory and select the type of mosfet model
   as required. The library has many mosfets so select according to the design requirement. Place the compoments on the
   schematic.

4. Now connect the wires to complete the circuit design. You can right click on mouse and click on Insert Wire or use
   the above given shortcut. 

5. Change the values of all the components as per the design specification.

6. Assign pins (inputs, outputs, VCC, VSS, etc.) to the circuit schematic. Right click on mouse and click on Insert Pin
   or use the above given shortcut.

## Creating a Symbol in Xschem from Schematic

Once you design the circuit, there is no need to design it again and again to use it in other schematics. Instead, you can create a symbol for it so you can use this circuit as a sub block in other schematics.

Follow these steps:

1. Open the schematic file of the designed circuit.

2. Now press `a` key on your keyboard. This will generate a symbol automatically. It will be saved in the same directory
   as the schematic file. 

3. You can edit the design of the symbol as per your need. Refer this tutorial for more information:
   https://xschem.sourceforge.io/stefan/xschem_man/creating_symbols.html.

## Simulation of a designed Circuit

Ngspice is a simulation software used to simulate analog circuits. Ngspice is already linked with Xschem. You just have
to write a netlist to simulate a circuit. 

1. Open a new circuit schematic file. Insert the designed symbol, input voltages, source voltages, etc. and connect it
   with wires to complete the circuit design. 

2. Once the circuit design is completed, you have to write a netlist code in order to run the simulation. To do this, go
   to insert symbols and use the **Analog Lib** library. In devices directory, you may select the `code` or `code_shown`
   symbol to create a netlist.

3. **Note:** To use mosfets, you need to add the library path for simulation as Ngspice does not know the components you
   added. To add the path of the mosfets, add `.lib /foss/pdks/sky130A/libs.tech/ngspice/sky130.lib.spice tt` this line
   in the start of your netlist.

4. Now, write a netlist code to simulate your circuit (eg. dc analysis, ac analysis, etc.) and to plot the inputs and outputs.

5. Check for errors if any. Run the schematic file and verify the outputs.

With the help of Xschem and Ngspice, you can design, create a symbol and simulate complicated analog circuits as
well. Thanks to the Sky130A library which helps to design the circuits on 130nm technology. You can also add more
libraries to Xschem to practice IC design.


## Reference Documentations

You can use these documentations as a reference.

* [**IIC-OSIC-TOOLS**](https://github.com/iic-jku/IIC-OSIC-TOOLS/tree/main)
* [**Xschem**](http://repo.hu/projects/xschem/xschem_man/xschem_man.html)
* [**Ngspice**](https://ngspice.sourceforge.io/docs.html)
* [**KLayout**](https://www.klayout.de/)
* [**Magic**](http://opencircuitdesign.com/magic/)  

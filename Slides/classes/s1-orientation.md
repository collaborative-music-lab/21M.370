# 21M.370 Orientation

This lecture covers all of the software we will use in the class. By the end of this lecture you should be:
- understand the different components of a DMI, and which software contributes to each component
- know how to setup audio and midi in PlugData
- the basics of interacting with PureData and automatonism
- understand why github is useful, and be able to pull and push to our class repo
- understand why it is important to only edit your own folder in the github
- know what circuitPython is, and how to mount your esp32 and copy code to it in Thonny

---

# About the course notes

* I am making these slides using markdown, and the markdown files are stored in the class repo:
* `21M.370/Slides/classes` 
* Links to any external images or videos will be in the markdown file.
<br>

* I will also try to remember to make PDF files of the slides and store them in:
* `21M.370/Slides/_pdf`
* The course notes will cover in-class micro-lectures, as well as video lectures assignmed to watch out of class.
	* I'd like to make each set of notes small enough that it is practical to use them as a reference - so if you have a question about a topic you know where to look.

---

# DMI Structure

- **Microcontroller**: A small computer that runs code called firmware (basically the same as software)
	- Much simpler than a PC, less overhead and therefore better control of timing
	- handles sensor input and interfacing with other hardware
- **Firmware**: The low-level software program installed on the microcontroller that manages sensor data and outputs USB MIDI messages.
- **USB MIDI**: The protocol that allows the device to communicate musical note and control data to a computer via USB connection.
	- The ESP32-s3 supports *class-compliant* USB MIDI, meaning there are no drivers to install and it will work with all PCs
- **Software Synthesis**: The computer-based audio processing that generates sounds based on MIDI messages received from the DMI.

---

# Our Digital Musical Instrument Framework

<img src="./images/dmi.png" class="large-img"/>

---

# PlugData and Automatonism

- PlugData is a port of the PureData sound synthesis software
	- it has lots of small user interface improvements
	- *vanilla* PD is very widely supported and open source
- **Audio and MIDI IO** setup
	- The hamburger icon opens up to let you select the setup dialog
	- or `Command-, / Ctrl-,` as a hotkey
	- Select the output device you want to use
	- Buffer size: prevents audio dropouts, but adds latency
		- try as low as you can go - 128 is great
- **MIDI** Select the port for your ESP32
	- Maybe called Waveshare or CircuitPython?

---

# PlugData

<img src="./images/plugdata.png" class="large-img"/>

---

# PureData patching mechanics

- PD has two modes: *edit* and *run*
	- *edit* mode lets you add, move, and connect objects
	- *run* mode lets you click buttons, type numbers, move sliders, etc.


<img src="./images/pd-edit-mode-2.png" class="med-img"/>

---

# PureData patching mechanics

- every object has inlets on top and outlets on the bottowm
- signal flow is top to bottom overall
- *audio* signals have a thick line
- *control* signals have a thin line
- audio and control signals are not always interchangeable!
	- there are ways to convert them
- *Bangs* are just a command to *do the thing you do*

<img src="./images/pd-signals.png" class="med-img"/>

---

# Automatonism Tricks

- `esc` should open the module browser. The modules always appear at the same position in PD.
- The `manual` button shows some useful information. 
	- `signal flow` contains examples of moving from audio to control signals and vice versa
	- `external messages` shows how to control parameters in automatonism remotely. We will use this a lot!
- Autamatonism is set to be pretty quiet. I will use `*~ 10` a lot to amplify signals before the `Maestro4` output

<img src="./images/automatonism-manual.png" class="medium-img"/>

---

# Version Control with Git

- **What is Version Control**: A system that tracks changes to files over time, allowing you to see history, revert to previous versions, and collaborate with others.
- **What is a Git Repo**: A folder containing your project files along with a hidden `.git` directory that stores all version history and metadata for the project.
- **Local vs Remote**: Local refers to the repository on your computer, while remote (like on Github) is the centralized copy that team members can access and sync with.

---

# Github Desktop

<img src="./images/github-desktop.png" class="large-img"/>

---

# Version Control with Git

- **Pulling and Stashing Code**: Pulling downloads the latest changes from the remote repository to your local version
	- if there are conflicts (the file on your computer and the remote file have different changes) you will need to resolve them
	- for now, you should only change code in *your personal folder*
	- if you accidentally change code in the main repo, you might save it outside the repo, and then delete the changes or *stash* the code (hiding it from the repo)
- **Pushing and Committing Code**: Committing saves your local changes to your repository's history with a descriptive message, and pushing uploads those commits to the remote repository.
	- committing only saves the changes on *your* computer

---

# Github Repo

- **Github Desktop**: A graphical user interface application that simplifies version control and file synchronization without using command-line commands.
- **Github Account**: A user profile on Github that stores your repositories and allows you to collaborate with other developers.
	- You will need to make this in order to push to our repo.
- **Making Your Own Folder**: Create a new directory `21M-370/personal/your-name/` and save your own files here, and then you can push them to the repo. This will let everyone see your files
- Alternatively, just copy class projects outside the repo and work on them there. 

---

# Thonny

- **Overview**: A beginner-friendly Python IDE designed for editing and running Python code directly on microcontrollers.
- **Connecting**: Your ESP32 will show up as a USB hard drive on your computer
	- on the bottom right hand side, you will see a drop-down to select it
	- this will open up a file browser for the files on the ESP32
	- files on your ESP32 are *not* saved on your local PC - get in the habit of making backups!

---

# Thonny

<img src="./images/thonny.png" class="large-img"/>

---

# Thonny

- **Monitoring, Debugging** in the *view* menu
	- Shell: a text log you can print to using `print()` functions
	- Plotter: a graphing tool we will use later on
	- Lots of other helpful tools. . . 
- **Up and Downloading Files** to move files from your PC to the ESP32
	- select the files you want to transfer, right-click, and you will see with upload or download
	- be aware that there is no undo - make backups of your files before overwriting them
- **Alternatives to Thonny**: Other IDEs and development tools like PyCharm, VS Code, or Mu that can be used to program microcontrollers.
	- You are on your own here!
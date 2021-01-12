# ECG interference removal from single channel EMG recording

This repository contains the source codes for the paper "A new algorithm for ECG interference removal from single channel EMG recording. Australasian physical & engineering sciences in medicine 40, no. 3 (2017): 575-584."


![plot](GUI.jpg)


## Required packages

    scipy
    numpy
    PyEMD
    matplotlib
    tkinter
You can also use the following command to install all the requiered packages together:
```
!pip install -r requirements.txt
```
## Usage

Run the following code to  start the gui

```
python GUI_EMG.py
```

**"Upload file"** button can be used to import contaminated EMG signal <br />
&nbsp;&nbsp;&nbsp;&nbsp;The file shoud be in txt format and have one columun with no header, starting from the first row as shown blow:  
<image src='input_data.jpg'>

**"Enter fs"** button can be used to enter the sampling frequency range <br />
**"Denoise"** button will apply denoising algorithm <br />
**"Save EMG"** button can be used to export clean EMG after applying denoising algorithm <br />
**"Save ECG"** button can be used to export clean ECG after applying denoising algorithm <br />

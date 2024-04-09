# LFC Bible App
## Introduction
This app was specifically made in mind with the intention of serving the purpose of living faith church and living faith chuch alone, but it then realize that what is the use of making sucha cool app, but people (except my church) can't use it, that is why I am releasing this on Github. You might not really care, but I deemed it fit to share my feelings with you

### Table of Content
* [About](#about)
* [Installation of app requirements](#installation-process)
* [Usage](#usage-after-install)
* [Functionality](#functionality)
* [What's Next](#whats-next)
* [Licence](#licence)
* [Acknowledgments to the contributors](#acknowledgments)

## About
* It can serve as a personal bible, where you can translate the word of God in 10 different languages and some have different versions.

* It is intended to be used as a free alternative to easy worship (that functionality has not been added).

* It is supposed to be a method of the gospel display in small congregations.


## Installation Process
- Download or clone the git repository
- The code is written in python so if python is not installed on your system, you would need to install it from their official website: [Python.org](https://www.python.org)
- By default pip will be installed along with python in the installation prompt but to make sure pip is installed, open command prompt and typing
    ```bash
    pip
    ```
    If it is install it will show commands and options that go with pip, but if it gives an error that pip is not recognized
     * Go to the environment variables and make the path to pip an environment variable or
     * Re-install python, so that it can automatically install pip (check the checkbox that says install pip during the installation)
- In your command prompt run the following:
    ```
    pip install customtkinter
    pip install tk
    ```
- If you are on windows and want to have elevated user privellages for the app, run the follwing in order to install pyuac and pywintypes
    ```
    pip install pyuac
    pip install pywintypes
    ```
- From here, you can open the code in your favorite editor and use it to your hearts content

## Usage after Install
In you command prompt or terminal, navigate to the folder where the code is installed and run 
```
py main.py
```
and then the app will run. **Note:** if the run_as_admin function is used the an admin request will popup before the app runs, and the app cannot run if the admin request is not agreed to.


## Functionality

#### Content
* [Header editor part of the app](#header-editor)
* [Footer editor part of the app](#footer-editor)
* [Body editor part of the app](#body-editor)
* [Background editor part of the app](#background-editor)
* [Save part of the app](#save)

#### Header Editor
The header is the part that is to show at the top of the document, it is prety self explanitory, the font, text, text-color, font-weight, font-style etc can all be changed within the app and seen updated in the input widget being shown, but the justification and the offset (offset will be added), will be added while the thing is updating on the screen

#### Footer Editor
The footer is basically the header but at the bottom of the screen

#### Body Editor
This is the main part of the app and the most elegant in my view, it consists of the old and new testament widgets with writeable verses and chapters, it has translations of the bible to different languages and different versions of those scripture. Note: The body also has all the features of the header and footer

#### Background Editor
This part you can use to add and edit the background, it is still a work in progress, that is why it is not perfect

#### Save
I just cobbled this up, just so that I could say we have a save screen, but don't worry, it will be updated


## What's Next
* Add a Preview tab, that can be used to preview the project

* Add functionality to the save and export the project

* Addition of custom themes (Not native to the customtk library)

* Bring everything together into an app that people will actually want to use

* Fix certain bugs


## Licence

### LFC Bible App License

LFC Bible App is made available under the terms of the MIT License. This application incorporates and redistributes Bible translations from Thiago Bodruk which are also made available under the Creative Commons BY-NC.

Portions of the software in LFC Bible App are provided under specific open-source licenses. This file and the source code files contain important notices and acknowledgments for those licenses. By using LFC Bible App, you agree to respect the intellectual property rights under these licenses and to adhere to the terms of the MIT License.

### LFC Bible App License

LFC Bible App is licensed under the MIT License. A copy of this license is included in the section below and is also available at [Licence](LICENCE).

### Thiago Bodruk's License

The Bible translations used in LFC Bible App are sourced from [thiagobodruk-bible-master](https://github.com/thiagobodruk/bible?tab=readme-ov-file), which is licensed under the Creative Commons BY-NC. A copy of this license is included below and is also available at [Creative Commons BY-NC full text](https://creativecommons.org/licenses/by-nc/2.0/br/).

## Acknowledgments
* Jesus Christ, who made heaven and earth, lord over my soul, who gave me the knowledge and idea to make this app

* We gratefully acknowledge the contributor [Thiago Bodruk](https://github.com/thiagobodruk) for making their work available under Creative Commons BY-NC, and we encourage users of LFC Bible App to also adhere to the terms of this license.

* Living faith teens church (Enugu branch), who are the inspirations of this project

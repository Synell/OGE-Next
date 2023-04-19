<h1 align="center"><img src="./data/icons/OGENext.svg" width="32" align="center" /> OGE Next: View your Grades Easily</h1>
<p align="center">
  <a href="https://www.python.org/downloads/">
    <img alt="Python 3.11" src="https://img.shields.io/badge/Python-3.11-blue" />
  </a>
  <a href="https://doc.qt.io/qtforpython/index.html">
    <img alt="PySide 6" src="https://img.shields.io/badge/PySide-6.4.1-brightgreen" />
  </a>
  <a href="https://github.com/Synell/OGE-Next/blob/master/LICENSE">
    <img alt="License: LGPL" src="https://img.shields.io/badge/License-LGPL-green" target="_blank" />
  </a>
  <img alt="Platforms: Windows, Linux and MacOS" src="https://img.shields.io/badge/Platforms-Windows%20|%20Linux%20|%20MacOS-yellow" />
  <a href="https://www.buymeacoffee.com/synell">
    <img alt="Donate: Buy me a coffee" src="https://img.shields.io/badge/Donate-Buy%20Me%20a%20Coffee-orange" target="_blank" />
  </a>
  <a href="https://www.patreon.com/synel">
    <img alt="Donate: Patreon" src="https://img.shields.io/badge/Donate-Patreon-red" target="_blank" />
  </a>
</p>

----------------------------------------------------------------------

OGE Next is a grade viewer for Windows, Linux and MacOS. It allows you to view your grades from the [OGE](https://iutdijon.u-bourgogne.fr/oge/stylesheets/etu/home.xhtml) website.


## Requirements

### Windows
- Windows 7 or later
- VC++ 2015 Redistributable

### Linux
- All Linux distributions supported by PySide6

### MacOS
- MacOS 10.14 (Mojave) or later


### Source Code
- Python 3.11 or later
  - Dependencies (use `pip install -r requirements.txt` in the project root folder to install them)


## Installation

### Windows, Linux and MacOS

<a href="https://github.com/Synell/OGE-Next/releases/latest">
  <img alt="Release: Latest" src="https://img.shields.io/badge/Release-Latest-00B4BE?style=for-the-badge" target="_blank" />
</a>

- Download the latest release from the [releases page](https://github.com/Synell/OGE-Next/releases) and extract it to a folder of your choice.


## Customization

### Language

- You can customize the language of the app by adding a new file into the `/data/lang/` folder. The language must be a valid [JSON](https://en.wikipedia.org/wiki/JavaScript_Object_Notation) code. If the language is not supported, the app will default to English. Then, you can change the language in the settings menu.

  *See [this file](https://github.com/Synell/OGE-Next/blob/main/data/lang/english.json) for an example.*

### Theme

- You can customize the theme of the app by adding new files into the `/data/themes/` folder. The theme must be contain valid [JSON](https://en.wikipedia.org/wiki/JavaScript_Object_Notation) codes and valid [QSS](https://doc.qt.io/qt-6/stylesheet-reference.html) codes. If the theme is not supported, the app will default to the default theme. Then, you can change the theme in the settings menu.

  *See [this file](https://github.com/Synell/OGE-Next/blob/main/data/themes/neutron.json) and [this folder](https://github.com/Synell/OGE-Next/tree/main/data/themes/neutron) for an example.*


## Usage

### Connecting

<img alt="Login screen" src="https://raw.githubusercontent.com/Synell/Assets/main/OGENext/readme/login.png" />

Enter your username and password in the login screen and click on the "Login" button. If the connection is successful, you will be redirected to the main screen.

*Note that OGE is super slow sometimes, so it may take a while to load the grades.*

### Viewing grades

<img alt="Grades" src="https://raw.githubusercontent.com/Synell/Assets/main/OGENext/readme/grades.png" />

#### Sidebar

On the left side of the screen, you can see the sidebar. It contains the semester list and the settings button.

Once the semester loaded, you can see an icon next to the semester ID. This icon indicates the status of the semester:

- <img alt="Perfect semester" src="https://raw.githubusercontent.com/Synell/OGE-Next/main/data/themes/neutron/dark/icons/sidepanel/semester_perfect.png" width=32px align="center" /> Perfect semester: you have no failed UE.

- <img alt="Good semester" src="https://raw.githubusercontent.com/Synell/OGE-Next/main/data/themes/neutron/dark/icons/sidepanel/semester_good.png" width=32px align="center" /> Good semester: you have one or two UE between 8/20 and 10/20 with the other UEs between 10/20 and 20/20.

- <img alt="Bad semester" src="https://raw.githubusercontent.com/Synell/OGE-Next/main/data/themes/neutron/dark/icons/sidepanel/semester_alert.png" width=32px align="center" /> Alert semester: you have at least one UE between 0/20 and 8/20.

- <img alt="Bad semester" src="https://raw.githubusercontent.com/Synell/OGE-Next/main/data/themes/neutron/dark/icons/sidepanel/semester_bad.png" width=32px align="center" /> Bad semester: you have all your UEs between 0/20 and 8/20.

- <img alt="Blue globe" src="https://raw.githubusercontent.com/Synell/OGE-Next/main/data/themes/neutron/dark/icons/sidepanel/semester_unknown.png" width=32px align="center" /> Missing data: the semester is not loaded yet and will be loaded when you click on it.

*Note that loading a semester may take a while as it makes a new request to the OGE website.*

#### Semesters

On the right side of the screen, you can see the UE list with their average grade.

On top of the UE list, you can see a refresh button and an encouragement message with the UEs to focus on if you want to improve your average grades (when you don't have the perfect grade).

<h1 align="center"><img src="./data/icons/AppManager.svg" width="32" align="center" /> App Manager: Manage your Apps with Ease</h1>
<p align="center">
  <a href="https://www.python.org/downloads/">
    <img alt="Python 3.11" src="https://img.shields.io/badge/Python-3.11-blue" />
  </a>
  <a href="https://doc.qt.io/qtforpython/index.html">
    <img alt="PySide 6" src="https://img.shields.io/badge/PySide-6.4.1-brightgreen" />
  </a>
  <a href="https://github.com/Synell/App-Manager/blob/master/LICENSE">
    <img alt="License: LGPL" src="https://img.shields.io/badge/License-LGPL-green" target="_blank" />
  </a>
  <img alt="Platforms: Windows" src="https://img.shields.io/badge/Platforms-Windows-yellow" />
  <a href="https://www.buymeacoffee.com/synell">
    <img alt="Donate: Buy me a coffee" src="https://img.shields.io/badge/Donate-Buy%20Me%20a%20Coffee-orange" target="_blank" />
  </a>
  <a href="https://www.patreon.com/synel">
    <img alt="Donate: Patreon" src="https://img.shields.io/badge/Donate-Patreon-red" target="_blank" />
  </a>
</p>

----------------------------------------------------------------------

App Manager is a simple app manager for Windows (Linux and MacOS versions are not available as they're untested). It allows you to install, uninstall, and update apps without using the command line or having to download and install the app from your browser. Everything is done in a simple and easy to use GUI.


## Requirements

### Windows

- Windows 7 or later
- VC++ 2015 Redistributable


### Source Code
- Python 3.11 or later
  - PySide6 (`pip install PySide6`)
  - multipledispatch (`pip install multipledispatch`)
  - requests (`pip install requests`)


## Installation

### Windows

<a href="https://github.com/Synell/App-Manager/releases/latest">
  <img alt="Release: Latest" src="https://img.shields.io/badge/Release-Latest-00B4BE?style=for-the-badge" target="_blank" />
</a>

- Download the latest release from the [releases page](https://github.com/Synell/App-Manager/releases) and extract it to a folder of your choice.


## Customization

### Language

- You can customize the language of the app by adding a new file into the `/data/lang/` folder. The language must be a valid [JSON](https://en.wikipedia.org/wiki/JavaScript_Object_Notation) code. If the language is not supported, the app will default to English. Then, you can change the language in the settings menu.

  *See [this file](https://github.com/Synell/App-Manager/blob/main/data/lang/english.json) for an example.*

### Theme

- You can customize the theme of the app by adding new files into the `/data/themes/` folder. The theme must be contain valid [JSON](https://en.wikipedia.org/wiki/JavaScript_Object_Notation) codes and valid [QSS](https://doc.qt.io/qt-6/stylesheet-reference.html) codes. If the theme is not supported, the app will default to the default theme. Then, you can change the theme in the settings menu.

  *See [this file](https://github.com/Synell/App-Manager/blob/main/data/themes/neutron.json) and [this folder](https://github.com/Synell/App-Manager/tree/main/data/themes/neutron) for an example.*


## Usage

### Installing Apps

You can start App Manager by double clicking the `AppManager` file in the folder you extracted the release to.

<img alt="Apps tab with no app installed" src="https://raw.githubusercontent.com/Synell/Assets/main/AppManager/readme/interface_empty.png" />

Once you have started App Manager, you can click on the settings button to configure the app and add the apps you want to follow in the `Followed Apps` tab.

*To add an app, you need to get its URL (e.g. `https://github.com/Synell/PERT-Maker`). You can then click on the `+` button and paste the URL into the text field.*

<br/>

<img alt="Settings window" src="https://raw.githubusercontent.com/Synell/Assets/main/AppManager/readme/settings.png" />

Once you have added the apps you want to follow, you can leave the settings and click on the `Install App` button to install an app. This will open a new menu where you can select the app you want to install.

*Note that you can only install apps that you have added to the `Followed Apps` tab.<br/>You also need to be connected to the internet to install apps.*

<br/>

Once you have found the app you want to install, you can click on the `Install` button to install it. This will open a new menu where you can select the version you want to install.

If you go into the `Downloads` tab, you can see all the apps you are currently downloading with their progress.

<img alt="Downloads tab" src="https://raw.githubusercontent.com/Synell/Assets/main/AppManager/readme/downloads.png" />

<br/>

If you go into the `Apps` tab, you can see all the apps you have installed with their version.

<img alt="Apps tab with an app installed" src="https://raw.githubusercontent.com/Synell/Assets/main/AppManager/readme/interface.png" />

Just click on the app to open it.


### Updating Apps

To update an app, you can click on the `Update` button in the `Apps` tab.

*This button will only be visible if there is an update available for the app.*

<img alt="Update button image" src="https://raw.githubusercontent.com/Synell/Assets/main/AppManager/readme/interface_update.png" />


### Uninstalling Apps

To uninstall an app, you can click on the setting button of the app in the `Apps` tab. Then, click on the `Uninstall` button.

<img alt="Uninstall popup image" src="https://raw.githubusercontent.com/Synell/Assets/main/AppManager/readme/uninstall.png" />


### Editing Apps Properties

In the `Apps` tab, you can click on the setting button of the app and then on the `Edit` button to edit the app's properties.

<img alt="Edit popup image" src="https://raw.githubusercontent.com/Synell/Assets/main/AppManager/readme/edit.png" />

*You can edit the app's icon, update interval, and the advanced settings like the current working directory and the command line to execute in order to start the app.*

<img alt="App Settings Image" src="https://raw.githubusercontent.com/Synell/Assets/main/AppManager/readme/app_settings.png" />

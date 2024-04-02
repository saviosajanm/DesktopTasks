# Desktop Tasks v0.1

Desktop Tasks is an application inspired by the iconic desktop widgets of Windows 7. With this application, users can create, edit, and delete tasks directly on their desktop background. The main goal of Desktop Tasks is to provide users with a convenient way to stay organized and never miss out on important tasks.

## Features
* Fetch Background Image: Desktop Tasks retrieves the current desktop background image.
* Task Manipulation: Users can create, edit, or delete tasks using the application's intuitive interface.
* Overlay Tasks: The application overlays the tasks onto the background image, ensuring they are prominently displayed on the desktop.
* Set New Background: Finally, Desktop Tasks sets the modified image as the new desktop background, allowing users to see their tasks every time they access their computer.


The inspiration behind Desktop Tasks is to provide users with a way to manage their tasks and stay organized. By integrating task management directly into the desktop environment, users can effortlessly keep track of their to-do lists and ensure nothing falls through the cracks. The application aims to enhance productivity and efficiency by providing users with immediate access to their tasks the moment they turn on their computer. Desktop Tasks is a promising application that aims to revolutionize task management by bringing it directly to the user's desktop. With its interface and integration, Desktop Tasks is poised to become an indispensable tool for users looking to stay organized and productive.

## Disclaimer: This is a WINDOWS ONLY release.

## Installation
1. Go to the [releases page](https://github.com/saviosajanm/DesktopTasks/releases/) and download the latest installer "DesktopTasksInstaller.exe"
   
   ![Releases page](https://github.com/saviosajanm/DesktopTasks/blob/main/photos/downloadpage.png)

2. After downloading the installer, run it and set the path you wish to install the application in.
   
   ![setup path](https://github.com/saviosajanm/DesktopTasks/blob/main/photos/setup1.png)

3. Continue with the setup including deciding whether the app should have a desktop shortcut created or not, and then click "Install" to initiate the installation
   
   ![shortcut choice](https://github.com/saviosajanm/DesktopTasks/blob/main/photos/shortcut.png)
   
4. Click "Finish" once the installation is done.
   
   ![installation finish](https://github.com/saviosajanm/DesktopTasks/blob/main/photos/complete.png)

## Usage

---

### Adding a task:

![Adding steps](https://github.com/saviosajanm/DesktopTasks/blob/main/photos/add.png)

To add a task, entering the description, hour, minute, date of the task is mandatory. To edit the colors of each component of the box namely the text, filling and border, click on the buttons to open the color selector and select the desired color for each component. To set to the default color, leave it as is or if inside the color selector, click on "***Cancel***". After filling all the details, click on the "***Add***" button.

---

### Editing a task:

![Editing steps](https://github.com/saviosajanm/DesktopTasks/blob/main/photos/edit.png)

To edit a task, first click on the task in the left pane that you want to edit. When you click on that task, the task details will fill all the inputs in the right pane. Then change these inputs to whatever you want. Once you are done with changing the values, click on the "***Edit***" button and the changes will be reflected onto the desktop background.

---

### Deleting a task:

![Deleting steps](https://github.com/saviosajanm/DesktopTasks/blob/main/photos/delete.png)

To delete a task, simply click on the task in the left pane that you want to delete. Once the task details fill the inputs in the right pane, click on the "***Delete***" button. This will automatically reflect on the desktop background.

---

### Configuring the box features:

![Configuring steps](https://github.com/saviosajanm/DesktopTasks/blob/main/photos/config.png)

To configure the box propertieas accross all tasks, go to the ***config.ini*** file inside the installation directory of the application. Edit the different values of the configuration file in accordance with how you want your boxes to look. 
Some key notes:
* ***box_width*** basically represents how many tasks do you want to put side by side accross the screen. If say box_width = 7, that means the width of the box is set in such a way that at max 7 boxes of equal width can be stacked next to each other accross the screen width.
* ***font*** is the font used for all the tasks' text. To use any font you like, place the .ttf file of that font into the fonts folder of the installation directory. Then set this variable value in the config file to the name of the font.
* ***box_margin*** is basically the space between each individual task box and between themselves and the display borders.
* ***box_padding*** is the amount of vertical space within the box. This is usually set when the text within the box is to be approppriately sized and spaced inside the borders of the box.
* ***border_radius*** and ***border_width*** are self explanatory and determine the border radius and width of all task boxes.
* ***taskbar_present*** is a binary value (1 or 0) which represents whether there is a taskbar present on the screen. This is applicable especially for people who sometimes prefer to set their taskbar to "auto-hide". For such users, they can set this value to 0, else 1.

---

### Setting the new background after a desktop background change:

![Background steps](https://github.com/saviosajanm/DesktopTasks/blob/main/photos/reset.png)

If the user wants to change their current background to a new one, they should make sure that the new background should be set as "stretch" in the windows settings menu. Once set, click on the "***Set this background as tasks background***" button, after which the application will register this new background as the background for tasks to be drawn on. If there are any active tasks that are lost after the background change, clicking this button will redraw these tasks onto the new background.

#### WARNING:
***Press this button ONLY AFTER setting the new background onto the desktop. If done so before, the background with the tasks already drawn on it will be registered as the base background and any further tasks added, edited or deleted will be drawn over this background without removing the tasks already previously drawn on it. If this accident occurs, you will have to clear all tasks and then manually set the original base background in the windows settings to correct this.***

---

### Clearing all the tasks:

![Clearing steps](https://github.com/saviosajanm/DesktopTasks/blob/main/photos/clear.png)

To clear all the tasks, simply click on the "***Clear all***" button and all the tasks will be automatically cleared from the registry and the desktop background itself.

---

## Note: This is an early build and a hobby project, so further development on this project may not be consistent.

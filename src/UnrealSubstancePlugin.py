import tkinter.filedialog  # Importing the file dialog module from tkinter for directory selection
from unreal import ToolMenuContext, ToolMenus, ToolMenuEntryScript, uclass, ufunction  # Importing Unreal Engine specific modules and decorators
import sys  # Importing the sys module to manipulate the Python runtime environment
import os  # Importing the os module for operating system dependent functionality
import importlib  # Importing the importlib module to reload modules
import tkinter  # Importing the tkinter module for GUI operations

# Getting the directory of the current script
srcDir = os.path.dirname(os.path.abspath(__file__))
# Adding the script directory to the system path if it's not already there
if srcDir not in sys.path:
    sys.path.append(srcDir)

import UnrealUtilities  # Importing a custom module named UnrealUtilities
importlib.reload(UnrealUtilities)  # Reloading the UnrealUtilities module to ensure it's up to date

@uclass()  # Declaring a class as an Unreal Engine class
class LoadFromDirEntryScript(ToolMenuEntryScript):
    @ufunction(override=True)  # Declaring a function that overrides a parent class function
    def execute(self, context):
        window = tkinter.Tk()  # Creating a hidden tkinter window
        window.withdraw()  # Hiding the tkinter window
        fileDir = tkinter.filedialog.askdirectory()  # Opening a dialog to select a directory
        window.destroy()  # Destroying the tkinter window
        UnrealUtilities.UnrealUtility().LoadFromDir(fileDir)  # Calling a method to load from the selected directory

@uclass()  # Declaring another Unreal Engine class
class BuildBaseMaterialEntryScript(ToolMenuEntryScript):
    @ufunction(override=True)  # Declaring a function that overrides a parent class function
    def execute(self, context: ToolMenuContext) -> None:
        UnrealUtilities.UnrealUtility().FindOrCreateBaseMaterial()  # Calling a method to find or create a base material

class UnrealSubstancePlugin:
    def __init__(self):
        self.subMenuName = "SubstancePlugin"  # Setting the submenu name
        self.subMenuLabel = "Substance Plugin"  # Setting the submenu label
        self.InitUI()  # Initializing the user interface

    def InitUI(self):
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu")  # Finding the main menu in the level editor
        self.subMenu = mainMenu.add_sub_menu(mainMenu.menu_name, "", "SubstancePlugin", "Substance Plugin")  # Adding a submenu to the main menu
        self.AddEntryScript("BuildBaseMaterial", "Build Base Material", BuildBaseMaterialEntryScript())  # Adding an entry script for building base material
        self.AddEntryScript("LoadFromDir", "Load From Directory", LoadFromDirEntryScript())  # Adding an entry script for loading from a directory
        ToolMenus.get().refresh_all_widgets()  # Refreshing all widgets to apply changes

    def AddEntryScript(self, name, label, script: ToolMenuEntryScript):
        script.init_entry(self.subMenu.menu_name, self.subMenu.menu_name, "", name, label)  # Initializing the menu entry script
        script.register_menu_entry()  # Registering the menu entry script

UnrealSubstancePlugin()  # Creating an instance of the UnrealSubstancePlugin class to execute the code
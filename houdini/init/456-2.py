import hou
# Set the auto save interval to 30 minutes (in seconds)
auto_save_interval = 30 * 60
# Enable auto save and set the interval
hou.hipFile.setAutoSave(True)
hou.hipFile.setAutoSaveInterval(auto_save_interval)
# Print a message to confirm that auto save is enabledprint("Auto save is now enabled with an interval of", auto_save_interval, "seconds.")


##############


import hou
# Set the auto save interval to 30 minutes (in seconds)
auto_save_interval = 30 * 60
# Enable auto save and set the interval
hou.hscriptExpression("set autosave = 1")
hou.hscriptExpression("set autosaveinterval = " + str(auto_save_interval))
# Print a message to confirm that auto save is enabled
print("Auto save is now enabled with an interval of", auto_save_interval, "seconds.")

########### 
import hou
# Get a reference to the "CA" shelf
shelf = hou.shelves.shelf("CA")
# Show the shelf in the Houdini interface
if shelf:
    shelf.setIsVisible(True)
    print("The 'CA' shelf is now visible.")
else:
    print("The 'CA' shelf was not found.")
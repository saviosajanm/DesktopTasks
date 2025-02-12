# build_exe.py
import PyInstaller.__main__
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'gui.py',  # Your main script
    '--onefile',  # Create a single executable
    '--windowed',  # Hide the console window
    '--icon=icon.ico',  # Set the application icon
    '--name=Desktop Tasks',  # Name of the output executable
    # Add all required files and folders
    '--add-data=icon.ico;.',
    '--add-data=tasks.json;.',
    '--add-data=config.ini;.',
    '--add-data=back.py;.',
    '--add-data=confgui.py;.',
    '--add-data=utils.py;.',
    '--add-data=fonts;fonts',  # Include entire fonts folder
    # Exclude unnecessary modules to reduce size
    '--exclude-module=matplotlib',
    '--exclude-module=numpy',
    '--exclude-module=pandas',
    '--exclude-module=scipy',
    # Add the directory containing your modules to Python path
    '--paths=.',
    # Clean and optimize
    '--clean',
    '--strip',
    '--noupx',
    # Specify paths
    f'--specpath={current_dir}',
    f'--distpath={os.path.join(current_dir, "dist")}',
    f'--workpath={os.path.join(current_dir, "build")}',
])
#!/bin/bash

# Set project and output details
APP_NAME="MyApp"
VERSION="1.0"
MAIN_SCRIPT="main.py"
DIST_DIR="dist"
BUILD_DIR="build"
INSTALLER_SCRIPT="installer.nsi"

# Clean up any previous builds
echo "Cleaning up old builds..."
rm -rf $DIST_DIR $BUILD_DIR $APP_NAME.spec

# Verify the PySide2 plugin path
QT_PLUGIN_PATH="/home/galopin/Área de Trabalho/Projects/Wa Its/Wa_its_venv/lib/python3.11/site-packages/PySide2/Qt/plugins"
if [ ! -d "$QT_PLUGIN_PATH" ]; then
    echo "Qt plugin directory does not exist at $QT_PLUGIN_PATH"
    exit 1
fi

# Package the app using PyInstaller
echo "Packaging the app with PyInstaller..."
pyinstaller --onefile \
            --add-data "assets:assets" \
            --add-data "resources:resources" \
            --add-data "src/data:src/data" \
            --add-data "src/ui:src/ui" \
            --add-data "src/utils:src/utils" \
            --add-binary "$QT_PLUGIN_PATH:PySide2/Qt/plugins" \
            $MAIN_SCRIPT

# Check if PyInstaller was successful
if [ $? -ne 0 ]; then
    echo "PyInstaller failed. Exiting."
    exit 1
fi

# Create the NSIS installer script
echo "Creating NSIS installer script..."
cat <<EOL > $INSTALLER_SCRIPT
!define APP_NAME "$APP_NAME"
!define VERSION "$VERSION"
!define INSTALL_DIR "\$PROGRAMFILES\\$APP_NAME"
!define ICON "assets\\icon.ico"

OutFile "$APP_NAME-Installer.exe"
InstallDir \${INSTALL_DIR}

!include "MUI2.nsh"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Section "Install"
    SetOutPath \$INSTDIR
    File /r "$DIST_DIR\\*.*"
    CreateShortcut "\$DESKTOP\\$APP_NAME.lnk" "\$INSTDIR\\$APP_NAME.exe"
SectionEnd

Section "Uninstall"
    Delete "\$DESKTOP\\$APP_NAME.lnk"
    RMDir /r \$INSTDIR
SectionEnd
EOL

# Check if NSIS script was created
if [ ! -f $INSTALLER_SCRIPT ]; then
    echo "Failed to create NSIS installer script. Exiting."
    exit 1
fi

# Build the installer with NSIS
echo "Building the installer with NSIS..."
makensis $INSTALLER_SCRIPT

# Check if NSIS was successful
if [ $? -eq 0 ]; then
    echo "Installer created successfully!"
else
    echo "NSIS failed to create the installer."
fi

echo "Cleaning up old builds..."
rm -rf build dist main.spec

echo "Packaging the app with PyInstaller..."
pyinstaller --onefile \
            --add-data "assets:assets" \
            --add-data "resources:resources" \
            --add-data "src/data:src/data" \
            --add-data "src/ui:src/ui" \
            --add-data "src/utils:src/utils" \
            --add-binary "Wa_its_venv/lib/python3.11/site-packages/PySide2/Qt/plugins" \
            main.py

# Check if PyInstaller succeeded
if [ $? -ne 0 ]; then
    echo "PyInstaller failed. Exiting."
    exit 1
fi

echo "PyInstaller packaging completed successfully."

echo "Creating Windows installer using Inno Setup..."
# Path to Inno Setup Compiler (adjust if installed elsewhere in Wine)
wine ~/.wine/drive_c/Program\ Files/Inno\ Setup\ 6/ISCC.exe installer_script.iss

# Check if Inno Setup succeeded
if [ $? -ne 0 ]; then
    echo "Inno Setup failed. Exiting."
    exit 1
fi

echo "Windows installer created successfully."
echo "Build complete. Installer is ready in the Output folder."

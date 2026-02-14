[app]

# (str) Title of your application
title = Emoser - Emotion Wellness

# (str) Package name
package.name = emoser

# (str) Package domain (needed for android/ios packaging)
package.domain = org.emoser

# (source.dir) Source code where the main.py live
source.dir = .

# (list) Source include patterns (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,images/*.png

# (list) Source exclude patterns
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Supported orientations
# Valid values: landscape, sensorLandscape, portrait or sensorPortrait
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Supported orientations. Can be one of landscape, sensorLandscape, portrait or sensorPortrait
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
#android.ndk = 21b

# (bool) Use legacy toolchain, set to False to use the new toolchain
android.skip_update = False

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a,armeabi-v7a

# (bool) Enable AndroidX support
android.enable_androidx = True

# (str) Android app icon
# Use 192x192 or higher resolution PNG
android.icon = images/icon-192x192.png

# (str) Android presplash icon
# Optional: presplash shown while app loads
android.presplash = images/icon-192x192.png

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (str) Android app theme, default is ok for Kivy-based app
android.theme = "@android:style/Theme.NoTitleBar"

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) Android Class for the Java entry point
# default is ok. If you changed the name of your main activity class, change
# here too. It should match what you put at the start of your Java activity.
# android.entrypoint = org.renpy.android.PythonActivity

# (list) Pattern matching allowed src dirs and files
#android.gradle_dependencies = 

# (list) Java files for OUYA console
#android.ouya.permissions = OUYA.CONSOLE

# (str) presplash background color (for new android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
#android.presplash_color = #FFFFFF

# (list) Gradle dependencies (for new android toolchain)
# Gradle dependencies can be useful to add java libraries to your APK.
# The format is then depends = shade:androidx.media:media
# Please avoid adding too many dependencies here as adding in too many Gradle
# dependencies will result in very Gradle books time to build as well as the entire
# graduation in the project.
# android.gradle_dependencies = 

# (str) API to use for Kivy bootstrap, default is ok.
#android.bootstrap = sdl2

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (str) Android application meta-data (new toolchain)
#android.meta_data = 

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file for custom backup agent declaration within the manifest
#android.backup_agent = 

# (str) XML file for custom backup agent declaration within the manifest
#android.backup_agent = 

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

#
# Python for android (p4a) specific
#

# (str) python for android API level
#p4a.api = 32

# (str) Release mode (optional), defaults to debug, can be set to release
#p4a.release_mode = release

#
# iOS specific
#

# (bool) Whether or not to sign the code
ios.codesign_allowed = False

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# Display warnings= 1
# display_warnings = 1

# (int) Display deprecation warnings (will be removed in 5.0)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file.
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab) storage
# bin_dir = ./bin

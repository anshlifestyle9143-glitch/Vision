[app]
title = Vision
package.name = vision
package.domain = org.vision
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,requests
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.permissions = INTERNET

[app]
title = Vision
package.name = vision
package.domain = org.vision
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.3.1,requests
android.archs = arm64-v8a
android.accept_sdk_license = True
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
p4a.branch = v2024.01.21

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.permissions = INTERNET

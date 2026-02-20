[app]
title = Gemi Techiz
package.name = gemitechiz
package.domain = org.gemi
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,pandas,openpyxl
orientation = portrait
fullscreen = 0
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.build_tools_version = 33.0.2

[buildozer]
log_level = 2

warn_on_root = 0

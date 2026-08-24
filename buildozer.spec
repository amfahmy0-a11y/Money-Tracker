[app]
title = Money Tracker
package.name = moneytracker
package.domain = org.moneytracker

version = 1.0.0

requirements = python3==3.11.0,kivy==2.3.0,kivymd==2.0.0,matplotlib==3.8.0,Pillow==10.0.0

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

android.api = 33
android.ndk = 25b
android.sdk = 33
android.minapi = 24

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.orientation = portrait
android.allow_backup = True
android.available_languages = ar,en

fullscreen = 0
window.size = (360, 640)

[buildozer]
log_level = 2
warn_on_root = 1

build_dir = ./.buildozer
cache_dir = ./.buildozer/cache

android.ndk_path = 
android.sdk_path = 

android.armeabi_v7a = 1
android.arm64_v8a = 1
android.x86 = 1
android.x86_64 = 1
p4a.branch = develop

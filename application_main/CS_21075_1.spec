# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['CS_21076_1.py'],
    pathex=['E:\Work Space\5th Semester\Artificial Intelligence\hand-written-digit-recognizer\application_main'],
    binaries=[],
    datas=[],
    hiddenimports=['kivy','kivymd','numpy','pandas','os','seaborn','sklearn','pillow','cv2','matplotlib'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CS_21076_1',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

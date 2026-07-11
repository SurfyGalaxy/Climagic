# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
a = Analysis(
    ['__main__.py'],  # Your main script
    pathex=[],
    binaries=[],
    datas=[
        ('config.yaml', '.')
    ],
    hiddenimports=[
        'pre_processor',
        'nltk',
        'yaml',
        'PyQt6'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,           # <-- CRUCIAL: Make sure a.datas is added right here!
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,      # Set to False if you want to hide the terminal window behind the GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
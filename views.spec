# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['views.py'],
    pathex=[],
    binaries=[],
    datas=[('UI', 'UI'), ('IMGS', 'IMGS'), ('SRC', 'SRC')],
    # Otras configuraciones de tu proyecto aquí
    # ...
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='views',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='views',
)

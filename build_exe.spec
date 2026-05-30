# -*- mode: python ; coding: utf-8 -*-
"""
Spec file pour PyInstaller - Création d'un exécutable Fairy Card
"""

a = Analysis(
    ['Fairy_Card.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('Image', 'Image'),
        ('Sound', 'Sound'),
        ('Fonts', 'Fonts'),
        ('settings.json', '.'),
    ],
    hiddenimports=['pygame'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Fairy_Card',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

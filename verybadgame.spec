# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['project/__main__.py'],
    pathex=['project'],
    binaries=[],
    datas=[
        ('project/assets/audio/point.ogg', 'project/assets/audio'),
        ('project/assets/audio/point.wav', 'project/assets/audio'),
        ('project/assets/characters/isaac.png', 'project/assets/characters'),
        ('project/assets/floors/floor_1.png', 'project/assets/floors'),
        ('project/assets/fonts/alpha_num.png', 'project/assets/fonts'),
        ('project/assets/fonts/pixel_num.png', 'project/assets/fonts'),
    ],
    hiddenimports=[
        'project.entities.entity',
        'project.entities.floor',
        'project.entities.player',
        'project.interfaces.interface',
        'project.interfaces.score',
        'project.settings.logging',
        'project.utils.common',
        'project.utils.controls',
        'project.utils.debug',
        'project.utils.game_config',
        'project.utils.images',
        'project.utils.sounds',
        'project.utils.utils',
        'project.utils.window',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='VeryBadGame',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='project/assets/icon.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='VeryBadGame',
)

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import subprocess
prefix = subprocess.run(['brew', '--prefix'], capture_output=True, text=True).stdout.strip()

# Specify paths for required libraries explicitly
pango_path = prefix + '/lib/libpangocairo-1.0.0.dylib'
harfbuzz_path = prefix + '/lib/libharfbuzz.0.dylib'
gtk_lib_path = prefix + '/lib/*.dylib'  # Adjust for other GTK-related libraries
sdl2_lib_path = prefix + '/lib/libSDL2.dylib'  # Path for SDL2 library
sdl2_image_lib_path = prefix + '/lib/libSDL2_image.dylib'  # Path for SDL2_image library

a = Analysis(['tauon.py'],
             binaries=[
                 ('lib/libphazor.so', 'lib/'),
                 (pango_path, '.'),  # Explicitly add libpangocairo
                 (harfbuzz_path, '.'),  # Explicitly add libharfbuzz
                 (gtk_lib_path, '.'),  # Add all other GTK-related dylibs
                 (sdl2_lib_path, '.'),  # Add SDL2 library explicitly
                 (sdl2_image_lib_path, '.'),  # Add SDL2_image library explicitly
                 (prefix + '/Cellar/ffmpeg@5', '.')
             ],
             datas=[('assets', 'assets'), ('theme', 'theme'), ('input.txt', '.')],
             hiddenimports=['sdl2', 'pylast', 'PySDL2'],  # Ensure sdl2 and PySDL2 are included
             hookspath=['extra/pyinstaller-hooks'],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='Tauon Music Box',
          debug=True,  # Enable debug for detailed error output
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='assets/tau-mac.icns')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='TauonMusicBox')

app = BUNDLE(coll,
             name='TauonMusicBox.app',
             icon='assets/tau-mac.icns',
             bundle_identifier=None,
             info_plist={
                'LSEnvironment': {
                    'LANG': 'en_US.UTF-8',
                    'LC_CTYPE': 'en_US.UTF-8',
                    # Set DYLD_LIBRARY_PATH to ensure the app can locate dynamic libraries
                    'DYLD_LIBRARY_PATH': f"{prefix}/lib:{prefix}/opt/sdl2/lib:{prefix}/opt/sdl2_image/lib"
                }
             }
             )

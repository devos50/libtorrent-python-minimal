# -*- mode: python -*-

block_cipher = None

import imp
import os
import sys
import shutil

show_console = True

a = Analysis(['main.py'],
             pathex=['/Users/martijndevos/Documents/tribler'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='libtorrentminimal',
          debug=False,
          strip=False,
          upx=True,
          console=show_console)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='libtorrentminimal')
app = BUNDLE(coll,
             name='libtorrentminimal.app',
             bundle_identifier='nl.tudelft.libtorrentminimal',
             console=show_console)

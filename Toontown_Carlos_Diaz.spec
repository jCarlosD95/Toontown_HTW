# -*- mode: python -*-

block_cipher = None


a = Analysis(['Toontown_Carlos_Diaz.py'],
             pathex=['C:\\Users\\Carlos Diaz\\Desktop\\Carlos_Diaz_Toontown_app'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Toontown_Carlos_Diaz',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='C:\\Users\\Carlos Diaz\\Desktop\\Carlos_Diaz_Toontown_app\\Toon_Icon.ico')

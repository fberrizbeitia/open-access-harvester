# -*- mode: python -*-

block_cipher = None

import gooey

gooey_root = os.path.dirname(gooey.__file__)

gooey_languages = Tree(os.path.join(gooey_root, 'languages'), prefix = 'gooey/languages')

gooey_images = Tree(os.path.join(gooey_root, 'images'), prefix = 'gooey/images')

a = Analysis(['get_open_access_articles_GUI.py'],
             pathex=['C:\\Projects\\CV-Parsing\\bin'],
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
		  gooey_languages, # Add them in to collected files
          gooey_images, # Same here.
          name='CU Open Access Harvester',
          debug=False,
          bootloader_ignore_signals=False,
          strip=None,
          upx=True,
          console=False )
		  

from time import sleep
from re import findall
from os.path import basename
from os import environ
from glob import glob

# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['wrapper.py'],
             pathex=[],
             binaries=[],
             # Fix xsel and xclip not being recognized in shell somehow
             datas = [
                        ('./icon.ico', '.'),
                        ('./baselib.ams', '.'),
                        ('/etc/ssl/certs/ca-bundle.crt', '.'),
                        ('/usr/bin/xclip', '.'),
                        ('/usr/bin/xsel', '.'),
                        ('/usr/lib64/libcrypt-2.21.so', '.'),
                        ('/usr/lib64/libcrypt.so.1', '.'),
                        ('./gui-assets/icons/sm/*', './gui-assets/icons/sm')
                    ],
             hiddenimports=['plyer.platforms.linux.filechooser', 'PIL._tkinter_finder', 'dataclasses'],
             hookspath=hookspath(),
             hooksconfig={},
             runtime_hooks=[],
             excludes=['pandas', 'matplotlib'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)


# Import assets, and only use icons that are needed
png_list = []

with open("./menu.py", 'r') as f:
    script_contents = f.read()
    [png_list.append(x) for x in findall(r"'(.*?)'", script_contents) if '.png' in x and '{' not in x]
    [png_list.append(x) for x in findall(r'"(.*?)"', script_contents) if '.png' in x and '{' not in x]

exclude_list = [basename(file) for file in glob("./gui-assets/icons/*") if (basename(file) not in png_list) and ("big" not in file)]

data_list = list(a.datas)
for item in data_list:
    if "tzdata" in item[0]:
        data_list.remove(item)
a.datas = tuple(data_list)

# Convert modified list back to a tuple
a.datas += Tree('./gui-assets', prefix='gui-assets', excludes=exclude_list)


# Remove binaries
final_list = []
excluded_binaries = [
	'libstdc++.so.6',
	'libgcc_s.so.1',
    'libfreetype.so.6',
    'libfontconfig.so.1',
    'libasound'
	]

for binary in a.binaries:
    remove = False
    for exclude in excluded_binaries:
        if exclude in binary[0]:
            remove = True
            break

    if not remove:
        final_list.append(binary)

a.binaries = TOC(final_list)


splash = Splash(
    './gui-assets/splash.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=None,
    text_size=12,
    minify_script=True,
    always_on_top=True,
    # max_img_size=(287, 65)
)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          splash,
          splash.binaries,
          name='auto-mcs',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=['tcl86t.dll', 'tk86t.dll'],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='icon.ico')

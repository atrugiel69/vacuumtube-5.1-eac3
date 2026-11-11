# VacuumTube 5.1 Surround Sound (E-AC-3) Runtime for LibreELEC

Enables native 5.1 surround sound (Dolby Digital Plus / E-AC-3) playback for the [VacuumTube](https://github.com/shy1132/VacuumTube) YouTube client running on LibreELEC (x86_64).

---

## Background

Stock Chromium and Electron builds on Linux report `false` for `ec-3` Media Source Extensions (MSE) capabilities, causing YouTube to fall back to stereo tracks even when 5.1 surround audio streams (`itag 328`) are present in the manifest. 

This repository provides:
1. Source patches for Chromium and FFmpeg to register E-AC-3 MSE decoders and demuxers in Electron.
2. The LibreELEC Flatpak launcher configuration required to map 6 discrete audio channels through PulseAudio.
3. Pre-built drop-in binaries under Releases to deploy without compiling Electron from source.

---

## Quick Installation (Pre-built Binaries)

### 1. Download & Extract
Download `vacuumtube-5.1-eac3-binaries.tar.gz` from the latest Release and copy it to your LibreELEC machine:

```bash
scp vacuumtube-5.1-eac3-binaries.tar.gz root@<LIBREELEC_IP>:/storage/
```

### 2. Deploy Binaries
SSH into LibreELEC and replace the runtime files inside the VacuumTube Flatpak installation:

```bash
# Locate your installation directory
TARGET="/storage/flatpak/app/rocks.shy.VacuumTube/x86_64/stable/active/files/bin/vacuumtube"

# Extract archive
tar -xzvf /storage/vacuumtube-5.1-eac3-binaries.tar.gz -C /storage/

# Backup stock files and install custom binaries
mv "$TARGET/vacuumtube" "$TARGET/vacuumtube.stock"
mv "$TARGET/libffmpeg.so" "$TARGET/libffmpeg.so.stock"
cp /storage/electron "$TARGET/vacuumtube"
cp /storage/libffmpeg.so "$TARGET/libffmpeg.so"
chmod 755 "$TARGET/vacuumtube" "$TARGET/libffmpeg.so"
```

### 3. Prevent Automatic Overwrites (Mask Flatpak)
Lock the package so background updates do not overwrite your custom binaries:

```bash
/storage/.kodi/addons/tools.flatpak/bin/flatpak mask rocks.shy.VacuumTube
```
*(To unmask in the future, run `/storage/.kodi/addons/tools.flatpak/bin/flatpak mask --remove rocks.shy.VacuumTube`)*

### 4. Configure Kodi Add-on
Update `/storage/.kodi/addons/flatpak.vacuumtube/default.py` to route 6 channels and apply the required Electron launch arguments:

```python
import xbmcaddon
from flatpakhelper.addon import FlatpakAddon

flatpak = FlatpakAddon(addon=xbmcaddon.Addon(), appid="rocks.shy.VacuumTube")
flatpak.start(
    args=[
        '--no-sandbox',
        '--try-supported-channel-layouts',
        '--disable-features=AudioServiceOutOfProcess',
    ],
    pulseaudio_channels=6,
)
```

---

## Building from Source

To compile the runtime manually using the provided patches:

1. Set up an Electron build environment for Linux x64.
2. Apply the Chromium media patch:
   ```bash
   cd src
   git apply /path/to/patches/chromium-eac3.patch
   ```
3. Apply the FFmpeg patch:
   ```bash
   cd src/third_party/ffmpeg
   git apply /path/to/patches/ffmpeg-eac3.patch
   ```
4. Copy `build/args.gn` to `src/out/Release/args.gn`.
5. Compile:
   ```bash
   ninja -C out/Release electron
   ```

---

## Credits & Acknowledgments

* **VacuumTube**: Developed by [shy1132](https://github.com/shy1132/VacuumTube).
* **Thorium Browser**: Media codec enablement patches adapted from [Alex313031/thorium](https://github.com/Alex313031/thorium).
* **LibreELEC**: Developed by [Team LibreELEC](https://libreelec.tv).
* **Electron**: [electron/electron](https://github.com/electron/electron).
* **Chromium & FFmpeg**: Upstream open-source contributors.

## License

The patches and integration scripts in this repository are released under the [GPL-2.0 License](LICENSE) to align with LibreELEC's addon toolchain. Upstream components remain subject to their respective licenses (Chromium BSD-style, Electron MIT, FFmpeg LGPL/GPL).

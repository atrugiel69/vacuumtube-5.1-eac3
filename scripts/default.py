# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present Team LibreELEC (https://libreelec.tv)

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

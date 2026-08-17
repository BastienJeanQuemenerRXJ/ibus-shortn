#!/bin/bash
# Copyright (c) 2026 - Bastien Jean Quemener <shortn@bastien.live>  (github.com/BastienJeanQuemerRXJ/ibus-shortn)
#
# This file is part of ibus-shortn, the IBus Shortn input method engine, forked from ibus-cangjie.
#
# ibus-shortn is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ibus-shortn is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ibus-shortn.  If not, see <http://www.gnu.org/licenses/>.

cd ~/Desktop/'the shortn projct'
sudo rm -rf ibus-shortn/ibus-shortn.deb
cp -r ibus-shortn ibus-shortn-clean
find ibus-shortn-clean -name '.git*' -exec rm -rf {} + 2>/dev/null
find ibus-shortn-clean -name '*.deb' -delete
find ibus-shortn-clean -name '*.swp' -delete
find ibus-shortn-clean -name '*.sh' -delete
find ibus-shortn-clean -name '*.mp4' -delete
find ibus-shortn-clean -name '*~' -delete
find ibus-shortn-clean -type f ! -path './DEBIAN/*' -exec md5sum {} \; > ibus-shortn-clean/DEBIAN/md5sums
dpkg-deb --root-owner-group --build ibus-shortn-clean
sudo dpkg -i --force-overwrite ibus-shortn-clean.deb
sudo mv ibus-shortn-clean.deb ~/Desktop/'the shortn projct'/ibus-shortn/ibus-shortn.deb
rm -rf ibus-shortn-clean
ibus restart
cd

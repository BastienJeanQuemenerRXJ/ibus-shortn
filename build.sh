#!/bin/bash
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

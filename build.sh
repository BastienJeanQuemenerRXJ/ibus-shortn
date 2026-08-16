#!/bin/bash
cd ~/Desktop/'the shortn projct'

# Create a temporary copy
rm -rf ibus-shortn-clean
cp -r ibus-shortn ibus-shortn-clean

# Remove .git and .deb files from the copy
find ibus-shortn-clean -name '.git*' -exec rm -rf {} + 2>/dev/null
find ibus-shortn-clean -name '*.deb' -delete
find ibus-shortn-clean -name '*.swp' -delete
find ibus-shortn-clean -name '*~' -delete

# Generate md5sums (excluding DEBIAN)
find ibus-shortn-clean -type f ! -path './DEBIAN/*' -exec md5sum {} \; > ibus-shortn-clean/DEBIAN/md5sums

# Build the package
dpkg-deb --root-owner-group --build ibus-shortn-clean

# Move and install
sudo mv ibus-shortn-clean.deb /home/bastien/ibus-shortn.deb
sudo dpkg -i --force-overwrite /home/bastien/ibus-shortn.deb

# Cleanup
rm -rf ibus-shortn-clean

ibus restart
cd
sudo mv /home/bastien/ibus-shortn.deb Desktop/'the shortn projct'/ibus-shortn

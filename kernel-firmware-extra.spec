#
# This rpm is based on the git tree from:
# git://git.kernel.org/pub/scm/linux/kernel/git/dwmw2/linux-firmware.git
# version is date of the younger commit
#

Summary:	Extra linux kernel firmware files
Name:   	kernel-firmware-extra
Version:	20130218
Release:	1
License:	Proprietary
Group:  	System/Kernel and hardware
URL:    	https://www.kernel.org/
# kernel-firmware tarball is generated from the git tree mentioned
# above, by simply cloning it and doing:
# tar --exclude-vcs -Jcf kernel-firmware-extra-version.tar.xz linux-firmware
Source: 	kernel-firmware-extra-%{version}.tar.xz
BuildRequires:	kernel-firmware >= 20120218
Conflicts:	kernel-firmware < 20120218
BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildArch:	noarch

%description
This package contains extra redistributable etc. firmwares for in-kernel
drivers. It is shared for all kernels.

%prep
%setup -q -n linux-firmware

# don't include firmware already in kernel-firmware package
for fir in `rpm -ql kernel-firmware | grep '^/lib/firmware/' | \
            sed 's|^/lib/firmware/||'`; do
	[ -f "$fir" ] || continue
	rm -f "$fir"
done
for dir in `find . -type d | sed -e 's|^\.||' -e 's|^/||'`; do
	rmdir -p --ignore-fail-on-non-empty $dir
done

# remove files provided in iwlwifi-*-ucode* packages
rm -f LICENCE.iwlwifi_firmware
rm -f iwlwifi-{100-5,1000-{3,5},{3945,4965,5150}-2,5000-{1,2,5},6000-4,6000g2{a,b}-5,6050-{4,5}}.ucode

# remove all radeon files as they are provided by kernel-firmware and radeon-firmware
rm -f LICENCE.radeon_rlc
rm -rf radeon

# remove files provided in rt*-firmware packages
rm -f LICENSE.ralink-firmware.txt
rm -f rt2561{,s}.bin rt2661.bin rt28{6,7}0.bin rt3070.bin rt3090.bin rt73.bin

# remove unwanted source files
rm -f dsp56k/bootstrap.asm keyspan_pda/*.S
# FIXME: usbdux*.bin firmware should be in kernel-firmware or another
# separate package (not in non-free), usbdux*.bin is GPL licensed
rm -rf usbdux

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/lib/firmware
cp -avf * %{buildroot}/lib/firmware
rm -f %{buildroot}/lib/firmware/LICENCE.*

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
/lib/firmware/*

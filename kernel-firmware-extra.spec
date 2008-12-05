#
# This rpm is based on the git tree from:
# git.kernel.org/pub/scm/linux/kernel/git/dwmw2/linux-firmware.git
# version is date of the younger commit
#

Summary:	Extra linux kernel firmware files
Name:   	kernel-firmware-extra
Version:	20081112
Release:	%manbo_mkrel 2
License:	Proprietary
Group:  	System/Kernel and hardware
URL:    	http://www.kernel.org/
# kernel-firmware tarball is generated from the git tree mentioned above, 
# by simply cloning it, doing a rm -rf linux-firmware/.git/ 
# and tar -cjvf kernel-firmware-extra-version.tar.bz2 linux-firmware
Source0: 	kernel-firmware-extra-%{version}.tar.bz2
BuildRequires:	kernel-firmware >= 20080922-2mnb2
Conflicts:	kernel-firmware < 20080922-2mnb2
Obsoletes:	korg1212-firmware
Obsoletes:	maestro3-firmware
Obsoletes:	sb16-firmware
Obsoletes:	yamaha-firmware
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

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/lib/firmware
cp -avf * %{buildroot}/lib/firmware
rm -f %{buildroot}/lib/firmware/LICENCE.*

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc LICENCE.*
/lib/firmware/*

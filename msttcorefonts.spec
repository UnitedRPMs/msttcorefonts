%global debug_package %{nil}
%define name msttcorefonts
%global _sfpath http://downloads.sourceforge.net/corefonts

# nowdays most (all?) distributions seems to use this. Oh the joys of the FHS
%define ttmkfdir /usr/bin/ttmkfdir

%define fontdir /usr/share/fonts/%{name}

Summary: TrueType core fonts for the web
Name: msttcorefonts
Version: 2.5
Release: 5%{?dist}
License: Spec file is GPL, binary rpm is gratis but non-distributable
Group: User Interface/X
BuildArch: noarch
BuildRoot: /var/tmp/%{name}-root
BuildRequires: wget
BuildRequires: cabextract
BuildRequires: %{ttmkfdir}

%description
The TrueType core fonts for the web that was once available from
http://www.microsoft.com/typography/fontpack/. The src rpm is cleverly
constructed so that the actual fonts are downloaded from Sourceforge's site
at build time. Therefore this package technically does not 'redistribute'
the fonts, it just makes it easy to install them on a linux system.

%prep
mkdir -p %{name}/downloads
cd %{name}/downloads

echo '%{_sfpath}/andale32.exe
%{_sfpath}/arial32.exe
%{_sfpath}/arialb32.exe
%{_sfpath}/comic32.exe
%{_sfpath}/courie32.exe
%{_sfpath}/georgi32.exe
%{_sfpath}/impact32.exe
%{_sfpath}/times32.exe
%{_sfpath}/trebuc32.exe
%{_sfpath}/webdin32.exe
%{_sfpath}/verdan32.exe
%{_sfpath}/wd97vwr32.exe' > fontlist

wget -i  fontlist

%build

font_files="andale32.exe arial32.exe arialb32.exe comic32.exe courie32.exe georgi32.exe impact32.exe times32.exe trebuc32.exe webdin32.exe verdan32.exe"

cd %{name}

rm -rf cab-contents fonts

mkdir cab-contents
mkdir fonts

for i in $font_files
do
	if [ -f downloads/$i ]
	then
		cabextract --lowercase --directory=cab-contents downloads/$i
	fi
	cp cab-contents/*.ttf fonts
	rm -f cab-contents/*
done

cabextract --lowercase --directory=cab-contents downloads/wd97vwr32.exe
cabextract --lowercase --directory=cab-contents cab-contents/viewer1.cab
cp cab-contents/*.ttf fonts

cd fonts

%{ttmkfdir} > fonts.dir

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
cd %{name}/fonts
mkdir -p $RPM_BUILD_ROOT/%{fontdir}
cp *.ttf fonts.dir $RPM_BUILD_ROOT/%{fontdir}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post
if [ -x /usr/sbin/chkfontpath -a $1 -eq 1 ]; then
	/usr/sbin/chkfontpath --add %{fontdir}
fi
# something has probably changed, update the font-config cache
if [ -x /usr/bin/fc-cache ]; then
	/usr/bin/fc-cache
fi

%preun
if [ -x /usr/sbin/chkfontpath -a $1 -eq 0 ]; then
	/usr/sbin/chkfontpath --remove %{fontdir}
fi

%files
%attr(-,root,root) 
%{fontdir}/

%changelog

* Fri Sep 01 2017 <Anonymous friend> 2.5-5
- Changes in fonts urls

* Wed Jul 05 2017 <Anonymous friend> 2.5-4
- Rebuilt

* Mon Apr 04 2016 <Anonymous friend> 2.5-3
- Rebuilt 

* Fri Oct 02 2015 Anonymous friend
- Rebuilt

* Sun Sep 09 2012 Noa Resare <noa@resare.com> 2.5-1
- Various updates from Deven T. Corzine, mirrors etc

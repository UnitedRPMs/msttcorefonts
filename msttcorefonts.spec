# This is the msttcorefonts spec file as distributed from
# http://corefonts.sourceforge.net/. 

%global debug_package %{nil}
%define name msttcorefonts

# nowdays most (all?) distributions seems to use this. Oh the joys of the FHS
%define ttmkfdir /usr/bin/ttmkfdir

%define fontdir /usr/share/fonts/%{name}

Summary: TrueType core fonts for the web
Name: msttcorefonts
Version: 2.5
Release: 4%{?dist}
License: Spec file is GPL, binary rpm is gratis but non-distributable
Group: User Interface/X
BuildArch: noarch
BuildRoot: /var/tmp/%{name}-root
BuildRequires: %{ttmkfdir}
BuildRequires: wget
BuildRequires: cabextract

%description
The TrueType core fonts for the web that was once available from
http://www.microsoft.com/typography/fontpack/. The src rpm is cleverly
constructed so that the actual fonts are downloaded from Sourceforge's site
at build time. Therefore this package technically does not 'redistribute'
the fonts, it just makes it easy to install them on a linux system.

%prep
mkdir -p %{name}/downloads
cd %{name}/downloads

# this is the sourceforge mirrorlist as of 2012-09-06. If someone spots changes
# over at sourceforge, feel free to email me and I'll update the list
mirrors="cdnetworks-kr-1+citylan+dfn+freefr+garr+heanet+hivelocity+ignum+internode+iweb+jaist+nchc+netcologne+space+superb-dca2+superb-dca3+superb-sea2+switch+tenet+ufpr+waix+aarnet"
mirror_count=23

andale32_md5="cbdc2fdd7d2ed0832795e86a8b9ee19a  andale32.exe"
arial32_md5="9637df0e91703179f0723ec095a36cb5  arial32.exe"
arialb32_md5="c9089ae0c3b3d0d8c4b0a95979bb9ff0  arialb32.exe"
comic32_md5="2b30de40bb5e803a0452c7715fc835d1  comic32.exe"
courie32_md5="4e412c772294403ab62fb2d247d85c60  courie32.exe"
georgi32_md5="4d90016026e2da447593b41a8d8fa8bd  georgi32.exe"
impact32_md5="7907c7dd6684e9bade91cff82683d9d7  impact32.exe"
times32_md5="ed39c8ef91b9fb80f76f702568291bd5  times32.exe"
trebuc32_md5="0d7ea16cac6261f8513a061fbfcdb2b5  trebuc32.exe"
webdin32_md5="230a1d13a365b22815f502eb24d9149b  webdin32.exe"
verdan32_md5="12d2a75f8156e10607be1eaa8e8ef120  verdan32.exe"
wd97vwr32_md5="efa72d3ed0120a07326ce02f051e9b42  wd97vwr32.exe"

download_files="andale32.exe arial32.exe arialb32.exe comic32.exe courie32.exe georgi32.exe impact32.exe times32.exe trebuc32.exe webdin32.exe verdan32.exe wd97vwr32.exe"


failures=0

function set_mirror {
        local r m
        r=`expr $RANDOM % $mirror_count + 1`
        m=`echo $mirrors |cut -d+ -f$r`
        mirror="http://${m}.dl.sourceforge.net/project/corefonts/the%20fonts/final/"
}

function check_file {
        matches=
        if [ ! -r $1 ]
        then
                echo "$1 does not exist"
                return
        fi
        local variable_name=`basename $1 .exe`_md5
        local stored_checksum
        eval stored_checksum=\$$variable_name
        local computed_checksum=`md5sum $1`
        if [ "$stored_checksum" = "$computed_checksum" ]
        then
                matches=yes
        else
                rm $1
                matches=
        fi
}

function download {
        wget -c -O "$2" $1$2
}

set_mirror
for f in $download_files
do
        check_file $f
        while [ ! $matches ]
        do
                download $mirror $f
                check_file $f
                if [ ! $matches ]
                then
                        echo "failed to download $mirror$f"
                        failures=`expr $failures + 1`
                        if [ $failures -gt 5 ]
                        then
                                echo "failed to download too many times."
                                exit
                        fi
                        set_mirror
                fi
        done
done


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
%attr(-,root,root) %{fontdir}
%dir %{fontdir}

%changelog

* Wed Jul 05 2017 <Anonymous friend> 2.5-4
- Rebuilt

* Mon Apr 04 2016 <Anonymous friend> 2.5-3
- Rebuilt 

* Fri Oct 02 2015 Anonymous friend
- Rebuilt

* Sun Sep 09 2012 Noa Resare <noa@resare.com> 2.5-1
- Various updates from Deven T. Corzine, mirrors etc

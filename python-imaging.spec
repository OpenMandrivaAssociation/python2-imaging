%define pyver %(python -V 2>&1 | cut -f2 -d" " | cut -f1,2 -d".")

Summary:	Python's own image processing library 
Name:		python-imaging
Version: 	1.1.4
Release: 	%mkrel 11
License:	MIT style
Group:		Development/Python
URL:		http://www.pythonware.com/products/pil/

Source0:	http://www.pythonware.com/downloads/Imaging-%{version}.tar.bz2 
Source1:	pil-handbook.pdf.bz2
Patch:		Imaging-1.1.4.patch
Patch1:		python-imaging-1.1.4-freetype2.patch
Icon:		linux-python-paint-icon.gif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	python >= 1.5, libjpeg >= 6b,  zlib >= 1.1.2, libpng >= 1.0.1 tix, tkinter
BuildRequires:	python-devel >= 1.5, jpeg-devel >= 6b, png-devel >= 1.0.1
BuildRequires:	tix tix-devel XFree86-devel freetype2-devel tkinter tcl tcl-devel tk tk-devel

%description
Python Imaging Library version %{version}
   
The Python Imaging Library (PIL) adds image processing capabilities 
to your Python interpreter.

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

%package devel
Summary:	Header files for python-imaging
Group:		Development/C
Requires:	python-imaging = %{version}

%description devel
Header files for the Python Imaging Library version %{version}.

%prep
%setup -q -n Imaging-%{version}
bzcat %SOURCE1 > pil-handbook.pdf

# fix tk version
perl -p -i -e 's/8.3/8.4/g' Setup.in

# fix distutils problem
%patch
%patch1 -p1
# Make sure to get the right python library
perl -pi -e "s,(\\\$\((exec_prefix|prefix|exec_installdir)\)|/usr/X11R6)/lib\b,\1/%{_lib},g" Makefile.pre.in Setup.in

# Nuke references to /usr/local
perl -pi -e "s,(-[IL]/usr/local/(include|lib)),,g" Setup.in


%build
cd libImaging
%configure2_5x
%make OPT="$RPM_OPT_FLAGS -fPIC"
cd ..
python setup.py build

%install
rm -fr $RPM_BUILD_ROOT

find . -type f | xargs perl -pi -e 's@/usr/local/bin/python@/usr/bin/python@'

python setup.py install --root=$RPM_BUILD_ROOT
cd libImaging
mkdir -p  $RPM_BUILD_ROOT%{_includedir}/python%{pyver}/
install -m 644 ImPlatform.h Imaging.h ImConfig.h $RPM_BUILD_ROOT%{_includedir}/python%{pyver}/
%multiarch_includes $RPM_BUILD_ROOT%{_includedir}/python%{pyver}/ImConfig.h

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-,root,root)
%doc pil-handbook.pdf Scripts Images Sane CHANGES* README
%py_platsitedir/*

%files devel
%defattr (-,root,root)
%{_includedir}/python%{pyver}/Imaging.h
%{_includedir}/python%{pyver}/ImPlatform.h
%{_includedir}/python%{pyver}/ImConfig.h
%multiarch %multiarch_includedir/python%{pyver}/ImConfig.h



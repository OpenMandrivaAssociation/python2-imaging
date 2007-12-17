%define pyver %(python -V 2>&1 | cut -f2 -d" " | cut -f1,2 -d".")
%define name python-imaging
%define version 1.1.6
%define release %mkrel 2

Summary:	Python's own image processing library 
Name:		%{name}
Version: 	%{version}
Release: 	%{release}
License:	MIT style
Group:		Development/Python
URL:		http://www.pythonware.com/products/pil/

Source0:	http://www.pythonware.com/downloads/Imaging-%{version}.tar.bz2 
Source1:	pil-handbook.pdf.bz2
Source2:	linux-python-paint-icon.gif
Requires:	python >= 1.5, libjpeg >= 6b,  zlib >= 1.1.2, libpng >= 1.0.1, tkinter
BuildRequires:	python-devel >= 1.5, jpeg-devel >= 6b, png-devel >= 1.0.1
BuildRequires:	X11-devel freetype2-devel tkinter tcl tcl-devel tk tk-devel >= 8.5

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
# perl -p -i -e 's/8.3/8.4/g' Setup.in

# fix distutils problem
# %patch
# Make sure to get the right python library
# perl -pi -e "s,(\\\$\((exec_prefix|prefix|exec_installdir)\)|/usr/X11R6)/lib\b,\1/%{_lib},g" Makefile.pre.in Setup.in

# Nuke references to /usr/local
perl -pi -e "s,(-[IL]/usr/local/(include|lib)),,g" setup.py


%build
python setup.py build_ext -i

%install
rm -fr $RPM_BUILD_ROOT

find . -type f | xargs perl -pi -e 's@/usr/local/bin/python@/usr/bin/python@'

python setup.py install --root=$RPM_BUILD_ROOT
cd libImaging
mkdir -p  $RPM_BUILD_ROOT%{_includedir}/python%{pyver}/
install -m 644 ImPlatform.h Imaging.h $RPM_BUILD_ROOT%{_includedir}/python%{pyver}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-,root,root)
%doc pil-handbook.pdf Scripts Images Sane CHANGES* README
%{_bindir}/pil*.py
%py_platsitedir/PIL.pth
%dir %py_platsitedir/PIL
%py_platsitedir/PIL/*.egg-info
%py_platsitedir/PIL/*.py*
%py_platsitedir/PIL/_imaging.so
%py_platsitedir/PIL/_imagingft.so
%py_platsitedir/PIL/_imagingmath.so
%py_platsitedir/PIL/_imagingtk.so

%files devel
%defattr (-,root,root)
%{_includedir}/python%{pyver}/Imaging.h
%{_includedir}/python%{pyver}/ImPlatform.h


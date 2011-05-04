Summary:	Python's own image processing library 
Name:		python-imaging
Version: 	1.1.7
Release: 	%mkrel 5
License:	MIT
Group:		Development/Python
URL:		http://www.pythonware.com/products/pil/
Source0:	http://effbot.org/downloads/Imaging-%{version}.tar.gz
Source1:	pil-handbook.pdf.bz2
Source2:	linux-python-paint-icon.gif
Patch0:		Imaging-1.1.7-link.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Buildrequires:	python-devel
BuildRequires:	jpeg-devel
BuildRequires:	png-devel
BuildRequires:	freetype2-devel
BuildRequires:	lcms-devel
BuildRequires:	libsane-devel
Buildrequires:	tcl-devel
BuildRequires:	tk-devel
Buildrequires:	zlib-devel
BuildRequires:	tkinter

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
%patch0 -p0
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
cd Sane
python setup.py build_ext -i

%install
rm -fr %{buildroot}

find . -type f | xargs perl -pi -e 's@/usr/local/bin/python@/usr/bin/python@'

python setup.py install --root=%{buildroot}
cd libImaging
mkdir -p  %{buildroot}%{_includedir}/python%{pyver}/
install -m 644 ImPlatform.h Imaging.h %{buildroot}%{_includedir}/python%{pyver}/
cd ..

cd Sane
python setup.py install --root=%{buildroot}
cd ..

%clean
rm -rf %{buildroot}

%files
%defattr (-,root,root)
%doc pil-handbook.pdf Scripts Images CHANGES* README
%{_bindir}/pil*.py
%py_platsitedir/PIL.pth
%dir %py_platsitedir/PIL
%py_platsitedir/PIL/*.egg-info
%py_platsitedir/PIL/*.py*
%py_platsitedir/PIL/_imaging.so
%py_platsitedir/PIL/_imagingcms.so
%py_platsitedir/PIL/_imagingft.so
%py_platsitedir/PIL/_imagingmath.so
%py_platsitedir/PIL/_imagingtk.so
%py_platsitedir/_sane.so
%py_platsitedir/*.egg-info
%py_platsitedir/sane.py*
%files devel
%defattr (-,root,root)
%{_includedir}/python%{pyver}/Imaging.h
%{_includedir}/python%{pyver}/ImPlatform.h


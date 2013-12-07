Summary:	Python's own image processing library 
Name:		python-imaging
Version:	1.1.7
Release:	14
License:	MIT
Group:		Development/Python
Url:		http://www.pythonware.com/products/pil/
Source0:	http://effbot.org/downloads/Imaging-%{version}.tar.gz
Source1:	pil-handbook.pdf.bz2
Source2:	linux-python-paint-icon.gif
Patch0:		Imaging-1.1.7-link.patch
BuildRequires:	python-pkg-resources
BuildRequires:	tkinter
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(lcms)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(sane-backends)
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
BuildRequires:	pkgconfig(zlib)

%description
Python Imaging Library version %{version}
   
The Python Imaging Library (PIL) adds image processing capabilities 
to your Python interpreter.

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

%package devel
Summary:	Header files for python-imaging
Group:		Development/C
Requires:	python-imaging = %{version}-%{release}

%description devel
Header files for the Python Imaging Library version %{version}.

%prep
%setup -qn Imaging-%{version}
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
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" python setup.py build_ext -i
cd Sane
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" python setup.py build_ext -i

%install
find . -type f | xargs perl -pi -e 's@/usr/local/bin/python@/usr/bin/python@'

python setup.py install --root=%{buildroot}

cd libImaging
mkdir -p  %{buildroot}%{_includedir}/python%{py_ver}/
install -m 644 ImPlatform.h Imaging.h %{buildroot}%{_includedir}/python%{py_ver}/
cd ..

cd Sane
python setup.py install --root=%{buildroot}
cd ..

%files
%doc pil-handbook.pdf Scripts Images CHANGES* README
%{_bindir}/pil*.py
%{py_platsitedir}/PIL.pth
%dir %{py_platsitedir}/PIL
%{py_platsitedir}/PIL/*.egg-info
%{py_platsitedir}/PIL/*.py*
%{py_platsitedir}/PIL/_imaging.so
%{py_platsitedir}/PIL/_imagingcms.so
%{py_platsitedir}/PIL/_imagingft.so
%{py_platsitedir}/PIL/_imagingmath.so
%{py_platsitedir}/PIL/_imagingtk.so
%{py_platsitedir}/_sane.so
%{py_platsitedir}/*.egg-info
%{py_platsitedir}/sane.py*

%files devel
%{_includedir}/python%{py_ver}/Imaging.h
%{_includedir}/python%{py_ver}/ImPlatform.h


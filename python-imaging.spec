Summary:	Python's own image processing library 
Name:		python2-imaging
Version:	2.8.1
Release:	4
License:	MIT
Group:		Development/Python
# Original:
#Url:		http://www.pythonware.com/products/pil/
#Source0:	http://effbot.org/downloads/Imaging-%{version}.tar.gz
# Much better maintained fork:
Url:		https://pypi.python.org/pypi/Pillow/2.8.1
Source0:	https://pypi.python.org/packages/source/P/Pillow/Pillow-%{version}.tar.gz
Source1:	pil-handbook.pdf.bz2
Source2:	linux-python-paint-icon.gif
Patch0:		Pillow-2.5.1-link.patch

BuildRequires:	python2-pkg-resources
BuildRequires:	python2-setuptools
BuildRequires:	tkinter
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	python2-devel
BuildRequires:	pkgconfig(sane-backends)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
BuildRequires:	pkgconfig(zlib)

Provides:       pithon2-pillow = %{EVRD}

%description
Python Imaging Library version %{version}

The Python Imaging Library (PIL) adds image processing capabilities 
to your Python interpreter.

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

%package devel
Summary:	Header files for python-imaging
Group:		Development/C
Requires:	python2-imaging = %{EVRD}
Provides:	python2-pillow-devel = %{EVRD}

%description devel
Header files for the Python Imaging Library version %{version}.

%prep
%setup -qn Pillow-%{version}
%apply_patches
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
CFLAGS="%{optflags} -fno-strict-aliasing" %__python2 setup.py build build_ext -i

%install
find . -type f | xargs perl -pi -e 's@/usr/local/bin/python@/usr/bin/python@'

PYTHONDONTWRITEBYTECODE=True %__python2 setup.py install --root=%{buildroot}

cd libImaging
mkdir -p  %{buildroot}%{_includedir}/python%{py_ver}/
install -m 644 ImPlatform.h Imaging.h %{buildroot}%{_includedir}/python%{py_ver}/
cd ..

# The scripts are packaged in %%doc
rm -rf %{buildroot}%{_bindir}

%files
%doc pil-handbook.pdf Scripts CHANGES*
%dir %{py2_platsitedir}/PIL
%{py2_platsitedir}/PIL/*.py*
%{py2_platsitedir}/PIL/_imaging*.so
%{py2_platsitedir}/PIL/_webp*.so
%{py2_platsitedir}/PIL/*.md
%{py2_platsitedir}/*.egg-info

%files devel
%{_includedir}/python%{py_ver}/Imaging.h
%{_includedir}/python%{py_ver}/ImPlatform.h


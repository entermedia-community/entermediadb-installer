%global VERSION  7.0.6
%global Patchlevel  1

Name:           ImageMagick
Version:        %{VERSION}
Release:        %{Patchlevel}
Summary:        Use ImageMagick to convert, edit, or compose bitmap images in a variety of formats.  In addition resize, rotate, shear, distort and transform images.
Group:          Applications/Multimedia
License:        http://www.imagemagick.org/script/license.php
Url:            http://www.imagemagick.org/
Source0:        http://www.imagemagick.org/download/%{name}/%{name}-%{VERSION}-%{Patchlevel}.tar.gz

Patch1:		useciecolor-delegates.patch
Patch2:		policy-security.patch

Requires:       %{name}-libs = %{version}-%{release}

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  bzip2-devel, freetype-devel, libjpeg-devel, libpng-devel
BuildRequires:  libtiff-devel, giflib-devel, zlib-devel, perl-devel >= 5.8.1
BuildRequires:  ghostscript-devel, djvulibre-devel
BuildRequires:  libwmf-devel, jasper-devel, libtool-ltdl-devel
BuildRequires:  libX11-devel, libXext-devel, libXt-devel
BuildRequires:  lcms2-devel, libxml2-devel, librsvg2-devel, OpenEXR-devel
BuildRequires:  fftw-devel, OpenEXR-devel, libwebp-devel

%description
ImageMagick is a software suite to create, edit, and compose bitmap images. It
can read, convert and write images in a variety of formats (about 100)
including DPX, GIF, JPEG, JPEG-2000, PDF, PhotoCD, PNG, Postscript, SVG,
and TIFF. Use ImageMagick to translate, flip, mirror, rotate, scale, shear
and transform images, adjust image colors, apply various special effects,
or draw text, lines, polygons, ellipses and B�zier curves.

The functionality of ImageMagick is typically utilized from the command line
or you can use the features from programs written in your favorite programming
language. Choose from these interfaces: G2F (Ada), MagickCore (C), MagickWand
(C), ChMagick (Ch), Magick++ (C++), JMagick (Java), L-Magick (Lisp), nMagick
(Neko/haXe), PascalMagick (Pascal), PerlMagick (Perl), MagickWand for PHP
(PHP), PythonMagick (Python), RMagick (Ruby), or TclMagick (Tcl/TK). With a
language interface, use ImageMagick to modify or create images automagically
and dynamically.

ImageMagick is free software delivered as a ready-to-run binary distribution
or as source code that you may freely use, copy, modify, and distribute in
both open and proprietary applications. It is distributed under an Apache
2.0-style license, approved by the OSI.

The ImageMagick development process ensures a stable API and ABI. Before
each ImageMagick release, we perform a comprehensive security assessment that
includes memory and thread error detection to help prevent exploits.ImageMagick
is free software delivered as a ready-to-run binary distribution or as source
code that you may freely use, copy, modify, and distribute in both open and
proprietary applications. It is distributed under an Apache 2.0-style license,
approved by the OSI.


%package devel
Summary: Library links and header files for ImageMagick application development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libX11-devel, libXext-devel, libXt-devel, ghostscript-devel
Requires: bzip2-devel, freetype-devel, libtiff-devel, libjpeg-devel, lcms2-devel
Requires: libwebp-devel, OpenEXR-devel, jasper-devel, pkgconfig
Requires: %{name}-libs = %{version}-%{release}

%description devel
ImageMagick-devel contains the library links and header files you'll
need to develop ImageMagick applications. ImageMagick is an image
manipulation program.

If you want to create applications that will use ImageMagick code or
APIs, you need to install ImageMagick-devel as well as ImageMagick.
You do not need to install it if you just want to use ImageMagick,
however.

%package libs
Summary: ImageMagick libraries to link with
Group: Applications/Multimedia

%description libs
This packages contains a shared libraries to use within other applications.


%package djvu
Summary: DjVu plugin for ImageMagick
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}

%description djvu
This packages contains a plugin for ImageMagick which makes it possible to
save and load DjvU files from ImageMagick and libMagickCore using applications.


%package doc
Summary: ImageMagick HTML documentation
Group: Documentation


%description doc
ImageMagick documentation, this package contains usage (for the
commandline tools) and API (for the libraries) documentation in HTML format.
Note this documentation can also be found on the ImageMagick website:
http://www.imagemagick.org/.


%package perl
Summary: ImageMagick perl bindings
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description perl
Perl bindings to ImageMagick.

Install ImageMagick-perl if you want to use any perl scripts that use
ImageMagick.


%package c++
Summary: ImageMagick Magick++ library (C++ bindings)
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description c++
This package contains the Magick++ library, a C++ binding to the ImageMagick
graphics manipulation library.

Install ImageMagick-c++ if you want to use any applications that use Magick++.


%package c++-devel
Summary: C++ bindings for the ImageMagick library
Group: Development/Libraries
Requires: %{name}-c++ = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description c++-devel
ImageMagick-devel contains the static libraries and header files you'll
need to develop ImageMagick applications using the Magick++ C++ bindings.
ImageMagick is an image manipulation program.

If you want to create applications that will use Magick++ code
or APIs, you'll need to install ImageMagick-c++-devel, ImageMagick-devel and
ImageMagick.

You don't need to install it if you just want to use ImageMagick, or if you
want to develop/compile applications using the ImageMagick C interface,
however.


%prep
%setup -q -n %{name}-%{VERSION}-%{Patchlevel}
sed -i 's/libltdl.la/libltdl.so/g' configure
iconv -f ISO-8859-1 -t UTF-8 README.txt > README.txt.tmp
touch -r README.txt README.txt.tmp
mv README.txt.tmp README.txt
# for %%doc
mkdir Magick++/examples
cp -p Magick++/demo/*.cpp Magick++/demo/*.miff Magick++/examples

%build
%configure --enable-shared \
        --disable-static \
        --with-modules \
        --with-perl \
        --with-x \
        --with-threads \
        --with-magick_plus_plus \
        --with-gslib \
        --with-wmf \
        --with-lcms2 \
        --with-webp \
        --with-openexr \
        --with-rsvg \
        --with-xml \
        --with-perl-options="INSTALLDIRS=vendor %{?perl_prefix} CC='%__cc -L$PWD/magick/.libs' LDDLFLAGS='-shared -L$PWD/magick/.libs'" \
        --without-dps

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Do *NOT* use %%{?_smp_mflags}, this causes PerlMagick to be silently misbuild
make


%install
rm -rf %{buildroot}

make %{?_smp_mflags} install DESTDIR=%{buildroot} INSTALL="install -p"
cp -a www/source %{buildroot}%{_datadir}/doc/%{name}-%{VERSION}
rm %{buildroot}%{_libdir}/*.la

# fix weird perl Magick.so permissions
chmod 755 %{buildroot}%{perl_vendorarch}/auto/Image/Magick/*/*.so

# perlmagick: fix perl path of demo files
%{__perl} -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)' PerlMagick/demo/*.pl

# perlmagick: cleanup various perl tempfiles from the build which get installed
find %{buildroot} -name "*.bs" |xargs rm -f
find %{buildroot} -name ".packlist" |xargs rm -f
find %{buildroot} -name "perllocal.pod" |xargs rm -f

# perlmagick: build files list
echo "%defattr(-,root,root,-)" > perl-pkg-files
find %{buildroot}/%{_libdir}/perl* -type f -print \
        | sed "s@^%{buildroot}@@g" > perl-pkg-files 
find %{buildroot}%{perl_vendorarch} -type d -print \
        | sed "s@^%{buildroot}@%dir @g" \
        | grep -v '^%dir %{perl_vendorarch}$' \
        | grep -v '/auto$' >> perl-pkg-files 
if [ -z perl-pkg-files ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit -1
fi

%check
export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}
make %{?_smp_mflags} check

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig

%post c++ -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%postun c++ -p /sbin/ldconfig


%files
%doc README.txt LICENSE NOTICE AUTHORS.txt NEWS.txt ChangeLog Platforms.txt
%{_bindir}/[a-z]*
%{_mandir}/man[145]/[a-z]*
%{_mandir}/man1/%{name}.*

%files libs
%defattr(-,root,root,-)
%doc LICENSE NOTICE AUTHORS.txt QuickStart.txt
%{_libdir}/libMagickCore-6.Q16.so*
%{_libdir}/libMagickWand-6.Q16.so*
%{_libdir}/%{name}-%{VERSION}
%{_datadir}/%{name}-6
%exclude %{_libdir}/%{name}-%{VERSION}/modules-Q16/coders/djvu.*
%{_sysconfdir}/%{name}-6

%files devel
%defattr(-,root,root,-)
%{_bindir}/MagickCore-config
%{_bindir}/Magick-config
%{_bindir}/MagickWand-config
%{_bindir}/Wand-config
%{_libdir}/libMagickCore-6.Q16.so
%{_libdir}/libMagickWand-6.Q16.so
%{_libdir}/pkgconfig/MagickCore.pc
%{_libdir}/pkgconfig/MagickCore-6.Q16.pc
%{_libdir}/pkgconfig/ImageMagick.pc
%{_libdir}/pkgconfig/ImageMagick-6.Q16.pc
%{_libdir}/pkgconfig/MagickWand.pc
%{_libdir}/pkgconfig/MagickWand-6.Q16.pc
%{_libdir}/pkgconfig/Wand.pc
%{_libdir}/pkgconfig/Wand-6.Q16.pc
%dir %{_includedir}/%{name}-6
%{_includedir}/%{name}-6/magick
%{_includedir}/%{name}-6/wand
%{_mandir}/man1/Magick-config.*
%{_mandir}/man1/MagickCore-config.*
%{_mandir}/man1/Wand-config.*
%{_mandir}/man1/MagickWand-config.*

%files djvu
%defattr(-,root,root,-)
%{_libdir}/%{name}-%{VERSION}/modules-Q16/coders/djvu.*

%files doc
%defattr(-,root,root,-)
%doc %{_datadir}/doc/%{name}-6
%doc %{_datadir}/doc/%{name}-%{VERSION}
%doc LICENSE

%files c++
%defattr(-,root,root,-)
%doc Magick++/AUTHORS Magick++/ChangeLog Magick++/NEWS Magick++/README
%doc www/Magick++/COPYING
%{_libdir}/libMagick++-6.Q16.so.*

%files c++-devel
%defattr(-,root,root,-)
%doc Magick++/examples
%{_bindir}/Magick++-config
%{_includedir}/%{name}-6/Magick++
%{_includedir}/%{name}-6/Magick++.h
%{_libdir}/libMagick++-6.Q16.so
%{_libdir}/pkgconfig/Magick++.pc
%{_libdir}/pkgconfig/Magick++-6.Q16.pc
%{_libdir}/pkgconfig/ImageMagick++.pc
%{_libdir}/pkgconfig/ImageMagick++-6.Q16.pc
%{_mandir}/man1/Magick++-config.*

%files perl -f perl-pkg-files
%defattr(-,root,root,-)
%{_mandir}/man3/*
%doc PerlMagick/demo/ PerlMagick/Changelog PerlMagick/README.txt

%changelog
* Sun May 01 2005 Cristy <cristy@mystic.es.dupont.com> 1.0-0
-  Port of Redhat's RPM script to support ImageMagick.

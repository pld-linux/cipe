%define		_kernel_ver %(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define		_kernel_ver_str	%(echo %{_kernel_ver} | sed s/-/_/g)
%define		smpstr		%{?_with_smp:-smp}
%define		smp		%{?_with_smp:1}%{!?_with_smp:0}

Summary:	CIPE - encrypted IP over UDP tunneling
Summary(pl):	CIPE - szyfrowany tunel IP po UDP
Name:		cipe
Version:	1.5.2
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	http://sites.inka.de/bigred/sw/%{name}-%{version}.tar.gz
Patch0:		%{name}-autoconf.patch
Patch1:		%{name}-makefile.patch
BuildRequires:	openssl-devel >= 0.9.6
BuildRequires:	%{_bindir}/openssl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

%description
CIPE (the name is shortened from *Crypto IP Encapsulation*) is a
package for an encrypting IP tunnel device. This can be used to build
encrypting routers for VPN (Virtual Private Networks) and similar
applications.

%description -l pl
CIPE (nazwa to skrót od *Crypto IP Encapsulation*) to pakiet do
tworzenia szyfrowanych tuneli IP. Mo¿na je wykorzystaæ do budowania
routerów szyfruj±cych w VPNach (Prywatnych Sieciach Wirtualnych) i
podobnych zastosowaniach.

%package -n kernel%{smpstr}-cipe
Summary:	CIPE kernel module
Summary(pl):	Modu³ j±dra CIPE
Release:	%{release}@%{_kernel_ver_str}
Group:		Base/Kernel
Group(de):	Grundsätzlich/Kern
Group(pl):	Podstawowe/J±dro
Prereq:		/sbin/depmod

%description -n kernel%{smpstr}-cipe
CIPE (the name is shortened from *Crypto IP Encapsulation*) is a
package for an encrypting IP tunnel device. This can be used to build
encrypting routers for VPN (Virtual Private Networks) and similar
applications. This package contains a kernel module compiled for
%{_kernel_ver}%{smpstr}.

%description -n kernel%{smpstr}-cipe -l pl
CIPE (nazwa to skrót od *Crypto IP Encapsulation*) to pakiet do
tworzenia szyfrowanych tuneli IP. Mo¿na je wykorzystaæ do budowania
routerów szyfruj±cych w VPNach (Prywatnych Sieciach Wirtualnych) i
podobnych zastosowaniach. Ten pakiet zawiera modu³ kernela
skompilowany dla %{_kernel_ver}%{smpstr}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
mv -f conf/aclocal.m4 conf/acinclude.m4
aclocal -I conf --output=conf/aclocal.m4
autoconf -l conf/
%if %{smp}
DEFS="-D__SMP__ -D__KERNEL_SMP=1" \
%endif
%configure \
	--with-linux=%{_kernelsrcdir} \
	--with-ciped=%{_sbindir}/ciped-cb \
%if %{smp}
	--enable-smp
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_infodir}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/cipe/pk \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc \
	$RPM_BUILD_ROOT%{_var}/run/cipe

install pkcipe/pkcipe $RPM_BUILD_ROOT%{_sbindir}
install pkcipe/rsa-keygen $RPM_BUILD_ROOT%{_bindir}
install */cipcb.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install */ciped-cb $RPM_BUILD_ROOT%{_sbindir}
install cipe.info $RPM_BUILD_ROOT%{_infodir}
gzip -9nf README* tcpdump.patch CHANGES

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f %{_sysconfdir}/cipe/identity.priv ] && %{_bindir}/rsa-keygen %{_sysconfdir}/cipe/identity
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post -n kernel%{smpstr}-cipe
/sbin/depmod -a

%postun -n kernel%{smpstr}-cipe
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc *.gz samples
%{_infodir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/*
%dir %{_sysconfdir}/cipe
%attr(700,root,root) %dir %{_sysconfdir}/cipe/pk
%attr(755,root,root) %dir %{_var}/run/cipe

%files -n kernel%{smpstr}-cipe
%defattr(644,root,root,755)
%attr(600,root,root) /lib/modules/*/misc/cipcb.o

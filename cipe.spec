Summary:	CIPE - encrypted IP over UDP tunneling
Summary(pl):	CIPE - szyfrowany tunel IP po UDP
Name:		cipe
Version:	1.5.2
%define		_rel 5
Release:	%{_rel}
License:	GPL
Group:		Networking/Daemons
Source0:	http://sites.inka.de/bigred/sw/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Patch0:		%{name}-autoconf.patch
Patch1:		%{name}-makefile.patch
Patch2:		%{name}-pkcipe-real-peer.patch
%{!?_without_dist_kernel:BuildRequires: kernel-headers}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	openssl-devel >= 0.9.6
BuildRequires:	%{_bindir}/openssl
BuildRequires:  %{kgcc_package}

BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc
%define		__cc		%{kgcc}

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

%package pkcipe-client
Summary:	The PKCIPE public key tool for CIPE
Summary(pl):	PKCIPE - narzêdzie do wykorzystania kluczy publicznych w CIPE
Group:		Networking/Daemons
Prereq:		%{_bindir}/openssl
Requires:	%{name} = %{version}
Obsoletes:	%{name}-pkcipe

%description pkcipe-client
CIPE (the name is shortened from *Crypto IP Encapsulation*) is a
package for an encrypting IP tunnel device. This can be used to build
encrypting routers for VPN (Virtual Private Networks) and similar
applications. This package contains PKCIPE, which simplifies setup of
CIPE tunnels by using autoconfiguration and public/private key
mechanisms.

%description pkcipe-client -l pl
CIPE (nazwa to skrót od *Crypto IP Encapsulation*) to pakiet do
tworzenia szyfrowanych tuneli IP. Mo¿na je wykorzystaæ do budowania
routerów szyfruj±cych w VPNach (Prywatnych Sieciach Wirtualnych) i
podobnych zastosowaniach. Ten pakiet zawiera PKCIPE, który uprasza
ustawienie tuneli CIPE przez korzystanie z autokonfiguracji oraz
mechanizmów kluczy publicznych/prywatnych.

%package pkcipe-server
Summary:	The PKCIPE public key tool for CIPE - server side
Summary(pl):	PKCIPE - narzêdzie do wykorzystania kluczy publicznych w CIPE
Group:		Networking/Daemons
Requires:	%{name}-pkcipe-client = %{version}
Requires:	inetdaemon

%description pkcipe-server
CIPE (the name is shortened from *Crypto IP Encapsulation*) is a
package for an encrypting IP tunnel device. This can be used to build
encrypting routers for VPN (Virtual Private Networks) and similar
applications. This package contains server part PKCIPE, which simplifies
setup of CIPE tunnels by using autoconfiguration and public/private key
mechanisms.

%description pkcipe-server -l pl
CIPE (nazwa to skrót od *Crypto IP Encapsulation*) to pakiet do
tworzenia szyfrowanych tuneli IP. Mo¿na je wykorzystaæ do budowania
routerów szyfruj±cych w VPNach (Prywatnych Sieciach Wirtualnych) i
podobnych zastosowaniach. Ten pakiet zawiera PKCIPE do u¿ycia po stronie
serwera, który uprasza ustawienie tuneli CIPE przez korzystanie z
autokonfiguracji oraz mechanizmów kluczy publicznych/prywatnych.

%package -n kernel-cipe
Summary:	CIPE kernel module
Summary(pl):	Modu³ j±dra CIPE
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_up}

%description -n kernel-cipe
CIPE (the name is shortened from *Crypto IP Encapsulation*) is a
package for an encrypting IP tunnel device. This can be used to build
encrypting routers for VPN (Virtual Private Networks) and similar
applications. This package contains a kernel module compiled for
%{_kernel_ver}%{smpstr}.

%description -n kernel-cipe -l pl
CIPE (nazwa to skrót od *Crypto IP Encapsulation*) to pakiet do
tworzenia szyfrowanych tuneli IP. Mo¿na je wykorzystaæ do budowania
routerów szyfruj±cych w VPNach (Prywatnych Sieciach Wirtualnych) i
podobnych zastosowaniach. Ten pakiet zawiera modu³ kernela
skompilowany dla %{_kernel_ver}%.

%package -n kernel-smp-cipe
Summary:	CIPE kernel module
Summary(pl):	Modu³ j±dra CIPE
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_smp}

%description -n kernel-smp-cipe
CIPE (the name is shortened from *Crypto IP Encapsulation*) is a
package for an encrypting IP tunnel device. This can be used to build
encrypting routers for VPN (Virtual Private Networks) and similar
applications. This package contains a kernel module compiled for
%{_kernel_ver}%{smpstr}.

%description -n kernel-smp-cipe -l pl
CIPE (nazwa to skrót od *Crypto IP Encapsulation*) to pakiet do
tworzenia szyfrowanych tuneli IP. Mo¿na je wykorzystaæ do budowania
routerów szyfruj±cych w VPNach (Prywatnych Sieciach Wirtualnych) i
podobnych zastosowaniach. Ten pakiet zawiera modu³ kernela
skompilowany dla %{_kernel_ver}-smp.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
mv -f conf/aclocal.m4 conf/acinclude.m4
aclocal -I conf --output=conf/aclocal.m4
autoconf -l conf/

%configure \
	--with-linux=%{_kernelsrcdir} \
	--with-ciped=%{_sbindir}/ciped-cb

%{__make} modules

mkdir modules/
mv -f */cipcb.o modules/

make clean

DEFS="-D__SMP__ -D__KERNEL_SMP=1" \
%configure \
	--with-linux=%{_kernelsrcdir} \
	--with-ciped=%{_sbindir}/ciped-cb \
	--enable-smp

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_infodir}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/cipe/pk \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc \
	$RPM_BUILD_ROOT%{_var}/run/cipe \
	$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd

install pkcipe/pkcipe $RPM_BUILD_ROOT%{_sbindir}
install pkcipe/rsa-keygen $RPM_BUILD_ROOT%{_bindir}
mv -f modules/cipcb.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
install */cipcb.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install */ciped-cb $RPM_BUILD_ROOT%{_sbindir}
install cipe.info $RPM_BUILD_ROOT%{_infodir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/pkcipe

gzip -9nf README* tcpdump.patch CHANGES

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post pkcipe-client
[ ! -f %{_sysconfdir}/cipe/identity.priv ] && %{_bindir}/rsa-keygen %{_sysconfdir}/cipe/identity

%post pkcipe-server
if [ -f /var/lock/subsys/rc-inetd ]; then
        /etc/rc.d/init.d/rc-inetd reload 1>&2
else
        echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun pkcipe-server
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%post -n kernel-cipe
/sbin/depmod -a

%postun -n kernel-cipe
/sbin/depmod -a

%post -n kernel-smp-cipe
/sbin/depmod -a

%postun -n kernel-smp-cipe
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc *.gz samples
%{_infodir}/*
%attr(755,root,root) %{_sbindir}/ciped-cb
%dir %{_sysconfdir}/cipe
%attr(755,root,root) %dir %{_var}/run/cipe

%files pkcipe-client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rsa-keygen
%attr(755,root,root) %{_sbindir}/pkcipe
%attr(700,root,root) %dir %{_sysconfdir}/cipe/pk

%files pkcipe-server
%defattr(644,root,root,755)
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/rc-inetd/pkcipe

%files -n kernel-cipe
%defattr(644,root,root,755)
%attr(600,root,root) /lib/modules/%{_kernel_ver}/misc/cipcb.o

%files -n kernel-smp-cipe
%defattr(644,root,root,755)
%attr(600,root,root) /lib/modules/%{_kernel_ver}smp/misc/cipcb.o

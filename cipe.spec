#
# Conditional build:
# _without_dist_kernel	- without kernel from distribution
#
Summary:	CIPE - encrypted IP over UDP tunneling
Summary(pl):	CIPE - szyfrowany tunel IP po UDP
Name:		cipe
Version:	1.5.4
%define	_rel	1
Release:	%{_rel}
License:	GPL
Group:		Networking/Daemons
Source0:	http://sites.inka.de/bigred/sw/%{name}-%{version}.tar.gz
# Source0-md5:	9d88f2d090fcafcd0e2fa73b018b6e16
Source1:	%{name}.inetd
Patch0:		%{name}-autoconf.patch
Patch1:		%{name}-makefile.patch
Patch2:		%{name}-pk%{name}-real-peer.patch
Patch3:		%{name}-get_fast_time.patch
Patch4:		%{name}-alpha.patch
URL:		http://sites.inka.de/bigred/devel/cipe.html
%{!?_without_dist_kernel:BuildRequires:	kernel-headers}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	/usr/bin/openssl
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRequires:	%{kgcc_package}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		__cc		%{kgcc}

%description
CIPE (the name is shortened from *Crypto IP Encapsulation*) is a
package for an encrypting IP tunnel device. This can be used to build
encrypting routers for VPN (Virtual Private Networks) and similar
applications.

%description -l pl
CIPE (nazwa to skr�t od *Crypto IP Encapsulation*) to pakiet do
tworzenia szyfrowanych tuneli IP. Mo�na je wykorzysta� do budowania
router�w szyfruj�cych w VPNach (Prywatnych Sieciach Wirtualnych) i
podobnych zastosowaniach.

%package pkcipe-client
Summary:	The PKCIPE public key tool for CIPE
Summary(pl):	PKCIPE - narz�dzie do wykorzystania kluczy publicznych w CIPE
Group:		Networking/Daemons
Prereq:		/usr/bin/openssl
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
CIPE (nazwa to skr�t od *Crypto IP Encapsulation*) to pakiet do
tworzenia szyfrowanych tuneli IP. Mo�na je wykorzysta� do budowania
router�w szyfruj�cych w VPNach (Prywatnych Sieciach Wirtualnych) i
podobnych zastosowaniach. Ten pakiet zawiera PKCIPE, kt�ry uprasza
ustawienie tuneli CIPE przez korzystanie z autokonfiguracji oraz
mechanizm�w kluczy publicznych/prywatnych.

%package pkcipe-server
Summary:	The PKCIPE public key tool for CIPE - server side
Summary(pl):	PKCIPE - narz�dzie do wykorzystania kluczy publicznych w CIPE
Group:		Networking/Daemons
Requires:	%{name}-pkcipe-client = %{version}
Requires:	inetdaemon

%description pkcipe-server
CIPE (the name is shortened from *Crypto IP Encapsulation*) is a
package for an encrypting IP tunnel device. This can be used to build
encrypting routers for VPN (Virtual Private Networks) and similar
applications. This package contains server part PKCIPE, which
simplifies setup of CIPE tunnels by using autoconfiguration and
public/private key mechanisms.

%description pkcipe-server -l pl
CIPE (nazwa to skr�t od *Crypto IP Encapsulation*) to pakiet do
tworzenia szyfrowanych tuneli IP. Mo�na je wykorzysta� do budowania
router�w szyfruj�cych w VPNach (Prywatnych Sieciach Wirtualnych) i
podobnych zastosowaniach. Ten pakiet zawiera PKCIPE do u�ycia po
stronie serwera, kt�ry uprasza ustawienie tuneli CIPE przez
korzystanie z autokonfiguracji oraz mechanizm�w kluczy
publicznych/prywatnych.

%package -n kernel-cipe
Summary:	CIPE kernel module
Summary(pl):	Modu� j�dra CIPE
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-cipe
CIPE (the name is shortened from *Crypto IP Encapsulation*) is a
package for an encrypting IP tunnel device. This can be used to build
encrypting routers for VPN (Virtual Private Networks) and similar
applications. This package contains a kernel module compiled for
%{_kernel_ver}%{smpstr}.

%description -n kernel-cipe -l pl
CIPE (nazwa to skr�t od *Crypto IP Encapsulation*) to pakiet do
tworzenia szyfrowanych tuneli IP. Mo�na je wykorzysta� do budowania
router�w szyfruj�cych w VPNach (Prywatnych Sieciach Wirtualnych) i
podobnych zastosowaniach. Ten pakiet zawiera modu� kernela
skompilowany dla %{_kernel_ver}%.

%package -n kernel-smp-cipe
Summary:	CIPE kernel module
Summary(pl):	Modu� j�dra CIPE
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-cipe
CIPE (the name is shortened from *Crypto IP Encapsulation*) is a
package for an encrypting IP tunnel device. This can be used to build
encrypting routers for VPN (Virtual Private Networks) and similar
applications. This package contains a kernel module compiled for
%{_kernel_ver}%{smpstr}.

%description -n kernel-smp-cipe -l pl
CIPE (nazwa to skr�t od *Crypto IP Encapsulation*) to pakiet do
tworzenia szyfrowanych tuneli IP. Mo�na je wykorzysta� do budowania
router�w szyfruj�cych w VPNach (Prywatnych Sieciach Wirtualnych) i
podobnych zastosowaniach. Ten pakiet zawiera modu� kernela
skompilowany dla %{_kernel_ver}-smp.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
# %patch3 -p1
%patch4 -p1

%build
mv -f conf/aclocal.m4 conf/acinclude.m4
%{__aclocal} -I conf --output=conf/aclocal.m4
%{__autoconf} --include conf/

%configure \
	--with-linux=%{_kernelsrcdir} \
	--with-ciped=%{_sbindir}/ciped-cb

%{__make} modules

%configure \
	--with-linux=%{_kernelsrcdir} \
	--with-ciped=%{_sbindir}/ciped-db \
	--enable-protocol=4

%{__make} modules

mkdir modules/
mv -f */cip?b.o modules/

%{__make} clean

DEFS="-D__SMP__ -D__KERNEL_SMP=1" \
%configure \
	--with-linux=%{_kernelsrcdir} \
	--with-ciped=%{_sbindir}/ciped-cb \
	--enable-smp

%{__make}

DEFS="-D__SMP__ -D__KERNEL_SMP=1" \
%configure \
	--with-linux=%{_kernelsrcdir} \
	--with-ciped=%{_sbindir}/ciped-cb \
	--enable-smp \
	--enable-protocol=4

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
mv -f modules/cip?b.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install */cip?b.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
install */ciped-?b $RPM_BUILD_ROOT%{_sbindir}
install cipe.info $RPM_BUILD_ROOT%{_infodir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/pkcipe

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

%post	-n kernel-cipe
%depmod %{_kernel_ver}

%postun -n kernel-cipe
%depmod %{_kernel_ver}

%post	-n kernel-smp-cipe
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-cipe
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc README* tcpdump.patch CHANGES samples
%{_infodir}/*
%attr(755,root,root) %{_sbindir}/ciped-*
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
/lib/modules/%{_kernel_ver}/misc/cip*.o*

%files -n kernel-smp-cipe
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/cip*.o*

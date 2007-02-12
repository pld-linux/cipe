#
# Conditional build:
%bcond_without	dist_kernel	# without kernel from distribution
#
%define	_rel	1
Summary:	CIPE - encrypted IP over UDP tunneling
Summary(pl.UTF-8):   CIPE - szyfrowany tunel IP po UDP
Name:		cipe
Version:	1.5.4
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
BuildRequires:	%{kgcc_package}
BuildRequires:	/usr/bin/openssl
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_dist_kernel:BuildRequires:	kernel-headers}
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		__cc		%{kgcc}

%description
CIPE (the name is shortened from *Crypto IP Encapsulation*) is a
package for an encrypting IP tunnel device. This can be used to build
encrypting routers for VPN (Virtual Private Networks) and similar
applications.

%description -l pl.UTF-8
CIPE (nazwa to skrót od *Crypto IP Encapsulation*) to pakiet do
tworzenia szyfrowanych tuneli IP. Można je wykorzystać do budowania
routerów szyfrujących w VPNach (Prywatnych Sieciach Wirtualnych) i
podobnych zastosowaniach.

%package pkcipe-client
Summary:	The PKCIPE public key tool for CIPE
Summary(pl.UTF-8):   PKCIPE - narzędzie do wykorzystania kluczy publicznych w CIPE
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Requires:	/usr/bin/openssl
Obsoletes:	cipe-pkcipe

%description pkcipe-client
CIPE (the name is shortened from *Crypto IP Encapsulation*) is a
package for an encrypting IP tunnel device. This can be used to build
encrypting routers for VPN (Virtual Private Networks) and similar
applications. This package contains PKCIPE, which simplifies setup of
CIPE tunnels by using autoconfiguration and public/private key
mechanisms.

%description pkcipe-client -l pl.UTF-8
CIPE (nazwa to skrót od *Crypto IP Encapsulation*) to pakiet do
tworzenia szyfrowanych tuneli IP. Można je wykorzystać do budowania
routerów szyfrujących w VPNach (Prywatnych Sieciach Wirtualnych) i
podobnych zastosowaniach. Ten pakiet zawiera PKCIPE, który uprasza
ustawienie tuneli CIPE przez korzystanie z autokonfiguracji oraz
mechanizmów kluczy publicznych/prywatnych.

%package pkcipe-server
Summary:	The PKCIPE public key tool for CIPE - server side
Summary(pl.UTF-8):   PKCIPE - narzędzie do wykorzystania kluczy publicznych w CIPE
Group:		Networking/Daemons
Requires:	%{name}-pkcipe-client = %{version}-%{release}
Requires:	inetdaemon

%description pkcipe-server
CIPE (the name is shortened from *Crypto IP Encapsulation*) is a
package for an encrypting IP tunnel device. This can be used to build
encrypting routers for VPN (Virtual Private Networks) and similar
applications. This package contains server part PKCIPE, which
simplifies setup of CIPE tunnels by using autoconfiguration and
public/private key mechanisms.

%description pkcipe-server -l pl.UTF-8
CIPE (nazwa to skrót od *Crypto IP Encapsulation*) to pakiet do
tworzenia szyfrowanych tuneli IP. Można je wykorzystać do budowania
routerów szyfrujących w VPNach (Prywatnych Sieciach Wirtualnych) i
podobnych zastosowaniach. Ten pakiet zawiera PKCIPE do użycia po
stronie serwera, który uprasza ustawienie tuneli CIPE przez
korzystanie z autokonfiguracji oraz mechanizmów kluczy
publicznych/prywatnych.

%package -n kernel-cipe
Summary:	CIPE kernel module
Summary(pl.UTF-8):   Moduł jądra CIPE
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-cipe
CIPE (the name is shortened from *Crypto IP Encapsulation*) is a
package for an encrypting IP tunnel device. This can be used to build
encrypting routers for VPN (Virtual Private Networks) and similar
applications. This package contains a kernel module compiled for
%{_kernel_ver}.

%description -n kernel-cipe -l pl.UTF-8
CIPE (nazwa to skrót od *Crypto IP Encapsulation*) to pakiet do
tworzenia szyfrowanych tuneli IP. Można je wykorzystać do budowania
routerów szyfrujących w VPNach (Prywatnych Sieciach Wirtualnych) i
podobnych zastosowaniach. Ten pakiet zawiera moduł kernela
skompilowany dla %{_kernel_ver}.

%package -n kernel-smp-cipe
Summary:	CIPE kernel module
Summary(pl.UTF-8):   Moduł jądra CIPE
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-cipe
CIPE (the name is shortened from *Crypto IP Encapsulation*) is a
package for an encrypting IP tunnel device. This can be used to build
encrypting routers for VPN (Virtual Private Networks) and similar
applications. This package contains a kernel module compiled for
%{_kernel_ver}smp.

%description -n kernel-smp-cipe -l pl.UTF-8
CIPE (nazwa to skrót od *Crypto IP Encapsulation*) to pakiet do
tworzenia szyfrowanych tuneli IP. Można je wykorzystać do budowania
routerów szyfrujących w VPNach (Prywatnych Sieciach Wirtualnych) i
podobnych zastosowaniach. Ten pakiet zawiera moduł kernela
skompilowany dla %{_kernel_ver}smp.

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

mkdir modules
mv -f */cip?b.o modules

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
%service -q rc-inetd reload

%postun pkcipe-server
if [ "$1" = "0" ]; then
	%service -q rc-inetd reload
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
%attr(755,root,root) %{_sbindir}/ciped-*
%dir %{_sysconfdir}/cipe
%attr(755,root,root) %dir %{_var}/run/cipe
%{_infodir}/*.info*

%files pkcipe-client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rsa-keygen
%attr(755,root,root) %{_sbindir}/pkcipe
%attr(700,root,root) %dir %{_sysconfdir}/cipe/pk

%files pkcipe-server
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/pkcipe

%files -n kernel-cipe
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/cip*.o*

%files -n kernel-smp-cipe
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/cip*.o*

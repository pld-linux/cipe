%define		_kernel_ver %(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define		_kernel_ver_str	%(echo %{_kernel_ver} | sed s/-/_/g)
%define		smpstr		%{?_with_smp:-smp}
%define		smp		%{?_with_smp:1}%{!?_with_smp:0}

Summary:	CIPE - encrypted IP over UDP tunneling
Summary(pl):	CIPE - szyfrowany tunel IP po UDP
Name:		cipe
Version:	1.5.2
Release:	3
License:	GPL
Group:		Networking/Daemons
Source0:	http://sites.inka.de/bigred/sw/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Patch0:		%{name}-autoconf.patch
Patch1:		%{name}-makefile.patch
BuildRequires:	autoconf
BuildRequires:	automake
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

%package pkcipe
Summary:	The PKCIPE public key tool for CIPE
Summary(pl):	PKCIPE - narzêdzie do wykorzystania kluczy publicznych w CIPE
Group:		Networking/Daemons
Prereq:		%{_bindir}/openssl
Requires:	%{name} = %{version}

%description pkcipe
CIPE (the name is shortened from *Crypto IP Encapsulation*) is a
package for an encrypting IP tunnel device. This can be used to build
encrypting routers for VPN (Virtual Private Networks) and similar
applications.
This package contains PKCIPE, which simplifies setup of CIPE tunnels by
using autoconfiguration and public/private key mechanisms.

%description pkcipe -l pl
CIPE (nazwa to skrót od *Crypto IP Encapsulation*) to pakiet do
tworzenia szyfrowanych tuneli IP. Mo¿na je wykorzystaæ do budowania
routerów szyfruj±cych w VPNach (Prywatnych Sieciach Wirtualnych) i
podobnych zastosowaniach.
Ten pakiet zawiera PKCIPE, który uprasza ustawienie tuneli CIPE przez
korzystanie z autokonfiguracji oraz mechanizmów kluczy
publicznych/prywatnych.

%package -n kernel%{smpstr}-cipe
Summary:	CIPE kernel module
Summary(pl):	Modu³ j±dra CIPE
Release:	%{release}@%{_kernel_ver_str}
Group:		Base/Kernel
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
	$RPM_BUILD_ROOT%{_var}/run/cipe \
	$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd

install pkcipe/pkcipe $RPM_BUILD_ROOT%{_sbindir}
install pkcipe/rsa-keygen $RPM_BUILD_ROOT%{_bindir}
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

%post pkcipe
[ ! -f %{_sysconfdir}/cipe/identity.priv ] && %{_bindir}/rsa-keygen %{_sysconfdir}/cipe/identity
if [ -f /var/lock/subsys/rc-inetd ]; then
        /etc/rc.d/init.d/rc-inetd reload 1>&2
else
        echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun pkcipe
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%post -n kernel%{smpstr}-cipe
/sbin/depmod -a

%postun -n kernel%{smpstr}-cipe
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc *.gz samples
%{_infodir}/*
%attr(755,root,root) %{_sbindir}/ciped-cb
%dir %{_sysconfdir}/cipe
%attr(755,root,root) %dir %{_var}/run/cipe

%files pkcipe
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rsa-keygen
%attr(755,root,root) %{_sbindir}/pkcipe
%attr(700,root,root) %dir %{_sysconfdir}/cipe/pk
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/rc-inetd/pkcipe

%files -n kernel%{smpstr}-cipe
%defattr(644,root,root,755)
%attr(600,root,root) /lib/modules/*/misc/cipcb.o

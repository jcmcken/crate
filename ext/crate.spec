%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           crate
Version:        0.1.0
Release:        1%{?dist}
Group:          Utilities
Summary:        Manage "virtual" file repositories with ease

License:        BSD  
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  coreutils
Requires:       createrepo
Requires:       python2
Requires:       PyYAML
BuildArch:      noarch

%description
Manage "virtual" file repositories with ease. 

%prep
%setup -q

%build
%{__python} setup.py build

%install
[ -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%{__install} -d -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/crate/repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/crate
%{python_sitelib}/*
%attr(0755,root,root) /etc/crate/repos.d

%changelog
* Sat May 18 2013 - Jon McKenzie - 0.1.0
- Initial implementation

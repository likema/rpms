%if 0%{?fedora} > 12 || 0%{?rhel} > 6
%global with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

%{!?PYTHON_NAME: %global PYTHON_NAME %(basename "%{__python}")}
%global srcname bottle

Name:          %{PYTHON_NAME}-%{srcname}
Version:       0.11.6
Release:       2%{?dist}
Summary:       Fast and simple WSGI-framework for small web-applications

Group:         Development/Languages
License:       MIT
URL:           http://bottlepy.org
Source0:       http://pypi.python.org/packages/source/b/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-root
BuildArch:     noarch
BuildRequires: %{PYTHON_NAME}-devel, tar

%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
%endif # if with_python3

%description
Bottle is a fast and simple micro-framework for small web-applications. 
It offers request dispatching (Routes) with URL parameter support, Templates, 
a built-in HTTP Server and adapters for many third party WSGI/HTTP-server and 
template engines. All in a single file and with no dependencies other than the 
Python Standard Library.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        Fast and simple WSGI-framework for small web-applications

%description -n python3-%{srcname}
Bottle is a fast and simple micro-framework for small web-applications. 
It offers request dispatching (Routes) with URL parameter support, Templates, 
a built-in HTTP Server and adapters for many third party WSGI/HTTP-server and 
template engines. All in a single file and with no dependencies other than the 
Python Standard Library.
%endif # if with_python3

%prep
echo "== %{PYTHONNAME} =="
%setup -q -n %{srcname}-%{version}
sed -i '/^#!/d' bottle.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # if with_python3

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # if with_python3

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
rm %{buildroot}%{_bindir}/bottle.py

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
rm %{buildroot}%{_bindir}/bottle.py
popd
%endif # if with_python3

%files
%doc README.rst PKG-INFO
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc README.rst PKG-INFO
%{python3_sitelib}/*
%endif # if with_python3

%changelog
* Thu Jul 18 2013 Like Ma <likemartinma@gmail.com> - 0.11.6-2
- Add macros PYTHON_NAME to build python2.7-bottle in CentOS 5

* Tue Apr 23 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 0.11.6-1
- upstream release 0.11.6
- add python3 subpackage. resolves rhbz#949240
- spec file patch from Haïkel Guémar <hguemar@fedoraproject.org>

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 01 2012 Ian Weller <iweller@redhat.com> - 0.10.7-1
- Update to 0.10.7 (required by python-mwlib)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 18 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.9.5-1
- Initial spec

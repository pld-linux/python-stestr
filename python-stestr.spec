#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (some failing)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	A parallel Python test runner built around subunit
Summary(pl.UTF-8):	Zrównoleglone narzędzie do uruchamiania testów w Pythonie zbudowane wokół subunit
Name:		python-stestr
# keep 2.x here for python2 support
Version:	2.6.0
Release:	3
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/stestr/
Source0:	https://files.pythonhosted.org/packages/source/s/stestr/stestr-%{version}.tar.gz
# Source0-md5:	1ed94a3b9990871ddc863d8651f58cf8
Patch0:		stestr-no-py3-future.patch
Patch1:		stestr-mock.patch
URL:		https://pypi.org/project/stestr/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-pbr >= 4.0.4
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-PyYAML >= 3.10.0
BuildRequires:	python-cliff >= 2.8.0
BuildRequires:	python-ddt >= 1.0.1
BuildRequires:	python-fixtures >= 3.0.0
BuildRequires:	python-mock >= 2.0
BuildRequires:	python-six >= 1.10.0
BuildRequires:	python-subunit >= 1.3.0
BuildRequires:	python-subunit2sql >= 1.8.0
BuildRequires:	python-testtools >= 2.2.0
BuildRequires:	python-voluptuous >= 0.8.9
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-pbr >= 4.0.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-PyYAML >= 3.10.0
BuildRequires:	python3-cliff >= 2.8.0
BuildRequires:	python3-ddt >= 1.0.1
BuildRequires:	python3-fixtures >= 3.0.0
BuildRequires:	python3-six >= 1.10.0
BuildRequires:	python3-subunit >= 1.3.0
BuildRequires:	python3-subunit2sql >= 1.8.0
BuildRequires:	python3-testtools >= 2.2.0
BuildRequires:	python3-voluptuous >= 0.8.9
%endif
%endif
%if %{with doc}
BuildRequires:	python-cliff >= 2.8.0
BuildRequires:	sphinx-pdg-2
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
stestr is parallel Python test runner designed to execute unittest
test suites using multiple processes to split up execution of a test
suite. It also will store a history of all test runs to help in
debugging failures and optimizing the scheduler to improve speed. To
accomplish this goal it uses the subunit protocol to facilitate
streaming and storing results from multiple workers.

%description -l pl.UTF-8
sestr to narzędzie do równoległego uruchamiania testów pythonowych,
zaprojektowane w celu uruchamiania zestawów testów unittest przy
użyciu wielu procesów, aby podzielić wykonywanie testów. Narzędzie
ponadto zapisuje historię wszystkich uruchomień testów, aby pomóc w
diagnostyce niepowodzeń i optymalizacji planisty pod kątem szybkości.
Aby osiągnąć ten cel, stestr używa protokołu subunit do strumieniowego
przesyłania i zapisywania wyników od wielu procesów roboczych.

%package -n python3-stestr
Summary:	A parallel Python test runner built around subunit
Summary(pl.UTF-8):	Zrównoleglone narzędzie do uruchamiania testów w Pythonie zbudowane wokół subunit
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-stestr
stestr is parallel Python test runner designed to execute unittest
test suites using multiple processes to split up execution of a test
suite. It also will store a history of all test runs to help in
debugging failures and optimizing the scheduler to improve speed. To
accomplish this goal it uses the subunit protocol to facilitate
streaming and storing results from multiple workers.

%description -n python3-stestr -l pl.UTF-8
sestr to narzędzie do równoległego uruchamiania testów pythonowych,
zaprojektowane w celu uruchamiania zestawów testów unittest przy
użyciu wielu procesów, aby podzielić wykonywanie testów. Narzędzie
ponadto zapisuje historię wszystkich uruchomień testów, aby pomóc w
diagnostyce niepowodzeń i optymalizacji planisty pod kątem szybkości.
Aby osiągnąć ten cel, stestr używa protokołu subunit do strumieniowego
przesyłania i zapisywania wyników od wielu procesów roboczych.

%package apidocs
Summary:	API documentation for Python stestr module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona stestr
Group:		Documentation

%description apidocs
API documentation for Python stestr module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona stestr.

%prep
%setup -q -n stestr-%{version}
%patch -P 0 -p1
%patch -P 1 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
install -d build-2/bin
ln -sf %{_bindir}/subunit2sql-db-manage-2 build-2/bin/subunit2sql-db-manage
cat >build-2/bin/stestr <<EOF
#!/bin/sh

%{__python} $(pwd)/stestr/__main__.py
EOF
chmod 755 build-2/bin/stestr

PATH=$(pwd)/build-2/bin:$PATH \
PYTHONPATH=$(pwd) \
%{__python} -m stestr run
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
install -d build-3/bin
ln -sf %{_bindir}/subunit2sql-db-manage-3 build-3/bin/subunit2sql-db-manage
cat >build-3/bin/stestr <<EOF
#!/bin/sh

%{__python3} $(pwd)/stestr/__main__.py
EOF
chmod 755 build-3/bin/stestr

PATH=$(pwd)/build-3/bin:$PATH \
PYTHONPATH=$(pwd) \
%{__python3} -m stestr run
%endif
%endif

%if %{with doc}
sphinx-build-2 -b html doc/source doc/build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/stestr/tests

%{__mv} $RPM_BUILD_ROOT%{_bindir}/stestr{,-2}
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/stestr/tests

%{__mv} $RPM_BUILD_ROOT%{_bindir}/stestr{,-3}
ln -sf stestr-3 $RPM_BUILD_ROOT%{_bindir}/stestr
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst
%lang(ja) %doc README_ja.rst
%attr(755,root,root) %{_bindir}/stestr-2
%{py_sitescriptdir}/stestr
%{py_sitescriptdir}/stestr-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-stestr
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst
%lang(ja) %doc README_ja.rst
%attr(755,root,root) %{_bindir}/stestr
%attr(755,root,root) %{_bindir}/stestr-3
%{py3_sitescriptdir}/stestr
%{py3_sitescriptdir}/stestr-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/html/{_static,api,*.html,*.js}
%endif

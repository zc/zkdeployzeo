Name: zeo
Version: 0
Release: 1

Summary: ZEO server configured using zkdeployment
Group: Applications/Database
Requires: cleanpython26
Requires: zcuser-zope
BuildRequires: cleanpython26
%define python /opt/cleanpython26/bin/python

##########################################################################
# Lines below this point normally shouldn't change

%define source zkdeployzeo-%{version}

Vendor: Zope Corporation
Packager: Zope Corporation <sales@zope.com>
License: ZVSL
AutoReqProv: no
Source: %{source}.tgz
Prefix: /opt
BuildRoot: /tmp/%{name}

%description
%{summary}

%prep
%setup -n %{source}

%build
rm -rf %{buildroot}
mkdir %{buildroot} %{buildroot}/opt
cp -r $RPM_BUILD_DIR/%{source} %{buildroot}/opt/%{name}
%{python} %{buildroot}/opt/%{name}/install.py bootstrap
%{python} %{buildroot}/opt/%{name}/install.py buildout:extensions=
%{python} -m compileall -q -f -d /opt/%{name}/eggs  \
   %{buildroot}/opt/%{name}/eggs \
   > /dev/null 2>&1 || true
rm -rf %{buildroot}/opt/%{name}/release-distributions
chmod -R a+rX %{buildroot}/opt/%{name}/

# Gaaaa! buildout doesn't handle relative paths in egg links. :(
sed -i s-/tmp/%{name}-- \
   %{buildroot}/opt/%{name}/develop-eggs/*.egg-link 

%clean
rm -rf %{buildroot}
rm -rf $RPM_BUILD_DIR/%{source}

%post
if [[ ! -d /home/databases ]]
then
   mkdir /home/databases
fi
if [[ ! -d /etc/%{name} ]]
then
   mkdir /etc/%{name}
fi

%files
%defattr(-, root, root)
/opt/%{name}

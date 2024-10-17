# Prevent brp-java-repack-jars from being run.
%global __jar_repack %{nil}

%global nb_            netbeans
%global nb_org         %{nb_}.org
%global nb_ver         6.7.1

%global svnCA          svnClientAdapter
%global svnCA_ver      1.6.0

Name:           libnb-svnClientAdapter
Version:        %{nb_ver}
Release:        3
Summary:        Subversion Client Adapter

License:        ASL 2.0
Url:            https://subclipse.tigris.org/svnClientAdapter.html
Group:          Development/Java

# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# svn export --force --username guest -r4383 \
#     http://subclipse.tigris.org/svn/subclipse/trunk/svnClientAdapter/ \
#     svnClientAdapter-1.6.0
# tar -czvf svnClientAdapter-1.6.0.tar.gz svnClientAdapter-1.6.0
Source0:        %{svnCA}-%{svnCA_ver}.tar.gz
Patch0:         %{svnCA}-%{svnCA_ver}-build.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  ant
BuildRequires:  ant-nodeps
BuildRequires:  ant-junit
BuildRequires:  java-devel >= 1.6.0
BuildRequires:  jpackage-utils
BuildRequires:  svn-javahl
BuildRequires:  java-rpmbuild >= 0:1.5.32

Requires:       java >= 1.6.0
Requires:       jpackage-utils
Requires:       subversion
Provides:       %{nb_}-svnclientadapter = 6.7.1

%description
SVNClientAdapter is a high-level Java API for Subversion.

%prep
%setup -q -n %{svnCA}-%{svnCA_ver}

# remove all binary libs
find . -name "*.jar" -exec %{__rm} -f {} \;

%patch0 -p1 -b .sav

%{__ln_s} -f %{_javadir}/svnkit-javahl.jar lib/svnjavahl.jar

%build
[ -z "$JAVA_HOME" ] && export JAVA_HOME=%{_jvmdir}/java 
ant -verbose svnClientAdapter.jar

%install
%{__rm} -fr %{buildroot}
# jar
%{__install} -d -m 755 %{buildroot}%{_javadir}
%{__install} -m 644 build/lib/svnClientAdapter.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%{__ln_s} %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc license.txt readme.txt
%{_javadir}/*



%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 6.7.1-2mdv2011.0
+ Revision: 620166
- the mass rebuild of 2010.0 packages

* Fri Sep 25 2009 Jaroslav Tulach <jtulach@mandriva.org> 6.7.1-1mdv2010.0
+ Revision: 448802
- Updating to adapter provided by NetBeans 6.7.1

* Sun Sep 13 2009 Thierry Vignaud <tv@mandriva.org> 0:6.5-2mdv2010.0
+ Revision: 438716
- rebuild

* Sat Jan 17 2009 Jaroslav Tulach <jtulach@mandriva.org> 0:6.5-1mdv2009.1
+ Revision: 330470
- Updating to version of the adapter that is present in NetBeans 6.5

* Fri Aug 15 2008 Jaroslav Tulach <jtulach@mandriva.org> 0:6.1-4mdv2009.0
+ Revision: 272357
- Also providing netbeans-svnclientadapter to satisfy netbeans-ide's dependency
- Also providing netbeans-svnclientadapter to satisfy netbeans-ide's dependency

* Wed Aug 13 2008 Jaroslav Tulach <jtulach@mandriva.org> 0:6.1-3mdv2009.0
+ Revision: 271350
- Updating for 6.1

* Sat Jul 26 2008 Thierry Vignaud <tv@mandriva.org> 0:6.0.1-3mdv2009.0
+ Revision: 250299
- rebuild

* Thu Jan 24 2008 Jaroslav Tulach <jtulach@mandriva.org> 0:6.0.1-1mdv2008.1
+ Revision: 157642
- Upgrade to version 6.0.1

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:6.0-3mdv2008.1
+ Revision: 120971
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Mon Dec 10 2007 Jaroslav Tulach <jtulach@mandriva.org> 0:6.0-2mdv2008.1
+ Revision: 116985
- Using pristine sources from svn repository rev. 3087, plus a modification patch

* Thu Dec 06 2007 Jaroslav Tulach <jtulach@mandriva.org> 0:6.0-1mdv2008.1
+ Revision: 115856
- create libnb-svnClientAdapter


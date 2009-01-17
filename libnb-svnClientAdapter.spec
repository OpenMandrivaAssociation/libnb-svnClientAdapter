%define section		free

Name:		libnb-svnClientAdapter
Version:	6.5
Release:	%mkrel 1
Epoch:		0
Summary:        Subversion Client Adapter
License:        Apache License
Url:            http://subversion.netbeans.org/teepee/svnclientadapter.html
Group:          Development/Java
%define svnCA_ver      1.4.0
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# svn --username guest co \
#     http://subclipse.tigris.org/svn/subclipse/tags/subclipse/%{svnCA_ver}/svnClientAdapter \
#     svnClientAdapter
# tar -czvf svnClientAdapter-%{svnCA_ver}.tar.gz svnClientAdapter
Source0:        svnClientAdapter-%{svnCA_ver}.tar.gz

Patch0:         svnClientAdapter-%{svnCA_ver}-build.patch
BuildRequires:	java-rpmbuild >= 1.6
BuildRequires:  ant
BuildRequires:  ant-nodeps
BuildRequires:  ant-junit
BuildRequires:  java >= 1.6.0
Requires:       java >= 1.6.0
Requires:       subversion >= 1.4.5
Provides:       libnb-svnclientadapter = %{version}
Provides:       netbeans-svnclientadapter = %{version}
BuildArch:      noarch
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root

%description
SvnClientAdapter is a higher level API (comparing to javahl ...). 
That's why svnClientAdapter is easier to use in many cases.
For example, you can use ISVNClientAdapter  
addToIgnoredPatterns method to add a pattern of files to ignore to a directory.
This is a NetBeans forked version of SvnClientAdapter.

%prep
%{__rm} -fr %{buildroot}
%{__rm} -fr svnClientAdapter-nb6.0.1-src
%setup -q -n svnClientAdapter
# remove all binary libs
find . -name "*.jar" -exec %{__rm} -f {} \;

%patch0 -p1 -b .sav

%{__ln_s} -f %{_javadir}//svnkit-javahl.jar lib/svnjavahl.jar

%build
[ -z "$JAVA_HOME" ] && export JAVA_HOME=%{_jvmdir}/java 
ant -verbose svnClientAdapter.jar

%install
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


%define section		free

Name:		libnb-svnClientAdapter
Version:	6.0
Release:	%mkrel 1
Epoch:		0
Summary:        Subversion Client Adapter
License:        Apache License
Url:            http://subversion.netbeans.org/teepee/svnclientadapter.html
Group:		Development/Java
#
Source0:        svnClientAdapter-netbeans6.0.zip
BuildRequires:	jpackage-utils >= 1.6
BuildRequires:  ant
BuildRequires:  ant-nodeps
BuildRequires:  ant-junit
BuildRequires:  ganymed-ssh2 >= 210
BuildRequires:  svnkit >= 1.1.4
BuildRequires:  svn-javahl >= 1.4.5
Requires:       java >= 1.6.0
Requires:       ganymed-ssh2 >= 210
Requires:       svnkit >= 1.1.4
Requires:       svn-javahl >= 1.4.5
BuildArch:      noarch
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root

%description
SvnClientAdapter is a higher level API (comparing to javahl ...). 
That's why svnClientAdapter is easier to use in many cases.
For example, you can use ISVNClientAdapter  
addToIgnoredPatterns method to add a pattern of files to ignore to a directory.
This is a NetBeans forked version of SvnClientAdapter.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java
Requires(post):   /bin/rm,/bin/ln
Requires(postun): /bin/rm

%description javadoc
Javadoc for %{name}.

%prep
%{__rm} -fr %{buildroot}
%setup -q -n svnClientAdapter-netbeans6.0
# remove all binary libs
find . -name "*.jar" -exec %{__rm} -f {} \;
#%{__rm} src/main/org/tigris/subversion/svnclientadapter/javahl/*Jhl*
%{__ln_s} %{_javadir}/ganymed-ssh2.jar lib/ganymed.jar
%{__ln_s} %{_javadir}/svnkit.jar lib/svnkit.jar
%{__ln_s} `find-jar svn-javahl` lib/svnjavahl.jar

%build
[ -z "$JAVA_HOME" ] && export JAVA_HOME=%{_jvmdir}/java 
ant -verbose

%install
# jar
%{__install} -d -m 755 %{buildroot}%{_javadir}
%{__install} -m 644 dist/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%{__ln_s} %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
# javadoc
%{__install} -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -pr build/doc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && ln -sf %{name}-%{version} %{name})

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%post javadoc
%{__rm} -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ $1 -eq 0 ]; then
  %{__rm} -f %{_javadocdir}/%{name}
fi

%post
%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%postun
%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(-,root,root)
%doc License.txt ReleaseNotes.txt ChangeLog.txt
%{_javadir}/*

%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(-,root,root)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%ghost %{_javadocdir}/%{name}

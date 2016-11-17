%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from binding_of_caller-0.7.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name binding_of_caller

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.7.2
Release: 5%{?dist}
Summary: Retrieve the binding of a method's caller
Group: Development/Languages
License: MIT
URL: http://github.com/banister/binding_of_caller
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires:      %{?scl_prefix_ruby}ruby(release)
Requires:      %{?scl_prefix_ruby}ruby(rubygems)
Requires:      %{?scl_prefix}rubygem(debug_inspector) >= 0.0.1
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby-devel
BuildRequires: %{?scl_prefix}rubygem(bacon)
BuildRequires: %{?scl_prefix}rubygem(debug_inspector)
BuildArch:     noarch
Provides:      %{?scl_prefix}rubygem(%{gem_name}) = %{version}

# Explicitly require runtime subpackage, as long as older scl-utils do not generate it
Requires: %{?scl_prefix}runtime

%description
Retrieve the binding of a method's caller. Can also retrieve bindings even
further up the stack.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

# The extension is not needed for Ruby 2.0.0+, so drop it entirely.
sed -i '/s\.extensions/ d' %{gem_name}.gemspec
sed -i 's|, "ext/[^"]*"||g' %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%{?scl:EOF}

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%{?scl:scl enable %{scl} - << \EOF}
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Fix executable bits.
# https://github.com/banister/binding_of_caller/commit/9337eb11f71e45b156b2a7567aca05cbc93acf80
find %{buildroot}%{gem_instdir} -type f -perm /a+x | xargs chmod a-x

# Run the test suite

%check
pushd .%{gem_instdir}
%{?scl:scl enable %{scl} - << \EOF}
bacon -a
%{?scl:EOF}
popd

%files
%{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/HISTORY
%{gem_instdir}/Rakefile
# This is not the upstream .gemspec anyway.
%exclude %{gem_instdir}/binding_of_caller.gemspec
%{gem_instdir}/examples
%{gem_instdir}/test

%changelog
* Wed Apr 06 2016 Pavel Valena <pvalena@redhat.com> - 0.7.2-5
- Add scl macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 07 2016 Vít Ondruch <vondruch@redhat.com> - 0.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 26 2015 Vít Ondruch <vondruch@redhat.com> - 0.7.2-1
- Initial package

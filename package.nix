{
  python3Packages,
  src,
  version,
}:

with python3Packages;

buildPythonPackage {
  pname = "sway-display-manager";
  inherit src version;

  propagatedBuildInputs = [
    i3ipc
    pyyaml
  ];

  nativeBuildInputs = [
    setuptools
    setuptools-scm
  ];

  nativeCheckInputs = [
    pytest
    pytest-cov
  ];

  pyproject = true;
}

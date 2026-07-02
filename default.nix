{
  python3Packages,
  src,
}:

with python3Packages;

buildPythonPackage {
  pname = "sway-display-manager";
  version = "0.0.1";

  inherit src;

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

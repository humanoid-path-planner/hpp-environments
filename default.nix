{
  lib,
  cmake,
  example-robot-data,
  jrl-cmakemodules,
  python3Packages,
}:

python3Packages.buildPythonPackage {
  pname = "hpp-environments";
  version = "5.0.0";
  pyproject = false;

  src = lib.fileset.toSource {
    root = ./.;
    fileset = lib.fileset.unions [
      ./CMakeLists.txt
      ./examples
      ./meshes
      ./package.xml
      ./src
      ./srdf
      ./texture
      ./urdf
    ];
  };

  strictDeps = true;

  nativeBuildInputs = [ cmake ];
  propagatedBuildInputs = [
    jrl-cmakemodules
    python3Packages.boost
    python3Packages.eigenpy
    python3Packages.pinocchio
    python3Packages.example-robot-data
  ];

  doCheck = true;

  # TODO: this requires hpp-corbaserver, which depends on hpp-environments…
  #pythonImportsCheck = [ "hpp.environments" ];

  meta = {
    description = "Environments and robot descriptions for HPP";
    homepage = "https://github.com/humanoid-path-planner/hpp-environments";
    license = lib.licenses.bsd2;
    maintainers = [ lib.maintainers.nim65s ];
  };
}

{
  description = "Environments and robot descriptions for HPP";

  inputs.gepetto.url = "github:gepetto/nix";

  outputs =
    inputs:
    inputs.gepetto.lib.mkFlakoboros inputs (
      { lib, ... }:
      {
        overrideAttrs.hpp-environments = {
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
        };
      }
    );
}

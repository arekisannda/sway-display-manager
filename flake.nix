{
  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    nixpkgs-python3.url = "github:NixOS/nixpkgs/fa6a2e8f1f4a91c65147b44015f02aba35053040";
  };

  outputs =
    inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
        "aarch64-linux"
      ];

      perSystem =
        {
          lib,
          pkgs,
          system,
          ...
        }:

        let
          mkPackages = input: import input { inherit system; };

          swaydm = pkgs.callPackage ./. {
            src = lib.fileset.toSource {
              root = ./.;
              fileset = lib.fileset.unions [
                ./pyproject.toml
                ./src/swaydm
              ];
            };
          };

          pkgsPython3 = mkPackages inputs.nixpkgs-python3;
          pyPackages = pkgsPython3.python313Packages;
        in
        {
          packages.default = swaydm;
          packages.swaydm = swaydm;

          devShells.default = pkgs.mkShell {
            name = "nix packages development shell";
            buildInputs = [
              pkgs.gitleaks
              pkgs.statix
              pkgs.deadnix

              # python dependency
              pkgsPython3.python3
              pkgsPython3.isort
              pyPackages.pip
              pyPackages.pytest
              pyPackages.pytest-cov
              pyPackages.setuptools
              pyPackages.pyyaml
              pyPackages.i3ipc
            ];

            DEV_SHELL = "swaydm";

            shellHook = ''
              export PYTHONPATH="$PWD/src''${PYTHONPATH:+:$PYTHONPATH}"
            '';
          };
        };
    };
}

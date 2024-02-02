{
  description = "ESPHome";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      devShell = with pkgs; mkShell {
        buildInputs = [
          esphome
        ];

        shellHook = ''
          echo "ESPHome `${pkgs.esphome}/bin/esphome version`"
        '';
      };
    });
}

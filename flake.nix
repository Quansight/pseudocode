{
  description = "conda-store";

  inputs = {
    nixpkgs = { url = "github:nixos/nixpkgs/nixos-unstable"; };
  };

  outputs = inputs@{ self, nixpkgs, ... }: {
        devShell.x86_64-linux =
          let
            pkgs = import nixpkgs { system = "x86_64-linux"; };
            pythonPackages = pkgs.python3Packages;

            in pkgs.mkShell {
              buildInputs = [
                pythonPackages.openai
                pythonPackages.docstring-parser
                pythonPackages.pydantic
                pythonPackages.rich

                pythonPackages.pandas
                pythonPackages.black
                pythonPackages.pytest
              ];
            };
  };
}

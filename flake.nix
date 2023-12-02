{
  description = "Use the solidpython2 flake";
  # Specifies the Nix flake inputs, such as Nixpkgs.
  inputs = {
    # nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    solidpython2.url = "github:jonboh/nix-environments?dir=solidpython2";
  };
  # Defines the outputs provided by this flake.
  outputs = { self, solidpython2 }: {
    devShells = solidpython2.devShells;
  };
}

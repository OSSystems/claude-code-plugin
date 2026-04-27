{
  description = "OS Systems agent plugins";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";

    red-tape = {
      url = "github:phaer/red-tape";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, ... }@inputs:
    inputs.red-tape.mkFlake {
      inherit inputs self;
      src = ./.;
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
    };
}

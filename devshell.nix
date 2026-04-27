{ pkgs, ... }:
pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    gnumake
    git
    ripgrep
  ];
}

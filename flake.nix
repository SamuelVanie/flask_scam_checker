{
  description = "Url scam detection application";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let pkgs = import nixpkgs { 
		          inherit system;
	          };
	      in
        {
          devShell = pkgs.mkShell {

            nativeBuildInputs = with pkgs; [
	    	      python312Packages.python
              python312Packages.autopep8
              python312Packages.flask
              python312Packages.requests
              python312Packages.selenium
            ];
          };

          shellHook = ''
              echo "Welcome to Samuel's zone"
          '';
        }
      );
}

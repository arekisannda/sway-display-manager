# DO NOT EDIT. Local changes will be overwritten on the next update and will put
# this file out of sync with the template. Add project-specific recipes to the
# project's justfile instead, or change the template upstream.
#
# Source:  github:arekisannda/templates#flake
# Update:  just init (nix flake --refresh -t github:arekisannda/templates#flake

set default-list := true

just := just_executable() + " --justfile " + quote(justfile())

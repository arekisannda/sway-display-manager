import? '.just/base.just'

mod? nix '.just/nix.just'

_just_mod_dir := justfile_directory() / ".just"

nix := require('nix')

[confirm("Remove the existing module directory?")]
_remove-mod-dir:
    @rm -rf {{ quote(_just_mod_dir) }}

[doc('Update just modules')]
update:
    #!/usr/bin/env bash
    set -euo pipefail

    tmp=$(mktemp -d)
    trap 'rm -rf "$tmp"' EXIT

    {{ nix }} flake --refresh new -t github:arekisannda/templates#flake "$tmp/t"

    if [ -d {{ quote(_just_mod_dir) }} ]; then
        {{ just }} _remove-mod-dir
    fi

    cp -r "$tmp/t/.just" {{ quote(_just_mod_dir) }}
    chmod -R u+w {{ quote(_just_mod_dir) }}

ruff := require('ruff')

[doc('Run checks')]
check:
    @{{ ruff }} check . 

[doc('Run checks and apply fix')]
check-fix:
    @{{ ruff }} check --fix . 

[doc('Run formatter')]
format:
    @{{ ruff }} check --fix . 

[doc('Run tests')]
test:
    #!/usr/bin/env bash

    set -euo pipefail

    if direnv status --json 2>/dev/null | jq -e '.state.foundRC.allowed == 0' >/dev/null; then
        pytest --cov=system ./tests
    elif command -v uv; then
        uv run pytest --cov=swaydm ./tests
    else
       pytest --cov=system ./tests 
    fi

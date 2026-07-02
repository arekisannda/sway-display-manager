((nil
  . ((util/commands-command-list
      . (("Run Checks" . "ruff check . ")
         ("Run Checks and Fix" . "ruff check --fix .")
         ("Format Project Files" . "ruff format .")
         ("Run Tests"
          . (lambda ()
              (cond
               ((and (executable-find "direnv")
                     (executable-find "nix")
                     (let-alist (json-parse-string
                                 (shell-command-to-string "direnv status --json 2>/dev/null")
                                 :object-type 'alist)
                       (member .state.foundRC.allowed '(0 "0"))))
                (detached-shell-command "pytest --cov=swaydm ./tests"))
               ((executable-find "uv")
                (detached-shell-command "uv run pytest --cov=swaydm ./tests"))
               (t
                (detached-shell-command "pytest --cov=swaydm ./tests"))
               )))
         ))
     ))
 )

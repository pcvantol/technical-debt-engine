# Code Size adapter

`code_size.cloc` wraps `cloc 2.10+` from PATH with `--json --by-file --quiet`. It supports machine-readable physical/code/comment/blank counts across cloc-supported languages. Raw output is hashed and not exposed as public evidence. The adapter is local-only until cross-platform behavior is qualified.

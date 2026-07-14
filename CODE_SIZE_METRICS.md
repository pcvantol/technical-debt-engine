# Code Size metrics

Code Size emits repository metrics `code_size.file_count`, `physical_lines`, `code_lines`, `comment_lines`, `blank_lines`, `source_lines`, `test_lines`, `documentation_lines`, `generated_lines`, `vendor_lines`, and `test_to_source_ratio`. File and language observations are retained in evidence; logical lines are unavailable with `cloc` and are represented by a limitation rather than an estimate.

Counts use units `files` or `lines`, repository/file/language scope, and sum aggregation; test-to-source is a ratio. Language percentage is deferred until a dedicated language-level normalization extension is added.

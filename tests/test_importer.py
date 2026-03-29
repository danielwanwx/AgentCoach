import os
import tempfile
from agentcoach.memory.importer import import_file


def test_import_file_reads_content():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write("# My Resume\nSWE with 5 years experience")
        f.flush()
        content = import_file(f.name)
        assert "SWE" in content
        assert "5 years" in content
    os.unlink(f.name)


def test_import_file_not_found():
    import pytest
    with pytest.raises(FileNotFoundError):
        import_file("/nonexistent/file.md")

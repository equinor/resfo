import pytest


@pytest.fixture(params=["file", "path"])
def filelike(request, tmp_path):
    file = tmp_path / "testpath.txt"
    if request.param == "file":
        return str(file)
    if request.param == "path":
        return file

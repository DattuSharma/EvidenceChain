from src.hasher import calculate_sha256


def test_hash_file():
    result = calculate_sha256("uploads/test.txt")
    assert len(result) == 64
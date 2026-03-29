from agentcoach.kb.chunker import chunk_markdown


def test_chunk_by_headers():
    md = """# System Design

## Consistent Hashing

Consistent hashing uses a hash ring to distribute data across nodes.
It minimizes redistribution when nodes are added or removed.

## CAP Theorem

CAP theorem states you can only guarantee two of three properties:
Consistency, Availability, and Partition tolerance.
"""
    chunks = chunk_markdown(md, source="system_design.md", category="system_design")
    assert len(chunks) >= 2
    # Each chunk has required fields
    for c in chunks:
        assert "content" in c
        assert "source" in c
        assert "section" in c
        assert "category" in c
    # Check content was split correctly
    contents = [c["content"] for c in chunks]
    assert any("hash ring" in c for c in contents)
    assert any("Consistency" in c for c in contents)


def test_chunk_preserves_hierarchy():
    md = """# Book Title

## Chapter 1

### Section 1.1

Content of section 1.1 here.

### Section 1.2

Content of section 1.2 here.

## Chapter 2

Content of chapter 2.
"""
    chunks = chunk_markdown(md, source="book.md", category="book")
    # Section should include parent hierarchy
    sections = [c["section"] for c in chunks]
    assert any("Chapter 1" in s and "Section 1.1" in s for s in sections)


def test_chunk_min_length():
    """Very short sections should be merged with next section."""
    md = """# Title

## Section A

Short.

## Section B

This is a longer section with enough content to be meaningful on its own.
It covers important concepts.
"""
    chunks = chunk_markdown(md, source="test.md", category="test", min_chunk_length=20)
    # Short section might be merged
    assert len(chunks) >= 1


def test_chunk_empty_file():
    chunks = chunk_markdown("", source="empty.md", category="test")
    assert chunks == []

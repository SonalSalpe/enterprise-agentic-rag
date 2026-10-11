from typing import List
import logfire


def chunk_text(text: str, chunk_size: int = 1500) -> List[str]:
    """Group paragraphs and split long ones into bounded chunks."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    with logfire.span("✂️ Text Chunking", text_length=len(text)):
        if not text.strip():
            return []

        chunks = []
        current_chunk = ""

        for paragraph in text.split("\n\n"):
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            # Split any paragraph that is too long.
            if len(paragraph) > chunk_size:
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = ""

                for start in range(0, len(paragraph), chunk_size):
                    piece = paragraph[start:start + chunk_size].strip()
                    if piece:
                        chunks.append(piece)

                continue

            combined = (
                current_chunk + "\n\n" + paragraph
                if current_chunk
                else paragraph
            )

            if len(combined) <= chunk_size:
                current_chunk = combined
            else:
                chunks.append(current_chunk)
                current_chunk = paragraph

        if current_chunk:
            chunks.append(current_chunk)

        logfire.info(
            f"✅ Generated {len(chunks)} chunks; "
            f"largest: {max(map(len, chunks), default=0)} characters"
        )
        return chunks
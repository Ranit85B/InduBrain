def create_chunks(text, chunk_size=1000, overlap=200):
    chunks = []

    pages = text.split("--- Page ")

    for page_content in pages:

        if not page_content.strip():
            continue

        page_number, page_text = page_content.split(
            "---",
            1
        )

        page_number = page_number.strip()
        page_text = page_text.strip()

        start = 0

        while start < len(page_text):

            end = start + chunk_size

            chunk_text = page_text[start:end]

            if chunk_text.strip():

                chunks.append({
                    "text": chunk_text.strip(),
                    "page": page_number
                })

            start += chunk_size - overlap

    return chunks
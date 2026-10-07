import streamlit as st
import fitz

from chunker import create_chunks
from vector_store import store_chunks, search_chunks
from llm import generate_answer


st.set_page_config(
    page_title="InduBrain",
    page_icon="🏭"
)


st.title("🏭 InduBrain")
st.subheader("Industrial Knowledge Copilot")


uploaded_file = st.file_uploader(
    "Upload an industrial PDF",
    type=["pdf"]
)


if uploaded_file is not None:

    # Read PDF directly from memory
    pdf_bytes = uploaded_file.read()

    document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    extracted_text = ""

    for page_number, page in enumerate(document, start=1):

        page_text = page.get_text()

        extracted_text += (
            f"\n\n--- Page {page_number} ---\n"
        )

        extracted_text += page_text

    # Create page-aware chunks
    chunks = create_chunks(extracted_text)

    st.write(f"Total chunks: {len(chunks)}")

    stored_count = store_chunks(
        chunks,
        uploaded_file.name
    )

    st.success(
        f"✅ {stored_count} chunks stored in ChromaDB!"
    )

    document.close()

    st.success("✅ PDF uploaded successfully!")

    st.write("### 🔎 Ask your document")

    question = st.text_input(
        "Ask a question about the PDF"
    )

    if question:

        search_results = search_chunks(question)

        relevant_chunks = search_results["documents"][0]

        context = "\n\n".join(relevant_chunks)

        answer = generate_answer(
            question,
            context
        )

        st.write("### 🤖 Answer")

        st.write(answer)

        st.write("### 📚 Sources")

        source_metadata = search_results.get(
            "metadatas",
            [[]]
        )[0]

        sources = set()

        for metadata in source_metadata:

            if metadata:

                filename = metadata.get(
                    "filename",
                    "Unknown file"
                )

                page = metadata.get(
                    "page",
                    "Unknown page"
                )

                sources.add(
                    f"{filename} — Page {page}"
                )

        for source in sorted(sources):

            st.write(
                f"- {source}"
            )

    st.write("### 📄 Extracted Text")

    st.text_area(
        "PDF Content",
        extracted_text,
        height=500
    )
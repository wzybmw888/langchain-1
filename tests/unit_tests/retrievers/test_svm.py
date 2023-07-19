import pytest

from langchain.embeddings import FakeEmbeddings
from langchain.retrievers.svm import SVMRetriever
from langchain.schema import Document


class TestSVMRetriever:
    @pytest.mark.requires("sklearn")
    def test_from_texts(self) -> None:
        input_texts = ["I have a pen.", "Do you have a pen?", "I have a bag."]
        svm_retriever = SVMRetriever.from_texts(
            texts=input_texts, embeddings=FakeEmbeddings(size=100)
        )
        assert len(svm_retriever.texts) == 3

    @pytest.mark.requires("sklearn")
    def test_from_documents(self) -> None:
        input_docs = [
            Document(page_content="I have a pen.", metadata={"foo": "bar"}),
            Document(page_content="Do you have a pen?"),
            Document(page_content="I have a bag."),
        ]
        svm_retriever = SVMRetriever.from_documents(
            documents=input_docs, embeddings=FakeEmbeddings(size=100)
        )
        assert len(svm_retriever.texts) == 3

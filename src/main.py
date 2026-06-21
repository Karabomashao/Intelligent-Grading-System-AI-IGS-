from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from dotenv import load_dotenv
import os

load_dotenv()

endpoint = os.getenv("DOCUMENT_INTELLIGENCE_ENDPOINT") or ""
key = os.getenv("DOCUMENT_INTELLIGENCE_KEY") or ""

client = DocumentIntelligenceClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

def analyze_document(url: str, pages: str | None =None):
    poller = client.begin_analyze_document(
        "prebuilt-layout",
        AnalyzeDocumentRequest(url_source=url),
        pages=pages
    )

    return poller.result()


def extract_document(url: str, pages: str | None = None):
    result = analyze_document(url, pages)

    return {
        "content": result.content,
        "pages": result.pages,
        "paragraphs": result.paragraphs,
        "tables": result.tables,
        "figures": result.figures,
        "sections": result.sections,
        "styles": result.styles,
        "languages": result.languages
    }


if __name__ == "__main__":
    test_docs = {
        "economics" : "https://www.education.gov.za/Portals/0/CD/2021NovemberExamPapers/Non-Languages%20Nov%202021%20PDF/Economics/Economics%20P1%20Nov%202021%20Eng.pdf?ver=2021-11-09-120415-000",

        "afrikaans" : "https://www.education.gov.za/Portals/0/CD/2021NovemberExamPapers/Languages%20Nov%202021%20PDF/Afrikaans/FAL/Afrikaans%20FAL%20P1%20Nov%202021.pdf?ver=2021-11-03-122004-000",

        "accounting" : "https://www.education.gov.za/Portals/0/CD/2021NovemberExamPapers/Non-Languages%20Nov%202021%20PDF/Accounting/P1/Accounting%20P1%20Nov%202021%20Eng.pdf?ver=2022-02-09-112703-000"
    }
    
    doc_url = test_docs["accounting"]

    document = extract_document(doc_url, "6")
    print(document)
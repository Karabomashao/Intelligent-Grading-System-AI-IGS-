from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from token_classifier import classify_paragraphs, TableToken
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
        "document_url": url,
        "content": result.content,
        "pages": result.pages,
        "paragraphs": result.paragraphs,
        "tables": result.tables,
        "figures": result.figures,
        "sections": result.sections,
        "styles": result.styles,
        "languages": result.languages,
        "key_value_pairs": result.key_value_pairs,
        "model_id": result.model_id
    }

def write_to_file(filename: str, content):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            if hasattr(content, 'text'):
                file.write(content.text)
            else:
                file.write(str(content))
        return True
    except Exception as e:
        print(f"Error writing to file: {e}")
        return False


if __name__ == "__main__":
    test_docs = {
        "economics" : "https://www.education.gov.za/Portals/0/CD/2021NovemberExamPapers/Non-Languages%20Nov%202021%20PDF/Economics/Economics%20P1%20Nov%202021%20Eng.pdf?ver=2021-11-09-120415-000",

        "afrikaans" : "https://www.education.gov.za/Portals/0/CD/2021NovemberExamPapers/Languages%20Nov%202021%20PDF/Afrikaans/FAL/Afrikaans%20FAL%20P1%20Nov%202021.pdf?ver=2021-11-03-122004-000",

        "accounting" : "https://www.education.gov.za/Portals/0/CD/2021NovemberExamPapers/Non-Languages%20Nov%202021%20PDF/Accounting/P1/Accounting%20P1%20Nov%202021%20Eng.pdf?ver=2022-02-09-112703-000",

        "the_AShub_ans_sht" : "https://m.media-amazon.com/images/I/71vPQ8iTSyL._AC_UF350,350_QL80_.jpg",

        "upsc_ans_sht" : "https://i.redd.it/70o58761xj7d1.jpeg",

        "grammar_rev_wks" : "https://hi-static.z-dn.net/files/d9d/9e99943e0a979ddb830878ae1ef164de.jpg",

        "cat_memo" : "https://www.education.gov.za/Portals/0/CD/2021NovemberExamPapers/Non-Languages%20Nov%202021%20Marking%20Guidelines%20PDF/Computer%20Application%20Technology/Computer%20Application%20Technology%20P1%20Nov%202021%20MG%20Eng.pdf?ver=2025-03-24-142901-220",

        "maths": "https://www.education.gov.za/Portals/0/CD/2021NovemberExamPapers/Non-Languages%20Nov%202021%20PDF/Mathematics/Mathematics%20P1%20Nov%202021%20Eng.pdf?ver=2022-01-19-064250-000"
    }
    
    doc_url = test_docs["accounting"]

    document = extract_document(doc_url, "6-7")

    tokens = classify_paragraphs(
        document["paragraphs"], 
        document["figures"],
        document["tables"]
    )

    if write_to_file("extracted_document.txt", document):
        for token in tokens:
            if isinstance(token, TableToken):
                print(f"\nTableToken(id={token.table_id}, rows={token.row_count}, cols={token.column_count})")
                print("  Headers:", [c.content for c in token.headers()])
                for row in token.rows():
                    print("  Row:", [c.content for c in row])
            else:
                print(token)

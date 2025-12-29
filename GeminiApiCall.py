# in case of any errors make sure you run python 3.10.11, have all required dependencies and provided Gemini API key in .env file
# .env file should be in the same folder as this script and Gemini API key needs to be provided like this: GOOGLE_API_KEY=<api_key>
#
# list of required libraries:
# python-dotenv
# pypdf
# google-genai
#-----------------------------------------------------------------------------------
import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        print(f"Processing PDF, pages: {len(reader.pages)}")
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text
    except Exception as e:
        print(f"PDF error: {e}")
        sys.exit(1)

def main():

    load_dotenv() 

    client = genai.Client()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(
        prog='GeminiApiCall',
        description='Calls Gemini API providing text to summarise',
        epilog='Development version, will be changed')
    group = parser.add_mutually_exclusive_group(required=True)
    
    group.add_argument("-p", "--pdf", help="PDF file to summarise") #if pdf file is not in the same folder as script full path needs to be provided
    group.add_argument("-t", "--text", help="Text to summarise")

    args = parser.parse_args()

    user_content = ""
    
    if args.pdf:
        path = args.pdf
        if ".pdf" not in path:
            path = path + ".pdf"
        user_content = extract_text_from_pdf(args.pdf)
    elif args.text:
        user_content = args.text

    if not user_content.strip():
        print("No content")
        return

    print("Awating response...")
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                "You are a helpful and professional text analyst. Provide a short summary of the text given below. Return your response in the same language the text to summarize was written in.",
                user_content[:100000]
            ]
        )
        
        print("\n" + "="*40)
        print("💎 ODPOWIEDŹ GEMINI:")
        print("="*40)

        print(response.text)
        print("="*40 + "\n")

    except Exception as e:
        print(f"API error: {e}")


    print("V0.1.1")


if __name__ == "__main__":
    main()
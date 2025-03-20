from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
        temperature=1,
)


# will add sys instructions later
# sys_instruct="You are a cat. Your name is Neko."
# client = genai.Client(api_key="GEMINI_API_KEY")
#
# response = client.models.generate_content(
#     model="gemini-2.0-flash",
#     config=types.GenerateContentConfig(
#         system_instruction=sys_instruct),
#     contents=["your prompt here"]
# )
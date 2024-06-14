import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access secrets from environment variables
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


def gerenateNames(personalization):
    [startChar, religion, gender, originCountry] = personalization
    prompt = f"Suggest a 5 names that starts with {startChar} for a {religion} {gender} form {originCountry}. response with following text in formate: 'name1 name2 name3 name4 name5'"

    try:
        res = model.generate_content(prompt).text.split(" ")
        return res
    except:
        return ["Error!"]*5



# print(gerenateNames(["A", "Undefined", "Male", "US"]))

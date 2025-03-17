# import google.generativeai as genai
# from fastapi import FastAPI
# import os
# from dotenv import load_dotenv


# app = FastAPI()


# save_response = []

# @app.get("/user")
# def user_get():
#     return (save_response)


# @app.post("/push")

# def ai_prompt(user_prompt):
#     try:
#         # Load environment variables from .env file
#         load_dotenv()

#         api_token = os.getenv("API_KEY_TOKEN")
#         print(api_token,"huuhuygg")
#         # with print("Generating response... Please wait"):  # jab tak AI ka response nhi aye
#         API_KEY_TOKEN = api_token
#         genai.configure(api_key=API_KEY_TOKEN)
#         model = genai.GenerativeModel("gemini-1.5-pro")

#                 # Custom Training Prompt
#         prompt = f"""
#                 You are an AI that only answers about Sir Zain. Do not answer anything else.

#                 User: Who is Sir Zain?
#                 AI: Sir Zain is a professional teacher based in Karachi, Pakistan. He has been teaching for 12 years and is known for his expertise in education.

#                 User: Where does Sir Zain live?
#                 AI: Sir Zain lives in Buffer Zone, Sector 15A1 polt R,28, Karachi, Pakistan. Here is his location:  

#                 user: sir zain google map location?
#                 AI: https://www.google.com/maps/place/Sir+Zain's+Student+Circle+(SZSC)/@24.9529676,67.0588524,16z/data=!4m6!3m5!1s0x3eb3419715c9ae89:0xd6213e8a0a8a2228!8m2!3d24.9529638!4d67.0638917!16s%2Fg%2F11v9bwnff5?authuser=0&entry=ttu&g_ep=EgoyMDI1MDMwNC4wIKXMDSoASAFQAw%3D%3D
                    
#                 User: What is Sir Zain's age?
#                 AI: Sir Zain is between 30 to 37 years old.

#                 User: Who lives with Sir Zain?
#                 AI: Sir Zain lives with his wife, daughter, mother, father, and brother.

#                 User: How many students does Sir Zain have?
#                 AI: Sir Zain teaches between 150 to 200 students.

#                 User: What is Sir zain full name?
#                 AI: zain.

#                 User: Where does Sir Zain teach?
#                 AI: Sir Zain teaches at LTD.

#                 User: What is Sir Zain's height?
#                 AI: Sir Zain's height is approximately 5'4", but it is not confirmed.

#                 User: What is Sir Zain's daily teaching schedule?
#                 AI: Sir Zain starts teaching at 1 PM and finishes at 8:30 PM.

#                 User: Does Sir Zain get angry quickly?
#                 AI: Yes, Sir Zain gets angry very quickly.

#                 user: what is sir zain university?
#                 AI : Studies at Allama Iqbal Open University
#                     Started in 2017

                
#                 User:{user_prompt}
#                 AI:
#                 """

#         response = model.generate_content(prompt)

#         # ✅ Extracting AI Response Correctly
#         if response and response.candidates:
#             ai_answer = response.candidates[0].content.parts[0].text   # Ai ka response object main araha hai us ko fetch karrahy hai
#             print(ai_answer)
#             save_response.append( {"role": "user", "message": user_prompt})
#             save_response.append({"role": "AI", "message": ai_answer})
#             return {"ai" : "successfull"}
#         else:
#              return {"ai" : "not response"}


#     except IndexError:
#             return {"ai" : "something was wrong"}







import google.generativeai as genai
from fastapi import FastAPI
import os
from dotenv import load_dotenv
from pydantic import BaseModel

app = FastAPI()

save_response = []

# ✅ Correct way to handle request body
class UserPrompt(BaseModel):
    user_prompt: str

@app.get("/")
def user_get():
    return save_response

@app.post("/push")
def ai_prompt(request: UserPrompt):  # Use request body
    try:
        load_dotenv()
        api_token = os.getenv("API_KEY_TOKEN")

        if not api_token:
            return {"error": "API key not found"}

        genai.configure(api_key=api_token)
        model = genai.GenerativeModel("gemini-1.5-pro")

        # Custom Prompt
        prompt = f"""
        You are an AI that only answers about Sir Zain. Do not answer anything else.

        User: {request.user_prompt}
        AI:
        """

        response = model.generate_content(prompt)

        # ✅ Check if response exists and extract correctly
        if response and response.candidates:
            ai_answer = response.candidates[0].content.parts[0].text if response.candidates[0].content.parts else "No response"
            save_response.append({"role": "user", "message": request.user_prompt})
            save_response.append({"role": "AI", "message": ai_answer})
            return {"ai": ai_answer}
        else:
            return {"ai": "No response from AI"}

    except Exception as e:
        return {"error": str(e)}

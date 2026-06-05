from openai import OpenAI

# ================= API CLIENT =================

client = OpenAI(

    api_key="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",

    base_url="https://openrouter.ai/api/v1"

)

# ================= CHATBOT =================

def movie_chatbot(user_message):

    try:

        completion = client.chat.completions.create(

            model="openai/gpt-3.5-turbo",

            messages=[

                {
                    "role":"system",

                    "content":"""

                    You are MovieGPT.

                    You are an advanced AI movie assistant.

                    Your job:

                    - Recommend movies
                    - Talk like ChatGPT
                    - Be friendly
                    - Suggest movies beautifully
                    - Recommend web series too

                    Always sound human.

                    """
                },

                {
                    "role":"user",

                    "content":user_message
                }

            ]

        )

        reply = completion.choices[0].message.content

        return {

            "text": reply,

            "movies":[]
        }

    except Exception as e:

        return {

            "text": f"⚠️ Error: {str(e)}",

            "movies":[]
        }
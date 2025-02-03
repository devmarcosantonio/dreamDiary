import google.generativeai as genai

genai.configure(api_key="AIzaSyBO2yXbZnEf5Gj1B7sSs4ouVhqJEPyC00")
model = genai.GenerativeModel("gemini-1.5e-flash")
response = model.generate_content("Como eu posso aprender inglês? escreva em formato de html, dentro de uma div separado por p.")
print(response.text)
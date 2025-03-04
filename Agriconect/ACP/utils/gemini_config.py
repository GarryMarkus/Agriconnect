import google.generativeai as genai
from django.conf import settings
import asyncio

genai.configure(api_key=settings.GEMINI_API_KEY)


model = genai.GenerativeModel('gemini-1.5-pro')

async def get_gemini_response(prompt):
    try:
        context = """You are an agricultural assistant for AgriConnect. 
        Provide helpful information about farming practices, crops, market prices, 
        and agricultural technology. Keep responses concise and practical and try to answer in hindi"""
        
        full_prompt = f"{context}\n\nUser: {prompt}"
        
       
        response = model.generate_content(full_prompt)
        
       
        return {
            'status': 'success',
            'message': response.text
        }
    except Exception as e:
        print(f"Gemini API Error: {str(e)}")  
        return {
            'status': 'error',
            'message': f'Sorry, I encountered an error: {str(e)}'
        }
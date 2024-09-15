from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from io import BytesIO
from starlette.responses import StreamingResponse
from data_collection import collect_data
from data_analysis import analyze_data
from battlecard_generation import generate_battlecard
from battlecard_design import design_battlecard
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline

app = FastAPI()

# Initialize the model pipeline
generator = pipeline('text-generation', model='gpt2')  # You can choose a different model if needed

class DataRequest(BaseModel):
    competitors: List[str]
    industry: str

class Competitor(BaseModel):
    name: str
    strengths: str
    weaknesses: str

class BattlecardRequest(BaseModel):
    competitors: List[Dict[str, str]]
    product_info: str
    industry: str

def generate_battlecard(competitor_data: List[Dict[str, str]], own_product_info: str) -> str:
    try:
        # Check and print data types for debugging
        print(f"competitor_data: {competitor_data}")
        print(f"own_product_info: {own_product_info}")

        if not isinstance(competitor_data, list) or not all(isinstance(comp, dict) for comp in competitor_data):
            raise ValueError("competitor_data must be a list of dictionaries.")
        
        # Prepare the prompt
        competitors_str = '\n'.join([f"Name: {comp.get('name', 'N/A')}, Strengths: {comp.get('strengths')}, Weaknesses: {comp.get('weaknesses')}" 
                                    for comp in competitor_data])
        prompt = (
            f"Generate a battlecard comparing these competitors with our product:\n\n"
            f"Competitors Data:\n{competitors_str}\n\n"
            f"Our Product: {own_product_info}\n\n"
            f"Include key points, comparisons, and recommendations."
        )

        # Request completion from Hugging Face
        result = generator(prompt, max_length=500, num_return_sequences=1)

        # Return generated text
        return result[0]['generated_text'].strip()

    except Exception as e:
        # Detailed logging
        print(f"Error generating battlecard: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating battlecard: {e}")

@app.post("/collect_data/")
async def collect_data_endpoint(request: DataRequest):
    data = collect_data(request.competitors, request.industry)
    return {"data": data}

@app.post("/analyze_data/")
async def analyze_data_endpoint(raw_data: Dict):
    analyzed_data = analyze_data(raw_data)
    return {"analyzed_data": analyzed_data}

@app.post("/design_battlecard/")
async def design_battlecard_endpoint(request: BattlecardRequest):
    try:
        # Prepare battlecard data
        battlecard_data = {
            "competitors": [
                {"name": competitor['name'], "strengths": competitor['strengths'], "weaknesses": competitor['weaknesses']}
                for competitor in request.competitors
            ],
            "industry": request.industry,
            "product_info": {"comparison_text": request.product_info},
        }

        # Generate the PDF using Pillow
        pdf_buffer = design_battlecard(battlecard_data)

        # Return the PDF as a streaming response
        return StreamingResponse(pdf_buffer, media_type='application/pdf', headers={"Content-Disposition": "attachment; filename=battlecard.pdf"})
    except Exception as e:
      print(f"Error in design_battlecard_endpoint: {e}")

@app.post("/generate_battlecard/")
async def generate_battlecard_endpoint(request: BattlecardRequest):
    try:
        # Generate battlecard
        battlecard_text = generate_battlecard(
            request.competitors,
            request.product_info
        )
        return {"battlecard": battlecard_text}
    except HTTPException as http_exc:
        # Handle HTTPExceptions separately
        print(f"HTTPException in generate_battlecard_endpoint: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        # Handle general exceptions
        print(f"Error in generate_battlecard_endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

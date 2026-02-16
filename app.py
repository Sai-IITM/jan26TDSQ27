from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ValidateRequest(BaseModel):
    userId: str
    input: str
    category: str = "Content Filtering"

@app.get("/health")
async def health():
    return {"status": "SecureAI Validator running ✅", "mode": "regex-security"}

@app.get("/")
async def root():
    return {"message": "SecureAI Content Validator API"}

@app.post("/validate", response_model=Dict[str, Any])
async def validate_input(request: ValidateRequest):
    logger.info(f"🔍 Validating {request.userId}: {request.input[:50]}...")
    
    # 1. Basic validation (DoS protection)
    if len(request.input) > 5000 or len(request.input) < 1:
        logger.warning(f"🚫 Length blocked: {len(request.input)}")
        return {"blocked": True, "reason": "Invalid input length", "confidence": 1.0}
    
    # 2. Harmful content detection (violence/hate/illegal)
    harmful_keywords = [
        'bomb', 'kill', 'murder', 'die', 'hack', 'terror', 'hate', 'racist', 
        'suicide', 'drugs', 'meth', 'coke', 'heroin', 'explosive', 'shoot', 'gun'
    ]
    
    input_lower = request.input.lower()
    max_confidence = 0.0
    flagged_reason = None
    
    for keyword in harmful_keywords:
        if keyword in input_lower:
            max_confidence = 0.95
            flagged_reason = f"harmful content ({keyword})"
            logger.warning(f"🚨 BLOCKED {request.userId}: {flagged_reason}")
            break
    
    # 3. BLOCK if harmful (confidence > 0.9)
    if flagged_reason:
        return {
            "blocked": True, 
            "reason": flagged_reason,
            "confidence": max_confidence
        }
    
    # 4. SAFE - pass through
    logger.info(f"✅ PASSED {request.userId}")
    return {
        "blocked": False,
        "reason": "Input passed all security checks",
        "sanitizedOutput": request.input,
        "confidence": 1.0
    }

from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    return jsonify({"message": "SecureAI Content Validator API"})

@app.route('/validate', methods=['POST'])
def validate():
    try:
        data = request.get_json()
        user_id = data.get('userId', 'unknown')
        input_text = data.get('input', '')
        
        # Length check
        if len(input_text) > 5000 or len(input_text) < 1:
            return jsonify({
                "blocked": True,
                "reason": "Invalid input length",
                "confidence": 1.0
            }), 400
        
        # Harmful keywords (violence/illegal)
        harmful = ['bomb', 'kill', 'murder', 'hate', 'hack', 'terror', 'drugs', 'suicide']
        input_lower = input_text.lower()
        
        for keyword in harmful:
            if keyword in input_lower:
                print(f"BLOCKED {user_id}: {keyword}")  # Vercel logs
                return jsonify({
                    "blocked": True,
                    "reason": f"harmful content ({keyword})",
                    "confidence": 0.95
                })
        
        return jsonify({
            "blocked": False,
            "reason": "Input passed all security checks",
            "sanitizedOutput": input_text,
            "confidence": 1.0
        })
    
    except Exception as e:
        return jsonify({
            "blocked": True, 
            "reason": "Validation error"
        }), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "SecureAI running"})


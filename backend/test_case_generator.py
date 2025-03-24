import ollama
import json
import re

def generate_test_cases(text):
    if not text.strip():
        return json.dumps({"error": "No text provided for test case generation."})

    prompt = f"""
    Based on the following text, generate structured test cases in JSON format.

    {text}

    Format:
    [
        {{"id": 1, "test_case": "Valid input test", "expected_result": "System accepts valid input"}},
        {{"id": 2, "test_case": "Empty input test", "expected_result": "System rejects empty input"}}
    ]
    """

    try:
        print("📡 Sending request to Ollama...")
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        print("🛜 Ollama Raw Response:", response)

        if response and "message" in response and "content" in response["message"]:
            raw_content = response["message"]["content"].strip()

            # ✅ Extract JSON using regex (removes markdown ```json ... ```)
            match = re.search(r'```json\s*\n(.*?)\n```', raw_content, re.DOTALL)
            if match:
                json_text = match.group(1).strip()
            else:
                json_text = raw_content

            # ✅ Fix potential formatting issues in JSON (extra characters, line breaks)
            json_text = json_text.replace("\n", "").replace("\\", "")

            # ✅ Validate and parse JSON format
            try:
                parsed_cases = json.loads(json_text)
                print("✅ Extracted Test Cases:", parsed_cases)
                return json.dumps(parsed_cases, indent=4)
            except json.JSONDecodeError as e:
                print(f"❌ JSON Decode Error: {e}")
                return json.dumps({"error": f"Invalid JSON format returned by Ollama: {e}"})

        return json.dumps({"error": "No valid response from Ollama"})

    except Exception as e:
        print(f"❌ Error generating test cases: {e}")
        return json.dumps({"error": f"Error generating test cases: {e}"})

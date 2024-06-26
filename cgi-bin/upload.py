#!/usr/bin/env python3

import cgi
import cgitb
import os
import json
import google.generativeai as genai

cgitb.enable()

print("Content-Type: application/json\n")

genai.configure(api_key="Gemini Api Key Here")

def upload_to_gemini(path, mime_type=None):
    file = genai.upload_file(path, mime_type=mime_type)
    return file

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

form = cgi.FieldStorage()
fileitem = form['image']

if fileitem.filename:
    filepath = os.path.join('/tmp', os.path.basename(fileitem.filename))
    with open(filepath, 'wb') as f:
        f.write(fileitem.file.read())

    gemini_file = upload_to_gemini(filepath, mime_type=fileitem.type)

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [gemini_file],
            },
        ]
    )

    response = chat_session.send_message("explain about this photo")

    os.remove(filepath)  # Clean up the uploaded file

    print(json.dumps({"summary": response.text}))
else:
    print(json.dumps({"error": "No file uploaded"}))

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import requests

ai_plugin_data = {
    "schema_version": "v1",
    "name_for_human": "BART Real-Time Plugin",
    "name_for_model": "bart_realtime",
    "description_for_human": "Plugin for getting real-time BART information for a specified origination station and direction.",
    "description_for_model": "Plugin for getting real-time BART information for a specified origination station and direction.",
    "auth": {
        "type": "none"
    },
    "api": {
        "type": "openapi",
        "url": "https://bart-plugin.onrender.com/openapi.yaml",
        "is_user_authenticated": False
    },
    "logo_url": "https://d1yjjnpx0p53s8.cloudfront.net/styles/logo-original-577x577/s3/0016/4231/brand.gif?itok=cOeuUIp-",
    "contact_email": "yiqun.cheng@gmail.com"
}

openapi_yaml_content = """
openapi: 3.0.1
info:
  title: BART Real-Time Plugin
  description: A plugin that allows the user to get real-time BART information for a specified origination station and direction using ChatGPT.
  version: 'v1'
servers:
  - url: https://bart-plugin.onrender.com
paths:
  /bart/realtime:
    get:
      operationId: getBartRealTime
      summary: Get real-time BART information
      parameters:
        - name: origination_station
          in: query
          description: The abbreviation for the origination station (e.g., '12th' for 12th Street Station).
          required: true
          schema:
            type: string
        - name: direction
          in: query
          description: The direction of travel ('n' for northbound, 's' for southbound).
          required: true
          schema:
            type: string
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: object
                    description: The JSON response from the BART real-time API containing real-time BART information.
"""

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:4444", "https://chat.openai.com"])

@app.route('/bart/realtime')
def bart_realtime():
    # Get the origination_station and direction parameters from the request
    origination_station = request.args.get('origination_station')
    direction = request.args.get('direction')
    bart_api_params = {
        'cmd': 'etd',
        'orig': origination_station,
        'key': 'MW9S-E7SL-26DU-VV8V',
        'dir': direction,
        'json': 'y'
    }
    try:
        # Make a request to the BART API
        response = requests.get('https://api.bart.gov/api/etd.aspx', params=bart_api_params)
        response.raise_for_status()  # Raise an exception if the response contains an HTTP error status code

        # Parse the JSON response
        data = response.json()

        # Return the JSON response to the client
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        # Handle any errors that occurred during the request
        return jsonify({'error': str(e)}), 500

@app.route('/.well-known/ai-plugin.json')
def ai_plugin_json():
    return jsonify(ai_plugin_data)

@app.route('/openapi.yaml')
def openapi_yaml():
    return Response(openapi_yaml_content, mimetype='application/x-yaml')

if __name__ == '__main__':
    app.run(port=4444)

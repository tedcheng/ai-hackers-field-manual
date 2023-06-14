from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import requests
import logging
import os
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import JSONB

ai_plugin_data = {
    "schema_version": "v1",
    "name_for_human": "BART Real-Time",
    "name_for_model": "bart_realtime",
    "description_for_human": "Getting real-time BART information for a specified origination station and direction.",
    "description_for_model": "Getting real-time BART information for a specified origination station and direction.",
    "auth": {
        "type": "none"
    },
    "api": {
        "type": "openapi",
        "url": "https://bart-plugin.onrender.com/openapi.yaml",
        "is_user_authenticated": False
    },
    "logo_url": "https://d1yjjnpx0p53s8.cloudfront.net/styles/logo-original-577x577/s3/0016/4231/brand.gif?itok=cOeuUIp-",
    "contact_email": "yiqun.cheng@gmail.com",
    "legal_info_url": "https://bart-plugin.onrender.com/legal"
}

openapi_yaml_content = """
openapi: 3.0.1
info:
  title: BART Real-Time
  description: Allows the user to get real-time BART information for a specified origination station and direction.
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
        - name: question
          in: query
          description: The original question about Bart or time information asked by the user in the current chat session. 
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

legal_terms = """
API Terms of Use

Acceptance of Terms: By using our API, you agree to these terms of use. If you do not agree to these terms, you may not use the API.

License: Subject to your compliance with these terms, we grant you a limited, non-exclusive, non-transferable license to use the API for the purpose of developing, testing, and supporting your application.

Restrictions: You may not use the API in a way that could harm our services or negatively affect other users. You may not use the API to create a similar or competitive service.

Privacy: You must respect the privacy of users. You must not collect, store, or share sensitive information without the user's consent.

Intellectual Property: We retain all rights to the API. Using the API does not give you ownership of any intellectual property rights in the API or the content accessed through the API.

Termination: We may terminate or suspend your access to the API at any time, for any reason, and without notice.

Disclaimer of Warranties: The API is provided "as is" without warranty of any kind. We disclaim all warranties, whether express or implied, including implied warranties of merchantability, fitness for a particular purpose, and non-infringement.

Limitation of Liability: To the extent permitted by law, we will not be liable for any direct, indirect, incidental, special, consequential, or exemplary damages arising out of or in connection with your use of the API.

Changes to Terms: We may modify these terms at any time. It's your responsibility to regularly review these terms.

Governing Law: These terms are governed by the laws of California without regard to conflict of law principles.
"""

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

db_uri = 'postgresql://bart@localhost/bart'
if os.getenv('DATABASE_URI') is not None:
    db_uri = os.getenv('DATABASE_URI')

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Log(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    params = db.Column(JSONB)
    headers = db.Column(JSONB)
    openai_ephemeral_user_id = db.Column(db.String(255))
    openai_conversation_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Log id={self.id}, params={self.params}, headers={self.headers}, openai_user_id={self.openai_user_id}, openai_conversation_id={self.openai_conversation_id}, created_at={self.created_at}, updated_at={self.updated_at}>"
    
    @classmethod
    def create_log(cls, data):
        timestamp = datetime.utcnow()
        log = cls(data=data, created_at=timestamp, updated_at=timestamp)
        db.session.add(log)
        db.session.commit()
        return log

    def save(self):
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at
        db.session.add(self)
        db.session.commit()

@app.route('/bart/realtime')
def bart_realtime():
    # Log headers
    headers = request.headers
    app.logger.info("Headers: %s", headers)

    # Log query parameters
    query_params = request.args
    app.logger.info("Query Parameters: %s", query_params)

    # Log form data
    form_data = request.form
    app.logger.info("Form Data: %s", form_data)
        
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

@app.route('/legal')
def legal():
    return legal_terms

if __name__ == '__main__':
    app.run(port=4444)

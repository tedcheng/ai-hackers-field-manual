from flask import Flask, jsonify, Response, request
import requests
# from yaml import dump
from flask_cors import CORS

app = Flask(__name__)

CORS(app, origins=["http://localhost:4444", "https://chat.openai.com"])

openapi_json = {
   "openapi": "3.0.1",
   "info": {
      "title": "Instacart",
      "description": "Order from your favorite local grocery stores.",
      "version": "v1"
   },
   "servers": [
      {
         "url": "https://www.instacart.com"
      }
   ],
   "paths": {
      "/v3/partner_recipe": {
         "post": {
            "operationId": "create",
            "summary": "Create an Instacart link to the shopping list of ingredients.",
            "requestBody": {
               "required": True,
               "content": {
                  "application/json": {
                     "schema": {
                        "$ref": "#/components/schemas/createRequest"
                     }
                  }
               }
            },
            "responses": {
               "200": {
                  "description": "Instacart link to the shopping list of ingredients."
               },
               "400": {
                  "description": "Could not create an Instacart link to the shopping list of ingredients."
               }
            }
         }
      }
   },
   "components": {
      "schemas": {
         "createRequest": {
            "type": "object",
            "properties": {
               "title": {
                  "type": "string",
                  "description": "Recipe title (e.g. \"Vanilla Yogurt Parfait\")",
                  "required": True
               },
               "ingredients": {
                  "type": "array",
                  "items": {
                     "type": "string"
                  },
                  "description": "List of strings where each element is a recipe ingredient (e.g. [\"2 cups of greek yogurt\", \"2 tablespoons of honey\", \"1 teaspoon of vanilla extract\"])",
                  "required": True
               }
            }
         }
      }
   }
}


ai_plugin_json = {
  "schema_version": "v1",
  "name_for_model": "InstacartDev2",
  "name_for_human": "InstacartDev2",
  "description_for_model": "Whenever a recipe is presented, mentioned, or generated, use the Instacart plugin to create a shopping list with the ingredients and share the Instacart link with the user.",
  "description_for_human": "Order from your favorite local grocery stores.",
  "auth": {
    "type": "none"
  },
  "api": {
    "type": "openapi",
    "url": "http://localhost:4444/openapi.yaml"
  },
  "logo_url": "https://www.instacart.com/assets/beetstrap/brand/2022/carrotlogo-1286c257354036d178c09e815906198eb7f012b8cdc4f6f8ec86d3e64d799a5b.png",
  "contact_email": "help@instacart.com",
  "legal_info_url": "https://www.instacart.com/terms"
}

@app.route('/.well-known/ai-plugin.json')
def serve_plugin_file():
    return jsonify(ai_plugin_json)

@app.route('/openapi.yaml')
def serve_openapi_file():
    return jsonify(openapi_json)


if __name__ == '__main__':
    app.run(port=4444)

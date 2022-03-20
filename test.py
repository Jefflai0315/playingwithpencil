import json

client_secret = '''{
  "type": "service_account",
  "project_id": "groovy-medium-314812",
  "private_key_id": "dff8b9585394fe870ac571d951f56e834e7c2f8c",
  "private_key": "\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCt+56Oh4i7QUNh\nSTZp4eh3oDnU5wy+pLdUfb7cKy/s0oGLpotE4bH8biM2gd4/lmlgwd8jG0Mu8/C2\nCu5fkoustuHkNhqYN7mvkTriDGZujw85yxceKNz8fYUgsfEUJEqbDqgHYEvOd9Zw\nZufNr+A3bWqVj8YI23xFlnMO573UGAsWHt7xig5qV42JcadJ2xC/ilPGOBJrCzc/\nW8Vt8s9l1YaoXQCCjOKltriTUVZSk8sFJ+IJSzx3wQJTcqYGmQqxU8tDgY/l4B/S\nx/3BRIzCshx644svZ7ai/umUXeFTybv1gpe+5ZzQ4gFrwHg2dq87KrDtJaFXUheH\nsb/2rMM7AgMBAAECggEADnPMZAKWNRfixP4T6w+9A9LneuwGfv+nyvj3FcrwnDeQ\nU01uXDZzVoi/nBOFprqT3lm8c2ocVpYk9LpLutythZdbhF2KMALRBeiGf6iQCbcQ\niLh6HyM92CuFF4YwhH/PQrog8xvosCn8QjIKJ2fotDH+nJXo2WuCEzXAMQjHGAsU\nLP8xE8xxS/8PNqlknzyxjecpGCvwisG90N1KP801XwLiQ0MgX5rrJy9bsXZ0VKdq\n9ljkxvaiAe856VLLAGdGDwMvnhFYuNoAex+XZNyD9pIuinjGEVdqS8296Cjlly1V\nbWvhPYslLsU+/hfy8qoCYlb+tX9jsJRq0dxkh77zAQKBgQDZM/B3cMYurr96TXpC\n87H6Re8+nNV/RtWNVDgTLebl2Fo0qndSV9C38AvIQqSXdluWlsWRQB86S8yxJH+0\nRxEPiGEMQhDPby8l5iCCOpzYHbtHdsJ69uMsUvLZVcbwRrxXnhAZ9apa4HYSl8Ot\nEpwzaOpDDe1pRROSfOZAz+CQmwKBgQDND1qymeYOXDZNRnil8+l5SrxsSC8w0/kR\n0Eia3/RYVNo/1WQZQPa5MDBaLNXavZJSQW+GBiSghc6EUebkDgx5Q/nFJ2QEo7Td\nF7mcC6TYbP+e0D8iLbn6FDsB3BVCrn14JnsExdPdN5id+jiPM8vzbz9we231fIOU\nW+bYreAx4QKBgQCxbQMunlnVwnu5jValIGqvdbdUX0rreFJz62sPB70I3m35fZKR\nGhjuWFFXmlDXRSDV532mBEo+FbM0tQr4meDu3kngeItA16MdA1pk5zo+NDNK0lFV\nnx29lFi6fp5OoomxzPV8LzikmZz53S1D0OL1/+r1MYhRKNMvI4X3RZg8pwKBgEm+\nC8/OqHzhjGWdwiVr4bpMthX6n33fvOI7FOEdSLG7UgFCrAyo4BEY00qadQ2Evun1\nvjVkYCeZ9vp+uZmps7KoT1onIEDK3m/j6EvFpDJwgDyMhyezaf4U6GNy0fJ47YYX\n0IWW3une5HNrWIunBOE2UIoS2Sg+7tKbehjR7p4BAoGAOJMi4QMO8KabxlPST760\nTmzu6rLeUsP1j4vqihar4Xp0DoTdISJmRaVd8GbUDWGv1BgnY90A+IHq4alcslDl\nEF3wtuma7OiTRg0/fbVi3TbdAMLWVnE8pPlBtJihj5VTGQzxP5gXwTAEOWEp4RlW\n88T379/Cy6Qe4x3+B4Lpouo=\n\n",
  "client_email": "groovy-medium-314812@groovy-medium-314812.iam.gserviceaccount.com",
  "client_id": "104865010480512617594",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/groovy-medium-314812%40groovy-medium-314812.iam.gserviceaccount.com"
}'''


client_secret = json.loads(client_secret)
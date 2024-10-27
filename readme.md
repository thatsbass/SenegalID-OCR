### API Documentation for CarteIdentiteOCR

#### API Name: **SenegalID-OCR**

---

### Overview

**SenegalID-OCR** is a RESTful API designed to extract information from the Senegalese national identity card (Carte d'Identité Sénégalaise) using Optical Character Recognition (OCR) technology. It processes images of the identity card and returns structured data in JSON format.

---

### Base URL

```
http://<your-server-ip>:5000/api
```

### Endpoints

#### 1. **Extract Information from Identity Card**

- **URL:** `/v1/ocr/cni`
- **Method:** `POST`
- **Content-Type:** `multipart/form-data`

##### Request Body

The request must include a file with the key `image`. The file should be an image of the Senegalese national identity card in one of the following formats: PNG, JPG, JPEG.

**Example:**

```bash
curl -X POST http://<your-server-ip>:5000/api/v1/ocr/cni \
-F 'image=@path/to/image.jpg'
```

##### Response

On success, the API will return a JSON object containing the extracted information:

- **Success Response (200 OK)**

```json
{
    "numero_carte": "021234567890123",
    "nom": "DIOP",
    "prenom": "Moussa",
    "date_naissance": "1990-01-01",
    "lieu_naissance": "Dakar",
    "sexe": "M",
    "adresse": "123 Rue de la Liberté",
    "nationalite": "Sénégalaise",
    "date_delivrance": "2020-01-01",
    "date_expiration": "2030-01-01"
}
```

- **Error Responses**

  - **400 Bad Request** (e.g., if no file is provided)

  ```json
  {
      "error": "Aucun fichier trouvé dans la requête",
      "status": 400
  }
  ```

  - **500 Internal Server Error** (e.g., for unexpected errors)

  ```json
  {
      "error": "An error occurred",
      "status": 500
  }
  ```

---

### File Upload Constraints

- **Maximum File Size:** 16 MB
- **Allowed Formats:** PNG, JPG, JPEG

---

### Error Handling

The API provides standardized error messages with HTTP status codes to facilitate client-side error handling.

| Status Code | Description                      |
|-------------|----------------------------------|
| 200         | Successfully processed request   |
| 400         | Bad request (client error)       |
| 500         | Internal server error            |

---

### Usage Notes

- Ensure that the image of the identity card is clear and properly oriented for the best OCR results.
- The API is designed for high accuracy in recognizing fields from the Senegalese national identity card; however, results may vary based on image quality.

---

### Dependencies

The following Python libraries are required to run the API:

- Flask
- OpenCV
- pytesseract
- Werkzeug
- NumPy
- Pillow

You can install these dependencies using pip:

```bash
pip install Flask opencv-python pytesseract werkzeug numpy Pillow
```

---

### Conclusion

**SenegalID-OCR** provides an efficient way to extract vital information from Senegalese national identity cards, making it easier to automate processes that require identity verification. With a simple API interface, it can be integrated into various applications to enhance functionality.

---
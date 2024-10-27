import cv2
import pytesseract
import re
import json
from models import CarteIdentiteSenegalaiseInformation

class CarteIdentiteSenegalaiseOCR:
    def __init__(self, image):
        self.image = image
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, self.threshed = cv2.threshold(self.gray, 127, 255, cv2.THRESH_TRUNC)
        self.result = CarteIdentiteSenegalaiseInformation()
        self.master_process()

    def process(self):
        raw_text = pytesseract.image_to_string(self.threshed, lang="fra")
        print(raw_text)
        return raw_text

    def extract(self, raw_text):
        lines = raw_text.split('\n')
        cleaned_lines = [line.strip() for line in lines if line.strip()]

        for i in range(len(cleaned_lines)):
            line = cleaned_lines[i]

            if "a carte d'identité" in line:
                if i + 1 < len(cleaned_lines):
                    num_match = re.search(r"(\d{2} \d{8} \d{5} \d)", cleaned_lines[i + 1])
                    if num_match:
                        self.result.numero_carte = num_match.group(0).replace(" ", "")


            elif "Prénoms" in line:
                if i + 1 < len(cleaned_lines):
                    self.result.prenom = cleaned_lines[i + 1]
            elif "Prenoms" in line:
              if i + 1 < len(cleaned_lines):
                    self.result.prenom = cleaned_lines[i + 1]


            elif "Nom" in line:
                if i + 1 < len(cleaned_lines):
                    self.result.nom = cleaned_lines[i + 1]


            elif "Date de naissance" in line:
                if i + 1 < len(cleaned_lines):
                    date_sexe = cleaned_lines[i + 1].split()
                    if len(date_sexe) >= 2:
                        self.result.date_naissance = date_sexe[0]
                        self.result.sexe = date_sexe[1]


            elif "Lieu de nais" in line:
                if i + 1 < len(cleaned_lines):
                    self.result.lieu_naissance = cleaned_lines[i + 1]


            # elif "Lieu de naissance" in line:
            #     if i + 1 < len(cleaned_lines):
            #         self.result.lieu_naissance = cleaned_lines[i + 1]


            elif "Date de délivrance" in line:
                if i + 1 < len(cleaned_lines):
                    dates = cleaned_lines[i + 1].split()
                    if len(dates) >= 2:
                        self.result.date_delivrance = dates[0]
                        self.result.date_expiration = dates[1]


            elif "Adrèsse du domicile" in line:
                if i + 1 < len(cleaned_lines):
                    self.result.adresse = cleaned_lines[i + 1]


            elif "Adresse du domicile" in line:
                if i + 1 < len(cleaned_lines):
                    self.result.adresse = cleaned_lines[i + 1]

    def master_process(self):
        raw_text = self.process()
        self.extract(raw_text)

    def to_json(self):
        return json.dumps(self.result.__dict__, indent=4)

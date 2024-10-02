import google.generativeai as genai
import requests
import json


GOOGLE_API_KEY="AIzaSyDw0QN-bfQ9xHIh7wjNqaNCIzcVl2zmHrI"
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

genai.configure(api_key=GOOGLE_API_KEY)



def get_product_info(ingredients):
    query1=f"""
    Based upon the food ingredients {ingredients} answer the following questions  in the format 'parameter name:response':- \
    parameter-1: How processed is the product, just answer HIGH,MEDIUM,LOW. \
    parameter-2: How nutricious is the product, just answer HIGH,MEDIUM,LOW.  \
    parameter-3: Harmful Ingredients present, just list them down. \
    parameter-4: Is it diabetes friendly, just answer as YES or NO.\
    parameter-5: Is it alergen friendly, just list down the allergens.\
    Answer concisely, do not make any assumption. \
    Do Not add any explaination. \
    DO not provide any explaination.
    """
    
    response=model.generate_content(query1)

    text_content = response._result.candidates[0].content.parts[0].text

    params={
    'parameter-1': 'processed',
    'parameter-2': 'nutrition',
    'parameter-3': 'harmful_ingredients',
    'parameter-4': 'diabetes_friendly',
    'parameter-5': 'alergen_friendly'
    }

    response_dict = {}
    for line in text_content.splitlines():
        line = line.strip() 
        if line.startswith("* **"):
            key_value = line.split(":", 1)  
            if len(key_value) == 2:
                key = key_value[0].strip(" ,*")  
                value = key_value[1].strip(" ,*")  
                response_dict[params[key]] = value

    return response_dict



def check_claim(claim, ingredients):
    def analyze_claim(claim, ingredients):
        base_url = "https://cwbackend-a3332a655e1f.herokuapp.com/claims/analyze"
        params = {
            'claim': claim,
            'ingredients': ingredients
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            return json.loads(response.json()) 
        else:
            return f"Error: {response.status_code}, {response.text}"
        
    return analyze_claim(claim, ingredients)



def check_diet_compliance(ingredients,diet):
    query2=f""" 
    Does my food containing ingredients {ingredients} compliant with my {diet} ? \
    Only answer as YES or NO.
    DO not provide any explaination
    """

    response=model.generate_content(query2)

    text_content = response._result.candidates[0].content.parts[0].text
    return text_content.strip()



def get_ingredients(img):
    sample_file = genai.upload_file(path=img,
                            display_name="image")
    # file = genai.get_file(name=sample_file.name)
    response = model.generate_content([sample_file, "list all the ingredients along with quantity"])
    msg=response._result.candidates[0].content.parts[0].text
    return msg
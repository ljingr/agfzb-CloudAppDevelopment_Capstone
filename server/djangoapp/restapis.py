import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions, EntitiesOptions
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url,api_key=None,**kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    if (api_key):
        try:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        except:
            # If any error occurs
            print("Network exception occurred")
    else:
        # no authentication GET
        response = requests.get(url, params=kwargs)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url,payload,**kwargs):
    response = requests.post(url,params=kwargs, json=payload)

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # - Call get_request() with specified arguments
    json_result = get_request(url)

    # - Parse JSON results into a CarDealer object list
    if json_result:
        dealers = json_result["result"]["docs"]
        for dealer in dealers:
            dealer_doc = dealer
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # - Call get_request() with specified arguments
    json_result = get_request(url,dealer_id=dealer_id)

    # - Parse JSON results into a DealerView object list
    if json_result:
        reviews = json_result["data"]["docs"]
        for dreview in reviews:
            
            review_obj = DealerReview(dealership=dreview["dealership"],
                        name=dreview["name"],purchase=dreview["purchase"],
                        review=dreview["review"],purchase_date=dreview["purchase_date"],
                        car_make=dreview["car_make"],car_model=dreview["car_model"],
                        car_year=dreview["car_year"], sentiment = analyze_review_sentiments(dreview["review"]),
                        id=dreview["_id"])
            results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text,**kwargs):
    api_key = "xx"
    url = "xx"
    
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07',authenticator=authenticator)

    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(text = text,
        features=Features(
            entities=EntitiesOptions(sentiment=True))).get_result()

    print(json.dumps(response, indent=2))
    for key, val in enumerate(response["entities"]):
        # print(key, ",", val)
        print(val["sentiment"]["label"])
        return (val["sentiment"]["label"])

# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative





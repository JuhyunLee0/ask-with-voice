import os
import requests
from openai import AzureOpenAI

aoai_api_key = os.getenv("AZURE_OPENAI_KEY")
aoai_api_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
aoai_api_deployment_name = os.getenv("AZURE_OPENAI_GPT4_DEPLOYMENT_NAME")


client = AzureOpenAI(
    api_key=aoai_api_key,
    api_version="2023-05-15",
    azure_endpoint=aoai_api_endpoint
)

default_system_message = "you are helpful assistant that answer is short and concise manner. respond in korean"

# # from https://gist.github.com/richdrummer33/0297121565315783daf978790c155488

# # OPENAI FUNCTION: Function to perform a Bing search
# def perform_bing_search(user_request):
#   global u_request
#   global s_query
#   global s_results

#   u_request = user_request
#   print(f"Generating a search_query for bing based on this user request: {user_request}")
#   openai_prompt = "Generate a search-engine query to satisfy this user's request: " + user_request
#   response = client.chat.completions.create(
#       model=base_model,
#       messages=[{"role": "user", "content": openai_prompt}],
#   )
#   # Get the response from OpenAI
#   bing_query = response.model_dump_json(indent=2)
#   s_query = bing_query
#   print(f"Bing search query: {bing_query}. Now executing the search...")
  
#   bing_response = run_bing_search(user_request)
#   s_results = bing_response
#   return bing_response

# # OPENAI FUNCTION: Function to process Bing search results
# def process_search_results(search_results):
#   global u_request
#   global s_query
#   global s_results

#   print(f"Analyzing/processing Bing search results")

#   # Use GPT to analyze the Bing search results
#   prompt = f"Analyze these Bing search results: '{s_results}'\nbased on this user request: {u_request}"
  
#   response = client.chat.completions.create(
#       model=base_model,
#       messages=[{"role": "user", "content": prompt}],
#   )
#   analysis =  response.choices[0].message.content.strip()

#   print(f"Analysis: {analysis}")
#   # Return the analysis
#   return analysis


# ############################################################################################################
# ### ANALYSIS: Perform a Bing search and process the results
# ############################################################################################################

# def run_bing_search(search_query):
#   # Returns data of type SearchResponse 
#   # https://learn.microsoft.com/en-us/python/api/azure-cognitiveservices-search-websearch/azure.cognitiveservices.search.websearch.models.searchresponse?view=azure-python
#   try:
#     base_url = "https://api.bing.microsoft.com/v7.0/search?"
#     encoded_query = quote_plus(search_query)
#     bing_search_query = base_url + 'q=' + encoded_query # + '&' + 'customconfig=' + custom_config_id --> uncomment this if you are using 'Bing Custom Search'
#     r = requests.get(bing_search_query, headers={'Ocp-Apim-Subscription-Key': subscription_key})
#   except Exception as err:
#     print("Encountered exception. {}".format(err))
#     raise err
  
#   # Old API
#   #try:
#   #  web_data = search_client.web.search(query=search_query)
#   #except Exception as err:
#   #  print("Encountered exception. {}".format(err))
#   #  raise err
  
#   response_data = json.loads(r.text)
#   results_text = ""
#   for result in response_data.get("webPages", {}).get("value", []):
#     results_text += result["name"] + "\n"
#     results_text += result["url"] + "\n"
#     results_text += result["snippet"] + "\n\n"
#     print(f"Title: {result['name']}")
#     print(f"URL: {result['url']}")
#     print(f"Snippet: {result['snippet']}\n")

#   return results_text



def init_conversation() -> list:
    """Initialize the conversation with a system message"""
    return [
        {"role": "system", "content": default_system_message}
    ]


def get_chat_response(user_input: str) -> str:
    """Generate a response to the user"""
    # return "this is test response"

    conversation = init_conversation()
    conversation.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=aoai_api_deployment_name,
        messages=conversation,
        temperature=0.7,
        top_p=1,
    )
    print(response)

    responseText = response.choices[0].message.content
    return responseText
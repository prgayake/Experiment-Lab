import wikipedia

def lambda_handler(event, context):
    result = wikipedia.summary("Maharashtra", sentences = 4)
    return result

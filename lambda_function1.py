import json
import pandas as pd
import wikipedia

def lambda_handler(event, context):
    result = wikipedia.summary("India", sentences=4)
    return result
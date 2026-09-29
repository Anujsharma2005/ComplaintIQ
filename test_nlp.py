from nlp.analyzer import analyze_complaint


complaint = """
I ordered my laptop five days ago and it still has not been
delivered. I have contacted customer support multiple times,
but nobody has responded. This is extremely frustrating and
I need the package immediately.
"""


result = analyze_complaint(complaint)


print("\n==============================")
print("       COMPLAINTIQ NLP")
print("==============================")

print("\nCategory:")
print(result["classification"]["category"])

print("\nCategory Confidence:")
print(result["classification"]["confidence"])

print("\nSentiment:")
print(result["sentiment"]["label"])

print("\nSentiment Score:")
print(result["sentiment"]["compound"])

print("\nUrgency:")
print(result["urgency"]["level"])

print("\nKeywords:")
print(result["keywords"])

print("\nTokens:")
print(result["tokens"])

print("\nCategory Scores:")
print(result["classification"]["scores"])
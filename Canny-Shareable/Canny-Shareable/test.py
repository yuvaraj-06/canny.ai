from cannyeval_v3 import *
evaluatorA = CannyEval()
dj = json.load(open('./minimal-data-4.json'))
report = evaluatorA.report_card(data_json=dj, max_marks=10, relative_marking=False, integer_marking=False, json_load_version="v2")
print("Report of the evaluations")
print(report)

print("Information about student answers")
print("Orienting sentences :", evaluatorA.orienting_sens), 
print("Orienting phrases :", evaluatorA.orienting_phrases),
print("Disorienting sentences :", evaluatorA.disorienting_sens)
print("Disorienting phrases :", evaluatorA.disorienting_phrases)

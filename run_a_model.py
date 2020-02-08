from QSNMC.tests import tests
from QSNMC.models import models
print(tests)
print(models)

for model in models:
    print("Model: %s" % model)
    for test in tests:
        print("Test: %s" % test)
        score = test.judge(model,deep_error=True)
        score.summarize()
        print("\r")
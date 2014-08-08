
from QSNMC.tests import tests
from QSNMC.models import models

# Parameters to instantiate a model.  
for model in models:
    for test in tests:
        score = test.judge(model,deep_error=True)
        score.summarize()


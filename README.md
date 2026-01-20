# Sphere Full Regression Test

Behaviour driven test development, switching from a procedural approach to the
page object model directive. Here we create a set of scenarios, which SPHERE is
tested against. Beyond the basic testing of the user manual functionality, this
allows for a more feature-centered approach.

## Setup
Runs on **python 3.8**

### Create an environment
_Example with `direnv`:_
```sh
python -m virtualenv <path/to/env> -p 3.8
echo "source <path/to/env>/bin/activate" > .envrc
direnv allow
```

### Install dependencies and package
Dependencies are pinned with hashes for stability and security reasons. [CLADE Python Dependency Management](https://app.nuclino.com/Clade/CLADE-Wiki/Python-Dependency-Management-0dc191b1-ae36-4831-bb1d-33001155c5dd)
```sh
python setup.py install

cd requirements
pip install -r linter.txt
pip install -r tests.txt
```

[Playwright](https://playwright.dev) has to be installed separatly:
```sh
playwright install
```

### Run tests
To see the current actions the browser is doing, call `pytest` with the `--headed` flag:
```sh
pytest --headed
```

## General Remarks

#### settings.json

Ensure that `settings.json` has `cucumberautocomplete` properties listed below:

    
    {
        "python.testing.pytestArgs": [
            "src"
        ],
        "python.testing.unittestEnabled": false,
        "python.testing.pytestEnabled": true,
        "cucumberautocomplete.syncfeatures": "src/test/features/*.feature",
        "cucumberautocomplete.steps": [
            "src/test/step_definition/consistency_test/*.py",
            "src/test/step_definition/ui/*.py"
        ],
        "cucumberautocomplete.strictGherkinCompletion": true,
        "cucumberautocomplete.strictGherkinValidation": true,
        "cucumberautocomplete.skipDocStringsFormat": true,
        "cucumberautocomplete.gherkinDefinitionPart": "(Given|When|Then)\\(",
        "cucumberautocomplete.smartSnippets": true,
        "cucumberautocomplete.customParameters": [
            {
                "parameter": "{/\\{.*\\}/}",
                "value": ".*"
            }
        ]
    }

#### Locating List of Element

In the **Constructor** of the **Page Objects**, if you are locating a list of element, 
do not use `.all()` function. `.all()` is not being handled dynamically in the constructor, 
meaning the initial locators are returned instead of the updated locators. 
Instead, use the `.all()` in the function itself.

**Do not do this:**

        class MethodsPage(ba.BrowserActions):
            def __init__(self, page: Page) -> None:
                super().__init__(page)
                self.methods_list = page.locator('[data-ref="eContainer"]').get_by_role("row").all()

            def get_method_list(self):
                return self.methods_list

**Instead, do this:**

        class MethodsPage(ba.BrowserActions):
            def __init__(self, page: Page) -> None:
                super().__init__(page)
                self.methods_list = page.locator('[data-ref="eContainer"]').get_by_role("row")

            def get_method_list(self):
                return self.methods_list.all()

#### Date Formats

Since in GITLAB we are using **Linux OS**, we need to use _dashes_ (-) in 
EU_DATE_FORMAT = "%-d.%-m.%Y". If you are using **Windows OS** and you need to run 
the automation locally, use _sharp_ (#) and update the EU_DATE_FORMAT = "%#d.%#m.%Y" 
on your local file. 

Ensure that this change is **NOT MERGED** to _main_ branch in GITLAB.


#### Assertions / Expects

Do not put assertions and expect functions inside of a Page Object. 
The only use of Page Objects is to encapsulate elements of a page and 
user transactions within the page. Assertions and expect functions must be put in step definitions.


# Sphere Replicability and Consistency Tests

## Consistency tests 
These are automated tests that creates an evaluation using a predetermined input from Data Science. We then compare the concentration value results with a tolerance value versus an expected concentration values from Data Science. This ensures concistency of our concentration values based on a `golden` data.

There are 2 types of Consistency tests for Data Driven Evaluations:
1. Consistency test with NaCl
2. Consistency test without NaCl

These 2 tests are almost the same when compared to each other. The only difference is one has NaCl as a component and the other does not.

There are 2 layers of tests that are checked for consistency of evaluation concentration values. These 2 layers are `API` vs. `UI` and `API` vs. `golden` data. For `API` vs. `UI`, we expect that the values from the API response is exactly the same as the value we show in our UI. For `API` vs. `golden` data, we compare the values with +-% tolerance. We includeded a tolerance since the decimal precision between analytics and MVDA are not the same. The tolerance can be modified in the feature files.

## Persistency Tests
These are automated tests that creates multiple evaluations using the same method and measurements. We then compare the concentration value results of all the evaluations against each other. There should be no difference on the concentration values since they are created using the same method and measurements. This ensures persistency of our concentration values when creating evaluations multiple times.

There are 2 types of Persistency Tests for Data Driven Evaluations:
1. Persistency using 1 method and creating multiple evaluation using that method
2. Persistency in creating multiple evaluations but there are different evaluations created in between

These 2 tests are checking that the values are uniform across all evaluations created. That means we are comparing concentration values from `evaluation1` to `evaluation{X}` depending on how many evaluations we want to create.

For Item 2 above, we are only checking the evaluation concentration values for the 1st method and not for the evaluations using the 2nd method.
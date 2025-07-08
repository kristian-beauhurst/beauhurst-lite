# Technical Assessment

We've included a tiny Django web app which is a wiki(-ish) of UK companies and
their employees. There's currently no front end views, and everything is getting
created, updated and deleted through the admin.

We want you to extend this app by implementing an integration with the HubSpot CRM, pushing the data to users' accounts.

The key goal is to have something which will push some of the data in the database to a HubSpot account. From the ideas below, pick and choose what interests you, what you think is important and what can best demonstrate your skills.

Feel free to make any other changes or improvements to the codebase that you think are necessary and use any tools that you like to build the integration.

## Ideas

You won't have time to do more than a handful of these, but make sure you read through them all. We might discuss some of those that you didn't tackle at interview so it'd be worth thinking about how you might approach them if you had time.

1. What data should we push?
    - HubSpot also has a [representation for companies](https://developers.hubspot.com/docs/reference/api/crm/objects/companies) so you'll want to push some of these. But what data would be interesting?
    - You'll want to send some of the basic fields from the Company model but maybe we should include some aggregate data too like the total amount raised from Deals for the company
    - Employees could probably be modeled as [contacts](https://developers.hubspot.com/docs/reference/api/crm/objects/contacts) in HubSpot so you might push these too
2. Our users might already have some companies and contacts in their HubSpot account so how do we match what we're pushing to what they already have? How do we make sure that our logic is idempotent so that when we push again we don't end up with 2 copies of everything?
3. We only have a small amount of data now but in production we might have millions of companies and users might have hundreds of thousands of companies in their HubSpot account. How would we optimise the performance of getting the data from the database, minimise the number of API calls we make and parallelise our integration process as much as possible?
4. There are steps below for setting up simple authentication for this project. But in production we'd want to use OAuth to authenticate users separately and store their individual credentials: how would you do this?
5. For simplicity you can just manually create some fields in your HubSpot developer test account to push the data to. But in production we might want to automatically create these fields for our users. Or we might want to allow users to create a custom mapping from our database fields onto the fields in their HubSpot account so you could build an interface for this.
6. HubSpot might be the first of many integrations we want to build so how can you architect the integration system to make it easy to add more in future?
7. Is there any metadata we should store in the database about the synchronisation process, how successful it was, what data was pushed and for which companies?
8. We'll want to regularly synchronise this data: how should we schedule your integration to be run daily?
9. Users might not be interested in every company we have data on so maybe we should just push those that they already have stored in their CRM. Or maybe we can use the companies they have marked as "monitoring" and only push those.

## Working with HubSpot

1. Go to [Create App Developer account](https://app.hubspot.com/signup-hubspot/developers) and setup an account using your email address.
2. Follow the initial setup instructions.
3. Then follow [these instructions](https://developers.hubspot.com/docs/getting-started/account-types#developer-test-accounts) to create a test account from inside your App Developer Account and once created click on the name of the test account you just created to access it.
4. Now you should be able to follow the [instructions here](https://developers.hubspot.com/docs/guides/apps/private-apps/overview#create-a-private-app) to setup a private app which you'll use to authenticate.
5. Most of the scopes you'll need will be in the CRM section so you can probably just select all of these.
6. Then copy the API token you receive and you should be able to use this directly with the [HubSpot REST APIs](https://developers.hubspot.com/docs/reference/api/crm/objects/companies) or with the [hubspot-api-python](https://github.com/HubSpot/hubspot-api-python) client.

## Expectations

- Please use Git to record the changes you make.
- But we would appreciate it if you did not publish this assessment on public
  repositories.
- To submit just send us back a zip containing the repository (including the `.git` directory)

## Installation

1. Clone the repo
2. Install python and a python package manager: we recommend `uv`
    ```
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
3. Set up a virtual env or equivalent to isolate your environment:
    ```
    uv sync
    ```
4. `uv run manage.py migrate`
5. `uv run manage.py loaddata assessment/fixtures.json` or `uv run manage.py populate_database`
6. `uv run manage.py createsuperuser`
7. `uv run manage.py runserver 0.0.0.0:8000`

## Linting and formatting

`ruff` has been setup so that you can call `uv run ruff check` to lint and `uv run ruff format` to auto-format.

## Testing

If testing is your thing, then 👍 we've set this repo up so you can use Django's builtin `unittest` or `pytest`, and we've set up `factory_boy` to help with some of the boilerplate to get you started.

You can call `uv run pytest` to run the tests.

## References

- https://docs.astral.sh/uv/
- https://docs.astral.sh/ruff/
- https://docs.djangoproject.com/en/5.1/topics/testing/
- https://docs.pytest.org
- https://pytest-django.readthedocs.io
- https://faker.readthedocs.io

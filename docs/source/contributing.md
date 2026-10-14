# Maintain the client and documentation

Use a Python environment with development and documentation dependencies:

```sh
python -m pip install -e 'packages/bsm-api-client[dev,docs]'
pre-commit run --all-files
pytest packages/bsm-api-client/tests
python scripts/generate_models.py --check
python scripts/generate_client.py packages/bsm-api-client/src/bsm_api_client/generated/openapi.json --check
python -m sphinx -W --keep-going -b html docs/source docs/_build/html
```

Native Sphinx docstrings start with a short purpose sentence. Add `:param name:`, `:returns:`, `:yields:`, `:raises Error:` or `:ivar name:` for meaningful behavior. Keep annotated types in signatures. Put longer runnable examples in guides; never put real credentials or tokens in examples.

`generate_models.py` adds model descriptions from OpenAPI. `generate_client.py` normalizes generated Google fields through `sphinx_docstrings.py`. Do not hand-edit generated descriptions; change the schema or generator and regenerate. CI tests supported minimum/maximum Python versions only.

The root `.readthedocs.yaml` builds this Sphinx site. Create/connect the Read the Docs project separately; repository configuration does not publish a site on its own. The older Markdown contract/generation notes remain linked from the repository README.

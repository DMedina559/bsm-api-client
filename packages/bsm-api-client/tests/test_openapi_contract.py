"""Contract parsing, component-aware diffing, and capabilities."""

import copy

import pytest

from bsm_api_client import ApiCapabilities, ApiOperation, diff_schemas
from bsm_api_client.exceptions import InvalidInputError
from bsm_api_client.openapi import generated_schema, index_operations


@pytest.fixture
def schema():
    return {
        "security": [{"oauth": []}],
        "components": {
            "securitySchemes": {"oauth": {"type": "http", "scheme": "bearer"}},
            "parameters": {
                "name": {
                    "in": "path",
                    "name": "name",
                    "required": True,
                    "schema": {"type": "string"},
                }
            },
            "schemas": {
                "Item": {"type": "object", "properties": {"value": {"type": "string"}}}
            },
        },
        "paths": {
            "/extra/{name}": {
                "parameters": [{"$ref": "#/components/parameters/name"}],
                "get": {
                    "operationId": "demo_status",
                    "x-bsm-plugin": "demo",
                    "tags": ["Plugin:Wrong"],
                    "deprecated": True,
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Item"}
                                }
                            }
                        }
                    },
                },
            }
        },
    }


def test_shared_metadata_resolves_inherited_parameters_and_plugin_ownership(schema):
    operation = index_operations(schema, {"demo_status"})["demo_status"]
    assert isinstance(operation, ApiOperation)
    assert operation.parameters[0]["name"] == "name"
    assert operation.security == ({"oauth": []},)
    assert operation.generated and operation.deprecated
    assert operation.plugin == "demo"
    capabilities = ApiCapabilities({"demo_status": operation})
    assert capabilities.has("demo_status") and not capabilities.has("missing")
    assert capabilities.runtime_only == ()
    assert capabilities.plugins["demo"] == (operation,)


def test_component_and_auth_scheme_changes_are_detected(schema):
    changed = copy.deepcopy(schema)
    changed["components"]["schemas"]["Item"]["properties"]["value"]["type"] = "integer"
    assert diff_schemas(schema, changed)["changed"] == ["demo_status"]
    changed = copy.deepcopy(schema)
    changed["components"]["securitySchemes"]["oauth"]["scheme"] = "basic"
    assert diff_schemas(schema, changed)["changed"] == ["demo_status"]


def test_diff_add_remove_and_reordered_documents(schema):
    after = copy.deepcopy(schema)
    after["paths"]["/extra/{name}"]["get"]["operationId"] = "replacement"
    assert diff_schemas(schema, after) == {
        "added": ["replacement"],
        "removed": ["demo_status"],
        "changed": [],
        "generated": [],
    }
    assert diff_schemas(schema, copy.deepcopy(schema))["changed"] == []


def test_duplicate_operation_ids_fail_instead_of_hiding_routes(schema):
    schema["paths"]["/other"] = {"post": {"operationId": "demo_status"}}
    with pytest.raises(InvalidInputError, match="Duplicate"):
        index_operations(schema)


def test_plugin_prefix_is_case_insensitive_and_core_management_is_not_a_plugin():
    operations = index_operations(
        {
            "paths": {
                "/one": {"get": {"operationId": "one", "tags": ["Plugin:Discord"]}},
                "/api/plugins/reload": {
                    "put": {
                        "operationId": "reload_plugins",
                        "tags": ["Plugin Management"],
                    }
                },
            }
        }
    )
    assert operations["one"].plugin == "Discord"
    assert operations["reload_plugins"].plugin is None


def test_bundled_schema_has_explicit_operation_ids():
    operations = index_operations(generated_schema())
    assert {
        "start_server",
        "list_servers",
        "create_backup",
        "login",
    } <= operations.keys()
    assert {
        "get_application_health",
        "get_application_metrics",
        "get_plugin_settings",
        "update_plugin_settings",
    } <= operations.keys()


def test_query_serialization_honors_form_explode():
    from bsm_api_client.openapi import serialize_query

    parameters = (
        {"name": "filter", "in": "query", "explode": True},
        {"name": "names", "in": "query", "explode": False},
    )
    assert serialize_query(
        parameters, {"filter": {"enabled": True}, "names": ["a", "b"]}
    ) == {"enabled": True, "names": "a,b"}
    with pytest.raises(InvalidInputError, match="Conflicting"):
        serialize_query(parameters, {"filter": {"names": "a"}, "names": "b"})


@pytest.mark.parametrize(
    "tags,expected",
    [
        (["Download Page Plugin", "plugin-json-ui"], "download_page_plugin"),
        (["Content Uploader Plugin"], "content_uploader_plugin"),
        (["Plugin Management"], None),
        (["plugin-json-ui"], None),
        (["Download Page Plugin", "Another Plugin"], None),
        (["Plugin:explicit", "Download Page Plugin"], "explicit"),
    ],
)
def test_backend_plugin_tags(tags, expected):
    schema = {
        "paths": {
            "/api/download_page/ui": {
                "get": {"operationId": "download_ui", "tags": tags}
            }
        }
    }
    operation = index_operations(schema)["download_ui"]
    assert operation.plugin == expected


def test_plugin_metadata_overrides_display_tag():
    schema = {
        "paths": {
            "/api/download_page/ui": {
                "get": {
                    "operationId": "download_ui",
                    "tags": ["Download Page Plugin"],
                    "x-bsm-plugin": "custom_owner",
                }
            }
        }
    }
    assert index_operations(schema)["download_ui"].plugin == "custom_owner"

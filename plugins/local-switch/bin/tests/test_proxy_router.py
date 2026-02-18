"""Tests du Proxy Router Local.

Created: 2026-02-18
Last Updated: 2026-02-18
Author: PhoenixProject

Tests TDD pour le proxy router local-switch.
Couvre : config, health check, switch, status, listing modeles, proxy.
"""

import json
import os
import tempfile

import pytest
import yaml


# ---------------------------------------------------------------------------
# FIXTURES
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_config_path(tmp_path):
    """Cree un fichier de config YAML dans un dossier temp isole par test."""
    config = {
        "default_backend": "cloud",
        "control_key": "test-secret-key",
        "proxy_port": 9999,
        "timeouts": {
            "health_check": 1.0,
            "model_list": 2.0,
            "proxy_request": 30.0,
        },
        "backends": {
            "cloud": {
                "url": "https://api.anthropic.com",
                "format": "anthropic",
                "token_env": "ANTHROPIC_API_KEY",
                "description": "Claude Cloud Officiel",
            },
            "ollama": {
                "url": "http://localhost:11434/v1",
                "format": "openai",
                "token": "ollama",
                "description": "Ollama Local",
            },
            "lmstudio": {
                "url": "http://localhost:1234/v1",
                "format": "openai",
                "token": "lmstudio",
                "description": "LM Studio Local",
            },
        },
    }
    config_file = tmp_path / "config.yaml"
    config_file.write_text(yaml.dump(config))

    return str(config_file)


@pytest.fixture
def router(sample_config_path):
    """Instancie un ProxyRouter avec la config de test."""
    from proxy_router import ProxyRouter

    return ProxyRouter(config_path=sample_config_path)


@pytest.fixture
def app(router):
    """Cree l'application Flask en mode test."""
    flask_app = router.create_app()
    flask_app.config["TESTING"] = True
    return flask_app


@pytest.fixture
def client(app):
    """Client de test Flask."""
    return app.test_client()


# ---------------------------------------------------------------------------
# TESTS CONFIG
# ---------------------------------------------------------------------------

class TestConfig:
    """Tests de chargement et validation de la configuration."""

    def test_load_valid_config(self, router):
        """La config YAML valide doit etre chargee correctement."""
        assert router.config is not None
        assert "backends" in router.config
        assert len(router.config["backends"]) == 3

    def test_default_backend_is_set(self, router):
        """Le backend par defaut doit etre initialise."""
        assert router.current_backend == "cloud"

    def test_config_has_timeouts(self, router):
        """Les timeouts doivent etre presents dans la config."""
        assert router.config["timeouts"]["health_check"] == 1.0
        assert router.config["timeouts"]["model_list"] == 2.0
        assert router.config["timeouts"]["proxy_request"] == 30.0

    def test_config_missing_file_raises(self):
        """Un fichier de config inexistant doit lever une erreur."""
        from proxy_router import ProxyRouter

        with pytest.raises(FileNotFoundError):
            ProxyRouter(config_path="/chemin/inexistant.yaml")

    def test_config_missing_backends_raises(self):
        """Une config sans section backends doit lever une erreur."""
        from proxy_router import ProxyRouter

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as tmp:
            yaml.dump({"default_backend": "cloud"}, tmp)
            tmp_path = tmp.name

        try:
            with pytest.raises(ValueError, match="backends"):
                ProxyRouter(config_path=tmp_path)
        finally:
            os.unlink(tmp_path)

    def test_config_invalid_default_backend_raises(self):
        """Un default_backend qui n'existe pas dans backends doit lever une erreur."""
        from proxy_router import ProxyRouter

        config = {
            "default_backend": "nexiste_pas",
            "backends": {
                "cloud": {
                    "url": "https://api.anthropic.com",
                    "format": "anthropic",
                },
            },
        }
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as tmp:
            yaml.dump(config, tmp)
            tmp_path = tmp.name

        try:
            with pytest.raises(ValueError, match="default_backend"):
                ProxyRouter(config_path=tmp_path)
        finally:
            os.unlink(tmp_path)

    def test_control_key_loaded(self, router):
        """La cle d'auth pour les endpoints de controle doit etre chargee."""
        assert router.control_key == "test-secret-key"


# ---------------------------------------------------------------------------
# TESTS STATUS
# ---------------------------------------------------------------------------

class TestStatus:
    """Tests de l'endpoint /_control/status."""

    def test_status_returns_current_backend(self, client):
        """GET /_control/status doit retourner le backend actif."""
        resp = client.get(
            "/_control/status",
            headers={"X-Control-Key": "test-secret-key"},
        )
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["backend"] == "cloud"
        assert data["target"] == "https://api.anthropic.com"
        assert data["format"] == "anthropic"

    def test_status_requires_auth(self, client):
        """GET /_control/status sans cle doit retourner 401."""
        resp = client.get("/_control/status")
        assert resp.status_code == 401


# ---------------------------------------------------------------------------
# TESTS SWITCH
# ---------------------------------------------------------------------------

class TestSwitch:
    """Tests de l'endpoint /_control/switch/<backend>."""

    def test_switch_to_valid_backend(self, client):
        """POST /_control/switch/ollama doit basculer vers ollama."""
        resp = client.post(
            "/_control/switch/ollama",
            headers={"X-Control-Key": "test-secret-key"},
        )
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["status"] == "ok"
        assert data["current"] == "ollama"

        # Verifier que le status reflète le changement
        resp = client.get(
            "/_control/status",
            headers={"X-Control-Key": "test-secret-key"},
        )
        data = json.loads(resp.data)
        assert data["backend"] == "ollama"

    def test_switch_to_invalid_backend(self, client):
        """POST /_control/switch/nexiste_pas doit retourner 400."""
        resp = client.post(
            "/_control/switch/nexiste_pas",
            headers={"X-Control-Key": "test-secret-key"},
        )
        assert resp.status_code == 400

    def test_switch_requires_auth(self, client):
        """POST /_control/switch/ollama sans cle doit retourner 401."""
        resp = client.post("/_control/switch/ollama")
        assert resp.status_code == 401

    def test_switch_wrong_key(self, client):
        """POST /_control/switch/ollama avec mauvaise cle doit retourner 401."""
        resp = client.post(
            "/_control/switch/ollama",
            headers={"X-Control-Key": "wrong-key"},
        )
        assert resp.status_code == 401


# ---------------------------------------------------------------------------
# TESTS BACKENDS LISTING
# ---------------------------------------------------------------------------

class TestBackendsListing:
    """Tests de l'endpoint /_control/backends."""

    def test_list_backends(self, client):
        """GET /_control/backends doit retourner tous les backends configures."""
        resp = client.get(
            "/_control/backends",
            headers={"X-Control-Key": "test-secret-key"},
        )
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert "backends" in data
        assert "cloud" in data["backends"]
        assert "ollama" in data["backends"]
        assert "lmstudio" in data["backends"]

    def test_list_backends_shows_active(self, client):
        """Le listing doit indiquer quel backend est actif."""
        resp = client.get(
            "/_control/backends",
            headers={"X-Control-Key": "test-secret-key"},
        )
        data = json.loads(resp.data)
        assert data["active"] == "cloud"


# ---------------------------------------------------------------------------
# TESTS ADD/REMOVE BACKENDS DYNAMIQUEMENT
# ---------------------------------------------------------------------------

class TestDynamicBackends:
    """Tests d'ajout et suppression dynamique de backends."""

    def test_add_backend(self, client):
        """POST /_control/backends doit ajouter un nouveau backend."""
        resp = client.post(
            "/_control/backends",
            headers={
                "X-Control-Key": "test-secret-key",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "name": "groq",
                "url": "https://api.groq.com/openai/v1",
                "format": "openai",
                "token_env": "GROQ_API_KEY",
                "description": "Groq Cloud",
            }),
        )
        assert resp.status_code == 201
        data = json.loads(resp.data)
        assert data["status"] == "ok"
        assert data["backend"] == "groq"

        # Verifier qu'il est dans la liste
        resp = client.get(
            "/_control/backends",
            headers={"X-Control-Key": "test-secret-key"},
        )
        data = json.loads(resp.data)
        assert "groq" in data["backends"]

    def test_add_duplicate_backend_fails(self, client):
        """Ajouter un backend qui existe deja doit retourner 409."""
        resp = client.post(
            "/_control/backends",
            headers={
                "X-Control-Key": "test-secret-key",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "name": "cloud",
                "url": "https://api.anthropic.com",
                "format": "anthropic",
            }),
        )
        assert resp.status_code == 409

    def test_delete_backend(self, client):
        """DELETE /_control/backends/lmstudio doit supprimer le backend."""
        resp = client.delete(
            "/_control/backends/lmstudio",
            headers={"X-Control-Key": "test-secret-key"},
        )
        assert resp.status_code == 200

        # Verifier qu'il n'est plus dans la liste
        resp = client.get(
            "/_control/backends",
            headers={"X-Control-Key": "test-secret-key"},
        )
        data = json.loads(resp.data)
        assert "lmstudio" not in data["backends"]

    def test_delete_active_backend_fails(self, client):
        """Supprimer le backend actif doit retourner 400."""
        resp = client.delete(
            "/_control/backends/cloud",
            headers={"X-Control-Key": "test-secret-key"},
        )
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# TESTS PERSISTENCE
# ---------------------------------------------------------------------------

class TestPersistence:
    """Tests de persistance de l'etat."""

    def test_state_file_created_on_switch(self, client, router):
        """Switcher doit sauvegarder l'etat dans un fichier."""
        client.post(
            "/_control/switch/ollama",
            headers={"X-Control-Key": "test-secret-key"},
        )
        assert router.state_path is not None
        assert os.path.exists(router.state_path)

        with open(router.state_path) as f:
            state = json.load(f)
        assert state["current_backend"] == "ollama"

    def test_state_restored_on_init(self, sample_config_path):
        """Un ProxyRouter doit restaurer l'etat sauvegarde."""
        from proxy_router import ProxyRouter

        # Premier router : switch vers ollama
        router1 = ProxyRouter(config_path=sample_config_path)
        app1 = router1.create_app()
        app1.config["TESTING"] = True
        with app1.test_client() as c:
            c.post(
                "/_control/switch/ollama",
                headers={"X-Control-Key": "test-secret-key"},
            )

        # Deuxieme router : doit reprendre sur ollama
        router2 = ProxyRouter(config_path=sample_config_path)
        assert router2.current_backend == "ollama"


# ---------------------------------------------------------------------------
# TESTS MODELS LISTING
# ---------------------------------------------------------------------------

class TestModelsListing:
    """Tests de l'endpoint /_control/models."""

    def test_models_returns_anthropic_defaults(self, client):
        """Le listing doit inclure les modeles Anthropic par defaut."""
        from unittest.mock import patch, MagicMock

        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.return_value = {
            "data": [{"id": "llama3"}, {"id": "mistral"}],
        }

        with patch("proxy_router.requests.get", return_value=mock_resp):
            resp = client.get(
                "/_control/models",
                headers={"X-Control-Key": "test-secret-key"},
            )

        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert any("claude-sonnet-4-20250514" in m for m in data["models"])
        assert any("claude-haiku" in m for m in data["models"])

    def test_models_includes_openai_compatible(self, client):
        """Le listing doit inclure les modeles des backends OpenAI-compatible."""
        from unittest.mock import patch, MagicMock

        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.return_value = {
            "data": [{"id": "llama3.1"}, {"id": "codestral"}],
        }

        with patch("proxy_router.requests.get", return_value=mock_resp):
            resp = client.get(
                "/_control/models",
                headers={"X-Control-Key": "test-secret-key"},
            )

        data = json.loads(resp.data)
        assert any("OLLAMA: llama3.1" in m for m in data["models"])

    def test_models_handles_backend_down(self, client):
        """Le listing ne doit pas crasher si un backend est injoignable."""
        from unittest.mock import patch
        import requests as req_lib

        with patch(
            "proxy_router.requests.get",
            side_effect=req_lib.exceptions.ConnectionError("refused"),
        ):
            resp = client.get(
                "/_control/models",
                headers={"X-Control-Key": "test-secret-key"},
            )

        assert resp.status_code == 200
        data = json.loads(resp.data)
        # Seuls les modeles Anthropic (hardcodes) doivent etre presents
        assert any("CLOUD:" in m for m in data["models"])

    def test_models_handles_non_ok_response(self, client):
        """Le listing doit ignorer les reponses non-OK des backends."""
        from unittest.mock import patch, MagicMock

        mock_resp = MagicMock()
        mock_resp.ok = False

        with patch("proxy_router.requests.get", return_value=mock_resp):
            resp = client.get(
                "/_control/models",
                headers={"X-Control-Key": "test-secret-key"},
            )

        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# TESTS HEALTH CHECK
# ---------------------------------------------------------------------------

class TestHealthCheck:
    """Tests de l'endpoint /_control/health/<backend>."""

    def test_health_reachable_openai(self, client):
        """Health check doit retourner reachable=true si le backend repond."""
        from unittest.mock import patch, MagicMock

        mock_resp = MagicMock()
        mock_resp.status_code = 200

        with patch("proxy_router.requests.get", return_value=mock_resp):
            resp = client.get(
                "/_control/health/ollama",
                headers={"X-Control-Key": "test-secret-key"},
            )

        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["reachable"] is True
        assert data["backend"] == "ollama"

    def test_health_reachable_anthropic(self, client):
        """Health check Anthropic doit verifier l'URL directe."""
        from unittest.mock import patch, MagicMock

        mock_resp = MagicMock()
        mock_resp.status_code = 200

        with patch("proxy_router.requests.get", return_value=mock_resp):
            resp = client.get(
                "/_control/health/cloud",
                headers={"X-Control-Key": "test-secret-key"},
            )

        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["reachable"] is True

    def test_health_unreachable(self, client):
        """Health check doit retourner reachable=false si le backend est down."""
        from unittest.mock import patch
        import requests as req_lib

        with patch(
            "proxy_router.requests.get",
            side_effect=req_lib.exceptions.ConnectionError("refused"),
        ):
            resp = client.get(
                "/_control/health/ollama",
                headers={"X-Control-Key": "test-secret-key"},
            )

        data = json.loads(resp.data)
        assert data["reachable"] is False

    def test_health_server_error(self, client):
        """Health check doit retourner reachable=false si status >= 500."""
        from unittest.mock import patch, MagicMock

        mock_resp = MagicMock()
        mock_resp.status_code = 500

        with patch("proxy_router.requests.get", return_value=mock_resp):
            resp = client.get(
                "/_control/health/ollama",
                headers={"X-Control-Key": "test-secret-key"},
            )

        data = json.loads(resp.data)
        assert data["reachable"] is False

    def test_health_unknown_backend(self, client):
        """Health check d'un backend inexistant doit retourner 404."""
        resp = client.get(
            "/_control/health/nexiste_pas",
            headers={"X-Control-Key": "test-secret-key"},
        )
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# TESTS PROXY CATCH-ALL
# ---------------------------------------------------------------------------

class TestProxy:
    """Tests du proxy catch-all."""

    def test_proxy_forwards_request(self, client):
        """Le proxy doit transmettre la requete au backend actif."""
        from unittest.mock import patch, MagicMock
        from io import BytesIO
        from urllib3.response import HTTPResponse

        raw = HTTPResponse(
            body=BytesIO(b'{"result": "ok"}'),
            headers={"Content-Type": "application/json"},
            preload_content=False,
        )
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.iter_content = MagicMock(
            return_value=[b'{"result": "ok"}']
        )
        mock_resp.raw = raw

        with patch(
            "proxy_router.requests.request", return_value=mock_resp
        ):
            resp = client.post(
                "/v1/messages",
                data=json.dumps({"model": "claude-3-haiku"}),
                content_type="application/json",
            )

        assert resp.status_code == 200

    def test_proxy_returns_502_on_connection_error(self, client):
        """Le proxy doit retourner 502 si le backend est injoignable."""
        from unittest.mock import patch
        import requests as req_lib

        with patch(
            "proxy_router.requests.request",
            side_effect=req_lib.exceptions.ConnectionError("refused"),
        ):
            resp = client.post(
                "/v1/messages",
                data=json.dumps({"model": "test"}),
                content_type="application/json",
            )

        assert resp.status_code == 502
        data = json.loads(resp.data)
        assert "Proxy Error" in data["error"]
        assert data["backend"] == "cloud"

    def test_proxy_catches_control_path(self, client):
        """Les chemins _control/ ne doivent pas etre proxifies."""
        resp = client.get(
            "/_control/unknown_endpoint",
            headers={"X-Control-Key": "test-secret-key"},
        )
        assert resp.status_code == 404

    def test_proxy_injects_token(self, client):
        """Le proxy doit injecter le token dans les headers."""
        from unittest.mock import patch, MagicMock, call
        from io import BytesIO
        from urllib3.response import HTTPResponse

        # Switch vers ollama (qui a un token direct)
        client.post(
            "/_control/switch/ollama",
            headers={"X-Control-Key": "test-secret-key"},
        )

        raw = HTTPResponse(
            body=BytesIO(b"ok"),
            headers={},
            preload_content=False,
        )
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.iter_content = MagicMock(return_value=[b"ok"])
        mock_resp.raw = raw

        with patch(
            "proxy_router.requests.request", return_value=mock_resp
        ) as mock_req:
            client.get("/v1/models")
            called_headers = mock_req.call_args[1]["headers"]
            assert called_headers["x-api-key"] == "ollama"
            assert called_headers["Authorization"] == "Bearer ollama"

    def test_proxy_root_path(self, client):
        """Le proxy doit fonctionner sur le chemin racine /."""
        from unittest.mock import patch, MagicMock
        from io import BytesIO
        from urllib3.response import HTTPResponse

        raw = HTTPResponse(
            body=BytesIO(b"ok"),
            headers={},
            preload_content=False,
        )
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.iter_content = MagicMock(return_value=[b"ok"])
        mock_resp.raw = raw

        with patch(
            "proxy_router.requests.request", return_value=mock_resp
        ):
            resp = client.get("/")
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# TESTS EDGE CASES CONFIG
# ---------------------------------------------------------------------------

class TestEdgeCasesConfig:
    """Tests des cas limites de la configuration."""

    def test_config_no_default_backend_uses_first(self, tmp_path):
        """Sans default_backend, le premier backend doit etre utilise."""
        from proxy_router import ProxyRouter

        config = {
            "backends": {
                "ollama": {
                    "url": "http://localhost:11434/v1",
                    "format": "openai",
                },
            },
        }
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump(config))

        router = ProxyRouter(config_path=str(config_file))
        assert router.current_backend == "ollama"
        assert router.control_key == ""

    def test_config_no_timeouts_uses_defaults(self, tmp_path):
        """Sans section timeouts, les defauts doivent etre appliques."""
        from proxy_router import ProxyRouter

        config = {
            "default_backend": "cloud",
            "backends": {
                "cloud": {
                    "url": "https://api.anthropic.com",
                    "format": "anthropic",
                },
            },
        }
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump(config))

        router = ProxyRouter(config_path=str(config_file))
        assert router.config["timeouts"]["health_check"] == 2.0
        assert router.config["timeouts"]["model_list"] == 3.0
        assert router.config["timeouts"]["proxy_request"] == 60.0

    def test_auth_disabled_when_no_key(self, tmp_path):
        """Sans control_key, les endpoints de controle sont ouverts."""
        from proxy_router import ProxyRouter

        config = {
            "default_backend": "cloud",
            "backends": {
                "cloud": {
                    "url": "https://api.anthropic.com",
                    "format": "anthropic",
                },
            },
        }
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump(config))

        router = ProxyRouter(config_path=str(config_file))
        app = router.create_app()
        app.config["TESTING"] = True
        c = app.test_client()

        # Pas de header X-Control-Key et ca passe quand meme
        resp = c.get("/_control/status")
        assert resp.status_code == 200

    def test_add_backend_missing_fields(self, client):
        """POST /_control/backends sans champs requis retourne 400."""
        resp = client.post(
            "/_control/backends",
            headers={
                "X-Control-Key": "test-secret-key",
                "Content-Type": "application/json",
            },
            data=json.dumps({"name": "test"}),
        )
        assert resp.status_code == 400

    def test_add_backend_no_json(self, client):
        """POST /_control/backends sans JSON retourne 400."""
        resp = client.post(
            "/_control/backends",
            headers={"X-Control-Key": "test-secret-key"},
        )
        assert resp.status_code == 400

    def test_add_backend_with_direct_token(self, client):
        """POST /_control/backends avec token direct doit le stocker."""
        resp = client.post(
            "/_control/backends",
            headers={
                "X-Control-Key": "test-secret-key",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "name": "custom",
                "url": "http://localhost:8080/v1",
                "token": "my-token",
            }),
        )
        assert resp.status_code == 201

    def test_delete_nonexistent_backend(self, client):
        """DELETE /_control/backends/inexistant retourne 404."""
        resp = client.delete(
            "/_control/backends/inexistant",
            headers={"X-Control-Key": "test-secret-key"},
        )
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# TESTS EDGE CASES STATE
# ---------------------------------------------------------------------------

class TestEdgeCasesState:
    """Tests des cas limites de la persistance d'etat."""

    def test_corrupted_state_file(self, tmp_path):
        """Un fichier d'etat corrompu doit etre ignore."""
        from proxy_router import ProxyRouter

        config = {
            "default_backend": "cloud",
            "backends": {
                "cloud": {
                    "url": "https://api.anthropic.com",
                    "format": "anthropic",
                },
            },
        }
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump(config))

        # Creer un fichier d'etat corrompu
        state_file = tmp_path / ".proxy_state.json"
        state_file.write_text("NOT VALID JSON{{{")

        router = ProxyRouter(config_path=str(config_file))
        assert router.current_backend == "cloud"

    def test_state_with_removed_backend(self, tmp_path):
        """Un etat pointant vers un backend supprime doit revenir au defaut."""
        from proxy_router import ProxyRouter

        config = {
            "default_backend": "cloud",
            "backends": {
                "cloud": {
                    "url": "https://api.anthropic.com",
                    "format": "anthropic",
                },
            },
        }
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump(config))

        # Etat pointe vers un backend qui n'existe plus
        state_file = tmp_path / ".proxy_state.json"
        state_file.write_text(json.dumps({"current_backend": "ollama_removed"}))

        router = ProxyRouter(config_path=str(config_file))
        assert router.current_backend == "cloud"

    def test_save_state_ioerror(self, tmp_path):
        """Une erreur IO lors de la sauvegarde ne doit pas crasher."""
        from proxy_router import ProxyRouter
        from unittest.mock import patch

        config = {
            "default_backend": "cloud",
            "backends": {
                "cloud": {
                    "url": "https://api.anthropic.com",
                    "format": "anthropic",
                },
            },
        }
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump(config))

        router = ProxyRouter(config_path=str(config_file))
        router.state_path = "/chemin/impossible/state.json"

        # Ne doit pas lever d'exception
        router._save_state()


# ---------------------------------------------------------------------------
# TESTS TOKEN RESOLUTION
# ---------------------------------------------------------------------------

class TestTokenResolution:
    """Tests de la resolution des tokens."""

    def test_token_from_env_var(self, router):
        """Le token doit etre resolu depuis une variable d'environnement."""
        os.environ["TEST_TOKEN_VAR"] = "env-secret-123"
        try:
            token = router._get_token({"token_env": "TEST_TOKEN_VAR"})
            assert token == "env-secret-123"
        finally:
            del os.environ["TEST_TOKEN_VAR"]

    def test_token_from_missing_env_var(self, router):
        """Un token_env manquant doit retourner une chaine vide."""
        token = router._get_token({"token_env": "NEXISTE_PAS_DU_TOUT"})
        assert token == ""

    def test_token_direct_value(self, router):
        """Un token direct doit etre retourne tel quel."""
        token = router._get_token({"token": "direct-key"})
        assert token == "direct-key"

    def test_no_token(self, router):
        """Sans token ni token_env, retourner chaine vide."""
        token = router._get_token({"url": "http://localhost"})
        assert token == ""


# ---------------------------------------------------------------------------
# TESTS MAIN
# ---------------------------------------------------------------------------

class TestMain:
    """Tests du point d'entree main."""

    def test_main_with_env_config(self, sample_config_path):
        """main() doit lire PROXY_CONFIG et demarrer l'app."""
        from unittest.mock import patch, MagicMock

        os.environ["PROXY_CONFIG"] = sample_config_path
        try:
            with patch("proxy_router.Flask") as mock_flask:
                mock_app = MagicMock()
                mock_flask.return_value = mock_app
                # On ne peut pas facilement mocker create_app, donc on mock app.run
                with patch(
                    "proxy_router.ProxyRouter.create_app"
                ) as mock_create:
                    mock_app_instance = MagicMock()
                    mock_create.return_value = mock_app_instance

                    from proxy_router import main
                    main()

                    mock_app_instance.run.assert_called_once()
        finally:
            del os.environ["PROXY_CONFIG"]

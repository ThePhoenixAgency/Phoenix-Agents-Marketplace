"""Proxy Router Local pour Claude Code.

Created: 2026-02-18
Last Updated: 2026-02-18
Author: PhoenixProject

Redirige le trafic API Claude vers le backend actif
(Cloud Anthropic, Ollama, LM Studio, ou tout backend configure).

Architecture :
- Config YAML externe pour les backends
- Classe ProxyRouter (thread-safe, testable)
- Auth par cle sur les endpoints de controle
- Persistance d'etat entre redemarrages
- Support formats Anthropic et OpenAI-compatible
"""

import json
import logging
import os
import threading

import requests
import yaml
from flask import Flask, Response, jsonify, request

# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("proxy_router")


# ---------------------------------------------------------------------------
# PROXY ROUTER
# ---------------------------------------------------------------------------

class ProxyRouter:
    """Gestionnaire central du proxy router.

    Charge la configuration, gere l'etat du backend actif,
    et fournit l'application Flask.

    Args:
        config_path: Chemin vers le fichier de config YAML.
    """

    def __init__(self, config_path):
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Fichier de configuration introuvable : {config_path}"
            )

        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        self._validate_config()

        self._lock = threading.Lock()
        self.config_path = config_path

        # -- Chemin du fichier d'etat (a cote de la config) --
        config_dir = os.path.dirname(os.path.abspath(config_path))
        self.state_path = os.path.join(config_dir, ".proxy_state.json")

        # -- Restaurer l'etat ou utiliser le defaut --
        self.current_backend = self._restore_state()

        # -- Cle d'auth pour les endpoints de controle --
        self.control_key = self.config.get("control_key", "")

    def _validate_config(self):
        """Valide que la configuration contient les sections obligatoires.

        Raises:
            ValueError: Si la config est invalide.
        """
        if "backends" not in self.config or not self.config["backends"]:
            raise ValueError(
                "La configuration doit contenir une section 'backends' "
                "avec au moins un backend."
            )

        default = self.config.get("default_backend", "")
        if default and default not in self.config["backends"]:
            raise ValueError(
                f"default_backend '{default}' n'existe pas dans "
                f"la liste des backends : "
                f"{list(self.config['backends'].keys())}"
            )

        if not default:
            self.config["default_backend"] = list(
                self.config["backends"].keys()
            )[0]

        # -- Timeouts par defaut --
        if "timeouts" not in self.config:
            self.config["timeouts"] = {}
        defaults_timeouts = {
            "health_check": 2.0,
            "model_list": 3.0,
            "proxy_request": 60.0,
        }
        for key, val in defaults_timeouts.items():
            self.config["timeouts"].setdefault(key, val)

    def _restore_state(self):
        """Restaure le backend actif depuis le fichier d'etat.

        Returns:
            Nom du backend actif.
        """
        if os.path.exists(self.state_path):
            try:
                with open(self.state_path) as f:
                    state = json.load(f)
                backend = state.get("current_backend", "")
                if backend in self.config["backends"]:
                    logger.info(
                        "[OK] Etat restaure : backend=%s", backend
                    )
                    return backend
            except (json.JSONDecodeError, IOError):
                logger.warning(
                    "[WARNING] Fichier d'etat corrompu, utilisation du defaut"
                )

        return self.config["default_backend"]

    def _save_state(self):
        """Sauvegarde le backend actif dans le fichier d'etat."""
        try:
            with open(self.state_path, "w") as f:
                json.dump({"current_backend": self.current_backend}, f)
        except IOError as exc:
            logger.error("[ERROR] Impossible de sauvegarder l'etat : %s", exc)

    def _get_current_config(self):
        """Retourne la config du backend actif.

        Returns:
            dict avec url, format, token, description.
        """
        with self._lock:
            return self.config["backends"][self.current_backend].copy()

    def _get_token(self, backend_config):
        """Resout le token d'un backend (direct ou via variable d'env).

        Args:
            backend_config: dict de config du backend.

        Returns:
            Token sous forme de string, ou chaine vide.
        """
        if "token" in backend_config:
            return backend_config["token"]
        if "token_env" in backend_config:
            return os.environ.get(backend_config["token_env"], "")
        return ""

    def _check_auth(self):
        """Verifie la cle d'authentification sur les endpoints de controle.

        Returns:
            True si l'auth est valide ou non configuree.
        """
        if not self.control_key:
            return True
        provided = request.headers.get("X-Control-Key", "")
        return provided == self.control_key

    # -----------------------------------------------------------------------
    # FLASK APP
    # -----------------------------------------------------------------------

    def create_app(self):
        """Cree et configure l'application Flask.

        Returns:
            Instance Flask configuree.
        """
        app = Flask(__name__)

        @app.before_request
        def check_control_auth():
            """Filtre les requetes /_control/ non authentifiees."""
            if request.path.startswith("/_control/"):
                if not self._check_auth():
                    return jsonify({"error": "Unauthorized"}), 401

        # -- STATUS --
        @app.route("/_control/status", methods=["GET"])
        def control_status():
            cfg = self._get_current_config()
            return jsonify({
                "backend": self.current_backend,
                "target": cfg["url"],
                "format": cfg.get("format", "unknown"),
                "description": cfg.get("description", ""),
            })

        # -- SWITCH --
        @app.route("/_control/switch/<backend_name>", methods=["POST"])
        def control_switch(backend_name):
            with self._lock:
                if backend_name not in self.config["backends"]:
                    return jsonify({
                        "error": f"Backend inconnu : {backend_name}",
                        "available": list(self.config["backends"].keys()),
                    }), 400

                self.current_backend = backend_name
                self._save_state()

            cfg = self._get_current_config()
            logger.info(
                "[OK] Switch vers %s -> %s",
                backend_name, cfg["url"],
            )
            return jsonify({
                "status": "ok",
                "current": backend_name,
                "target": cfg["url"],
            })

        # -- LIST BACKENDS --
        @app.route("/_control/backends", methods=["GET"])
        def control_list_backends():
            with self._lock:
                backends_info = {}
                for name, cfg in self.config["backends"].items():
                    backends_info[name] = {
                        "url": cfg["url"],
                        "format": cfg.get("format", "unknown"),
                        "description": cfg.get("description", ""),
                    }
                return jsonify({
                    "active": self.current_backend,
                    "backends": backends_info,
                })

        # -- ADD BACKEND --
        @app.route("/_control/backends", methods=["POST"])
        def control_add_backend():
            data = request.get_json(silent=True)
            if not data or "name" not in data or "url" not in data:
                return jsonify({
                    "error": "Champs requis : name, url",
                }), 400

            name = data["name"]
            with self._lock:
                if name in self.config["backends"]:
                    return jsonify({
                        "error": f"Le backend '{name}' existe deja",
                    }), 409

                self.config["backends"][name] = {
                    "url": data["url"],
                    "format": data.get("format", "openai"),
                    "description": data.get("description", ""),
                }
                if "token" in data:
                    self.config["backends"][name]["token"] = data["token"]
                if "token_env" in data:
                    self.config["backends"][name]["token_env"] = data[
                        "token_env"
                    ]

            logger.info("[OK] Backend ajoute : %s -> %s", name, data["url"])
            return jsonify({"status": "ok", "backend": name}), 201

        # -- DELETE BACKEND --
        @app.route("/_control/backends/<backend_name>", methods=["DELETE"])
        def control_delete_backend(backend_name):
            with self._lock:
                if backend_name not in self.config["backends"]:
                    return jsonify({
                        "error": f"Backend inconnu : {backend_name}",
                    }), 404

                if backend_name == self.current_backend:
                    return jsonify({
                        "error": "Impossible de supprimer le backend actif. "
                                 "Switchez d'abord.",
                    }), 400

                del self.config["backends"][backend_name]

            logger.info("[OK] Backend supprime : %s", backend_name)
            return jsonify({"status": "ok", "deleted": backend_name})

        # -- LIST MODELS --
        @app.route("/_control/models", methods=["GET"])
        def control_models():
            timeout = self.config["timeouts"]["model_list"]
            models = []

            with self._lock:
                backends = dict(self.config["backends"])

            for name, cfg in backends.items():
                url = cfg["url"]
                fmt = cfg.get("format", "openai")

                if fmt == "openai":
                    endpoint = f"{url}/models"
                    try:
                        resp = requests.get(endpoint, timeout=timeout)
                        if resp.ok:
                            for m in resp.json().get("data", []):
                                models.append(
                                    f"{name.upper()}: {m.get('id', '?')}"
                                )
                    except requests.exceptions.RequestException:
                        pass

                elif fmt == "anthropic":
                    # Anthropic n'a pas d'endpoint /models public
                    models.append(f"{name.upper()}: claude-sonnet-4-20250514")
                    models.append(f"{name.upper()}: claude-haiku")

            return jsonify({"models": models})

        # -- HEALTH CHECK --
        @app.route("/_control/health/<backend_name>", methods=["GET"])
        def control_health(backend_name):
            with self._lock:
                if backend_name not in self.config["backends"]:
                    return jsonify({
                        "error": f"Backend inconnu : {backend_name}",
                    }), 404
                cfg = self.config["backends"][backend_name].copy()

            timeout = self.config["timeouts"]["health_check"]
            url = cfg["url"]
            fmt = cfg.get("format", "openai")

            if fmt == "openai":
                check_url = f"{url}/models"
            else:
                check_url = url

            try:
                resp = requests.get(check_url, timeout=timeout)
                reachable = resp.status_code < 500
            except requests.exceptions.RequestException:
                reachable = False

            return jsonify({
                "backend": backend_name,
                "reachable": reachable,
                "url": url,
            })

        # -- PROXY CATCH-ALL --
        @app.route(
            "/", defaults={"path": ""},
            methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        )
        @app.route(
            "/<path:path>",
            methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        )
        def proxy_request(path):
            if path.startswith("_control/"):
                return jsonify({"error": "Not found"}), 404

            cfg = self._get_current_config()
            target_url = f"{cfg['url']}/{path}"
            token = self._get_token(cfg)
            timeout = self.config["timeouts"]["proxy_request"]

            headers = {
                key: value
                for (key, value) in request.headers
                if key.lower() != "host"
            }
            if token:
                headers["x-api-key"] = token
                headers["Authorization"] = f"Bearer {token}"

            try:
                resp = requests.request(
                    method=request.method,
                    url=target_url,
                    headers=headers,
                    data=request.get_data(),
                    cookies=request.cookies,
                    allow_redirects=False,
                    stream=True,
                    timeout=timeout,
                )

                excluded_headers = {
                    "content-encoding",
                    "content-length",
                    "transfer-encoding",
                    "connection",
                }
                response_headers = [
                    (name, value)
                    for (name, value) in resp.raw.headers.items()
                    if name.lower() not in excluded_headers
                ]

                return Response(
                    resp.iter_content(chunk_size=10 * 1024),
                    status=resp.status_code,
                    headers=response_headers,
                )
            except requests.exceptions.RequestException as exc:
                logger.error(
                    "[ERROR] Proxy vers %s : %s", target_url, exc
                )
                return jsonify({
                    "error": f"Proxy Error: {str(exc)}",
                    "backend": self.current_backend,
                    "target": cfg["url"],
                }), 502

        return app


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    """Point d'entree principal du proxy router."""
    config_path = os.environ.get(
        "PROXY_CONFIG",
        os.path.join(os.path.dirname(__file__), "config.yaml"),
    )
    router = ProxyRouter(config_path=config_path)
    app = router.create_app()

    port = router.config.get("proxy_port", 9999)
    logger.info("[OK] Proxy Router demarre sur port %d", port)
    logger.info("[OK] Backend actif : %s", router.current_backend)

    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()

from flask import Blueprint, request, jsonify
import requests

subscriptions_bp = Blueprint("subscriptions", __name__)


@subscriptions_bp.route("/subscriptions/delete", methods=["POST"])
def subscriptions_delete():
    resp = requests.delete(
        url="http://binoas.openstate.eu/subscriptions/delete",
        json={
            "query_id": request.args.get("query_id", ""),
            "user_id": request.args.get("user_id", ""),
        },
    )
    try:
        result = resp.json()
    except Exception as e:
        result = {
            "error": "Er ging iets verkeerd",
            "status": "error",
            "msg": str(resp.content),
        }
    return jsonify(result)


@subscriptions_bp.route("/subscriptions/unsubscribe", methods=["POST"])
def do_unsubscribe():
    binoas_user = request.args.get("user_id")
    if binoas_user is None:
        return jsonify({"error": "No user_id provided"}), 400

    response = requests.get("http://binoas.openstate.eu/subscriptions")

    if response.status_code != 200:
        return jsonify({"error": "Error getting subscriptions"}), 500

    subscriptions = response.json()

    try:
        for subscription in subscriptions["results"]:
            if subscription["user_id"] != binoas_user:
                continue

            response = requests.delete(
                f"http://binoas.openstate.eu/subscriptions/delete/",
                json={
                    "user_id": subscription["user_id"],
                    "query_id": subscription["query_id"],
                },
            )

            if response.status_code != 200:
                return jsonify({"error": "Error deleting subscription"}), 500
    except:
        return jsonify({"error": "Error deleting subscriptions"}), 500

    return jsonify({"success": "true"}), 200

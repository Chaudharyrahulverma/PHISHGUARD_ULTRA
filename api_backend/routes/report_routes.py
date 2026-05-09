from flask import Blueprint, request, jsonify
from services.report_service import save_report

report_bp = Blueprint("report", __name__)


@report_bp.route("/report", methods=["POST"])
def report_issue():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    result = save_report(data)

    return jsonify(result)
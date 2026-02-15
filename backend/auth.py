import os
from flask import Blueprint, request, jsonify, session
from utils import login_required
auth_router = Blueprint("auth", __name__)

# ============================================================
# Login
# ============================================================
@auth_router.route("/login", methods=["POST"])
@login_required
def login():

    return jsonify({"success": True})
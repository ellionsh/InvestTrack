from flask import Flask, request, jsonify, abort
from models import db, Institution, Product
from config import DATABASE_URI
from decimal import Decimal
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/institutions", methods=["GET"])
    def list_institutions():
        items = Institution.query.all()
        return jsonify([i.to_dict() for i in items]), 200

    @app.route("/institutions", methods=["POST"])
    def create_institution():
        data = request.get_json() or {}
        name = data.get("name")
        if not name:
            return jsonify({"error": "name is required"}), 400
        inst = Institution(name=name)
        db.session.add(inst)
        db.session.commit()
        return jsonify(inst.to_dict()), 201

    @app.route("/institutions/<int:inst_id>/products", methods=["GET"])
    def list_products(inst_id):
        inst = Institution.query.get_or_404(inst_id)
        prods = inst.products.all()
        return jsonify([p.to_dict() for p in prods]), 200

    @app.route("/institutions/<int:inst_id>/products", methods=["POST"])
    def create_product(inst_id):
        inst = Institution.query.get_or_404(inst_id)
        data = request.get_json() or {}
        required = ["name", "invested_amount", "term_months"]
        for r in required:
            if r not in data:
                return jsonify({"error": f"{r} is required"}), 400

        p = Product(
            institution_id=inst.id,
            name=data.get("name"),
            invested_amount=Decimal(str(data.get("invested_amount"))),
            term_months=int(data.get("term_months")),
            purchase_date=data.get("purchase_date"),
            current_value=Decimal(str(data.get("current_value"))) if data.get("current_value") is not None else None,
            expected_profit=Decimal(str(data.get("expected_profit"))) if data.get("expected_profit") is not None else None,
            actual_profit=Decimal(str(data.get("actual_profit"))) if data.get("actual_profit") is not None else None,
            annualized_return=Decimal(str(data.get("annualized_return"))) if data.get("annualized_return") is not None else None
        )

        # If annualized_return not provided, compute if possible
        if p.annualized_return is None:
            computed = p.compute_annualized_return()
            if computed is not None:
                p.annualized_return = computed

        db.session.add(p)
        db.session.commit()
        return jsonify(p.to_dict()), 201

    @app.route("/products/<int:product_id>", methods=["GET"])
    def get_product(product_id):
        p = Product.query.get_or_404(product_id)
        return jsonify(p.to_dict()), 200

    @app.route("/products/<int:product_id>", methods=["PUT", "PATCH"])
    def update_product(product_id):
        p = Product.query.get_or_404(product_id)
        data = request.get_json() or {}

        # 更新允许的字段
        for field in ["name", "invested_amount", "term_months", "purchase_date", "current_value", "expected_profit", "actual_profit", "annualized_return"]:
            if field in data:
                val = data.get(field)
                if field in ["invested_amount", "current_value", "expected_profit", "actual_profit", "annualized_return"] and val is not None:
                    setattr(p, field, Decimal(str(val)))
                elif field == "term_months" and val is not None:
                    setattr(p, field, int(val))
                else:
                    setattr(p, field, val)

        # 如果没有提供 annualized_return，尝试计算
        if data.get("annualized_return") is None:
            computed = p.compute_annualized_return()
            if computed is not None:
                p.annualized_return = computed

        db.session.commit()
        return jsonify(p.to_dict()), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))

from flask_sqlalchemy import SQLAlchemy
from decimal import Decimal

db = SQLAlchemy()

class Institution(db.Model):
    __tablename__ = "institutions"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    products = db.relationship("Product", backref="institution", cascade="all, delete-orphan", lazy="dynamic")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "created_at": self.created_at.isoformat() if self.created_at else None}

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    institution_id = db.Column(db.BigInteger, db.ForeignKey("institutions.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    invested_amount = db.Column(db.Numeric(18,4), nullable=False)
    term_months = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.Date)
    current_value = db.Column(db.Numeric(18,4))
    expected_profit = db.Column(db.Numeric(18,4))
    actual_profit = db.Column(db.Numeric(18,4))
    annualized_return = db.Column(db.Numeric(10,6))  # e.g., 0.123456 for 12.3456%
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=db.func.current_timestamp(), server_onupdate=db.func.current_timestamp())

    def compute_annualized_return(self):
        # If invested_amount and current_value and term_months are present, compute annualized return:
        try:
            if self.invested_amount and self.current_value and self.term_months and float(self.invested_amount) > 0 and self.term_months > 0:
                invested = Decimal(self.invested_amount)
                current = Decimal(self.current_value)
                months = Decimal(self.term_months)
                years = months / Decimal(12)
                # Avoid division by zero for very small months
                if years == 0:
                    return None
                # Annualized return = (current / invested) ** (1 / years) - 1
                rate = (current / invested) ** (Decimal(1) / years) - Decimal(1)
                return round(rate, 6)
        except Exception:
            return None

    def to_dict(self):
        return {
            "id": self.id,
            "institution_id": self.institution_id,
            "name": self.name,
            "invested_amount": float(self.invested_amount) if self.invested_amount is not None else None,
            "term_months": self.term_months,
            "purchase_date": self.purchase_date.isoformat() if self.purchase_date else None,
            "current_value": float(self.current_value) if self.current_value is not None else None,
            "expected_profit": float(self.expected_profit) if self.expected_profit is not None else None,
            "actual_profit": float(self.actual_profit) if self.actual_profit is not None else None,
            "annualized_return": float(self.annualized_return) if self.annualized_return is not None else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

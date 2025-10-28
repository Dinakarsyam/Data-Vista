from flask import Blueprint, jsonify, request
from apps.models import SessionLocal, Order, Product
from sqlalchemy import func

sales_bp = Blueprint('sales_bp', __name__)

@sales_bp.route('/api/sales-manager/revenue_over_time', methods=['GET'])
def revenue_over_time_sales():
    storeid = request.args.get('storeid', type=int)
    db = SessionLocal()

    try:
        query = db.query(
            Product.category,
            Product.subcategory,
            func.sum(Order.profit).label('totalprofit')
        ).join(Product, Order.productid == Product.productid)

        if storeid:
            query = query.filter(Order.storeid == storeid)

        result = query.group_by(Product.category, Product.subcategory).all()

        return jsonify([{'category': r.category, 'subcategory': r.subcategory, 'totalprofit': r.totalprofit} for r in result])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@sales_bp.route('/api/sales-manager/average-order-value-over-time', methods=['GET'])
def average_order_value_over_time():
    store_id = request.args.get('store_id', type=int)
    db = SessionLocal()

    try:
        query = db.query(
            func.date_trunc('month', Order.orderdate).label('order_month'),
            func.avg(Order.totalprice).label('average_order_value')
        )

        if store_id:
            query = query.filter(Order.storeid == store_id)

        result = query.group_by('order_month').order_by('order_month').all()

        return jsonify([{'order_month': r.order_month.isoformat(), 'average_order_value': r.average_order_value} for r in result])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@sales_bp.route('/api/sales-manager/sales-by-category', methods=['GET'])
def sales_by_category_sales():
    store_id = request.args.get('store_id', type=int)
    db = SessionLocal()

    try:
        query = db.query(
            Product.category,
            Product.subcategory,
            func.sum(Order.totalprice).label('totalsales')
        ).join(Product, Order.productid == Product.productid)

        if store_id:
            query = query.filter(Order.storeid == store_id)

        result = query.group_by(Product.category, Product.subcategory).all()

        return jsonify([{'category': r.category, 'subcategory': r.subcategory, 'totalsales': r.totalsales} for r in result])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@sales_bp.route('/api/sales-manager/sales-over-time', methods=['GET'])
def sales_over_time():
    store_id = request.args.get('store_id', type=int)
    db = SessionLocal()

    try:
        query = db.query(
            Order.orderdate,
            func.sum(Order.totalprice).label('TotalSales')
        )

        if store_id:
            query = query.filter(Order.storeid == store_id)

        result = query.group_by(Order.orderdate).order_by(Order.orderdate).all()

        return jsonify([{'OrderDate': r.orderdate.isoformat(), 'TotalSales': r.TotalSales} for r in result])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@sales_bp.route('/api/sales-manager/profit-margin-over-time', methods=['GET'])
def profit_margin_over_time_sales():
    store_id = request.args.get('store_id', type=int)
    db = SessionLocal()

    try:
        query = db.query(
            Order.orderdate,
            func.sum(Order.profit).label('TotalProfit')
        )

        if store_id:
            query = query.filter(Order.storeid == store_id)

        result = query.group_by(Order.orderdate).order_by(Order.orderdate).all()

        return jsonify([{'orderdate': r.orderdate.isoformat(), 'TotalProfit': r.TotalProfit} for r in result])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@sales_bp.route('/api/sales-manager/customer-feedback', methods=['GET'])
def customer_feedback_sales():
    store_id = request.args.get('store_id', type=int)
    db = SessionLocal()

    try:
        query = db.query(
            Order.customerfeedback,
            func.count().label('feedbackcount')
        )

        if store_id:
            query = query.filter(Order.storeid == store_id)

        result = query.group_by(Order.customerfeedback).order_by(Order.customerfeedback).all()

        return jsonify([{'customerfeedback': r.customerfeedback, 'feedbackcount': r.feedbackcount} for r in result])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@sales_bp.route('/api/sales-manager/sales-mapping-by-country', methods=['GET'])
def sales_mapping_by_country_sales():
    store_id = request.args.get('store_id', type=int)
    db = SessionLocal()

    try:
        query = db.query(
            Store.storelocation,
            func.sum(Order.totalprice).label('TotalSales')
        ).join(Store, Order.storeid == Store.storeid)

        if store_id:
            query = query.filter(Order.storeid == store_id)

        result = query.group_by(Store.storelocation).order_by(Store.storelocation).all()

        return jsonify([{'Country': r.storelocation, 'TotalSales': r.TotalSales} for r in result])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@sales_bp.route('/api/sales-manager/discounts-promotions', methods=['GET'])
def get_discounts_promotions_sales():
    store_id = request.args.get('store_id', type=int)
    db = SessionLocal()

    try:
        query = db.query(
            func.sum(Order.totalprice).label('TotalSales'),
            func.when([(Order.discount > 0, 'Discounted')], else_='Regular').label('SalesType')
        )

        if store_id:
            query = query.filter(Order.storeid == store_id)

        result = query.group_by('SalesType').order_by('SalesType').all()

        return jsonify([{'SalesType': r.SalesType, 'TotalSales': r.TotalSales} for r in result])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@sales_bp.route('/api/sales-manager/order-status-distribution', methods=['GET'])
def order_status_distribution_sales():
    store_id = request.args.get('store_id', type=int)
    db = SessionLocal()

    try:
        query = db.query(
            Order.orderstatus,
            func.count(Order.orderid).label('OrderCount')
        )

        if store_id:
            query = query.filter(Order.storeid == store_id)

        result = query.group_by(Order.orderstatus).all()

        return jsonify([{'orderstatus': r.orderstatus, 'OrderCount': r.OrderCount} for r in result])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

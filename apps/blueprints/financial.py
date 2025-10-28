from flask import Blueprint, jsonify, request
from apps.models import Order, Product, Store
from sqlalchemy import func
from apps import db

financial_bp = Blueprint('financial_bp', __name__)

@financial_bp.route('/api/financial-analyst/customer-feedback', methods=['GET'])
def customer_feedback_financial():
    store_id = request.args.get('store_id', type=int)

    query = db.session.query(
        Order.customerfeedback,
        func.count().label('FeedbackCount')
    )

    if store_id:
        query = query.filter(Order.storeid == store_id)

    result = query.group_by(Order.customerfeedback).order_by(Order.customerfeedback).all()

    return jsonify([{'customerfeedback': r.customerfeedback, 'FeedbackCount': r.FeedbackCount} for r in result])

@financial_bp.route('/api/financial-analyst/order-status-distribution', methods=['GET'])
def order_status_distribution_financial():
    store_id = request.args.get('store_id', type=int)

    query = db.session.query(
        Order.orderstatus,
        func.count(Order.orderid).label('OrderCount')
    )

    if store_id:
        query = query.filter(Order.storeid == store_id)

    result = query.group_by(Order.orderstatus).all()

    return jsonify([{'orderstatus': r.orderstatus, 'OrderCount': r.OrderCount} for r in result])

@financial_bp.route('/api/financial-analyst/order-volume-over-time', methods=['GET'])
def order_volume_over_time_financial():
    store_id = request.args.get('store_id', type=int)

    query = db.session.query(
        Order.orderdate,
        func.count(Order.orderid).label('OrderCount')
    )

    if store_id:
        query = query.filter(Order.storeid == store_id)

    result = query.group_by(Order.orderdate).order_by(Order.orderdate).all()

    return jsonify([{'orderdate': r.orderdate.isoformat(), 'OrderCount': r.OrderCount} for r in result])

@financial_bp.route('/api/financial-analyst/profit-by-orderdate', methods=['GET'])
def profit_by_orderdate_financial():
    store_id = request.args.get('store_id', type=int)

    query = db.session.query(
        Order.orderdate,
        func.sum(Order.profit).label('TotalProfit')
    )

    if store_id:
        query = query.filter(Order.storeid == store_id)

    result = query.group_by(Order.orderdate).order_by(Order.orderdate).all()

    return jsonify([{'orderdate': r.orderdate.isoformat(), 'TotalProfit': r.TotalProfit} for r in result])

@financial_bp.route('/api/financial-analyst/revenue-over-time', methods=['GET'])
def revenue_over_time_financial():
    storeid = request.args.get('storeid', type=int)

    query = db.session.query(
        Order.orderdate,
        func.sum(Order.totalprice).label('TotalRevenue')
    )

    if storeid:
        query = query.filter(Order.storeid == storeid)

    result = query.group_by(Order.orderdate).order_by(Order.orderdate).all()

    return jsonify([{'orderdate': r.orderdate.isoformat(), 'TotalRevenue': r.TotalRevenue} for r in result])

@financial_bp.route('/api/financial-analyst/total-sales-map-overview', methods=['GET'])
def total_sales_map_overview_financial():
    store_id = request.args.get('store_id', type=int)

    query = db.session.query(
        Store.storelocation,
        func.sum(Order.totalprice).label('TotalSales')
    ).join(Store, Order.storeid == Store.storeid)

    if store_id:
        query = query.filter(Order.storeid == store_id)

    result = query.group_by(Store.storelocation).all()

    return jsonify([{'storelocation': r.storelocation, 'TotalSales': r.TotalSales} for r in result])

@financial_bp.route('/api/financial-analyst/profit-distribution', methods=['GET'])
def profit_distribution_financial():
    store_id = request.args.get('store_id', type=int)

    query = db.session.query(
        Product.category,
        func.sum(Order.profit).label('total_profit')
    ).join(Product, Order.productid == Product.productid)

    if store_id:
        query = query.filter(Order.storeid == store_id)

    result = query.group_by(Product.category).all()

    return jsonify([{'category': r.category, 'total_profit': r.total_profit} for r in result])

@financial_bp.route('/api/financial-analyst/profit-over-time', methods=['GET'])
def profit_over_time_financial():
    store_id = request.args.get('store_id', type=int)

    query = db.session.query(
        Order.orderdate,
        func.sum(Order.profit).label('TotalProfit')
    )

    if store_id:
        query = query.filter(Order.storeid == store_id)

    result = query.group_by(Order.orderdate).order_by(Order.orderdate).all()

    return jsonify([{'orderdate': r.orderdate.isoformat(), 'TotalProfit': r.TotalProfit} for r in result])

@financial_bp.route('/api/financial-analyst/revenue-vs-profit-by-category', methods=['GET'])
def revenue_vs_profit_by_category_financial():
    store_id = request.args.get('store_id', type=int)

    query = db.session.query(
        Product.category,
        func.sum(Order.totalprice).label('TotalRevenue'),
        func.sum(Order.profit).label('TotalProfit')
    ).join(Product, Order.productid == Product.productid)

    if store_id:
        query = query.filter(Order.storeid == store_id)

    result = query.group_by(Product.category).order_by(Product.category).all()

    return jsonify([{'Category': r.category, 'TotalRevenue': r.TotalRevenue, 'TotalProfit': r.TotalProfit} for r in result])

@financial_bp.route('/api/financial-analyst/profit-by-category', methods=['GET'])
def get_profit_by_category():
    store_id = request.args.get('store_id', type=int)

    query = db.session.query(
        Product.category,
        func.sum(Order.profit).label('total_profit')
    ).join(Product, Order.productid == Product.productid)

    if store_id:
        query = query.filter(Order.storeid == store_id)

    result = query.group_by(Product.category).order_by(func.sum(Order.profit).desc()).all()

    return jsonify([{'category': r.category, 'total_profit': r.total_profit} for r in result])

@financial_bp.route('/api/financial-analyst/profit-by-product', methods=['GET'])
def get_profit_by_product():
    store_id = request.args.get('store_id', type=int)

    query = db.session.query(
        Product.productname,
        func.sum(Order.profit).label('total_profit')
    ).join(Product, Order.productid == Product.productid)

    if store_id:
        query = query.filter(Order.storeid == store_id)

    result = query.group_by(Product.productname).order_by(func.sum(Order.profit).desc()).all()

    return jsonify([{'productname': r.productname, 'total_profit': r.total_profit} for r in result])

@financial_bp.route('/api/financial-analyst/data-metrics', methods=['GET'])
def get_metrics():
    store_id = request.args.get('store_id', type=int)

    kpi_query = db.session.query(
        func.sum(Order.totalprice).label('total_sales'),
        func.sum(Order.profit).label('total_profit'),
        func.count(Order.orderid).label('total_orders'),
        func.sum(Order.shippingcost).label('total_shipping'),
        ((func.sum(Order.totalprice) - func.sum(Order.costofgoodssold)) / func.sum(Order.totalprice) * 100).label('gross_margin')
    )

    if store_id:
        kpi_query = kpi_query.filter(Order.storeid == store_id)

    kpi_data = kpi_query.one()

    profit_over_time_query = db.session.query(
        func.date_trunc('month', Order.orderdate).label('month'),
        func.sum(Order.profit).label('total_profit')
    )

    if store_id:
        profit_over_time_query = profit_over_time_query.filter(Order.storeid == store_id)

    profit_over_time_data = profit_over_time_query.group_by('month').order_by('month').all()

    revenue_over_time_query = db.session.query(
        func.date_trunc('month', Order.orderdate).label('month'),
        func.sum(Order.totalprice).label('total_revenue')
    )

    if store_id:
        revenue_over_time_query = revenue_over_time_query.filter(Order.storeid == store_id)

    revenue_over_time_data = revenue_over_time_query.group_by('month').order_by('month').all()

    sales_by_region_query = db.session.query(
        func.trim(func.split_part(Store.storelocation, ',', 3)).label('country'),
        func.sum(Order.totalprice).label('total_sales')
    ).join(Store, Order.storeid == Store.storeid)

    if store_id:
        sales_by_region_query = sales_by_region_query.filter(Order.storeid == store_id)

    sales_by_region_data = sales_by_region_query.group_by('country').all()

    profit_distribution_query = db.session.query(
        Product.category,
        func.sum(Order.profit).label('total_profit')
    ).join(Product, Order.productid == Product.productid)

    if store_id:
        profit_distribution_query = profit_distribution_query.filter(Order.storeid == store_id)

    profit_distribution_data = profit_distribution_query.group_by(Product.category).all()

    revenue_vs_profit_query = db.session.query(
        Product.category,
        func.sum(Order.totalprice).label('total_revenue'),
        func.sum(Order.profit).label('total_profit')
    ).join(Product, Order.productid == Product.productid)

    if store_id:
        revenue_vs_profit_query = revenue_vs_profit_query.filter(Order.storeid == store_id)

    revenue_vs_profit_data = revenue_vs_profit_query.group_by(Product.category).all()

    result = {
        "kpi": {
            'total_sales': kpi_data.total_sales,
            'total_profit': kpi_data.total_profit,
            'total_orders': kpi_data.total_orders,
            'total_shipping': kpi_data.total_shipping,
            'gross_margin': kpi_data.gross_margin
        },
        "profit_over_time": [{'month': r.month.isoformat(), 'total_profit': r.total_profit} for r in profit_over_time_data],
        "revenue_over_time": [{'month': r.month.isoformat(), 'total_revenue': r.total_revenue} for r in revenue_over_time_data],
        "sales_by_region": [{'country': r.country, 'total_sales': r.total_sales} for r in sales_by_region_data],
        "profit_distribution": [{'category': r.category, 'total_profit': r.total_profit} for r in profit_distribution_data],
        "revenue_vs_profit": [{'category': r.category, 'total_revenue': r.total_revenue, 'total_profit': r.total_profit} for r in revenue_vs_profit_data],
    }
    return jsonify(result)

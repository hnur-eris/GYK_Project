import pandas as pd
from sqlalchemy import create_engine

class DataLoader:
    def __init__(self, user, password, host, db_name):
        self.user = user
        self.password = password
        self.host = host
        self.db_name = db_name
        self.engine = self.create_db_engine()

    def create_db_engine(self):
        url = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}/{self.db_name}"
        engine = create_engine(url)
        print("The connection was successful")
        return engine

    def load_data(self):        
        query = """
            SELECT
                o.order_id,
                o.order_date,
                o.customer_id,
                c.company_name,
                od.product_id,
                p.product_name,
                p.category_id,
                od.unit_price,
                od.quantity,
                od.discount,
                (od.unit_price * od.quantity * (1 - od.discount)) AS total_sales
            FROM orders o
            JOIN order_details od ON o.order_id = od.order_id
            JOIN products p ON od.product_id = p.product_id
            LEFT JOIN customers c ON o.customer_id = c.customer_id
        """
        df = pd.read_sql(query, self.engine)
        print(f"Data successfully loaded! Total number of records: {len(df)}")
        return df

    def get_all_products(self):
        query = """
        SELECT product_id, product_name, unit_price, category_id, discontinued
        FROM products
        """
        df = pd.read_sql(query, self.engine)
        return df

    def get_sales_summary(self):
        query = """
        SELECT
            EXTRACT(YEAR FROM o.order_date) AS year,
            EXTRACT(MONTH FROM o.order_date) AS month,
            p.product_name,
            SUM(od.quantity * od.unit_price * (1 - od.discount)) AS total_sales
        FROM order_details od
        JOIN orders o ON od.order_id = o.order_id
        JOIN products p ON od.product_id = p.product_id
        GROUP BY year, month, p.product_name
        ORDER BY year, month;
        """
        df = pd.read_sql(query, self.engine)
        return df
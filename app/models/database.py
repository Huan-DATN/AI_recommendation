from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config import Config
import json

# Create database engine
engine = create_engine(Config.DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    """Get a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def execute_query(query, params=None):
    """Execute a raw SQL query and return results"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query), params or {})
            # Convert each row to a dictionary with proper key handling
            return [dict(zip(result.keys(), row)) for row in result.fetchall()]
    except Exception as e:
        print(f"SQL execution error: {str(e)}")
        print(f"Query: {query}")
        print(f"Params: {params}")
        return []


def get_all_products():
    """Get all active products from the database"""
    try:
        # First, get basic product information
        base_query = """
        SELECT
            p."id", p."name", p."description", p."price", p."star", p."quantity",
            p."groupProductId", p."cityId", p."isActive", p."createdAt", p."updatedAt",
            g."name" as "groupName", c."name" as "cityName"
        FROM
            "Product" p
        LEFT JOIN
            "GroupProduct" g ON p."groupProductId" = g."id"
        LEFT JOIN
            "City" c ON p."cityId" = c."id"
        WHERE
            p."isActive" = true
            AND p."deletedAt" IS NULL
        """
        products = execute_query(base_query)

        # If no products found, return empty list
        if not products:
            return []

        # For each product, get its categories and images
        for product in products:
            product_id = product["id"]

            # Get categories
            categories_query = """
            SELECT cat."name"
            FROM "Category" cat
            JOIN "_CategoryToProduct" cp ON cat."id" = cp."A"
            WHERE cp."B" = :product_id
            """
            categories = execute_query(categories_query, {"product_id": product_id})
            product["categories"] = [cat["name"] for cat in categories] if categories else []

            # Get images
            images_query = """
            SELECT "publicUrl"
            FROM "Image"
            WHERE "productId" = :product_id
            """
            images = execute_query(images_query, {"product_id": product_id})
            product["images"] = [img["publicUrl"] for img in images] if images else []

        return products
    except Exception as e:
        print(f"Error fetching products: {str(e)}")
        return []


def get_product_by_id(product_id):
    """Get a specific product by ID"""
    try:
        # First, get basic product information
        base_query = """
        SELECT
            p."id", p."name", p."description", p."price", p."star", p."quantity",
            p."groupProductId", p."cityId", p."isActive", p."createdAt", p."updatedAt",
            g."name" as "groupName", c."name" as "cityName"
        FROM
            "Product" p
        LEFT JOIN
            "GroupProduct" g ON p."groupProductId" = g."id"
        LEFT JOIN
            "City" c ON p."cityId" = c."id"
        WHERE
            p."id" = :product_id
            AND p."isActive" = true
            AND p."deletedAt" IS NULL
        """
        products = execute_query(base_query, {"product_id": product_id})

        # If product not found, return None
        if not products:
            return None

        product = products[0]

        # Get categories
        categories_query = """
        SELECT cat."name"
        FROM "Category" cat
        JOIN "_CategoryToProduct" cp ON cat."id" = cp."A"
        WHERE cp."B" = :product_id
        """
        categories = execute_query(categories_query, {"product_id": product_id})
        product["categories"] = [cat["name"] for cat in categories] if categories else []

        # Get images
        images_query = """
        SELECT "publicUrl"
        FROM "Image"
        WHERE "productId" = :product_id
        """
        images = execute_query(images_query, {"product_id": product_id})
        product["images"] = [img["publicUrl"] for img in images] if images else []

        return product
    except Exception as e:
        print(f"Error fetching product {product_id}: {str(e)}")
        return None


def get_products_by_category(category_id):
    """Get products by category"""
    try:
        # First, get product IDs in this category
        product_ids_query = """
        SELECT "B" as "product_id"
        FROM "_CategoryToProduct"
        WHERE "A" = :category_id
        """
        product_ids_result = execute_query(product_ids_query, {"category_id": category_id})

        if not product_ids_result:
            return []

        product_ids = [item["product_id"] for item in product_ids_result]

        # Then get full product data for these IDs
        products = []
        for pid in product_ids:
            product = get_product_by_id(pid)
            if product:
                products.append(product)

        return products
    except Exception as e:
        print(f"Error fetching products for category {category_id}: {str(e)}")
        return []


def get_products_by_group(group_id):
    """Get products by group"""
    try:
        # Get basic product information
        base_query = """
        SELECT
            p."id", p."name", p."description", p."price", p."star", p."quantity",
            p."groupProductId", p."cityId", p."isActive", p."createdAt", p."updatedAt",
            g."name" as "groupName", c."name" as "cityName"
        FROM
            "Product" p
        LEFT JOIN
            "GroupProduct" g ON p."groupProductId" = g."id"
        LEFT JOIN
            "City" c ON p."cityId" = c."id"
        WHERE
            p."groupProductId" = :group_id
            AND p."isActive" = true
            AND p."deletedAt" IS NULL
        """
        products = execute_query(base_query, {"group_id": group_id})

        # If no products found, return empty list
        if not products:
            return []

        # For each product, get its categories and images
        for product in products:
            product_id = product["id"]

            # Get categories
            categories_query = """
            SELECT cat."name"
            FROM "Category" cat
            JOIN "_CategoryToProduct" cp ON cat."id" = cp."A"
            WHERE cp."B" = :product_id
            """
            categories = execute_query(categories_query, {"product_id": product_id})
            product["categories"] = [cat["name"] for cat in categories] if categories else []

            # Get images
            images_query = """
            SELECT "publicUrl"
            FROM "Image"
            WHERE "productId" = :product_id
            """
            images = execute_query(images_query, {"product_id": product_id})
            product["images"] = [img["publicUrl"] for img in images] if images else []

        return products
    except Exception as e:
        print(f"Error fetching products for group {group_id}: {str(e)}")
        return []

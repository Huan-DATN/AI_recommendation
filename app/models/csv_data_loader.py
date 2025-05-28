import pandas as pd
import os
from app.models.text_preprocessing import preprocess_text

def get_price_range(price):
    """Convert price to a categorical range for better recommendation"""
    # Since we don't have price in the CSV, we'll use a default value
    return "medium"

def load_csv_data(csv_path="app/data/product_data.csv"):
    """
    Load product data from CSV file

    Args:
        csv_path (str): Path to the CSV file

    Returns:
        pandas.DataFrame: DataFrame containing product data
    """
    try:
        # Check if file exists
        if not os.path.exists(csv_path):
            print(f"CSV file not found at {csv_path}")
            return None

        # Load CSV data
        df = pd.read_csv(csv_path)

        # Add ID column if not exists
        if 'id' not in df.columns:
            df['id'] = range(1, len(df) + 1)

        # Rename columns to match expected format
        column_mapping = {
            'Tên sản phẩm': 'name',
            'Số sao': 'star',
            'Xuất xứ': 'cityName',
            'Loại sản phẩm': 'groupName',
            'Hệ thống phân phối': 'distribution',
            'Từ khóa': 'keywords',
            'Trang Web': 'website',
            'Mô tả': 'description'
        }

        df = df.rename(columns=column_mapping)

        # Add missing columns with default values
        if 'price' not in df.columns:
            df['price'] = 100000  # Default price

        if 'categories' not in df.columns:
            # Extract categories from groupName if available
            df['categories'] = df['groupName'].apply(lambda x: [x] if pd.notna(x) else [])

        # Add additional fields for compatibility with the recommendation system
        df['quantity'] = 100  # Default quantity
        df['isActive'] = True
        df['groupProductId'] = 1  # Default group ID
        df['cityId'] = 1  # Default city ID

        # Prepare content features for recommendation
        df = prepare_content_features(df)

        return df

    except Exception as e:
        print(f"Error loading CSV data: {str(e)}")
        return None

def prepare_content_features(products_df):
    """Prepare content features from product data"""
    products_df['content'] = products_df.apply(
        lambda x: ' '.join(filter(None, [
            preprocess_text(str(x.get('name', ''))),
            preprocess_text(str(x.get('description', ''))),
            f"price_{get_price_range(x.get('price', 0))}",
            f"group_{preprocess_text(str(x.get('groupName', '')))}",
            f"city_{preprocess_text(str(x.get('cityName', '')))}",
            f"star_{str(x.get('star', 2))}",
            preprocess_text(str(x.get('keywords', ''))),
            ' '.join([f"category_{preprocess_text(cat)}" for cat in x.get('categories', []) if cat]) if isinstance(x.get('categories'), list) else '',
        ])),
        axis=1
    )
    return products_df

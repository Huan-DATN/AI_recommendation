# 🐍 Flask Project - Setup & Run Guide

Hướng dẫn từng bước để khởi tạo, cấu hình và chạy dự án Flask trong môi trường local.

---

## ✅ Yêu cầu hệ thống

- Python 3.8 trở lên
- pip
- Git (nếu clone dự án từ Git)

---

## 🚀 Bắt đầu

### 1. Tạo virtual environment (venv)

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 2. Cài đặt các thư viện cần thiết

```bash
pip install -r requirements.txt
```

---

### 3. Tạo file `.env` và cấu hình biến môi trường

Tạo một file tên là `.env` trong thư mục gốc của dự án và thêm các dòng sau:

```env
# Database
DB_URL=

# Gemini API
GEMINI_API_KEY=
GEMINI_MODEL=

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

> 💡 Gợi ý: Điền các thông tin kết nối thực tế vào những biến môi trường này. Không commit file `.env` lên Git để tránh lộ thông tin nhạy cảm.

---

### 4. Khởi động ứng dụng

```bash
python run.py
```

Mặc định, ứng dụng sẽ chạy ở địa chỉ `http://localhost:5000`.

## 📝 Ghi chú

- Luôn kích hoạt virtual environment trước khi chạy hoặc phát triển ứng dụng.
- Sử dụng `.env` để quản lý thông tin nhạy cảm một cách an toàn.
- Đảm bảo Redis và các dịch vụ liên quan đã được khởi chạy nếu ứng dụng cần.

---

## 📬 Liên hệ

Nếu bạn gặp vấn đề khi khởi động dự án, hãy kiểm tra kỹ các bước hoặc liên hệ với nhóm phát triển để được hỗ trợ.

# AI Recommendation Service

This service provides content-based recommendation functionality using TF-IDF and cosine similarity.

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on `.example.env` and configure your environment variables.

## Running the Service

Start the Flask server:

```bash
python run.py
```

The service will be available at http://localhost:5000.

## API Endpoints

### Train the Recommendation Model

```
POST /api/train
```

This endpoint fetches all products from the database and trains the recommendation model.

Response:

```json
{
	"message": "Content-based recommendation model trained successfully"
}
```

### Refresh the Recommendation Model

```
POST /api/refresh
```

This endpoint refreshes the recommendation model with the latest data from the database.

Response:

```json
{
	"message": "Content-based recommendation model trained successfully"
}
```

### Get Product Recommendations

```
GET /api/recommend?product_id=1&num=5
```

Parameters:

- `product_id`: ID of the product to get recommendations for
- `num`: Number of recommendations to return (default: 5)

Response:

```json
{
  "recommendations": [
    {
      "id": 2,
      "name": "Similar Product",
      "description": "Product description",
      "price": 249.99,
      "star": 3,
      "quantity": 15,
      "groupProductId": 5,
      "cityId": 2,
      "isActive": true,
      "groupName": "Wedding Dresses",
      "cityName": "New York",
      "categories": ["Dress", "Wedding"],
      "images": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
      "similarity_score": 0.87
    },
    ...
  ]
}
```

### Get Category Recommendations

```
GET /api/recommend/category?category_id=1&num=5
```

Parameters:

- `category_id`: ID of the category to get recommendations for
- `num`: Number of recommendations to return (default: 5)

Response:

```json
{
  "recommendations": [
    {
      "id": 2,
      "name": "Similar Product",
      "description": "Product description",
      "price": 249.99,
      "star": 3,
      "quantity": 15,
      "groupProductId": 5,
      "cityId": 2,
      "isActive": true,
      "groupName": "Wedding Dresses",
      "cityName": "New York",
      "categories": ["Dress", "Wedding"],
      "images": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
      "similarity_score": 0.87
    },
    ...
  ]
}
```

### Get Group Recommendations

```
GET /api/recommend/group?group_id=1&num=5
```

Parameters:

- `group_id`: ID of the product group to get recommendations for
- `num`: Number of recommendations to return (default: 5)

Response:

```json
{
  "recommendations": [
    {
      "id": 2,
      "name": "Similar Product",
      "description": "Product description",
      "price": 249.99,
      "star": 3,
      "quantity": 15,
      "groupProductId": 5,
      "cityId": 2,
      "isActive": true,
      "groupName": "Wedding Dresses",
      "cityName": "New York",
      "categories": ["Dress", "Wedding"],
      "images": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
      "similarity_score": 0.87
    },
    ...
  ]
}
```

## Database Integration

The recommendation system is integrated with the database:

1. **Product Data**: All product data is fetched directly from the database using the Prisma schema
2. **Enhanced Features**: Recommendations use product name, description, price, category, group, city, and images
3. **Multiple Recommendation Types**: Get recommendations by product, category, or product group
4. **Automatic Training**: The model is trained using all active products in the database
5. **Daily Updates**: The recommendation model is automatically refreshed daily at 3 AM

## How It Works

The content-based recommendation system works as follows:

1. **Feature Extraction**: Features from product name, description, price range, group product ID, city ID, and star rating are combined.
2. **TF-IDF Vectorization**: Text features are converted to TF-IDF vectors.
3. **Similarity Calculation**: Cosine similarity is used to find products similar to the target product.
4. **Recommendation**: The most similar products are returned as recommendations with similarity scores.

The model is trained once and then stored on disk for future recommendations.

## Code Structure

The recommendation system follows a clean architecture:

```
app/
├── models/
│   └── recommendation/
│       ├── __init__.py
│       ├── constants.py       # Constants and configuration
│       └── content_based.py   # Content-based recommendation model
├── services/
│   ├── __init__.py
│   └── recommendation_service.py  # Business logic layer
└── routes/
    └── recommendation.py      # API endpoints
```

### Components:

- **Models**: Core recommendation algorithms and data structures
- **Services**: Business logic that coordinates between models and routes
- **Routes**: API endpoints that handle HTTP requests and responses

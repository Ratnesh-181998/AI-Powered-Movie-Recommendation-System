# 🎬 Zee Movie Recommender System

A comprehensive movie recommendation system implementing multiple collaborative filtering approaches using the MovieLens 1M dataset.

## 📋 Project Overview

This project implements a complete recommender system with the following approaches:

1. **Item-based Pearson Correlation** - Recommends movies based on rating pattern similarity
2. **Item-based Cosine Similarity (KNN)** - Uses K-Nearest Neighbors with cosine distance
3. **Matrix Factorization** - Latent factor model using cmfrec library
4. **User-based Collaborative Filtering** - Personalized recommendations based on similar users

## 🎯 Concepts Tested

- ✅ Recommender Engine Design
- ✅ Collaborative Filtering (Item-based & User-based)
- ✅ Pearson Correlation
- ✅ Cosine Similarity
- ✅ K-Nearest Neighbors (KNN)
- ✅ Matrix Factorization (ALS)
- ✅ Sparse Matrix Representations (CSR)
- ✅ Model Evaluation (RMSE, MAPE)
- ✅ Embedding Visualization

## 📊 Dataset

**MovieLens 1M Dataset** containing:
- 1,000,209 ratings
- 3,883 movies
- 6,040 users
- Rating scale: 1-5 stars

### Data Files

- `ratings.dat` - User ratings (UserID::MovieID::Rating::Timestamp)
- `movies.dat` - Movie information (MovieID::Title::Genres)
- `users.dat` - User demographics (UserID::Gender::Age::Occupation::Zip-code)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download Dataset

Download the MovieLens 1M dataset from:
https://drive.google.com/drive/folders/1RY4RG7rVfY8-0uGeOPWqWzNIuf-iosuv

Extract the files to a `data/` folder in the project directory.

### 3. Run the Complete Pipeline

```bash
python main_recommender_pipeline.py
```

## 📁 Project Structure

```
Zee/
├── data/
│   ├── ratings.dat
│   ├── movies.dat
│   └── users.dat
├── movie_recommender_system.py          # Item-based approaches
├── matrix_factorization_recommender.py  # MF implementation
├── user_based_recommender.py            # User-based CF
├── main_recommender_pipeline.py         # Complete pipeline
├── requirements.txt
└── README.md
```

## 🔧 Individual Components

### Item-based Recommender

```python
from movie_recommender_system import MovieRecommenderSystem

recommender = MovieRecommenderSystem(data_path='./data/')
recommender.load_data().format_and_merge_data()

# Pearson Correlation
recommender.pearson_correlation_recommender("Liar Liar (1997)", top_n=5)

# Cosine Similarity
recommender.cosine_similarity_recommender("Liar Liar (1997)", top_n=5)

# KNN
recommender.knn_recommender("Liar Liar (1997)", top_n=5)
```

### Matrix Factorization

```python
from matrix_factorization_recommender import MatrixFactorizationRecommender

mf = MatrixFactorizationRecommender(ratings_df, movies_df, n_factors=4)
train_data, test_data = mf.train_test_split_data()
mf.train_model(train_data)
metrics = mf.evaluate_model(test_data)

# Item recommendations using embeddings
mf.get_item_recommendations_mf("Liar Liar (1997)", top_n=5)

# User recommendations
mf.get_user_recommendations_mf(user_id=1, top_n=10)

# Visualize embeddings
mf.visualize_embeddings_2d(n_movies=100)
```

### User-based Collaborative Filtering

```python
from user_based_recommender import UserBasedRecommender

user_rec = UserBasedRecommender(ratings_df, movies_df)
recommendations = user_rec.run_user_based_recommendation(
    n_movies_to_rate=15,
    top_similar_users=10,
    top_n_recommendations=10
)
```

## 📊 Output Files

The pipeline generates the following visualizations and reports:

1. **eda_visualizations.png** - Exploratory data analysis plots
2. **mf_evaluation.png** - Matrix factorization performance metrics
3. **mf_embeddings_2d.png** - 2D visualization of movie embeddings
4. **project_summary.txt** - Comprehensive project report

## 📝 Key Findings

### Questionnaire Answers

1. **Age group with most ratings**: 25 (25-34 age group)
2. **Occupation with most ratings**: Students and programmers
3. **Gender distribution**: ~72% Male, ~28% Female
4. **Most popular decade**: 1990s
5. **Most rated movie**: "American Beauty (1999)"
6. **Similarity ranges**:
   - Pearson Correlation: -1 to +1
   - Cosine Similarity: 0 to 1

### Model Performance

- **RMSE**: ~0.85-0.95 (Matrix Factorization)
- **MAPE**: ~15-20%
- **Sparsity**: ~95%+ (highly sparse data)

## 🎓 Implementation Highlights

### 1. Data Processing
- Proper handling of `::` separated files
- Feature engineering (release year extraction)
- Genre parsing and analysis
- Timestamp conversion

### 2. Exploratory Data Analysis
- Missing value analysis
- Distribution visualizations
- User and movie statistics
- Rating patterns

### 3. Recommendation Algorithms

**Pearson Correlation**
- Measures linear correlation between rating patterns
- Range: -1 (negative correlation) to +1 (positive correlation)
- Good for finding similar rating behaviors

**Cosine Similarity**
- Measures angle between rating vectors
- Range: 0 (orthogonal) to 1 (identical direction)
- Efficient with sparse matrices

**Matrix Factorization**
- Decomposes user-item matrix into latent factors
- Captures hidden preferences
- Handles sparsity well
- Enables embedding-based similarity

**User-based CF**
- Finds similar users
- Weighted recommendations
- Personalized for new users

### 4. Evaluation
- Train-test split
- RMSE (Root Mean Squared Error)
- MAPE (Mean Absolute Percentage Error)
- Visualization of predictions vs actuals

## 🔍 Advanced Features

### Sparse Matrix Representation
```python
# Dense matrix: [[1, 0], [3, 7]]
# Sparse (COO format): (0,0) 1  (1,0) 3  (1,1) 7
```

### CSR Matrix for Efficiency
- Compressed Sparse Row format
- Efficient for matrix operations
- Reduces memory usage for sparse data

### Embedding Visualization
- 2D projection of latent factors
- Reveals movie clusters
- Helps understand model behavior

## 🛠️ Technologies Used

- **Python 3.8+**
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **matplotlib/seaborn** - Visualization
- **scipy** - Statistical functions
- **scikit-learn** - KNN, metrics
- **cmfrec** - Matrix factorization

## 📈 Future Enhancements

1. **Hybrid Recommender** - Combine multiple approaches
2. **Content-based Filtering** - Use movie metadata
3. **Deep Learning** - Neural collaborative filtering
4. **Real-time Updates** - Online learning
5. **A/B Testing** - Compare recommendation strategies
6. **Cold Start Handling** - Better new user/item recommendations

## 📚 References

- MovieLens Dataset: https://grouplens.org/datasets/movielens/
- Collaborative Filtering: Koren et al., "Matrix Factorization Techniques for Recommender Systems"
- cmfrec Documentation: https://cmfrec.readthedocs.io/

## 👨‍💻 Author

Zee Recommender Systems Project

## 📄 License

This project is for educational purposes.

---

**Note**: Make sure to download the dataset and place it in the `data/` folder before running the scripts.

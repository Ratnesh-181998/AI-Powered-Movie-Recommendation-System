"""
QUICK START - Basic Recommender System
=======================================
Runs item-based approaches without requiring cmfrec
"""

import sys
sys.path.append('.')

from movie_recommender_system import MovieRecommenderSystem

def main():
    """Quick start with basic approaches"""
    
    print("\n" + "🎬"*50)
    print(" "*35 + "ZEE MOVIE RECOMMENDER SYSTEM")
    print(" "*40 + "QUICK START DEMO")
    print("🎬"*50 + "\n")
    
    # Initialize recommender
    print("Initializing recommender system...")
    recommender = MovieRecommenderSystem(data_path='./data/')
    
    # Load and process data
    print("\n📊 Loading and processing data...")
    (recommender
     .load_data()
     .format_and_merge_data()
     .perform_eda()
     .group_and_aggregate()
     .create_pivot_table()
     .visualize_data()
     .answer_questions())
    
    # Test movie for recommendations
    test_movie = "Liar Liar (1997)"
    
    print("\n" + "="*100)
    print(f"TESTING RECOMMENDATIONS FOR: {test_movie}")
    print("="*100)
    
    # 1. Pearson Correlation
    print("\n" + "🔵"*50)
    print("APPROACH 1: PEARSON CORRELATION")
    print("🔵"*50)
    pearson_recs = recommender.pearson_correlation_recommender(test_movie, top_n=5)
    
    # 2. Cosine Similarity
    print("\n" + "🟢"*50)
    print("APPROACH 2: COSINE SIMILARITY")
    print("🟢"*50)
    cosine_recs = recommender.cosine_similarity_recommender(test_movie, top_n=5)
    
    # 3. KNN
    print("\n" + "🟡"*50)
    print("APPROACH 3: K-NEAREST NEIGHBORS")
    print("🟡"*50)
    knn_recs = recommender.knn_recommender(test_movie, top_n=5)
    
    # Summary
    print("\n" + "="*100)
    print("✅ QUICK START COMPLETED SUCCESSFULLY!")
    print("="*100)
    
    print("\n📁 Generated Files:")
    print("   ✅ eda_visualizations.png - Exploratory data analysis plots")
    
    print("\n💡 Next Steps:")
    print("   1. Install cmfrec: pip install cmfrec")
    print("   2. Run full pipeline: python main_recommender_pipeline.py")
    print("   3. Explore individual modules for custom recommendations")
    
    print("\n" + "="*100 + "\n")
    
    return recommender


if __name__ == "__main__":
    try:
        recommender = main()
        print("🎉 Success! Check the generated visualizations.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease ensure:")
        print("  1. Data files are in ./data/ folder")
        print("  2. Required packages are installed: pip install -r requirements.txt")
        import traceback
        traceback.print_exc()

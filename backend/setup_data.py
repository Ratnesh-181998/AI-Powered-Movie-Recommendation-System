"""
DATA SETUP HELPER
=================
Helper script to check and guide data setup
"""

import os
import sys


def check_data_files():
    """Check if data files exist"""
    print("\n" + "="*80)
    print("DATA FILES CHECK")
    print("="*80)
    
    data_dir = './data'
    required_files = ['ratings.dat', 'movies.dat', 'users.dat']
    
    # Check if data directory exists
    if not os.path.exists(data_dir):
        print(f"\n❌ Data directory '{data_dir}' not found!")
        print("\n📥 Please follow these steps:")
        print("   1. Create a 'data' folder in the project directory")
        print("   2. Download the MovieLens 1M dataset from:")
        print("      https://drive.google.com/drive/folders/1RY4RG7rVfY8-0uGeOPWqWzNIuf-iosuv")
        print("   3. Extract the following files to the 'data' folder:")
        for file in required_files:
            print(f"      - {file}")
        
        # Create data directory
        os.makedirs(data_dir, exist_ok=True)
        print(f"\n✅ Created '{data_dir}' directory")
        return False
    
    # Check for required files
    missing_files = []
    existing_files = []
    
    for file in required_files:
        file_path = os.path.join(data_dir, file)
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            existing_files.append((file, file_size))
        else:
            missing_files.append(file)
    
    # Report status
    if existing_files:
        print("\n✅ Found data files:")
        for file, size in existing_files:
            print(f"   - {file} ({size:,} bytes)")
    
    if missing_files:
        print("\n❌ Missing data files:")
        for file in missing_files:
            print(f"   - {file}")
        
        print("\n📥 Please download from:")
        print("   https://drive.google.com/drive/folders/1RY4RG7rVfY8-0uGeOPWqWzNIuf-iosuv")
        return False
    
    print("\n✅ All required data files are present!")
    return True


def verify_data_format():
    """Verify data file format"""
    print("\n" + "="*80)
    print("DATA FORMAT VERIFICATION")
    print("="*80)
    
    try:
        import pandas as pd
        
        # Try to load ratings
        print("\n🔍 Checking ratings.dat...")
        ratings = pd.read_csv(
            './data/ratings.dat',
            sep='::',
            engine='python',
            names=['user_id', 'movie_id', 'rating', 'timestamp'],
            encoding='ISO-8859-1',
            nrows=10
        )
        print(f"   ✅ Format OK - Sample shape: {ratings.shape}")
        print(f"   Columns: {list(ratings.columns)}")
        
        # Try to load movies
        print("\n🔍 Checking movies.dat...")
        movies = pd.read_csv(
            './data/movies.dat',
            sep='::',
            engine='python',
            names=['movie_id', 'title', 'genres'],
            encoding='ISO-8859-1',
            nrows=10
        )
        print(f"   ✅ Format OK - Sample shape: {movies.shape}")
        print(f"   Columns: {list(movies.columns)}")
        
        # Try to load users
        print("\n🔍 Checking users.dat...")
        users = pd.read_csv(
            './data/users.dat',
            sep='::',
            engine='python',
            names=['user_id', 'gender', 'age', 'occupation', 'zip_code'],
            encoding='ISO-8859-1',
            nrows=10
        )
        print(f"   ✅ Format OK - Sample shape: {users.shape}")
        print(f"   Columns: {list(users.columns)}")
        
        print("\n✅ All data files have correct format!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error reading data files: {e}")
        return False


def main():
    """Main setup check"""
    print("\n" + "🎬"*40)
    print(" "*30 + "ZEE MOVIE RECOMMENDER SYSTEM")
    print(" "*35 + "DATA SETUP HELPER")
    print("🎬"*40)
    
    # Check files
    files_ok = check_data_files()
    
    if not files_ok:
        print("\n" + "="*80)
        print("⚠️  Please download and setup data files before running the recommender system")
        print("="*80 + "\n")
        return False
    
    # Verify format
    format_ok = verify_data_format()
    
    if format_ok:
        print("\n" + "="*80)
        print("✅ DATA SETUP COMPLETE!")
        print("="*80)
        print("\n🚀 You can now run the recommender system:")
        print("   python main_recommender_pipeline.py")
        print("\n" + "="*80 + "\n")
        return True
    else:
        print("\n" + "="*80)
        print("⚠️  Data format verification failed")
        print("="*80 + "\n")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

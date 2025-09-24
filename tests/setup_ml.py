#!/usr/bin/env python3
"""
Installation script for ML-enhanced recommendation system
Installs required dependencies and downloads pre-trained model
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing ML dependencies...")
    
    packages = [
        "Flask==3.1.1",
        "scikit-learn==1.4.2", 
        "numpy==1.26.4",
        "sentence-transformers==2.2.2",
        "torch==2.1.0",
        "transformers==4.35.0"
    ]
    
    for package in packages:
        try:
            print(f"   Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"   ✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {package}: {e}")
            return False
    
    return True

def download_model():
    """Download the pre-trained model"""
    print("\n🤖 Downloading pre-trained ML model...")
    
    try:
        from sentence_transformers import SentenceTransformer
        
        print("   Downloading paraphrase-multilingual-MiniLM-L12-v2...")
        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # Test the model
        test_texts = ["Python programming", "Développement Python"]
        embeddings = model.encode(test_texts)
        print(f"   ✅ Model downloaded and tested successfully!")
        print(f"   Model size: {len(embeddings[0])} dimensions")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to download model: {e}")
        return False

def test_installation():
    """Test the complete installation"""
    print("\n🧪 Testing installation...")
    
    try:
        # Test imports
        import flask
        import sklearn
        import numpy
        import sentence_transformers
        import torch
        import transformers
        
        print("   ✅ All packages imported successfully")
        
        # Test ML model
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # Test encoding
        test_text = "Python Django React"
        embedding = model.encode([test_text])
        
        print(f"   ✅ ML model working - embedding size: {len(embedding[0])}")
        print("   ✅ Installation test passed!")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Installation test failed: {e}")
        return False

def main():
    """Main installation process"""
    print("🚀 ML-Enhanced Recommendation System Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return False
    
    # Download model
    if not download_model():
        print("❌ Failed to download ML model")
        return False
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed")
        return False
    
    print("\n🎉 Installation completed successfully!")
    print("\nNext steps:")
    print("1. Run: python run.py")
    print("2. Test: python test_ml_enhanced.py")
    print("3. Check README.md for more details")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

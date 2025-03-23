import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def download_nltk_data():
    print("Downloading required NLTK data...")
    required_packages = [
        'punkt',
        'averaged_perceptron_tagger',
        'brown',
        'wordnet',
        'conll2000',
        'movie_reviews'
    ]
    
    for package in required_packages:
        try:
            nltk.download(package)
            print(f"Successfully downloaded {package}")
        except Exception as e:
            print(f"Error downloading {package}: {e}")

if __name__ == "__main__":
    download_nltk_data()
import sys
from url_analyzer import URLAnalyzer

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_auto_detection():
    analyzer = URLAnalyzer()
    
    print("=" * 80)
    print("AUTOMATIC DETECTION TEST (No comparison domain)")
    print("=" * 80)
    
    # Test without comparison domain - should detect from known list
    url = "https://tcsnextsttep.com"
    
    print(f"\nTesting: {url}")
    print("No comparison domain provided - using built-in known domains")
    print("-" * 80)
    
    result = analyzer.analyze(url)
    
    print(f"Risk Score: {result['risk_score']}/100")
    print(f"Suspicious: {result['is_suspicious']}")
    
    if result['warnings']:
        print(f"\nWarnings ({len(result['warnings'])}):")
        for warning in result['warnings']:
            print(f"  - {warning}")
    else:
        print("\nNo warnings detected")
    
    print(f"\nDetails:")
    details = result['details']
    print(f"  Domain: {details.get('parsed_domain', 'N/A')}")
    print(f"  Lookalike Match: {details.get('lookalike_match', 'None')}")
    print(f"  Similarity: {details.get('lookalike_similarity', 0)}%")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    test_auto_detection()

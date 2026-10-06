import sys
from url_analyzer import URLAnalyzer

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_typo_detection():
    analyzer = URLAnalyzer()
    
    print("=" * 80)
    print("TYPO DETECTION TEST")
    print("=" * 80)
    
    # Test the specific case: tcsnextsttep.com vs tcsnextstep.com
    url = "https://tcsnextsttep.com"
    compare_domain = "tcsnextstep.com"
    
    print(f"\nTesting: {url}")
    print(f"Comparing against: {compare_domain}")
    print("-" * 80)
    
    result = analyzer.analyze(url, compare_domain=compare_domain)
    
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
    print(f"  Has Repeated Chars: {details.get('has_repeated_chars', 'N/A')}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    test_typo_detection()

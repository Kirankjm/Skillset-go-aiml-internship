import sys
from url_analyzer import URLAnalyzer

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_url_analyzer():
    analyzer = URLAnalyzer()
    
    test_cases = [
        # Suspicious URLs
        ("http://paypa1.com", "Lookalike domain", None),
        ("http://google.com-security.xyz", "Suspicious TLD and structure", None),
        ("https://bit.ly/3abc123", "URL shortener", None),
        ("http://secure.login.fake-bank.com", "Multiple subdomains", None),
        ("http://sub1.sub2.sub3.sub4.evil.com", "Excessive subdomains", None),
        ("http://192.168.1.1/login", "IP address", None),
        ("http://xn--pple-43d.com", "Punycode (homograph attack)", None),
        ("http://my-secure-login-site.com", "Hyphens in domain", None),
        
        # Test with comparison domain (typo detection)
        ("https://tcsnextsttep.com", "Typo detection - extra 't'", "tcsnextstep.com"),
        
        # Legitimate URLs
        ("https://www.google.com", "Legitimate Google", None),
        ("https://amazon.com", "Legitimate Amazon", None),
        ("https://github.com", "Legitimate GitHub", None),
        ("https://paypal.com", "Legitimate PayPal", None),
    ]
    
    print("=" * 80)
    print("URL ANALYZER TEST RESULTS")
    print("=" * 80)
    
    for url, description, compare_domain in test_cases:
        print(f"\n{'=' * 80}")
        print(f"Testing: {description}")
        print(f"URL: {url}")
        if compare_domain:
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
        print(f"  Scheme: {details.get('scheme', 'N/A')}")
        print(f"  Domain: {details.get('parsed_domain', 'N/A')}")
        print(f"  HTTPS: {details.get('has_https', 'N/A')}")
        print(f"  Shortened: {details.get('is_shortened', 'N/A')}")
        print(f"  Subdomains: {details.get('subdomain_count', 'N/A')}")
        print(f"  Lookalike Match: {details.get('lookalike_match', 'None')}")
        print(f"  Suspicious TLD: {details.get('suspicious_tld', 'N/A')}")
        print(f"  IP Address: {details.get('is_ip_address', 'N/A')}")
        print(f"  Punycode: {details.get('is_punycode', 'N/A')}")
        print(f"  Hyphens: {details.get('has_hyphens', 'N/A')}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    test_url_analyzer()

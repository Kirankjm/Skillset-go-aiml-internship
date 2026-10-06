# Suspicious Link Checker

A Python Flask web application that analyzes URLs for potential phishing and security threats. The tool checks for various warning signs including lookalike domains, missing HTTPS, shortened links, excessive subdomains, and suspicious characters.

## Features

- **Lookalike Domain Detection**: Automatically identifies domains that resemble popular legitimate sites (e.g., `paypa1.com` vs `paypal.com`, `tcsnextsttep.com` vs `tcsnextstep.com`)
- **HTTPS Check**: Verifies if the URL uses secure HTTPS protocol
- **URL Shortener Detection**: Flags URLs from known URL shortening services
- **Subdomain Analysis**: Detects excessive subdomains often used to hide true domains
- **Suspicious Character Detection**: Identifies unusual character patterns
- **Suspicious TLD Check**: Flags domains with TLDs commonly used for malicious sites
- **IP Address Detection**: Identifies URLs using direct IP addresses
- **Punycode Detection**: Detects IDN homograph attacks using punycode encoding
- **Hyphen Detection**: Flags domains with hyphens (common in phishing)
- **Domain Length Check**: Identifies unusually long domain names
- **Repeated Character Detection**: Detects suspicious character repetitions that may indicate typos
- **WHOIS Lookup**: Attempts to verify domain ownership and registration age

## Installation

1. Install Python 3.8 or higher if not already installed

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python app.py
```

The application will start on `http://localhost:5000`

Open your browser and navigate to `http://localhost:5000` to use the link checker.

### How to Use

1. **Enter URL**: Paste any URL in the input field
2. **Click Check**: Click "Check URL" to analyze it for suspicious patterns
3. **View Results**: The tool will automatically detect lookalike domains, typos, and other security indicators. It compares against a built-in database of known legitimate domains including major tech companies, banks, and Indian corporations.

The tool will automatically detect:
- Typosquatting (e.g., `tcsnextsttep.com` vs `tcsnextstep.com`)
- Lookalike domains (e.g., `paypa1.com` vs `paypal.com`)
- Missing HTTPS
- URL shorteners
- Excessive subdomains
- Suspicious TLDs
- IP addresses
- And more...

## Testing Examples

The app includes several test URLs you can try:

- `paypa1.com` - Lookalike domain (should be flagged)
- `google.com-security.xyz` - Suspicious TLD and structure
- `bit.ly/3abc123` - URL shortener (should be flagged)
- `secure.login.fake-bank.com` - Multiple subdomains
- `www.google.com` - Legitimate site (should pass)
- `sub1.sub2.sub3.sub4.evil.com` - Excessive subdomains
- `192.168.1.1/login` - IP address usage
- `amazon.com` - Legitimate site (should pass)

## Risk Scoring

The tool calculates a risk score from 0-100 based on detected warning signs:

- **0-19**: Low risk - No major warning signs
- **20-49**: Medium risk - Some suspicious indicators
- **50-100**: High risk - Multiple serious warning signs

## API Endpoint

### POST /check

Analyzes a URL and returns detailed security analysis.

**Request Body:**
```json
{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "url": "https://example.com",
  "is_suspicious": false,
  "warnings": [],
  "risk_score": 0,
  "details": {
    "parsed_domain": "example.com",
    "registered_domain": "example.com",
    "scheme": "https",
    "has_https": true,
    "is_shortened": false,
    "subdomain_count": 0,
    "subdomains": [],
    "lookalike_match": null,
    "lookalike_similarity": 0,
    "suspicious_chars": [],
    "tld": "com",
    "suspicious_tld": false,
    "is_ip_address": false,
    "has_hyphens": false,
    "is_punycode": false,
    "decoded_domain": "example.com",
    "domain_length": 11,
    "has_repeated_chars": false,
    "whois_info": {
      "registrar": "Example Registrar",
      "creation_date": "2020-01-01",
      "updated_date": "2023-01-01",
      "country": "US"
    },
    "content_analysis": {
      "skipped": "Disabled for performance"
    }
  }
}
```

## Security Notes

This tool is designed to help identify potentially suspicious URLs, but it cannot guarantee 100% accuracy. Always:

- Verify URLs through official channels
- Look for additional security indicators (SSL certificates, domain age, etc.)
- Be cautious with URLs from unknown sources
- Use additional security tools and practices

## Limitations

- Cannot detect all sophisticated phishing attempts
- May produce false positives for legitimate sites with unusual structures
- Does not check actual website content or behavior
- Does not verify SSL certificate validity beyond checking HTTPS presence
- Lookalike detection is based on a predefined list of known domains

## License

This project is for educational purposes.

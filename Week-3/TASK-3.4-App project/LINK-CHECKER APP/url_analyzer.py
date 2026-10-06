import re
import idna
from urllib.parse import urlparse, urlunparse
from collections import Counter
import tldextract
import whois
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class URLAnalyzer:
    def __init__(self):
        # Known legitimate domains for lookalike comparison
        self.known_domains = {
            'google.com', 'facebook.com', 'amazon.com', 'apple.com',
            'microsoft.com', 'netflix.com', 'paypal.com', 'ebay.com',
            'twitter.com', 'instagram.com', 'linkedin.com', 'yahoo.com',
            'outlook.com', 'gmail.com', 'hotmail.com', 'bankofamerica.com',
            'chase.com', 'wellsfargo.com', 'citibank.com', 'paypal.com',
            'icloud.com', 'dropbox.com', 'adobe.com', 'spotify.com',
            'steam.com', 'epicgames.com', 'roblox.com', 'discord.com',
            'tiktok.com', 'snapchat.com', 'reddit.com', 'wikipedia.org',
            'youtube.com', 'zoom.us', 'slack.com', 'github.com',
            # Indian companies
            'tcs.com', 'tcsnextstep.com', 'infosys.com', 'wipro.com',
            'hcltech.com', 'techmahindra.com', 'accenture.com',
            # Banks
            'hdfcbank.com', 'icicibank.com', 'sbi.co.in', 'axisbank.com',
            'kotak.com', 'onlinesbi.com',
            # More tech companies
            'oracle.com', 'salesforce.com', 'sap.com', 'ibm.com',
            'cisco.com', 'vmware.com', 'intel.com', 'amd.com',
            'nvidia.com', 'samsung.com', 'sony.com', 'lg.com'
        }
        
        # Known URL shorteners
        self.shorteners = {
            'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'bit.do',
            'ow.ly', 'is.gd', 'buff.ly', 'adf.ly', 'bitly.com',
            'short.link', 'cutt.ly', 'rebrand.ly', 'snip.ly',
            'bl.ink', 'linktr.ee', 'tiny.cc', 'rb.gy', 'shrtco.de'
        }
        
        # Suspicious TLDs
        self.suspicious_tlds = {
            '.xyz', '.top', '.zip', '.mov', '.tk', '.ml', '.ga',
            '.cf', '.gq', '.cc', '.cn', '.ru', '.su', '.pw'
        }

    def analyze(self, url, compare_domain=None):
        """Perform comprehensive URL analysis
        
        Args:
            url: The URL to analyze
            compare_domain: Optional domain to compare against for lookalike detection
        """
        result = {
            'url': url,
            'is_suspicious': False,
            'warnings': [],
            'risk_score': 0,
            'details': {}
        }
        
        try:
            # Parse URL
            parsed = urlparse(url)
            
            if not parsed.scheme or not parsed.netloc:
                result['warnings'].append('Invalid URL format')
                result['is_suspicious'] = True
                result['risk_score'] += 30
                return result
            
            # Normalize domain
            domain = parsed.netloc.lower()
            if domain.startswith('www.'):
                domain = domain[4:]
            
            # Extract domain parts
            extracted = tldextract.extract(domain)
            registered_domain = f"{extracted.domain}.{extracted.suffix}"
            
            result['details']['parsed_domain'] = domain
            result['details']['registered_domain'] = registered_domain
            result['details']['scheme'] = parsed.scheme
            
            # Check 1: HTTPS
            https_check = self._check_https(parsed.scheme)
            result['details']['has_https'] = https_check['has_https']
            if https_check['warning']:
                result['warnings'].append(https_check['warning'])
                result['risk_score'] += https_check['risk']
            
            # Check 2: URL shortener
            shortener_check = self._check_shortener(domain)
            result['details']['is_shortened'] = shortener_check['is_shortened']
            if shortener_check['warning']:
                result['warnings'].append(shortener_check['warning'])
                result['risk_score'] += shortener_check['risk']
            
            # Check 3: Subdomain count
            subdomain_check = self._check_subdomains(extracted.subdomain)
            result['details']['subdomain_count'] = subdomain_check['count']
            result['details']['subdomains'] = subdomain_check['subdomains']
            if subdomain_check['warning']:
                result['warnings'].append(subdomain_check['warning'])
                result['risk_score'] += subdomain_check['risk']
            
            # Check 4: Lookalike domain (with optional user-specified domain)
            lookalike_check = self._check_lookalike(registered_domain, compare_domain)
            result['details']['lookalike_match'] = lookalike_check['match']
            result['details']['lookalike_similarity'] = lookalike_check.get('similarity', 0)
            if lookalike_check['warning']:
                result['warnings'].append(lookalike_check['warning'])
                result['risk_score'] += lookalike_check['risk']
            
            # Check 5: Suspicious characters
            char_check = self._check_suspicious_characters(domain)
            result['details']['suspicious_chars'] = char_check['suspicious_chars']
            if char_check['warning']:
                result['warnings'].append(char_check['warning'])
                result['risk_score'] += char_check['risk']
            
            # Check 6: Suspicious TLD
            tld_check = self._check_suspicious_tld(extracted.suffix)
            result['details']['tld'] = extracted.suffix
            result['details']['suspicious_tld'] = tld_check['is_suspicious']
            if tld_check['warning']:
                result['warnings'].append(tld_check['warning'])
                result['risk_score'] += tld_check['risk']
            
            # Check 7: IP address in domain
            ip_check = self._check_ip_address(domain)
            result['details']['is_ip_address'] = ip_check['is_ip']
            if ip_check['warning']:
                result['warnings'].append(ip_check['warning'])
                result['risk_score'] += ip_check['risk']
            
            # Check 8: Hyphenated domain
            hyphen_check = self._check_hyphens(extracted.domain)
            result['details']['has_hyphens'] = hyphen_check['has_hyphens']
            if hyphen_check['warning']:
                result['warnings'].append(hyphen_check['warning'])
                result['risk_score'] += hyphen_check['risk']
            
            # Check 9: Punycode/IDN homograph attacks
            punycode_check = self._check_punycode(domain)
            result['details']['is_punycode'] = punycode_check['is_punycode']
            result['details']['decoded_domain'] = punycode_check['decoded']
            if punycode_check['warning']:
                result['warnings'].append(punycode_check['warning'])
                result['risk_score'] += punycode_check['risk']
            
            # Check 10: Long domain name
            length_check = self._check_domain_length(domain)
            result['details']['domain_length'] = length_check['length']
            if length_check['warning']:
                result['warnings'].append(length_check['warning'])
                result['risk_score'] += length_check['risk']
            
            # Check 11: Repeated characters (typo detection)
            repeat_check = self._check_repeated_characters(extracted.domain)
            result['details']['has_repeated_chars'] = repeat_check['has_repeats']
            if repeat_check['warning']:
                result['warnings'].append(repeat_check['warning'])
                result['risk_score'] += repeat_check['risk']
            
            # Check 12: WHOIS domain ownership (with timeout)
            whois_check = self._check_whois(registered_domain)
            result['details']['whois_info'] = whois_check['info']
            if whois_check['warning']:
                result['warnings'].append(whois_check['warning'])
                result['risk_score'] += whois_check['risk']
            
            # Check 13: Page content analysis (for phishing detection) - optional/slow
            # content_check = self._check_page_content(url)
            # result['details']['content_analysis'] = content_check['analysis']
            # if content_check['warning']:
            #     result['warnings'].append(content_check['warning'])
            #     result['risk_score'] += content_check['risk']
            result['details']['content_analysis'] = {'skipped': 'Disabled for performance'}
            
            # Determine overall suspicion
            result['is_suspicious'] = result['risk_score'] >= 20
            
            # Cap risk score at 100
            result['risk_score'] = min(result['risk_score'], 100)
            
        except Exception as e:
            result['warnings'].append(f'Error analyzing URL: {str(e)}')
            result['is_suspicious'] = True
            result['risk_score'] = 50
        
        return result
    
    def _check_https(self, scheme):
        """Check if URL uses HTTPS"""
        if scheme != 'https':
            return {
                'has_https': False,
                'warning': 'No HTTPS encryption - connection is not secure',
                'risk': 15
            }
        return {'has_https': True, 'warning': None, 'risk': 0}
    
    def _check_shortener(self, domain):
        """Check if domain is a known URL shortener"""
        for shortener in self.shorteners:
            if shortener in domain:
                return {
                    'is_shortened': True,
                    'warning': f'URL uses known shortener ({shortener}) - destination is hidden',
                    'risk': 25
                }
        return {'is_shortened': False, 'warning': None, 'risk': 0}
    
    def _check_subdomains(self, subdomain):
        """Check for excessive subdomains"""
        if not subdomain:
            return {'count': 0, 'subdomains': [], 'warning': None, 'risk': 0}
        
        subdomains = [s for s in subdomain.split('.') if s]
        count = len(subdomains)
        
        if count >= 4:
            return {
                'count': count,
                'subdomains': subdomains,
                'warning': f'Excessive subdomains ({count}) - may be trying to hide true domain',
                'risk': 20
            }
        elif count >= 3:
            return {
                'count': count,
                'subdomains': subdomains,
                'warning': f'Multiple subdomains ({count}) - suspicious structure',
                'risk': 10
            }
        
        return {'count': count, 'subdomains': subdomains, 'warning': None, 'risk': 0}
    
    def _check_lookalike(self, registered_domain, compare_domain=None):
        """Check for lookalike/squatting domains
        
        Args:
            registered_domain: The domain to check
            compare_domain: Optional specific domain to compare against
        """
        domains_to_check = self.known_domains.copy()
        
        # If user provided a specific domain to compare, prioritize it
        if compare_domain:
            domains_to_check.add(compare_domain.lower())
        
        for known in domains_to_check:
            similarity = self._calculate_similarity(registered_domain, known)
            if similarity >= 0.75:  # 75% similarity threshold (more sensitive)
                if registered_domain != known:
                    return {
                        'match': known,
                        'similarity': round(similarity * 100, 1),
                        'warning': f'Lookalike domain - {similarity*100:.1f}% similar to {known} but is different',
                        'risk': 35
                    }
        return {'match': None, 'similarity': 0, 'warning': None, 'risk': 0}
    
    def _calculate_similarity(self, s1, s2):
        """Calculate string similarity using Levenshtein distance"""
        if s1 == s2:
            return 1.0
        
        len1, len2 = len(s1), len(s2)
        if len1 == 0 or len2 == 0:
            return 0.0
        
        # Dynamic programming for Levenshtein distance
        matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        
        for i in range(len1 + 1):
            matrix[i][0] = i
        for j in range(len2 + 1):
            matrix[0][j] = j
        
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                cost = 0 if s1[i-1] == s2[j-1] else 1
                matrix[i][j] = min(
                    matrix[i-1][j] + 1,      # deletion
                    matrix[i][j-1] + 1,      # insertion
                    matrix[i-1][j-1] + cost  # substitution
                )
        
        distance = matrix[len1][len2]
        max_len = max(len1, len2)
        similarity = 1 - (distance / max_len)
        return similarity
    
    def _check_suspicious_characters(self, domain):
        """Check for suspicious characters in domain"""
        suspicious_chars = []
        
        # Check for numbers mixed with letters (common in phishing)
        if re.search(r'[a-z]\d+[a-z]', domain):
            suspicious_chars.append('numbers in middle of letters')
        
        # Check for repeated characters
        if re.search(r'(.)\1{3,}', domain):
            suspicious_chars.append('repeated characters')
        
        # Check for special characters (aside from hyphens and dots)
        special_chars = re.findall(r'[^a-z0-9\-\.]', domain)
        if special_chars:
            suspicious_chars.extend([f'special char: {c}' for c in special_chars])
        
        if suspicious_chars:
            return {
                'suspicious_chars': suspicious_chars,
                'warning': f'Suspicious characters detected: {", ".join(suspicious_chars)}',
                'risk': 15
            }
        
        return {'suspicious_chars': [], 'warning': None, 'risk': 0}
    
    def _check_suspicious_tld(self, tld):
        """Check if TLD is commonly used for malicious sites"""
        if tld.lower() in self.suspicious_tlds:
            return {
                'is_suspicious': True,
                'warning': f'Suspicious TLD (.{tld}) - often used for malicious sites',
                'risk': 20
            }
        return {'is_suspicious': False, 'warning': None, 'risk': 0}
    
    def _check_ip_address(self, domain):
        """Check if domain is an IP address"""
        # IPv4 pattern
        ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        # IPv6 pattern (simplified)
        ipv6_pattern = r'^[0-9a-f:]+$'
        
        domain_clean = domain.split(':')[0]  # Remove port if present
        
        if re.match(ipv4_pattern, domain_clean) or re.match(ipv6_pattern, domain_clean):
            return {
                'is_ip': True,
                'warning': 'Domain is an IP address - bypasses domain name checks',
                'risk': 30
            }
        
        return {'is_ip': False, 'warning': None, 'risk': 0}
    
    def _check_hyphens(self, domain):
        """Check for hyphens in domain name"""
        if '-' in domain:
            hyphen_count = domain.count('-')
            if hyphen_count >= 2:
                return {
                    'has_hyphens': True,
                    'warning': f'Multiple hyphens in domain ({hyphen_count}) - often used in phishing',
                    'risk': 15
                }
            return {
                'has_hyphens': True,
                'warning': 'Hyphen in domain - can be used to mimic legitimate sites',
                'risk': 8
            }
        return {'has_hyphens': False, 'warning': None, 'risk': 0}
    
    def _check_punycode(self, domain):
        """Check for punycode encoding (IDN homograph attacks)"""
        if 'xn--' in domain:
            try:
                decoded = idna.decode(domain)
                return {
                    'is_punycode': True,
                    'decoded': decoded,
                    'warning': f'Punycode encoding detected - decoded as: {decoded} (possible homograph attack)',
                    'risk': 40
                }
            except:
                return {
                    'is_punycode': True,
                    'decoded': 'Unable to decode',
                    'warning': 'Punycode encoding detected - possible homograph attack',
                    'risk': 40
                }
        return {'is_punycode': False, 'decoded': domain, 'warning': None, 'risk': 0}
    
    def _check_domain_length(self, domain):
        """Check for unusually long domain names"""
        length = len(domain)
        if length > 50:
            return {
                'length': length,
                'warning': f'Unusually long domain name ({length} characters)',
                'risk': 10
            }
        return {'length': length, 'warning': None, 'risk': 0}
    
    def _check_repeated_characters(self, domain):
        """Check for repeated characters that might indicate typos"""
        # Check for double letters (common typos)
        if re.search(r'(.)\1{2,}', domain):  # 3+ same chars in a row
            return {
                'has_repeats': True,
                'warning': 'Repeated characters detected - possible typo',
                'risk': 10
            }
        
        # Check for character swapping patterns (e.g., "sttep" vs "step")
        common_typos = {
            'pp': 'p', 'tt': 't', 'ee': 'e', 'oo': 'o', 'll': 'l',
            'ss': 's', 'nn': 'n', 'mm': 'm', 'rr': 'r'
        }
        
        for typo, original in common_typos.items():
            if typo in domain and domain.count(typo) > 1:
                return {
                    'has_repeats': True,
                    'warning': f'Suspicious character repetition ({typo}) - possible typo',
                    'risk': 15
                }
        
        return {'has_repeats': False, 'warning': None, 'risk': 0}
    
    def _check_whois(self, domain):
        """Check WHOIS information for domain ownership"""
        try:
            w = whois.whois(domain)
            
            info = {
                'registrar': w.registrar if w.registrar else 'Unknown',
                'creation_date': str(w.creation_date) if w.creation_date else 'Unknown',
                'updated_date': str(w.updated_date) if w.updated_date else 'Unknown',
                'country': w.country if w.country else 'Unknown'
            }
            
            # Check if domain is very new (suspicious)
            if w.creation_date:
                if isinstance(w.creation_date, list):
                    creation_date = w.creation_date[0]
                else:
                    creation_date = w.creation_date
                
                days_old = (datetime.now() - creation_date).days
                if days_old < 30:
                    info['age_warning'] = f'Domain is only {days_old} days old'
                    return {
                        'info': info,
                        'warning': f'Very new domain ({days_old} days old) - recently registered domains are often used for phishing',
                        'risk': 25
                    }
                elif days_old < 90:
                    info['age_warning'] = f'Domain is {days_old} days old'
                    return {
                        'info': info,
                        'warning': f'Recently registered domain ({days_days} days) - exercise caution',
                        'risk': 15
                    }
            
            return {'info': info, 'warning': None, 'risk': 0}
            
        except Exception as e:
            return {
                'info': {'error': str(e)},
                'warning': 'Unable to verify domain ownership - WHOIS lookup failed',
                'risk': 10
            }
    
    def _check_page_content(self, url):
        """Analyze page content for phishing indicators"""
        try:
            # Only fetch if using HTTPS to avoid security issues
            if not url.startswith('https://'):
                return {
                    'analysis': {'skipped': 'Not HTTPS'},
                    'warning': None,
                    'risk': 0
                }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            
            if response.status_code != 200:
                return {
                    'analysis': {'status': response.status_code},
                    'warning': None,
                    'risk': 0
                }
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            analysis = {
                'title': soup.title.string if soup.title else 'No title',
                'has_login_form': bool(soup.find('form')),
                'has_password_field': bool(soup.find('input', {'type': 'password'})),
                'has_credit_card_field': bool(soup.find('input', {'name': re.compile(r'card|cc', re.I)})),
                'external_links': len(soup.find_all('a', href=re.compile(r'^http'))),
                'suspicious_keywords': []
            }
            
            # Check for suspicious keywords in page text
            suspicious_keywords = [
                'verify your account', 'confirm your identity', 'urgent action required',
                'account suspended', 'security alert', 'unusual activity',
                'update payment', 'verify information', 'confirm details'
            ]
            
            page_text = soup.get_text().lower()
            for keyword in suspicious_keywords:
                if keyword in page_text:
                    analysis['suspicious_keywords'].append(keyword)
            
            # Calculate risk based on content
            risk = 0
            warnings = []
            
            if analysis['has_password_field'] and analysis['has_login_form']:
                risk += 10
            
            if analysis['has_credit_card_field']:
                risk += 20
                warnings.append('Page requests credit card information')
            
            if len(analysis['suspicious_keywords']) >= 2:
                risk += 25
                warnings.append(f'Page contains suspicious phrases: {", ".join(analysis["suspicious_keywords"][:3])}')
            
            if risk > 0:
                return {
                    'analysis': analysis,
                    'warning': '; '.join(warnings),
                    'risk': risk
                }
            
            return {'analysis': analysis, 'warning': None, 'risk': 0}
            
        except Exception as e:
            return {
                'analysis': {'error': str(e)},
                'warning': None,
                'risk': 0
            }

from app.utils.ml_utils import PhishingDetector

class PhishingSimulator:
    """Simulates phishing detection and analysis"""
    
    def __init__(self):
        self.detector = PhishingDetector()
    
    def analyze_email(self, email_subject: str, email_body: str, 
                     sender_email: str = "") -> dict:
        """Analyze email for phishing indicators"""
        return self.detector.detect_phishing(email_subject, email_body, sender_email)
    
    def simulate_campaign(self, emails: list) -> dict:
        """Simulate a phishing campaign with multiple emails"""
        results = []
        total_phishing_score = 0
        total_click_rate = 0
        
        for email in emails:
            analysis = self.analyze_email(
                email.get('subject', ''),
                email.get('body', ''),
                email.get('sender', '')
            )
            results.append({
                'email': email,
                'analysis': analysis
            })
            total_phishing_score += analysis['phishing_score']
            total_click_rate += analysis['click_rate_simulation']
        
        avg_phishing_score = total_phishing_score / len(emails) if emails else 0
        avg_click_rate = total_click_rate / len(emails) if emails else 0
        
        return {
            'campaign_results': results,
            'average_phishing_score': round(avg_phishing_score, 2),
            'average_click_rate': round(avg_click_rate, 2),
            'total_emails': len(emails),
            'high_risk_emails': sum(1 for r in results if r['analysis']['phishing_score'] > 70)
        }

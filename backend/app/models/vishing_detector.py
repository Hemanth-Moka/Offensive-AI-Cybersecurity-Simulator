from app.utils.ml_utils import VishingDetector

class VishingSimulator:
    """Simulates voice phishing (vishing) detection and analysis"""
    
    def __init__(self):
        self.detector = VishingDetector()
    
    def analyze_call(self, call_script: str, caller_id: str = "", call_duration: float = 0) -> dict:
        """Analyze voice call script for vishing indicators"""
        return self.detector.detect_vishing(call_script, caller_id, call_duration)
    
    def simulate_campaign(self, calls: list) -> dict:
        """Simulate a vishing campaign with multiple calls"""
        results = []
        total_vishing_score = 0
        total_success_rate = 0
        
        for call in calls:
            analysis = self.analyze_call(
                call.get('script', ''),
                call.get('caller_id', ''),
                call.get('duration', 0)
            )
            results.append({
                'call': call,
                'analysis': analysis
            })
            total_vishing_score += analysis['vishing_score']
            total_success_rate += analysis['success_rate_simulation']
        
        avg_vishing_score = total_vishing_score / len(calls) if calls else 0
        avg_success_rate = total_success_rate / len(calls) if calls else 0
        
        return {
            'campaign_results': results,
            'average_vishing_score': round(avg_vishing_score, 2),
            'average_success_rate': round(avg_success_rate, 2),
            'total_calls': len(calls),
            'high_risk_calls': sum(1 for r in results if r['analysis']['vishing_score'] > 70)
        }

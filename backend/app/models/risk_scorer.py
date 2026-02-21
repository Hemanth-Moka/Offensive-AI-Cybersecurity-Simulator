from typing import Dict, List

class RiskScorer:
    """Calculate comprehensive risk scores for security assessments"""
    
    @staticmethod
    def calculate_password_risk(password_data: Dict) -> Dict:
        """Calculate overall password risk score"""
        if not password_data.get('cracked'):
            return {
                'overall_risk': 0,
                'risk_level': 'Low',
                'factors': ['Password not cracked in simulation']
            }
        
        pattern_analysis = password_data.get('pattern_analysis', {})
        risk_score = password_data.get('risk_score', 0)
        
        factors = []
        
        # Analyze risk factors
        if pattern_analysis.get('strength_score', 100) < 50:
            factors.append('Weak password strength')
        
        if len(pattern_analysis.get('patterns_found', [])) > 2:
            factors.append('Multiple weak patterns detected')
        
        if pattern_analysis.get('length', 0) < 8:
            factors.append('Password too short')
        
        if pattern_analysis.get('complexity', 0) < 3:
            factors.append('Insufficient character variety')
        
        if password_data.get('attempts', 0) < 100:
            factors.append('Cracked with minimal attempts')
        
        # Determine risk level
        if risk_score >= 80:
            risk_level = 'Critical'
        elif risk_score >= 60:
            risk_level = 'High'
        elif risk_score >= 40:
            risk_level = 'Medium'
        elif risk_score >= 20:
            risk_level = 'Low'
        else:
            risk_level = 'Very Low'
        
        return {
            'overall_risk': round(risk_score, 2),
            'risk_level': risk_level,
            'factors': factors,
            'recommendations': RiskScorer._get_password_recommendations(risk_score, pattern_analysis)
        }
    
    @staticmethod
    def _get_password_recommendations(risk_score: float, pattern_analysis: Dict) -> List[str]:
        """Generate password security recommendations"""
        recommendations = []
        
        if risk_score > 70:
            recommendations.append("CRITICAL: Change password immediately")
            recommendations.append("Use a password manager to generate strong passwords")
        
        if pattern_analysis.get('length', 0) < 12:
            recommendations.append("Use passwords with at least 12 characters")
        
        if pattern_analysis.get('complexity', 0) < 4:
            recommendations.append("Include uppercase, lowercase, numbers, and special characters")
        
        if len(pattern_analysis.get('patterns_found', [])) > 0:
            recommendations.append("Avoid common patterns like sequential numbers or keyboard walks")
        
        if not recommendations:
            recommendations.append("Password appears strong, maintain current practices")
        
        return recommendations
    
    @staticmethod
    def calculate_phishing_risk(phishing_data: Dict) -> Dict:
        """Calculate overall phishing risk score"""
        phishing_score = phishing_data.get('phishing_score', 0)
        
        factors = []
        
        if phishing_score > 70:
            factors.append('High phishing likelihood detected')
        
        if phishing_data.get('urgency_score', 0) > 50:
            factors.append('High urgency indicators')
        
        if phishing_data.get('emotional_manipulation_score', 0) > 50:
            factors.append('Emotional manipulation tactics identified')
        
        if len(phishing_data.get('suspicious_keywords', [])) > 5:
            factors.append('Multiple suspicious keywords found')
        
        # Determine risk level
        if phishing_score >= 80:
            risk_level = 'Critical'
        elif phishing_score >= 60:
            risk_level = 'High'
        elif phishing_score >= 40:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        return {
            'overall_risk': round(phishing_score, 2),
            'risk_level': risk_level,
            'factors': factors,
            'recommendations': phishing_data.get('recommendations', [])
        }

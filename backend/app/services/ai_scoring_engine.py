"""
Advanced AI Scoring Engine for cybersecurity threat analysis
"""
import string
import math
import re
from typing import Dict, List, Tuple, Any
from collections import Counter
import hashlib
from datetime import datetime, timedelta

class AIScoringEngine:
    """
    Enterprise-grade AI scoring engine for:
    - Password strength analysis
    - Phishing/phishing detection
    - Vishing (voice phishing) detection
    - Behavioral risk assessment
    - Adaptive threat modeling
    """
    
    def __init__(self):
        self.common_passwords = self._load_common_passwords()
        self.phishing_keywords = self._load_phishing_keywords()
        self.vishing_keywords = self._load_vishing_keywords()
        self.social_engineering_patterns = self._load_se_patterns()
    
    # ==================== PASSWORD ANALYSIS ====================
    
    def analyze_password(self, password: str, metadata: Dict = None) -> Dict:
        """
        Comprehensive password strength analysis
        Returns: strength_score, entropy, crack_time, patterns, recommendations
        """
        metadata = metadata or {}
        
        strength_score = self._calculate_strength_score(password, metadata)
        entropy_score = self._calculate_entropy(password)
        crack_time = self._estimate_crack_time(password, entropy_score)
        patterns = self._detect_password_patterns(password, metadata)
        behavioral_risk = self._assess_behavioral_risk(password, metadata)
        vulnerability_factors = self._identify_vulnerabilities(password, patterns)
        recommendations = self._generate_password_recommendations(strength_score, patterns, vulnerability_factors)
        
        return {
            "strength_score": round(strength_score, 2),
            "entropy_score": round(entropy_score, 2),
            "crack_time_seconds": crack_time,
            "attack_success_probability": round(self._calculate_attack_success(strength_score), 2),
            "behavioral_risk_score": round(behavioral_risk, 2),
            "patterns_detected": patterns,
            "vulnerability_factors": vulnerability_factors,
            "recommendations": recommendations,
            "crack_time_readable": self._format_crack_time(crack_time)
        }
    
    def _calculate_strength_score(self, password: str, metadata: Dict) -> float:
        """Calculate password strength (0-100)"""
        score = 0
        
        # Length scoring (base)
        length = len(password)
        if length >= 8:
            score += 20
        elif length >= 6:
            score += 10
        else:
            score += 5
        
        # Character variety
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:,.<>?]', password))
        
        variety_score = sum([has_lower, has_upper, has_digit, has_special]) * 15
        score += min(variety_score, 60)
        
        # Deductions for common patterns
        is_common = password.lower() in self.common_passwords
        if is_common:
            score -= 40
        
        # Deductions for sequential/repetitive patterns
        if self._has_sequential_pattern(password):
            score -= 15
        if self._has_repetitive_pattern(password):
            score -= 10
        
        # Deductions for metadata-based patterns
        if metadata:
            if self._contains_user_info(password, metadata):
                score -= 20
            if self._contains_date_pattern(password, metadata.get('dob')):
                score -= 15
        
        return max(0, min(score, 100))
    
    def _calculate_entropy(self, password: str) -> float:
        """Calculate Shannon entropy of password"""
        if not password:
            return 0
        
        charset_size = 0
        if re.search(r'[a-z]', password):
            charset_size += 26
        if re.search(r'[A-Z]', password):
            charset_size += 26
        if re.search(r'\d', password):
            charset_size += 10
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};:,.<>?]', password):
            charset_size += 32
        
        entropy = len(password) * math.log2(charset_size) if charset_size > 0 else 0
        return entropy
    
    def _estimate_crack_time(self, password: str, entropy: float) -> float:
        """Estimate crack time in seconds"""
        # Assumptions:
        # - 1 billion guesses per second (modern GPU)
        # - Average is 50% of attempts needed
        
        if entropy == 0:
            return 0
        
        total_combinations = 2 ** entropy
        guesses_per_second = 1_000_000_000
        average_attempts = total_combinations / 2
        
        crack_time = average_attempts / guesses_per_second
        return max(crack_time, 0.1)
    
    def _detect_password_patterns(self, password: str, metadata: Dict) -> List[str]:
        """Detect common password patterns"""
        patterns = []
        
        # Sequential patterns
        if self._has_sequential_pattern(password):
            patterns.append("sequential_characters")
        
        # Keyboard patterns
        if self._has_keyboard_pattern(password):
            patterns.append("keyboard_walk")
        
        # Repetitive
        if self._has_repetitive_pattern(password):
            patterns.append("repetitive_characters")
        
        # Dictionary word
        if any(word.lower() in password.lower() for word in ['password', 'admin', 'user', 'login', 'welcome']):
            patterns.append("dictionary_word")
        
        # Common substitutions
        if re.search(r'[0o][0o]|l1|i!|\$s|@a', password, re.IGNORECASE):
            patterns.append("common_substitution")
        
        # Date patterns
        if re.search(r'(19|20)\d{2}|0?[1-9]|1[0-2]|0?[1-9]|[12]\d|3[01]', password):
            patterns.append("date_pattern")
        
        # User info patterns
        if metadata:
            if metadata.get('username') and metadata.get('username').lower() in password.lower():
                patterns.append("contains_username")
            if metadata.get('name') and metadata.get('name').lower() in password.lower():
                patterns.append("contains_name")
        
        return patterns
    
    def _assess_behavioral_risk(self, password: str, metadata: Dict) -> float:
        """Assess behavioral/contextual risks"""
        risk = 0
        
        # Risk for common passwords
        if password.lower() in self.common_passwords:
            risk += 40
        
        # Risk for password reuse indicators
        if any(word in password.lower() for word in ['password', 'pass', '123', 'qwerty']):
            risk += 20
        
        # Risk for personal info usage
        if metadata:
            if self._contains_user_info(password, metadata):
                risk += 25
            if self._contains_date_pattern(password, metadata.get('dob')):
                risk += 15
        
        return min(risk, 100)
    
    def _identify_vulnerabilities(self, password: str, patterns: List[str]) -> List[str]:
        """Identify specific vulnerabilities"""
        vulnerabilities = []
        
        if len(password) < 8:
            vulnerabilities.append("Password is too short (< 8 characters)")
        
        if not re.search(r'[A-Z]', password):
            vulnerabilities.append("Missing uppercase letters")
        
        if not re.search(r'\d', password):
            vulnerabilities.append("Missing numeric characters")
        
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:,.<>?]', password):
            vulnerabilities.append("Missing special characters")
        
        if 'sequential_characters' in patterns:
            vulnerabilities.append("Contains sequential characters (abc, 123)")
        
        if 'repetitive_characters' in patterns:
            vulnerabilities.append("Contains repetitive characters (aaa, 111)")
        
        if 'keyboard_walk' in patterns:
            vulnerabilities.append("Contains keyboard patterns (qwerty, asdf)")
        
        if 'dictionary_word' in patterns:
            vulnerabilities.append("Contains common dictionary words")
        
        return vulnerabilities
    
    def _generate_password_recommendations(self, strength: float, patterns: List[str], 
                                         vulnerabilities: List[str]) -> List[str]:
        """Generate actionable security recommendations"""
        recommendations = []
        
        if strength < 40:
            recommendations.append("Create a strong password: at least 12 characters with mixed case, numbers, and symbols")
        elif strength < 70:
            recommendations.append("Strengthen password: add more character variety")
        
        if 'sequential_characters' in patterns or 'keyboard_walk' in patterns:
            recommendations.append("Avoid patterns like 'abc123' or 'qwerty'")
        
        if 'dictionary_word' in patterns:
            recommendations.append("Use uncommon words or create a passphrase")
        
        if not all(re.search(r, "") for r in ['[A-Z]', '[a-z]', '[0-9]', '[!@#$%^&*]']):
            recommendations.append("Use a mix of: Uppercase, lowercase, numbers, and symbols")
        
        recommendations.append("Never reuse passwords across different accounts")
        recommendations.append("Use a password manager to generate and store complex passwords")
        recommendations.append("Enable multi-factor authentication (MFA) wherever possible")
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def _calculate_attack_success(self, strength_score: float) -> float:
        """Calculate probability of successful password attack"""
        # Inverse relationship: lower strength = higher success probability
        return max(0, 100 - strength_score)
    
    # ==================== HELPER METHODS ====================
    
    def _has_sequential_pattern(self, password: str) -> bool:
        """Check for sequential character patterns"""
        for i in range(len(password) - 2):
            if ord(password[i+1]) == ord(password[i]) + 1 and ord(password[i+2]) == ord(password[i+1]) + 1:
                return True
        return False
    
    def _has_keyboard_pattern(self, password: str) -> bool:
        """Check for QWERTY keyboard patterns"""
        qwerty_patterns = ['qwerty', 'asdfgh', 'zxcvbn', '12345', 'qazwsx', 'qweasd']
        return any(pattern in password.lower() for pattern in qwerty_patterns)
    
    def _has_repetitive_pattern(self, password: str) -> bool:
        """Check for repetitive character patterns"""
        return bool(re.search(r'(.)\1{2,}', password))
    
    def _contains_user_info(self, password: str, metadata: Dict) -> bool:
        """Check if password contains personal information"""
        user_info = [
            metadata.get('username', '').lower(),
            metadata.get('name', '').lower(),
            metadata.get('email', '').lower(),
        ]
        return any(info and info in password.lower() for info in user_info)
    
    def _contains_date_pattern(self, password: str, dob: str = None) -> bool:
        """Check if password contains date-based patterns"""
        if dob:
            dob_parts = [dob.replace('-', ''), dob.replace('/', '')]
            if any(part in password for part in dob_parts):
                return True
        
        # Check for year patterns
        current_year = datetime.now().year
        for year in range(1950, current_year + 1):
            if str(year) in password:
                return True
        
        return False
    
    def _format_crack_time(self, seconds: float) -> str:
        """Format crack time in human-readable format"""
        if seconds < 1:
            return "< 1 second"
        elif seconds < 60:
            return f"{seconds:.0f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.0f} minutes"
        elif seconds < 86400:
            return f"{seconds/3600:.0f} hours"
        elif seconds < 2592000:
            return f"{seconds/86400:.0f} days"
        elif seconds < 31536000:
            return f"{seconds/2592000:.0f} months"
        else:
            return f"{seconds/31536000:.0f} years"
    
    # ==================== PHISHING ANALYSIS ====================
    
    def analyze_phishing(self, email_text: str, sender_email: str = None) -> Dict:
        """Comprehensive phishing email analysis"""
        risk_score = self._calculate_phishing_risk(email_text, sender_email)
        urgency_score = self._calculate_urgency_score(email_text)
        emotional_score = self._calculate_emotional_manipulation(email_text)
        tactics = self._detect_se_tactics(email_text)
        indicators = self._detect_suspicious_indicators(email_text)
        domain_spoofed = self._detect_domain_spoofing(sender_email)
        success_rate = self._estimate_victim_success_rate(risk_score, tactics)
        recommendations = self._generate_phishing_recommendations(tactics, indicators)
        
        return {
            "risk_score": round(risk_score, 2),
            "urgency_score": round(urgency_score, 2),
            "emotional_manipulation_score": round(emotional_score, 2),
            "social_engineering_tactics": tactics,
            "suspicious_indicators": indicators,
            "spoofed_domain_detected": domain_spoofed,
            "victim_success_rate": round(success_rate, 2),
            "recommendations": recommendations,
            "overall_assessment": self._get_phishing_assessment(risk_score)
        }
    
    def _calculate_phishing_risk(self, email_text: str, sender_email: str = None) -> float:
        """Calculate phishing risk score (0-100)"""
        score = 0
        text_lower = email_text.lower()
        
        # Urgency language
        urgency_keywords = ['urgent', 'immediately', 'asap', 'act now', 'verify now', 'confirm identity']
        urgency_count = sum(1 for word in urgency_keywords if word in text_lower)
        score += min(urgency_count * 10, 30)
        
        # Fear/threat language
        threat_words = ['suspended', 'locked', 'compromised', 'unauthorized', 'fraud', 'attack']
        threat_count = sum(1 for word in threat_words if word in text_lower)
        score += min(threat_count * 8, 20)
        
        # Links
        link_count = len(re.findall(r'https?://[^\s]+', email_text))
        score += min(link_count * 5, 15)
        
        # Requests for sensitive data
        sensitive_keywords = ['password', 'credit card', 'social security', 'bank account', 'pin', 'cvv']
        sensitive_count = sum(1 for word in sensitive_keywords if word in text_lower)
        score += min(sensitive_count * 10, 20)
        
        # Poor grammar/spelling
        if self._detect_poor_grammar(email_text):
            score += 10
        
        # Domain spoofing
        if sender_email and self._detect_domain_spoofing(sender_email):
            score += 15
        
        return min(score, 100)
    
    def _calculate_urgency_score(self, email_text: str) -> float:
        """Calculate urgency tactics score"""
        score = 0
        text_lower = email_text.lower()
        
        urgency_phrases = [
            'verify immediately', 'confirm now', 'act now', 'urgent action required',
            'verify your account', 'confirm your identity', 'immediate action'
        ]
        
        for phrase in urgency_phrases:
            score += email_text.lower().count(phrase) * 10
        
        # ALL CAPS
        all_caps_words = len(re.findall(r'\b[A-Z]{3,}\b', email_text))
        score += min(all_caps_words * 3, 20)
        
        # Exclamation marks
        exclamation_count = email_text.count('!')
        score += min(exclamation_count * 2, 15)
        
        return min(score, 100)
    
    def _calculate_emotional_manipulation(self, email_text: str) -> float:
        """Calculate emotional manipulation tactics score"""
        score = 0
        text_lower = email_text.lower()
        
        # Fear tactics
        fear_words = ['danger', 'risk', 'threat', 'loss', 'leak', 'steal', 'fraud', 'attacked']
        score += sum(1 for word in fear_words if word in text_lower) * 8
        
        # Greed/reward tactics
        reward_words = ['bonus', 'gift', 'prize', 'claim', 'reward', 'free']
        score += sum(1 for word in reward_words if word in text_lower) * 6
        
        # Authority/legitimacy tactics
        authority_words = ['bank', 'paypal', 'apple', 'microsoft', 'official', 'administrator']
        score += sum(1 for word in authority_words if word in text_lower) * 7
        
        return min(score, 100)
    
    def _detect_domain_spoofing(self, sender_email: str) -> bool:
        """Detect potentially spoofed domains"""
        if not sender_email:
            return False
        
        suspicious_patterns = [
            r'@.*paypal.*\.com',
            r'@.*apple.*\.com',
            r'@.*amazon.*\.com',
            r'@.*bank.*\.com',
            r'support@.*\.tk',
            r'noreply@.*\.info'
        ]
        
        return any(re.search(pattern, sender_email, re.IGNORECASE) for pattern in suspicious_patterns)
    
    def _estimate_victim_success_rate(self, risk_score: float, tactics: List[str]) -> float:
        """Estimate probability of successful phishing attack"""
        base_rate = risk_score
        
        # Increase if multiple tactics used
        tactic_multiplier = 1 + (len(tactics) * 0.05)
        
        return min(base_rate * tactic_multiplier, 100)
    
    def _generate_phishing_recommendations(self, tactics: List[str], indicators: List[str]) -> List[str]:
        """Generate phishing awareness recommendations"""
        recommendations = []
        
        if 'urgency_tactics' in tactics:
            recommendations.append("Be wary of messages demanding immediate action")
        
        if 'authority_impersonation' in tactics:
            recommendations.append("Verify requests from official sources through known channels")
        
        if 'data_harvesting' in tactics:
            recommendations.append("Never provide sensitive information via email or links")
        
        recommendations.append("Hover over links before clicking to verify the URL")
        recommendations.append("Check sender email address carefully for spoofing attempts")
        recommendations.append("Enable multi-factor authentication on email accounts")
        recommendations.append("Report suspicious emails to your IT security team")
        
        return recommendations[:5]
    
    def _detect_suspicious_indicators(self, email_text: str) -> List[str]:
        """Detect specific suspicious indicators"""
        indicators = []
        
        if re.search(r'verify.*account|confirm.*identity', email_text, re.IGNORECASE):
            indicators.append("Requests account verification or identity confirmation")
        
        if re.search(r'password|credit card|bank account|social security', email_text, re.IGNORECASE):
            indicators.append("Requests sensitive financial or personal information")
        
        if re.search(r'click.*here|verify.*now|act.*now', email_text, re.IGNORECASE):
            indicators.append("Pressing tone with immediate action requested")
        
        if self._detect_poor_grammar(email_text):
            indicators.append("Contains spelling or grammatical errors")
        
        return indicators
    
    def _detect_poor_grammar(self, text: str) -> bool:
        """Simple grammar check"""
        grammar_issues = re.findall(r'\b(?:teh|recieve|occured|seperate|definately)\b', text, re.IGNORECASE)
        return len(grammar_issues) > 0
    
    def _get_phishing_assessment(self, risk_score: float) -> str:
        """Get overall phishing assessment"""
        if risk_score >= 80:
            return "CRITICAL - Highly likely to be phishing"
        elif risk_score >= 60:
            return "HIGH - Probable phishing attempt"
        elif risk_score >= 40:
            return "MEDIUM - Suspicious indicators present"
        elif risk_score >= 20:
            return "LOW - Minor concerns detected"
        else:
            return "MINIMAL - Appears legitimate"
    
    # ==================== VISHING ANALYSIS ====================
    
    def analyze_vishing(self, call_script: str, caller_id: str = None, 
                       call_duration: float = 0) -> Dict:
        """Comprehensive vishing (voice phishing) analysis"""
        vishing_score = self._calculate_vishing_risk(call_script, caller_id, call_duration)
        urgency_score = self._calculate_vishing_urgency(call_script)
        emotional_score = self._calculate_vishing_emotional(call_script)
        tactics = self._detect_vishing_tactics(call_script)
        indicators = self._detect_vishing_indicators(call_script)
        suspicious_caller = self._analyze_caller_id(caller_id)
        success_rate = self._estimate_vishing_success_rate(vishing_score, tactics)
        risk_factors = self._identify_vishing_risk_factors(call_script, caller_id, tactics)
        recommendations = self._generate_vishing_recommendations(tactics, indicators)
        
        return {
            "vishing_score": round(vishing_score, 2),
            "urgency_score": round(urgency_score, 2),
            "emotional_manipulation_score": round(emotional_score, 2),
            "social_engineering_tactics": tactics,
            "suspicious_indicators": indicators,
            "caller_analysis": {
                "caller_id": caller_id or "Not provided",
                "call_duration": call_duration,
                "suspicious_caller": suspicious_caller
            },
            "success_rate_simulation": round(success_rate, 2),
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "overall_assessment": self._get_vishing_assessment(vishing_score)
        }
    
    def _calculate_vishing_risk(self, call_script: str, caller_id: str, call_duration: float) -> float:
        """Calculate vishing risk score"""
        score = 0
        script_lower = call_script.lower()
        
        # Authority impersonation
        authority_keywords = ['irs', 'fbi', 'bank', 'microsoft', 'apple', 'officer', 'agent', 'representative']
        authority_count = sum(1 for word in authority_keywords if word in script_lower)
        score += min(authority_count * 12, 30)
        
        # Urgency
        urgency_count = sum(1 for word in ['urgent', 'immediately', 'asap', 'now', 'immediately'] if word in script_lower)
        score += min(urgency_count * 10, 25)
        
        # Threat/Fear
        threat_count = sum(1 for word in ['suspended', 'locked', 'fraud', 'legal action'] if word in script_lower)
        score += min(threat_count * 12, 25)
        
        # Data requests
        data_keywords = ['verify', 'confirm', 'provide', 'account number', 'social security', 'password']
        data_count = sum(1 for word in data_keywords if word in script_lower)
        score += min(data_count * 8, 20)
        
        # Caller ID spoofing indicators
        if self._is_suspicious_caller_id(caller_id):
            score += 15
        
        return min(score, 100)
    
    def _calculate_vishing_urgency(self, call_script: str) -> float:
        """Calculate urgency tactics in vishing script"""
        score = 0
        script_lower = call_script.lower()
        
        urgency_phrases = [
            'act immediately', 'must verify', 'verify now', 'confirm immediately',
            'take action', 'right now', 'without delay'
        ]
        
        for phrase in urgency_phrases:
            score += script_lower.count(phrase) * 15
        
        return min(score, 100)
    
    def _calculate_vishing_emotional(self, call_script: str) -> float:
        """Calculate emotional manipulation in vishing"""
        score = 0
        script_lower = call_script.lower()
        
        # Fear-based
        fear_count = sum(1 for word in ['danger', 'risk', 'problem', 'issue', 'fraud', 'attack'] 
                        if word in script_lower)
        score += fear_count * 10
        
        # Authority/legitimacy
        authority_count = sum(1 for word in ['official', 'authorized', 'legal', 'government'] 
                             if word in script_lower)
        score += authority_count * 8
        
        return min(score, 100)
    
    def _detect_vishing_tactics(self, call_script: str) -> List[str]:
        """Detect specific vishing tactics"""
        tactics = []
        script_lower = call_script.lower()
        
        if any(word in script_lower for word in ['verify', 'confirm', 'authenticate']):
            tactics.append("verification_request")
        
        if any(word in script_lower for word in ['account number', 'password', 'pin', 'social security']):
            tactics.append("sensitive_data_harvesting")
        
        if any(word in script_lower for word in ['irs', 'fbi', 'bank', 'microsoft', 'apple']):
            tactics.append("authority_impersonation")
        
        if any(word in script_lower for word in ['suspended', 'locked', 'fraud', 'legal action']):
            tactics.append("fear_tactics")
        
        if any(word in script_lower for word in ['urgent', 'immediately', 'now', 'asap']):
            tactics.append("urgency_creation")
        
        return tactics
    
    def _detect_vishing_indicators(self, call_script: str) -> List[str]:
        """Detect suspicious vishing indicators"""
        indicators = []
        
        if re.search(r'verify.*account|confirm.*identity|authenticate', call_script, re.IGNORECASE):
            indicators.append("Verification of account or identity requested")
        
        if re.search(r'account.*number|password|pin|social.*security|bank.*account', call_script, re.IGNORECASE):
            indicators.append("Request for sensitive financial information")
        
        if re.search(r'act.*now|immediate|urgency|right.*now', call_script, re.IGNORECASE):
            indicators.append("High-pressure tactics used")
        
        if re.search(r'legal.*action|law.*enforcement|fraud.*charge|suspension', call_script, re.IGNORECASE):
            indicators.append("Threat of legal consequences")
        
        return indicators
    
    def _analyze_caller_id(self, caller_id: str) -> bool:
        """Analyze caller ID for spoofing patterns"""
        if not caller_id:
            return False
        
        # Check for masking indicators
        suspicious_patterns = [
            r'^\+?1?800',  # Generic 1-800
            r'unknown|blocked|private|anonymous',
            r'\*\*\*',  # Masking
            r'^1-800',  # Obvious toll-free
        ]
        
        return any(re.search(pattern, caller_id, re.IGNORECASE) for pattern in suspicious_patterns)
    
    def _is_suspicious_caller_id(self, caller_id: str) -> bool:
        """Check if caller ID is suspicious"""
        return self._analyze_caller_id(caller_id)
    
    def _estimate_vishing_success_rate(self, vishing_score: float, tactics: List[str]) -> float:
        """Estimate vishing attack success rate"""
        base_rate = vishing_score * 0.8
        
        # Increase if multiple tactics
        if len(tactics) >= 3:
            base_rate *= 1.15
        
        return min(base_rate, 100)
    
    def _identify_vishing_risk_factors(self, call_script: str, caller_id: str, 
                                      tactics: List[str]) -> List[str]:
        """Identify specific risk factors"""
        factors = []
        
        if len(tactics) >= 3:
            factors.append("Multiple social engineering tactics detected")
        
        if 'authority_impersonation' in tactics:
            factors.append("Impersonation of trusted authority figure")
        
        if 'fear_tactics' in tactics:
            factors.append("Fear-based manipulation tactics")
        
        if 'sensitive_data_harvesting' in tactics:
            factors.append("Attempts to harvest sensitive information")
        
        if self._is_suspicious_caller_id(caller_id):
            factors.append("Suspicious or spoofed caller ID")
        
        return factors
    
    def _generate_vishing_recommendations(self, tactics: List[str], indicators: List[str]) -> List[str]:
        """Generate vishing awareness recommendations"""
        recommendations = []
        
        recommendations.append("Verify caller identity through official channels before providing information")
        recommendations.append("Financial institutions never request passwords or PINs via phone")
        recommendations.append("Hang up and call back official phone numbers from verified sources")
        recommendations.append("Never provide passwords, PINs, or sensitive data over the phone")
        recommendations.append("Enable call filtering and authentication services on your phone")
        recommendations.append("Train employees on vishing tactics and reporting procedures")
        
        return recommendations[:5]
    
    def _get_vishing_assessment(self, risk_score: float) -> str:
        """Get overall vishing assessment"""
        if risk_score >= 80:
            return "CRITICAL - High probability of vishing attack"
        elif risk_score >= 60:
            return "HIGH - Likely voice phishing attempt"
        elif risk_score >= 40:
            return "MEDIUM - Possible social engineering"
        elif risk_score >= 20:
            return "LOW - Minor concerns"
        else:
            return "MINIMAL - Appears legitimate"
    
    # ==================== DETECTION HELPERS ====================
    
    def _detect_se_tactics(self, email_text: str) -> List[str]:
        """Detect social engineering tactics"""
        tactics = []
        text_lower = email_text.lower()
        
        if any(word in text_lower for word in ['verify', 'confirm', 'authenticate']):
            tactics.append("verification_request")
        
        if any(word in text_lower for word in ['password', 'credit card', 'ssn']):
            tactics.append("data_harvesting")
        
        if any(word in text_lower for word in ['bank', 'paypal', 'apple', 'microsoft']):
            tactics.append("authority_impersonation")
        
        if any(word in text_lower for word in ['urgent', 'immediately', 'asap']):
            tactics.append("urgency_tactics")
        
        return tactics
    
    # ==================== DATA LOADERS ====================
    
    def _load_common_passwords(self) -> set:
        """Load common passwords database"""
        return {
            'password', '123456', '123456789', 'qwerty', 'password123',
            '12345678', '111111', '1234567', '123123', '1234567890',
            '000000', '555555', '666666', '123321', '654321',
            'superman', 'letmein', 'welcome', 'monkey', 'dragon',
            'admin', 'master', 'pussy', 'login', 'passw0rd'
        }
    
    def _load_phishing_keywords(self) -> list:
        """Load phishing detection keywords"""
        return ['verify', 'confirm', 'urgent', 'immediate', 'click here', 'act now']
    
    def _load_vishing_keywords(self) -> list:
        """Load vishing detection keywords"""
        return ['verify', 'confirm', 'account', 'password', 'security', 'urgent']
    
    def _load_se_patterns(self) -> dict:
        """Load social engineering patterns"""
        return {
            'urgency': r'urgent|immediately|asap|act now',
            'fear': r'fraud|compromised|suspended|locked',
            'authority': r'bank|irs|fbi|microsoft|apple',
            'data_request': r'password|credit card|social security|pin'
        }


# Singleton instance
_scoring_engine = None

def get_scoring_engine() -> AIScoringEngine:
    """Get or create scoring engine instance"""
    global _scoring_engine
    if _scoring_engine is None:
        _scoring_engine = AIScoringEngine()
    return _scoring_engine

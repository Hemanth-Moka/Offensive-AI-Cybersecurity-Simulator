import re
import numpy as np
from typing import List, Dict, Tuple
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

class PasswordPatternLearner:
    """AI model to learn common password patterns and user behavior"""
    
    def __init__(self):
        self.common_patterns = {
            'sequential': r'(123|abc|qwerty|password)',
            'repetitive': r'(.)\1{2,}',
            'keyboard_walk': r'(qwerty|asdf|zxcv)',
            'dates': r'(19|20)\d{2}',
            'names': r'[A-Z][a-z]{3,}',
            'common_words': r'(password|admin|welcome|login)'
        }
        # Learned patterns from historical data
        self.learned_patterns = []
        self.user_behavior_trends = {}
        
    def analyze_password(self, password: str) -> Dict:
        """Analyze password for common patterns"""
        patterns_found = []
        strength_score = 100
        
        for pattern_name, pattern in self.common_patterns.items():
            if re.search(pattern, password, re.IGNORECASE):
                patterns_found.append(pattern_name)
                strength_score -= 15
        
        # Length check
        if len(password) < 8:
            strength_score -= 20
        elif len(password) < 12:
            strength_score -= 10
        
        # Complexity check
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        
        complexity = sum([has_upper, has_lower, has_digit, has_special])
        strength_score += (complexity - 2) * 10
        
        strength_score = max(0, min(100, strength_score))
        
        return {
            'patterns_found': patterns_found,
            'strength_score': strength_score,
            'length': len(password),
            'complexity': complexity,
            'has_upper': has_upper,
            'has_lower': has_lower,
            'has_digit': has_digit,
            'has_special': has_special
        }
    
    def learn_from_password(self, password: str, user_id: str = None):
        """Learn patterns from analyzed passwords to improve future guesses"""
        analysis = self.analyze_password(password)
        patterns = analysis.get('patterns_found', [])
        
        if user_id:
            if user_id not in self.user_behavior_trends:
                self.user_behavior_trends[user_id] = {
                    'common_patterns': [],
                    'password_lengths': [],
                    'complexity_scores': []
                }
            
            self.user_behavior_trends[user_id]['common_patterns'].extend(patterns)
            self.user_behavior_trends[user_id]['password_lengths'].append(len(password))
            self.user_behavior_trends[user_id]['complexity_scores'].append(analysis.get('complexity', 0))
        
        self.learned_patterns.extend(patterns)
    
    def generate_guesses(self, user_metadata: Dict = None, user_id: str = None) -> List[str]:
        """Generate AI-guided password guesses based on learned patterns and user behavior"""
        guesses = []
        
        # Common passwords
        common_passwords = [
            'password', '123456', '12345678', 'qwerty', 'abc123',
            'password123', 'admin', 'welcome', 'letmein', 'monkey'
        ]
        guesses.extend(common_passwords)
        
        # Use learned patterns if available
        if self.learned_patterns:
            pattern_counts = Counter(self.learned_patterns)
            most_common = [p for p, _ in pattern_counts.most_common(5)]
            # Generate guesses based on learned patterns
            for pattern in most_common:
                if pattern == 'dates':
                    guesses.extend(['2024', '2023', '2022', '2021', '2020'])
                elif pattern == 'names':
                    guesses.extend(['John', 'Mary', 'David', 'Sarah', 'Michael'])
        
        # Use user-specific behavior if available
        if user_id and user_id in self.user_behavior_trends:
            trends = self.user_behavior_trends[user_id]
            avg_length = sum(trends['password_lengths']) / len(trends['password_lengths']) if trends['password_lengths'] else 8
            common_user_patterns = Counter(trends['common_patterns']).most_common(3)
            
            # Generate guesses based on user's historical patterns
            for pattern, _ in common_user_patterns:
                if pattern == 'sequential':
                    guesses.extend(['123', '1234', '12345', 'abc', 'qwerty'])
                elif pattern == 'dates':
                    guesses.extend(['1990', '2000', '1985', '1995'])
        
        # If user metadata provided, generate personalized guesses
        if user_metadata:
            name = user_metadata.get('name', '')
            dob = user_metadata.get('dob', '')
            
            if name:
                name_lower = name.lower()
                guesses.extend([
                    name_lower,
                    name_lower + '123',
                    name_lower + '1234',
                    name_lower.capitalize() + '1',
                    name_lower + '!',
                    name_lower + '@123',
                ])
            
            if dob:
                year = dob.split('-')[0] if '-' in dob else dob[:4]
                month = dob.split('-')[1] if '-' in dob and len(dob.split('-')) > 1 else None
                day = dob.split('-')[2] if '-' in dob and len(dob.split('-')) > 2 else None
                
                guesses.extend([
                    year,
                    'password' + year,
                    name_lower + year if name else None
                ])
                
                if month:
                    guesses.append(month + year)
                if day:
                    guesses.append(day + month + year if month else None)
                
                guesses = [g for g in guesses if g]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_guesses = []
        for guess in guesses:
            if guess and guess not in seen:
                seen.add(guess)
                unique_guesses.append(guess)
        
        return unique_guesses[:50]  # Limit to 50 guesses

class PhishingDetector:
    """AI model to detect phishing attempts"""
    
    def __init__(self):
        self.suspicious_keywords = [
            'urgent', 'immediately', 'verify', 'suspended', 'locked',
            'click here', 'verify now', 'limited time', 'act now',
            'your account', 'confirm identity', 'security alert',
            'unauthorized access', 'update payment', 'expired'
        ]
        
        self.urgency_indicators = [
            'urgent', 'immediately', 'asap', 'now', 'today',
            'expires', 'limited', 'last chance', 'final notice'
        ]
        
        self.emotional_manipulators = [
            'fear', 'worry', 'concern', 'important', 'critical',
            'suspended', 'locked', 'terminated', 'violation'
        ]
    
    def detect_phishing(self, email_subject: str, email_body: str, sender: str = "") -> Dict:
        """Analyze email for phishing indicators"""
        text = f"{email_subject} {email_body}".lower()
        
        # Find suspicious keywords
        found_keywords = [kw for kw in self.suspicious_keywords if kw in text]
        
        # Calculate urgency score
        urgency_count = sum(1 for indicator in self.urgency_indicators if indicator in text)
        urgency_score = min(100, urgency_count * 20)
        
        # Calculate emotional manipulation score
        emotional_count = sum(1 for manipulator in self.emotional_manipulators if manipulator in text)
        emotional_score = min(100, emotional_count * 15)
        
        # Sender analysis
        sender_score = 0
        if sender:
            suspicious_domains = ['gmail', 'yahoo', 'hotmail', 'outlook']
            if any(domain in sender.lower() for domain in suspicious_domains):
                # Check for domain spoofing patterns
                if '@' in sender and '.' in sender:
                    domain = sender.split('@')[1]
                    if domain not in ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']:
                        sender_score = 30
        
        # Calculate overall phishing score
        phishing_score = (
            len(found_keywords) * 10 +
            urgency_score * 0.3 +
            emotional_score * 0.3 +
            sender_score
        )
        phishing_score = min(100, phishing_score)
        
        # Simulate click rate (higher score = higher click rate)
        click_rate = min(95, max(5, phishing_score * 0.8 + np.random.normal(0, 5)))
        
        # Generate recommendations
        recommendations = []
        if phishing_score > 70:
            recommendations.append("High risk: This appears to be a phishing attempt")
        if urgency_score > 50:
            recommendations.append("Warning: High urgency indicators detected")
        if emotional_score > 50:
            recommendations.append("Warning: Emotional manipulation tactics identified")
        if found_keywords:
            recommendations.append(f"Found {len(found_keywords)} suspicious keywords")
        
        if phishing_score < 30:
            recommendations.append("Low risk: Email appears legitimate")
        
        return {
            'phishing_score': round(phishing_score, 2),
            'urgency_score': round(urgency_score, 2),
            'emotional_manipulation_score': round(emotional_score, 2),
            'suspicious_keywords': found_keywords,
            'click_rate_simulation': round(click_rate, 2),
            'recommendations': recommendations,
            'sender_analysis': {
                'sender': sender,
                'suspicious_domain': sender_score > 0
            }
        }

class VishingDetector:
    """AI model to detect voice phishing (vishing) attempts"""
    
    def __init__(self):
        self.vishing_keywords = [
            'verify your account', 'suspended immediately', 'unauthorized transaction',
            'confirm your identity', 'update your information', 'security breach',
            'account locked', 'fraudulent activity', 'verify payment', 'confirm details'
        ]
        
        self.urgency_indicators = [
            'right now', 'immediately', 'urgent', 'as soon as possible', 'within minutes',
            'before it\'s too late', 'expires today', 'final warning', 'last chance'
        ]
        
        self.emotional_manipulators = [
            'fraud', 'stolen', 'compromised', 'hacked', 'unauthorized',
            'suspended', 'locked', 'terminated', 'violation', 'penalty',
            'legal action', 'arrest', 'warrant', 'lawsuit'
        ]
        
        self.social_engineering_tactics = [
            'authority_impersonation',  # Pretending to be bank, IRS, etc.
            'urgency_creation',  # Creating false urgency
            'fear_appeal',  # Using fear tactics
            'trust_building',  # Building false trust
            'information_gathering',  # Asking for personal info
            'pretexting'  # Creating false scenario
        ]
        
        self.suspicious_call_patterns = [
            'asking for passwords', 'requesting pin', 'asking for ssn',
            'requesting credit card', 'asking for otp', 'requesting verification code',
            'calling from unknown number', 'spoofed caller id', 'robocall'
        ]
    
    def detect_vishing(self, call_script: str, caller_id: str = "", call_duration: float = 0) -> Dict:
        """Analyze voice call script for vishing indicators"""
        text = call_script.lower()
        
        # Find vishing keywords
        found_keywords = [kw for kw in self.vishing_keywords if kw in text]
        
        # Calculate urgency score
        urgency_count = sum(1 for indicator in self.urgency_indicators if indicator in text)
        urgency_score = min(100, urgency_count * 25)
        
        # Calculate emotional manipulation score
        emotional_count = sum(1 for manipulator in self.emotional_manipulators if manipulator in text)
        emotional_score = min(100, emotional_count * 20)
        
        # Detect social engineering tactics
        tactics_found = []
        if any(keyword in text for keyword in ['bank', 'irs', 'government', 'police', 'fbi', 'official']):
            tactics_found.append('authority_impersonation')
        if urgency_score > 50:
            tactics_found.append('urgency_creation')
        if emotional_score > 50:
            tactics_found.append('fear_appeal')
        if any(keyword in text for keyword in ['trust', 'verify', 'confirm', 'legitimate']):
            tactics_found.append('trust_building')
        if any(keyword in text for keyword in ['ssn', 'social security', 'credit card', 'account number', 'pin']):
            tactics_found.append('information_gathering')
        if any(keyword in text for keyword in ['situation', 'problem', 'issue', 'concern', 'matter']):
            tactics_found.append('pretexting')
        
        # Caller ID analysis
        caller_score = 0
        suspicious_indicators = []
        if caller_id:
            # Check for suspicious patterns
            if caller_id.startswith('+1') and len(caller_id) > 12:
                suspicious_indicators.append('International number spoofing')
                caller_score += 20
            if 'unknown' in caller_id.lower() or 'blocked' in caller_id.lower():
                suspicious_indicators.append('Unknown/Blocked caller ID')
                caller_score += 15
            if any(pattern in caller_id for pattern in ['000', '111', '222']):
                suspicious_indicators.append('Suspicious number pattern')
                caller_score += 10
        
        # Call duration analysis (very short or very long calls can be suspicious)
        duration_score = 0
        if call_duration > 0:
            if call_duration < 30:  # Very short call
                suspicious_indicators.append('Unusually short call duration')
                duration_score += 10
            elif call_duration > 600:  # Very long call (>10 minutes)
                suspicious_indicators.append('Unusually long call duration')
                duration_score += 5
        
        # Detect suspicious call patterns
        pattern_matches = [pattern for pattern in self.suspicious_call_patterns if pattern in text]
        if pattern_matches:
            suspicious_indicators.extend(pattern_matches)
        
        # Calculate overall vishing score
        vishing_score = (
            len(found_keywords) * 12 +
            urgency_score * 0.25 +
            emotional_score * 0.25 +
            len(tactics_found) * 8 +
            caller_score +
            duration_score
        )
        vishing_score = min(100, vishing_score)
        
        # Simulate success rate (higher score = higher success rate)
        success_rate = min(90, max(5, vishing_score * 0.75 + np.random.normal(0, 5)))
        
        # Generate recommendations
        recommendations = []
        if vishing_score > 70:
            recommendations.append("CRITICAL: This appears to be a vishing attempt")
            recommendations.append("Never provide personal information over the phone")
            recommendations.append("Hang up and call the organization directly using official number")
        elif vishing_score > 50:
            recommendations.append("HIGH RISK: Multiple suspicious indicators detected")
            recommendations.append("Verify caller identity through independent channels")
            recommendations.append("Do not provide sensitive information")
        elif vishing_score > 30:
            recommendations.append("MODERATE RISK: Some suspicious indicators present")
            recommendations.append("Be cautious and verify before sharing information")
        else:
            recommendations.append("LOW RISK: Call appears relatively safe")
            recommendations.append("Remain vigilant and verify caller identity if unsure")
        
        if urgency_score > 50:
            recommendations.append("Warning: High urgency indicators - legitimate organizations rarely pressure you")
        if emotional_score > 50:
            recommendations.append("Warning: Fear-based tactics detected - be skeptical")
        if tactics_found:
            recommendations.append(f"Detected {len(tactics_found)} social engineering tactic(s)")
        
        return {
            'vishing_score': round(vishing_score, 2),
            'urgency_score': round(urgency_score, 2),
            'emotional_manipulation_score': round(emotional_score, 2),
            'social_engineering_tactics': tactics_found,
            'suspicious_indicators': suspicious_indicators,
            'success_rate_simulation': round(success_rate, 2),
            'recommendations': recommendations,
            'caller_analysis': {
                'caller_id': caller_id,
                'call_duration': call_duration,
                'suspicious_caller': caller_score > 0
            }
        }

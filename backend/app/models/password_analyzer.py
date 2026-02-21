from typing import List, Dict, Optional
import time
import random
from app.utils.hash_utils import hash_md5, hash_sha256, hash_bcrypt, verify_hash
from app.utils.ml_utils import PasswordPatternLearner

class PasswordAttackSimulator:
    """Simulates password attacks for educational purposes"""
    
    def __init__(self):
        self.pattern_learner = PasswordPatternLearner()
        self.common_passwords = self._load_common_passwords()
    
    def _load_common_passwords(self) -> List[str]:
        """Load common password dictionary"""
        return [
            'password', '123456', '12345678', 'qwerty', 'abc123',
            'password123', 'admin', 'welcome', 'letmein', 'monkey',
            '123456789', '1234567890', '1234', '12345', '1234567',
            'dragon', 'baseball', 'football', 'master', 'hello',
            'shadow', 'superman', 'qwertyuiop', '123qwe', 'trustno1'
        ]
    
    def dictionary_attack(self, hash_value: str, hash_type: str, 
                         custom_dict: Optional[List[str]] = None) -> Dict:
        """Simulate dictionary attack"""
        dictionary = custom_dict or self.common_passwords
        start_time = time.time()
        attempts = 0
        
        for password in dictionary:
            attempts += 1
            if verify_hash(password, hash_value, hash_type):
                time_taken = time.time() - start_time
                pattern_analysis = self.pattern_learner.analyze_password(password)
                risk_score = 100 - pattern_analysis['strength_score']
                
                return {
                    'cracked': password,
                    'attack_type': 'dictionary',
                    'attempts': attempts,
                    'time_taken': round(time_taken, 4),
                    'risk_score': round(risk_score, 2),
                    'pattern_analysis': pattern_analysis
                }
        
        time_taken = time.time() - start_time
        return {
            'cracked': None,
            'attack_type': 'dictionary',
            'attempts': attempts,
            'time_taken': round(time_taken, 4),
            'risk_score': 0,
            'pattern_analysis': {}
        }
    
    def brute_force_attack(self, hash_value: str, hash_type: str, 
                          max_length: int = 4, max_attempts: int = 1000) -> Dict:
        """Simulate brute-force attack (limited scope for lab)"""
        import string
        chars = string.ascii_lowercase + string.digits
        start_time = time.time()
        attempts = 0
        
        def generate_passwords(length):
            if length == 1:
                for c in chars:
                    yield c
            else:
                for c in chars:
                    for p in generate_passwords(length - 1):
                        yield c + p
        
        for length in range(1, max_length + 1):
            for password in generate_passwords(length):
                attempts += 1
                if attempts > max_attempts:
                    break
                
                if verify_hash(password, hash_value, hash_type):
                    time_taken = time.time() - start_time
                    pattern_analysis = self.pattern_learner.analyze_password(password)
                    risk_score = 100 - pattern_analysis['strength_score']
                    
                    return {
                        'cracked': password,
                        'attack_type': 'brute_force',
                        'attempts': attempts,
                        'time_taken': round(time_taken, 4),
                        'risk_score': round(risk_score, 2),
                        'pattern_analysis': pattern_analysis
                    }
            
            if attempts > max_attempts:
                break
        
        time_taken = time.time() - start_time
        return {
            'cracked': None,
            'attack_type': 'brute_force',
            'attempts': attempts,
            'time_taken': round(time_taken, 4),
            'risk_score': 0,
            'pattern_analysis': {}
        }
    
    def hybrid_attack(self, hash_value: str, hash_type: str, 
                     user_metadata: Optional[Dict] = None) -> Dict:
        """Simulate hybrid attack combining dictionary and AI-guided guessing"""
        start_time = time.time()
        attempts = 0
        
        # Combine dictionary and AI-generated guesses
        ai_guesses = self.pattern_learner.generate_guesses(user_metadata)
        all_guesses = self.common_passwords + ai_guesses
        
        # Remove duplicates while preserving order
        seen = set()
        unique_guesses = []
        for guess in all_guesses:
            if guess not in seen:
                seen.add(guess)
                unique_guesses.append(guess)
        
        for password in unique_guesses:
            attempts += 1
            if verify_hash(password, hash_value, hash_type):
                time_taken = time.time() - start_time
                pattern_analysis = self.pattern_learner.analyze_password(password)
                risk_score = 100 - pattern_analysis['strength_score']
                
                return {
                    'cracked': password,
                    'attack_type': 'hybrid',
                    'attempts': attempts,
                    'time_taken': round(time_taken, 4),
                    'risk_score': round(risk_score, 2),
                    'pattern_analysis': pattern_analysis
                }
        
        time_taken = time.time() - start_time
        return {
            'cracked': None,
            'attack_type': 'hybrid',
            'attempts': attempts,
            'time_taken': round(time_taken, 4),
            'risk_score': 0,
            'pattern_analysis': {}
        }
    
    def ai_guided_attack(self, hash_value: str, hash_type: str, 
                        user_metadata: Optional[Dict] = None) -> Dict:
        """AI-guided password guessing based on user behavior patterns"""
        start_time = time.time()
        attempts = 0
        
        # Generate intelligent guesses based on patterns
        guesses = self.pattern_learner.generate_guesses(user_metadata)
        
        # Prioritize guesses based on common patterns
        prioritized_guesses = sorted(guesses, key=lambda x: len(x))
        
        for password in prioritized_guesses:
            attempts += 1
            if verify_hash(password, hash_value, hash_type):
                time_taken = time.time() - start_time
                pattern_analysis = self.pattern_learner.analyze_password(password)
                risk_score = 100 - pattern_analysis['strength_score']
                
                return {
                    'cracked': password,
                    'attack_type': 'ai_guided',
                    'attempts': attempts,
                    'time_taken': round(time_taken, 4),
                    'risk_score': round(risk_score, 2),
                    'pattern_analysis': pattern_analysis
                }
        
        time_taken = time.time() - start_time
        return {
            'cracked': None,
            'attack_type': 'ai_guided',
            'attempts': attempts,
            'time_taken': round(time_taken, 4),
            'risk_score': 0,
            'pattern_analysis': {}
        }

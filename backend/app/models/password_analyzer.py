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
        """Load comprehensive common password dictionary"""
        return [
            # Top 100 most common passwords
            'password', '123456', '12345678', 'qwerty', 'abc123',
            'password123', 'admin', 'welcome', 'letmein', 'monkey',
            '123456789', '1234567890', '1234', '12345', '1234567',
            'dragon', 'baseball', 'football', 'master', 'hello',
            'shadow', 'superman', 'qwertyuiop', '123qwe', 'trustno1',
            'password1', '123456a', 'qwerty123', 'welcome123', 'admin123',
            'letmein1', 'password12', '123456789a', 'qwerty1', 'password!',
            '123456!', 'admin1', 'welcome1', 'letmein!', 'password@',
            '123456@', 'qwerty!', 'admin!', 'welcome!', 'password#',
            # Common patterns
            'password2024', 'password2023', 'password2022', 'password2021',
            'admin2024', 'admin2023', 'welcome2024', 'qwerty2024',
            # Keyboard patterns
            'asdfgh', 'zxcvbn', 'qwertyui', 'asdfghjkl', '1qaz2wsx',
            'qazwsx', 'qwerty1', 'asdf1234', 'zxcv1234',
            # Common words with numbers
            'password0', 'password01', 'password02', 'password03',
            'admin0', 'admin01', 'welcome0', 'qwerty0',
            # Year-based
            'password2020', 'password2019', 'password2018', 'password2017',
            'admin2020', 'admin2019', 'welcome2020',
            # Simple variations
            'Password', 'PASSWORD', 'Password1', 'Password123',
            'Admin', 'ADMIN', 'Admin1', 'Admin123',
            'Welcome', 'WELCOME', 'Welcome1', 'Welcome123',
            # Common phrases
            'iloveyou', 'princess', 'rockyou', '1234567890',
            'qwerty12345', '1q2w3e4r', '1q2w3e4r5t', 'qwertyuiop123',
            # More patterns
            'password!@#', '123456!@#', 'admin!@#', 'qwerty!@#',
            'pass1234', 'pass12345', 'pass123456', 'passw0rd',
            'p@ssw0rd', 'P@ssw0rd', 'P@$$w0rd', 'p@$$w0rd',
            # Additional common passwords
            'sunshine', 'princess', 'dragon', 'password', 'master',
            'hello', 'freedom', 'whatever', 'qazwsx', 'trustno1',
            'jordan23', 'harley', 'batman', 'tigger', 'shadow',
            'superman', 'qwertyuiop', '123qwe', 'zxcvbnm', 'hunter'
        ]
    
    def dictionary_attack(self, hash_value: str, hash_type: str, 
                         custom_dict: Optional[List[str]] = None,
                         max_attempts: Optional[int] = None) -> Dict:
        """Simulate dictionary attack with comprehensive wordlist"""
        dictionary = custom_dict or self.common_passwords
        start_time = time.time()
        attempts = 0
        total_passwords = len(dictionary)
        max_attempts = max_attempts or total_passwords
        
        # Add common mutations
        mutations = []
        for pwd in dictionary[:50]:  # Limit mutations to first 50
            mutations.extend([
                pwd + '1', pwd + '12', pwd + '123', pwd + '!',
                pwd + '@', pwd + '#', pwd.capitalize(), pwd.upper(),
                '1' + pwd, '12' + pwd, '!' + pwd, '@' + pwd
            ])
        
        # Combine original and mutations
        all_passwords = dictionary + mutations
        all_passwords = list(dict.fromkeys(all_passwords))  # Remove duplicates
        
        for password in all_passwords:
            if attempts >= max_attempts:
                break
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
                    'pattern_analysis': pattern_analysis,
                    'total_attempts': len(all_passwords),
                    'attempts_per_second': round(attempts / time_taken, 2) if time_taken > 0 else 0
                }
        
        time_taken = time.time() - start_time
        return {
            'cracked': None,
            'attack_type': 'dictionary',
            'attempts': attempts,
            'time_taken': round(time_taken, 4),
            'risk_score': 0,
            'pattern_analysis': {},
            'total_attempts': len(all_passwords),
            'attempts_per_second': round(attempts / time_taken, 2) if time_taken > 0 else 0
        }
    
    def brute_force_attack(self, hash_value: str, hash_type: str, 
                          max_length: int = 4, max_attempts: int = 10000,
                          charset: str = 'lowercase+digits') -> Dict:
        """Simulate brute-force attack with configurable charset"""
        import string
        
        # Define character sets
        charsets = {
            'lowercase': string.ascii_lowercase,
            'uppercase': string.ascii_uppercase,
            'digits': string.digits,
            'lowercase+digits': string.ascii_lowercase + string.digits,
            'uppercase+digits': string.ascii_uppercase + string.digits,
            'mixed': string.ascii_letters + string.digits,
            'full': string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?'
        }
        
        chars = charsets.get(charset, charsets['lowercase+digits'])
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
        
        # Calculate total possible combinations
        total_combinations = sum(len(chars) ** i for i in range(1, max_length + 1))
        
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
                        'pattern_analysis': pattern_analysis,
                        'total_combinations': total_combinations,
                        'attempts_per_second': round(attempts / time_taken, 2) if time_taken > 0 else 0,
                        'charset_used': charset
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
            'pattern_analysis': {},
            'total_combinations': total_combinations,
            'attempts_per_second': round(attempts / time_taken, 2) if time_taken > 0 else 0,
            'charset_used': charset
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
                        user_metadata: Optional[Dict] = None, user_id: Optional[str] = None) -> Dict:
        """AI-guided password guessing based on learned user behavior patterns"""
        start_time = time.time()
        attempts = 0
        
        # Generate intelligent guesses based on learned patterns and user behavior
        guesses = self.pattern_learner.generate_guesses(user_metadata, user_id)
        
        # Prioritize guesses based on learned patterns and common patterns
        prioritized_guesses = sorted(guesses, key=lambda x: (len(x), x))
        
        for password in prioritized_guesses:
            attempts += 1
            if verify_hash(password, hash_value, hash_type):
                time_taken = time.time() - start_time
                pattern_analysis = self.pattern_learner.analyze_password(password)
                
                # Learn from this successful crack
                if user_id:
                    self.pattern_learner.learn_from_password(password, user_id)
                
                risk_score = 100 - pattern_analysis['strength_score']
                
                return {
                    'cracked': password,
                    'attack_type': 'ai_guided',
                    'attempts': attempts,
                    'time_taken': round(time_taken, 4),
                    'risk_score': round(risk_score, 2),
                    'pattern_analysis': pattern_analysis,
                    'ai_learning_applied': True
                }
        
        time_taken = time.time() - start_time
        return {
            'cracked': None,
            'attack_type': 'ai_guided',
            'attempts': attempts,
            'time_taken': round(time_taken, 4),
            'risk_score': 0,
            'pattern_analysis': {},
            'ai_learning_applied': True
        }

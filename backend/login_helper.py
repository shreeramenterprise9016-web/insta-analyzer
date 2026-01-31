import instaloader
import getpass
import os

def interactive_login():
    print("=== Instagram Login for Real Data Mode ===")
    print("Logging in creates a session file that the Analyzer will use to bypass rate limits.")
    print("This runs locally on your machine. Credentials are NOT stored in plaintext, only the session cookies are saved.")
    
    user = input("Enter Instagram Username: ")
    password = getpass.getpass("Enter Instagram Password: ")
    
    L = instaloader.Instaloader()
    
    try:
        print(f"Attempting to login as {user}...")
        L.login(user, password)
        print("Login successful!")
        
        # Save session to 'session' file (default expected by analyzer.py)
        # Note: Instaloader typically saves as 'session-{username}'
        # We will save it there AND rename/copy to 'session' for our simple logic
        
        session_file = f"session-{user}"
        L.save_session_to_file(filename=session_file)
        print(f"Session saved to {session_file}")
        
        # Also save to 'session' because we hardcoded 'session' in analyzer.py for simplicity
        # or we could make analyzer.py smarter. Let's make analyzer.py look for session-{user} if we knew the user
        # But for now, let's just use 'session'
        
        # We need to manually save to 'session' file manually if we want a generic name
        # Actually Instaloader save_session_to_file uses the username or filename provided? 
        # It usually expects a filename parameter.
        L.save_session_to_file(filename="session") 
        print("Detailed session saved to 'session' file for the backend.")
        
    except instaloader.TwoFactorAuthRequiredException:
        print("2FA is required!")
        code = input("Enter 2FA Code: ")
        L.two_factor_login(code)
        L.save_session_to_file(filename="session")
        print("Login with 2FA successful and session saved.")
        
    except Exception as e:
        print(f"Login failed: {e}")

if __name__ == "__main__":
    interactive_login()

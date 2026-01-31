import instaloader
import random
import datetime
import requests
import config
import re
from collections import Counter

class InstagramAnalyzer:
    def __init__(self):
        self.username = "session" # Default session name

    def log_debug(self, msg):
        try:
            with open("debug_log.txt", "a", encoding="utf-8") as f:
                f.write(f"{datetime.datetime.now()} - {msg}\n")
        except:
            pass
        print(msg, flush=True)

    def __init__(self):
        self.L = instaloader.Instaloader()
        self.log_debug(f"InstagramAnalyzer Initialized. Config Token: {config.IG_ACCESS_TOKEN[:5] if config.IG_ACCESS_TOKEN else 'None'}")

        try:
             # Load from file named 'session' - using a dummy username as placeholder
             self.L.load_session_from_file(username="user", filename="session")
             print("Loaded session from file.")
        except FileNotFoundError:
             print("No session file found. Running anonymously (rate limits may apply).")

    def _extract_keywords(self, texts):
        """Extracts top keywords from a list of text strings, ignoring stopwords."""
        stopwords = {
            "the", "and", "to", "of", "a", "in", "is", "for", "on", "with", "it", "that", "this", "my",
            "at", "by", "from", "be", "an", "or", "as", "if", "but", "so", "are", "was", "were", "me",
            "you", "your", "we", "our", "he", "she", "they", "them", "link", "bio", "check", "new",
            "dm", "click", "out", "up", "can", "will", "what", "which", "how", "when", "why", "just",
            "do", "not", "no", "yes", "have", "has", "had", "reels", "post", "video", "photo", "image",
            "instagram", "follow", "like", "share", "comment", "save", "daily", "today", "now", "getting",
            "being", "doing", "going", "making", "taking", "looking", "want", "need", "love", "good",
            "great", "best", "better", "day", "time", "life", "world", "more", "some", "any", "all"
        }
        
        all_words = []
        for text in texts:
            if not text: continue
            # Remove hashtags and mentions
            clean_text = re.sub(r'[#@]\w+', '', text)
            # Remove non-alphanumeric (keep spaces)
            clean_text = re.sub(r'[^a-zA-Z\s]', '', clean_text)
            # Tokenize and lowercase
            words = clean_text.lower().split()
            # Filter stopwords and short words
            keywords = [w for w in words if w not in stopwords and len(w) > 2]
            all_words.extend(keywords)
            
        return [{"word": w[0], "count": w[1]} for w in Counter(all_words).most_common(10)]

    def get_mock_data(self, username, error_message=None):
        """Returns plausible mock data when scraping fails."""
        mock_keywords = [
            {"word": "fashion", "count": 15},
            {"word": "style", "count": 12},
            {"word": "summer", "count": 10},
            {"word": "vibes", "count": 8},
            {"word": "beautiful", "count": 7},
            {"word": "happy", "count": 6}
        ]
        return {
            "is_mock": True,
            "error_message": error_message,
            "username": username,
            "full_name": f"{username.capitalize()} (Mock)",
            "biography": "This is a mock profile description generated because valid scraping was blocked or failed.",
            "profile_pic_url": "https://via.placeholder.com/150",
            "is_verified": True,
            "followers": 12345,
            "followees": 456,
            "mediacount": 789,
            "engagement_rate": 2.5,
            "avg_likes": 300,
            "avg_comments": 45,
            "uploads_per_week": 3.5,
            "recent_posts": [
                {
                    "url": "https://via.placeholder.com/300",
                    "likes": random.randint(100, 500),
                    "comments": random.randint(10, 50),
                    "caption": "Mock caption #test",
                    "date": (datetime.datetime.now() - datetime.timedelta(days=i)).isoformat()
                } for i in range(6)
            ],
            "posting_schedule": [{"hour": h, "count": random.randint(0, 5) if 8 <= h <= 20 else 0} for h in range(24)],
            "top_hashtags": [
                {"tag": "love", "count": 10},
                {"tag": "instagood", "count": 8},
                {"tag": "photooftheday", "count": 5},
                {"tag": "fashion", "count": 3}
            ],
            "top_keywords": mock_keywords
        }

    def fetch_graph_api(self, target_username):
        """Fetches data using the Official Instagram Graph API (Business Discovery)."""
        self.log_debug(f"DEBUG: Config Token Prefix: {config.IG_ACCESS_TOKEN[:5] if config.IG_ACCESS_TOKEN else 'None'}")
        
        if config.IG_ACCESS_TOKEN == "YOUR_ACCESS_TOKEN_HERE" or config.IG_BUSINESS_ACCOUNT_ID == "YOUR_BUSINESS_ACCOUNT_ID_HERE":
            self.log_debug("DEBUG: Config still showing default values.")
            return None, "API Config Not Set"

        self.log_debug(f"Attempting Graph API fetch for {target_username}...")
        
        # Business Discovery Endpoint
        # We ask our business account to 'discover' the target username
        fields = "business_discovery.username(" + target_username + "){username,website,name,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count,media{caption,comments_count,like_count,media_url,permalink,timestamp,media_type}}"
        
        url = f"https://graph.facebook.com/v18.0/{config.IG_BUSINESS_ACCOUNT_ID}"
        params = {
            "fields": fields,
            "access_token": config.IG_ACCESS_TOKEN
        }
        
        try:
            # Force no proxy to avoid WinError 10061
            resp = requests.get(url, params=params, proxies={"http": None, "https": None})
            data = resp.json()
            self.log_debug(f"DEBUG: Full Graph API Response: {str(data)[:500]}...")
            
            if "error" in data:
                self.log_debug(f"Graph API Error: {data['error']['message']}")
                return None, data['error']['message']
            
            bd = data.get("business_discovery", {})
            if not bd:
                return None, "Profile not found via Graph API"

            # Parse to match our internal format
            result = {
                "is_mock": False,
                "data_source": "graph_api",
                "username": bd.get("username"),
                "full_name": bd.get("name"),
                "biography": bd.get("biography"),
                "profile_pic_url": bd.get("profile_picture_url"),
                "followers": bd.get("followers_count", 0),
                "followees": bd.get("follows_count", 0),
                "mediacount": bd.get("media_count", 0),
                "is_verified": False # Graph API doesn't easily return this in basic fields
            }
            
            # Process Media
            media_list = bd.get("media", {}).get("data", [])
            posts = []
            captions_list = []
            total_likes = 0
            total_comments = 0
            post_dates = []
            
            count = 0
            for item in media_list:
                # Limit to 12
                if count >= 12: break
                
                # Get image url (handle carousel/video)
                img_url = item.get("media_url")
                if not img_url: img_url = "https://via.placeholder.com/300?text=Video/Restricted"
                
                caption = item.get("caption", "")
                captions_list.append(caption) # Collect for keywords
                
                posts.append({
                    "url": img_url,
                    "likes": item.get("like_count", 0),
                    "comments": item.get("comments_count", 0),
                    "caption": caption,
                    "date": item.get("timestamp", "")
                })
                total_likes += item.get("like_count", 0)
                total_comments += item.get("comments_count", 0)
                if item.get("timestamp"):
                    try:
                        # Fix ISO format with Z
                        ts = item.get("timestamp").replace('Z', '+00:00')
                        dt = datetime.datetime.fromisoformat(ts)
                        post_dates.append(dt)
                        # self.log_debug(f"Parsed date: {dt}")
                    except Exception as ex:
                        self.log_debug(f"Date parse error: {ex}")
                else:
                    self.log_debug("Item missing timestamp")
                count += 1
                
            self.log_debug(f"Processed {count} items. Found {len(post_dates)} valid dates.")
                
            # Calcs
            if count > 0:
                result["avg_likes"] = round(total_likes / count, 1)
                result["avg_comments"] = round(total_comments / count, 1)
                if result["followers"] > 0:
                    er = ((total_likes + total_comments) / (count * result["followers"])) * 100
                    result["engagement_rate"] = round(er, 2)
                else:
                    result["engagement_rate"] = 0
            else:
                result["avg_likes"] = 0
                result["avg_comments"] = 0
                result["engagement_rate"] = 0

            result["recent_posts"] = posts
            
            # Uploads per week
            if len(post_dates) > 1:
                days_diff = (post_dates[0] - post_dates[-1]).days
                if days_diff > 0:
                    result["uploads_per_week"] = round((count / days_diff) * 7, 1)
                else:
                    result["uploads_per_week"] = 0
            else:
                result["uploads_per_week"] = 0

            # Posting Schedule (Hourly)
            hours = [dt.hour for dt in post_dates]
            hourly_counts = Counter(hours)
            schedule = [{"hour": h, "count": hourly_counts.get(h, 0)} for h in range(24)]
            # self.log_debug(f"Generated Schedule: {schedule}")
            result["posting_schedule"] = schedule

            # Hashtags & Keywords
            all_hashtags = []
            for post in posts:
                if post['caption']:
                    tags = [tag.strip("#") for tag in post['caption'].split() if tag.startswith("#")]
                    all_hashtags.extend(tags)
            
            # from collections import Counter # REMOVED: Already imported globally
            top_hashtags = Counter(all_hashtags).most_common(10)
            result["top_hashtags"] = [{"tag": t[0], "count": t[1]} for t in top_hashtags]
            
            result["top_keywords"] = self._extract_keywords(captions_list)
            
            self.log_debug(f"Graph API Success for {target_username}")
            return result, None

        except Exception as e:
            import traceback
            traceback.print_exc()
            self.log_debug(f"Graph API Exception: {e}")
            return None, str(e)


    def analyze_profile(self, username: str):
        # 1. Try Graph API First
        data, error = self.fetch_graph_api(username)
        if data:
            print(f"Graph API Success for {username}")
            return data
        
        graph_error = error
        
        # 2. Fallback to Instaloader
        try:
            profile = instaloader.Profile.from_username(self.L.context, username)
            
            # Basic info
            data = {
                "is_mock": False,
                "username": profile.username,
                "full_name": profile.full_name,
                "biography": profile.biography,
                "profile_pic_url": profile.profile_pic_url,
                "is_verified": profile.is_verified,
                "followers": profile.followers,
                "followees": profile.followees,
                "mediacount": profile.mediacount,
            }

            # Calculate stats from recent posts (limit to last 12 for speed)
            posts = []
            captions_list = []
            total_likes = 0
            total_comments = 0
            post_dates = []
            
            count = 0
            for post in profile.get_posts():
                if count >= 12:
                    break
                
                caption = post.caption if post.caption else ""
                captions_list.append(caption)

                posts.append({
                    "url": post.url,
                    "likes": post.likes,
                    "comments": post.comments,
                    "caption": caption,
                    "date": post.date_local.isoformat()
                })
                total_likes += post.likes
                total_comments += post.comments
                post_dates.append(post.date_local)
                count += 1
            
            if count > 0:
                data["avg_likes"] = round(total_likes / count, 1)
                data["avg_comments"] = round(total_comments / count, 1)
                # Simple ER formula: ((Likes + Comments) / Followers) * 100
                if profile.followers > 0:
                    er = ((total_likes + total_comments) / (count * profile.followers)) * 100
                    data["engagement_rate"] = round(er, 2)
                else:
                    data["engagement_rate"] = 0
            else:
                data["avg_likes"] = 0
                data["avg_comments"] = 0
                data["engagement_rate"] = 0

            data["recent_posts"] = posts
            
            # Simple uploads per week est.
            if len(post_dates) > 1:
                days_diff = (post_dates[0] - post_dates[-1]).days
                if days_diff > 0:
                    data["uploads_per_week"] = round((count / days_diff) * 7, 1)
                else:
                     data["uploads_per_week"] = 0
            else:
                 data["uploads_per_week"] = 0

            # Posting Schedule (Hourly)
            hours = [dt.hour for dt in post_dates]
            hourly_counts = Counter(hours)
            # Ensure all hours 0-23 exist
            schedule = [{"hour": h, "count": hourly_counts.get(h, 0)} for h in range(24)]
            data["posting_schedule"] = schedule

            # Extract hashtags
            all_hashtags = []
            for post in posts:
                if post['caption']:
                    tags = [tag.strip("#") for tag in post['caption'].split() if tag.startswith("#")]
                    all_hashtags.extend(tags)
            
            # from collections import Counter
            top_hashtags = Counter(all_hashtags).most_common(10)
            data["top_hashtags"] = [{"tag": t[0], "count": t[1]} for t in top_hashtags]
            
            # Extract Keywords
            data["top_keywords"] = self._extract_keywords(captions_list)

            return data

        except Exception as e:
            print(f"Error fetching data for {username}: {str(e)}")
            # If Graph API was attempted but failed, maybe show that error too?
            # For now return the scraping error, but if user provided config, they might want to know why Graph API failed
            
            combined_error = str(e)
            if graph_error and graph_error != "API Config Not Set":
                combined_error = f"Graph API: {graph_error} | Scraper: {str(e)}"
                
            return self.get_mock_data(username, error_message=combined_error)

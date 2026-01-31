import requests
import config
import datetime
import re
from collections import Counter

def _extract_keywords(texts):
    stopwords = {"the", "and"} # abbreviated for test
    all_words = []
    for text in texts:
        if not text: continue
        clean_text = re.sub(r'[#@]\w+', '', text)
        clean_text = re.sub(r'[^a-zA-Z\s]', '', clean_text)
        words = clean_text.lower().split()
        keywords = [w for w in words if w not in stopwords and len(w) > 2]
        all_words.extend(keywords)
    return [{"word": w[0], "count": w[1]} for w in Counter(all_words).most_common(10)]

def debug_graph_api(target_username):
    print(f"Testing Graph API for: {target_username}")
    url = f"https://graph.facebook.com/v18.0/{config.IG_BUSINESS_ACCOUNT_ID}"
    fields = "business_discovery.username(" + target_username + "){username,website,name,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count,media{caption,comments_count,like_count,media_url,permalink,timestamp,media_type}}"
    
    params = {
        "fields": fields,
        "access_token": config.IG_ACCESS_TOKEN
    }
    
    try:
        resp = requests.get(url, params=params)
        print(f"Status Code: {resp.status_code}")
        data = resp.json()
        
        bd = data.get("business_discovery", {})
        if not bd:
            print("No Business Discovery Data")
            return

        print(f"Username: {bd.get('username')}")
        
        media_list = bd.get("media", {}).get("data", [])
        captions_list = []
        for item in media_list:
            caption = item.get("caption", "")
            captions_list.append(caption)
            
        print("Extracting keywords...")
        kws = _extract_keywords(captions_list)
        print(f"Keywords: {kws}")
        print("Parsing SUCCESS")

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    debug_graph_api("scalewithpb")

import re
import os
import time

def extract_website_name(url):
  match = re.search(r"//([^/]+)", url)
  if match:
    website_name = match.group(1)
    website_name = website_name.replace("www.","")
    website_name = website_name.split(".")[0] if "." in website_name else website_name

    return website_name
  else:
    return None

def is_social_media(url,selecto_only):
  if selecto_only==None:
    social_media_sites = ["facebook", "twitter", "instagram", "linkedin", "youtube", "tiktok"]
  else :
    social_media_sites=["lr413",selecto_only]
  website_name = extract_website_name(url)
  if str(website_name) in social_media_sites:
    return True
  else:
    return False
  
def is_image_url(url):
  return url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg'))

def is_file_present_updated(file_path):
  isExist = os.path.exists(file_path)
  if not isExist:
    return False,""
  else:
    last_updated_time=os.path.getmtime(file_path)
    if last_updated_time+86400<time.time():
        pass
    else:
        content_of_file=""
        for i in open(file_path,"r"):
          content_of_file+=i
        return True,content_of_file

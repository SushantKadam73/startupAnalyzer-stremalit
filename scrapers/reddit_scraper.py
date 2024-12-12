import praw
import sys
import csv
import os 
sys.path.append('../6-12-2024')
from modules import api_calls_module
def reddit_scrape_post_comment(link):
    commented_time=[]
    comments_list=[]
    names_of_commentor=[]
    reddit= praw.Reddit(client_id="vXMP5m8vI2g1tBe51bUfzw",client_secret="w1oMJa8AgySG5yKDb2eRVUrBXBpHMA",user_agent="rajeshwar",username="South_Turnip_5618",password="123qwertyuiop@")
    link = link
    reddit_submission=reddit.submission(url=link)
    name_of_poster=reddit_submission.author
    title_body=reddit_submission.title
    title_body=title_body+reddit_submission.selftext
    for top_level_comment in reddit_submission.comments:
        if top_level_comment.body.find("contact the moderators")>=0:
            pass
        else:
            comments_list.append(top_level_comment.body)
            names_of_commentor.append(top_level_comment.author)
            commented_time.append(top_level_comment.created_utc)


    return(str(title_body),comments_list,name_of_poster,names_of_commentor,commented_time)




def reddit_scrape_and_explainer(link,comapany_name):
    title_body,comments_list,name_of_poster,names_of_commentor,time_of_post=reddit_scrape_post_comment(link)
    print(title_body,comments_list,name_of_poster,names_of_commentor,time_of_post)
    scraped_before=False
    combinator=[]
    for i in names_of_commentor,time_of_post:
        combinator.append(i)
    isExist = os.path.exists("knowlege_base/"+comapany_name+"/reddit_comments.csv")
    if not isExist:
        open("knowlege_base/"+comapany_name+"/reddit_comments.csv","w")
    else:
        with open("knowlege_base/"+comapany_name+"/reddit_comments.csv", 'r') as csvfile:
            
            list_read_csv = csv.reader(csvfile)
            for read_row in list_read_csv:
                try:
                    if read_row[0]==title_body:
                        title_body,reaction_of_audince,comments_list=read_row[0],read_row[1],read_row[2]
                        scraped_before=True
                        return title_body,reaction_of_audince,comments_list
                except:
                    pass
    if scraped_before==True:
        pass
    else :           
        reaction_of_audince=[]
        for comment in comments_list:
            response=api_calls_module.ask_llm(comment,False,["with refrence to a soical media post their are some comments rate them wheather they are postive or negative and give a reason for each comment. post:"+title_body,"do not make up answer and i will give you comments","please provide sentiment only"])
            reaction_of_audince.append(response)
        reaction_of_audince="\n\n".join(reaction_of_audince)
        comments_list="\n\n".join(comments_list)
        with open("knowlege_base/"+comapany_name+"/reddit_comments.csv", 'a',encoding="utf") as csv_file:
                writer_object = csv.writer(csv_file)
                writer_object.writerow([title_body,reaction_of_audince,comments_list,"posted by:"+str(name_of_poster),names_of_commentor])



    return title_body,reaction_of_audince,comments_list
    
import requests
from bs4 import BeautifulSoup
import re
import json
import base64
import datetime
import os
import random
import time
import csv


#####  CHAPTERS   #####

def proxies_pool():
    url = 'https://www.sslproxies.org/'
    
    # Retrieve the site's page. The 'with'(Python closure) is used here in order to automatically close the session when done
    with requests.Session() as res:
        proxies_page = res.get(url)
        
    # Create a BeutifulSoup object and find the table element which consists of all proxies
    soup = BeautifulSoup(proxies_page.content, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')
  
    # Go through all rows in the proxies table and store them in the right format (IP:port) in our proxies list
    proxies = []
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append('{}:{}'.format(row.find_all('td')[0].string, row.find_all('td')[1].string))
    return proxies


proxies=proxies_pool()

cwd=os.getcwd()


HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"}
SITE = "https://novel_website.com"

user="username"
password="password"

creds= user+":"+password
token = base64.b64encode(creds.encode())
heade={
    "Authorization":"Basic "+ str(token.decode("utf-8")),
}

url="http://localhost/wordpress/wp-json/wp/v2"




def post_chapters(catf):

    POSTS=[]
    PAGES=[]
    pnum=1
    while True:
        try:
            param={'page':pnum,'per_page':100}
            r=requests.get(url+"/posts", headers=heade,params=param)           # get wordpress categories
            POSTS2=json.loads(r.content)

            if 'message' in POSTS2:
                break
            elif len(POSTS2)<=0:
                break
            else:
                for p in POSTS2:
                    POSTS.append(p)
                
            pnum=pnum+1

        except requests.exceptions.InvalidURL:
            break
        except:
            print("Reloading")
            time.sleep(random.randint(1, 5))

    pnum=1

    while True:
        try:
            param={'page':pnum,'per_page':100,'status':'future'}
            r=requests.get(url+"/posts", headers=heade,params=param)           # get wordpress categories
            POSTS1=json.loads(r.content)

            if 'message' in POSTS1:
                break
            elif len(POSTS1)<=0:
                break
            else:
                for p in POSTS1:
                    POSTS.append(p)
            pnum=pnum+1
            
        except requests.exceptions.InvalidURL:
            break
        except:
            print("Reloading")
            time.sleep(random.randint(1, 5))

    pnum=1
    while True:
        try:
            param={'page':pnum, 'per_page':100}
            r=requests.get(url+"/pages", headers=heade,params=param)           # get wordpress categories
            PAGES2=json.loads(r.content)

            if 'message' in PAGES2:
                break
            elif len(PAGES2)<=0:
                break
            else:
                for p in PAGES2:
                    PAGES.append(p)
            pnum=pnum+1
        except requests.exceptions.InvalidURL:
            break
        except:
            print("Reloading")
            time.sleep(random.randint(1, 5))

    pnum=1
    while True:
        try:
            param={'page':pnum, 'per_page':100,'status':'future'}
            r=requests.get(url+"/pages", headers=heade,params=param)           # get wordpress categories
            PAGES1=json.loads(r.content)

            if 'message' in PAGES1:
                break
            elif len(PAGES1)<=0:
                break
            else:
                for p in PAGES1:
                    PAGES.append(p)
            pnum=pnum+1
        except requests.exceptions.InvalidURL:
            break
        except:
            print("Reloading")
            time.sleep(random.randint(1, 5))

    cat_id=0
    
    ss1=catf.split("\\")           # If you want to run on windows then uncomment this 
    #ss1=catf.split("/")             # for linux uncomment this
    if len(ss1)>0:
        ss=ss1[-1].split("_")
        if len(ss)>0:
            cat_id=int(ss[0])
            cat_name=ss[1]
    novel_links=[]
    n_links=[]

    try:
        with open(catf,'r') as f:
            n_links=f.readlines()
    except IOError as e:
        print(e)
    except:
        pass

    for l in n_links:
        if not l in novel_links:
            novel_links.append(l)

    for i in range(len(novel_links)):
        
        novel_link = ""
        novel_name=""
        if "incomplete" in novel_links[i]:

            ss=novel_links[i].split(",")
            if len(ss)>0:
                novel_name=ss[0]
            if len(ss)>1:
                novel_name=ss[0]
                novel_link=ss[1]

            novel_name=novel_name.replace(","," ")
            soup=None
            print("Loading novel : "+ novel_link)

            if len(novel_link)>0:
                while True:
                    try:
                        proxy_index = random.randint(0, len(proxies) - 1)
                        proxy = {"http": proxies[proxy_index], "https": proxies[proxy_index]}
                        # Getting Novel's Info
                        req = requests.get(novel_link, headers=HEADERS)                 # Load Novel List
                        soup = BeautifulSoup(req.text, "html.parser")
                        print("Novel Loaded : "+ novel_link)
                        break
                    except requests.exceptions.InvalidURL:
                        break
                    except:
                        print("Reloading")
                        time.sleep(random.randint(1, 5))


                
                page_slug = novel_name.strip().replace(" ","-").lower()
                page_slug = page_slug.replace("–","-")
                page_slug = page_slug.replace(",","")
                page_slug = page_slug.replace("’","")
                page_slug = page_slug.replace(":","")
                page_slug = page_slug.replace(".","-")
                page_slug = page_slug.replace("!","")   
                sl1=page_slug.split("-")
                page_slug1=""
                if len(sl1) > 0:
                    for s in range(len(sl1)-1):
                        if len(sl1[s])>0:
                            page_slug1=page_slug1+sl1[s]+"-"
                
                page_slug1=page_slug1+sl1[-1]


                page_slug=page_slug1
                page_id=0
                page_content=""
                page_exist=False
                pslugs=[]
                for p in PAGES:
                    pslugs.append(p['slug'])


                for page in PAGES:
                    if page_slug in page['slug']:
                        page_exist=True
                        page_id=page['id']
                        page_content=page['content']['rendered']
                        break

                pcontent=""
                
                if not page_exist:
                    rightside=soup.select(".novel-right .novel-detail-item")
                    if rightside!=None and len(rightside)>0:
                        pcontent=rightside[0].text.strip()

                    dt=datetime.datetime.now()
                    wp_page={
                        'date':dt.replace(microsecond=0).isoformat(),
                        'date_gmt': datetime.datetime.now().replace(microsecond=0).isoformat(),
                        "slug":page_slug,
                        "status":"publish",
                        "title":novel_name.strip(),
                        "content":pcontent,
                        "author":1,
                        "comment_status":"open",
                        "ping_status":"open"
                    }

                    r=requests.post(url+"/pages", headers=heade, json=wp_page)      # Request to create Page
                    res5=json.loads(r.content)
                    page_id=res5['id']
                    page_content=res5['content']['rendered']
                    PAGES.append(res5)


                article_list=soup.findAll(class_="chapter-chs")                         # Get Articles List
                print("Articles :" + str(len(article_list)))
                    # Novel Chapters
                for articles in article_list:

                    chapter_list=articles.findAll("a")                                  # Get Chapters List
                    print("Chapters : "+str(len(chapter_list)))

                    for chapters in chapter_list:
                        ch = chapters["href"]
                        soup=BeautifulSoup("<html></html>", "html.parser")
                        print("loading chapter : "+ch)
                        while True:
                            try:
                                proxy_index = random.randint(0, len(proxies) - 1)
                                proxy = {"http": proxies[proxy_index], "https": proxies[proxy_index]}

                                # Getting article
                                req = requests.get(ch, headers=HEADERS)            # Get Chapter 
                                soup = BeautifulSoup(req.content, "html.parser")
                                print("Chapter Loaded : "+ch)

                                break
                            except requests.exceptions.InvalidURL:
                                break
                            except:
                                print("Reloading")
                                time.sleep(random.randint(1, 5))

                        art_title=""
                        title = soup.select(".block-title")
                        if len(title)>0:    # Check if chapter exists 
                            art_title=title[0].get_text().strip()
                        
                            full_article = soup.find("div", {"class": "desc"})

                            # remove ads inside the text:
                            for ads in full_article.select('center, small, a, .hidden'):
                                ads.extract()

                            txt=full_article.get_text(strip=True, separator='\n')
                            
                            date=datetime.datetime.now()
                            slug=art_title.replace(" ","-").lower()   # Slug for page link
                            slug=slug.replace("–","-")
                            slug=slug.replace(",","")
                            slug=slug.replace("'","'")
                            slug=slug.replace("’","")
                            slug=slug.replace(":","")
                            slug=slug.replace(".","-")
                            slug=slug.replace("!","")

                            sl=slug.split("-")
                            slug1=""
                            if len(sl) > 0:
                                for s in range(len(sl)-1):
                                    if len(sl[s])>0:
                                        slug1=slug1 + sl[s] + "-"
                            slug1=slug1 + sl[-1]

                            slug=slug1

                            found=False

                            slugs=[]
                            for p in POSTS:
                                slugs.append(p['slug'])

                            for post in POSTS:
                                if slug in post['slug']:
                                    found=True
                                    break
                            
                            if not found:
                                post={
                                    'date':date.replace(microsecond=0).isoformat(),
                                    'date_gmt': datetime.datetime.now().replace(microsecond=0).isoformat() + "Z",
                                    'author':1,
                                    'slug': slug,
                                    'title': art_title,
                                    'content': txt,
                                    'excerpt': 'Exceptional post!',
                                    'status': 'publish',
                                    'format': 'standard',
                                    'categories': cat_id
                                }
                                print("Creating Post")
                                r=requests.post(url+"/posts", headers=heade, json=post)
                                res=json.loads(r.content)
                                POSTS.append(res)
                                post_link=res['link']
                                
                                print("Post created")
                                
                                page_content=page_content+"<a href=\""+post_link+"\">"+art_title+"</a><hr>"
                                
                                wp_page={
                                    "id":page_id,
                                    "content":page_content
                                }

                                r=requests.post(url+"/pages/"+str(page_id), headers=heade, json=wp_page)
                                res=json.loads(r.content)

            novel_links[i]=novel_links[i].replace("incomplete","completed")
            try:
                with open(catf,'w',newline='') as f:
                    f.writelines(novel_links)
            except IOError as e:
                print(e.strerror)
            except:
                pass





#### END CHAPTERS  ######


while True:


    #######   CATEGORIES    ########



    categories=[]
    print("Loading Website to scrape")
    while True:
        try:
            req = requests.get(SITE, headers=HEADERS)       # Load main website
            req.encoding=req.apparent_encoding
            soup = BeautifulSoup(req.text, "html.parser")
            category = soup.findAll(class_="search-by-genre")

            categories = [link['href'] for link in soup.findAll(href=re.compile(r'/category/\w+$'))]        # get All categories links

            try:
                with open(cwd+"\\categories_links_list.csv",'w',newline='') as f:
                    writer=csv.writer(f,delimiter=',', quotechar='"',quoting=csv.QUOTE_MINIMAL)
                    for cat in categories:
                        writer.writerow([cat,"incomplete"])
            except IOError as e:
                print(e.strerror)
            except:
                pass

            break
        except requests.exceptions.InvalidURL:
            break
        except:
            print("Reloading")
            time.sleep(random.randint(1, 5))

    print("Completed")



    ######   END CATEGORIES  ######

    #######    Generate Novels LINKS    #######



    cats=[]
    cwd=os.getcwd()



    print("Getting Categories From Own Wordpres Website")
    while True:
        try:
            param={'per_page':100}
            r=requests.get(url+"/categories", headers=heade,params=param)           # get wordpress categories
            cats=json.loads(r.content)
            break
        except requests.exceptions.InvalidURL:
            break
        except:
            print("Reloading")
            time.sleep(random.randint(1, 5))

    print("WordPress Categories :"+str(len(cats)))
    wp_categories=[]
    try:
        for i in range(len(cats)):                      # make list of name and id
            wp_categories.append({'name': cats[i]['name'],'id':cats[i]['id']})
    except Exception:
        pass



    categories=[]
    try:
        with open(cwd+"\\categories_links_list.csv","r",newline='') as f:
            categories=f.readlines()
    except IOError as e:
        print(e.strerror)
    except:
        pass




    for i in range(len(categories)):

        cat_link=""
        fname=""
        if "incomplete" in categories[i]:
            ss=categories[i].split(",")
            if len(ss)>0:
                cat_link=ss[0]
                
        print("\nCategory : "+cat_link+" Is in process")
        
        if len(cat_link)>0:
            cat_name=cat_link.split("/")[-1]
            cat_id=0
            cat_found=False
            for k in range(len(wp_categories)):         # Loop to check if novel category already exists at wordpress website.
                c1=str(wp_categories[k]['name'].encode("utf-8")).lower()
                if cat_name.lower() in c1:
                    cat_found=True
                    cat_id=wp_categories[k]['id']
                    break

            if not cat_found:                           # if category not found then create category
                print("Adding category to website")
                wp_cat={
                    'name':cat_name,
                    'slug':cat_name,
                    'description':"This Category Will Contain " + cat_name + " Novels",
                    'count':0,
                    'taxonomy':""
                }
                
                r=requests.post(url+"/categories", headers=heade, json=wp_cat)      # Request to create category
                res=json.loads(r.content)
                cat_id=res['id']
            
            fname=cwd+"\\"+str(cat_id)+"_"+cat_name+"_novels_links_list.csv"

            try:
                with open(fname,'w',newline='') as f:
                    f.write("")
            except IOError as e:
                print(e.strerror)
            except:
                pass

            novels_links=[]
            print("Loading category")
            while True:
                try:
                    req = requests.get(cat_link, headers=HEADERS)       # Load category
                    soup = BeautifulSoup(req.text, "html.parser")
                    novels_header = soup.findAll(class_="top-novel-header")
                    print("Category Loaded")
                    
                    # Find pagination if any
                    lis=soup.select(".pagination li")   
                    if len(lis)>0:
                        last_p=lis[-1].select('a')
                        last_page=0
                        if len(last_p)>0:
                            x=last_p[0]
                            href=x["href"]
                            last_page=int(href.split("/")[-1])
                        print("Total Pages :"+str(last_page))
                        page_num=1
                        while True:                                                 # Loop to get all pages
                            print("Loading Page : "+str(page_num))
                            try:
                                page_url="https://www.readlightnovel.org/category/"+cat_name+"/"+str(page_num)       # Open pages 
                                req = requests.get(page_url, headers=HEADERS)       #get page
                                soup1 = BeautifulSoup(req.text, "html.parser")
                                novels_header1 = soup1.findAll(class_="top-novel-header")

                                try:
                                    with open(fname,'a',newline='') as f:
                                        writer=csv.writer(f,delimiter=',', quotechar='"',quoting=csv.QUOTE_MINIMAL)
                                        for n in novels_header1:
                                            novel_link = n.select('a')
                                            if len(novel_link) > 0:
                                                nname=novel_link[0].text.strip()
                                                nname=nname.replace(",","")
                                                writer.writerow([nname,novel_link[0]["href"],"incomplete"])    # Add links of all novels on the page
                                        
                                except IOError as e:
                                    print(e.strerror)
                                except:
                                    pass

                                print("Loaded Page : "+str(page_num))
                                page_num=page_num+1

                                if page_num>last_page:                              # check if end of pages
                                    break
                                time.sleep(random.randint(1, 5))
                            except Exception as e:
                                print("Reloading")
                                time.sleep(random.randint(1, 5))

                    break
                except requests.exceptions.InvalidURL:
                    break
                except:
                    print("Reloading")
                    time.sleep(random.randint(1, 5))

            try:
                with open(cwd+"\\categories_links_list.csv",'w',newline='') as f:

                    categories[i]=categories[i].replace("incomplete","completed")
                    f.writelines(categories)
                    
            except IOError as e:
                print(e.strerror)
            except:
                pass

        post_chapters(fname)

    print("completed")

    print("System will start again after 1 hour")
    #time.sleep(3600)

    #######   END Generate Novels LINKS    #######

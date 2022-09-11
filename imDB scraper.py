from bs4 import BeautifulSoup
import requests
import pandas as pd
import time



def store_data(information_map):
    df = pd.DataFrame.from_dict(information_map) 
    df.to_csv (r'amzn_books.csv', index = False, header=True)

def get_rated(soup):
    try:
        rating=soup.find('span',attrs={'class':"sc-8c396aa2-2 itZqyK"})
        return rating.string
    except:
        return "NULL"

def get_box_office(soup):
    try:
        boxoffice=soup.find('span',attrs={'class':"ipc-metadata-list-item__list-content-item"})
        return boxoffice.string.strip()
        pass
    except:
        return 'NULL'
    
# Function to extract Product Title
def get_title(soup):
	
	try:
		title = soup.find("h1", attrs={'class':"sc-b73cd867-0 eKrKux"})
		title_value = title.string
		title_string = title_value.strip()
  
	except AttributeError:
		title_string = "NULL"	

	return title_string

# Function to extract Product Price
def get_year_rated(soup):
    local=list()
    for td in soup.find("span", attrs={'class':"sc-8c396aa2-2 itZqyK"}).parent.find_next_siblings():
        local.append(td)
        
    year.append(local[0])
    rated.append(local[1])
	
def get_meta(soup):
    try:
        meta=soup.find('span',attrs={'class':"score-meta"})
        return meta.string
    except:
        return 'NULL'

def get_director(soup):
    try:
        direc=soup.find('a',attrs={'class':"ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"})
        return direc.string
    except:
        return 'NULL'
    
def get_genre(soup):
    gen_temp=list()
    try:
        for td in soup.find("h1", attrs={'class':"sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt"}).parent.find_next_siblings():
            gen_temp.append(td)
        return gen_temp
    except:
        return "NULL"
    
# Function to extract Product Rating
def get_rating(soup):

	try:
		rate = soup.find("span", attrs={'class':"sc-7ab21ed2-1 jGRxWM"}).string.strip()
		
	except:
		return "NULL"

	return rate+'/10'

# Function to extract Number of User Reviews
def get_rating_count(soup):
	try:
		review_count = soup.find("div", attrs={'class':"sc-7ab21ed2-3 dPVcnq"}).string.strip()
		
	except AttributeError:
		review_count = "NULL"	

	return review_count

# Function to extract Availability Status
def get_length(soup):
	try:
		length = soup.find("li", attrs={'class':"ipc-inline-list__item"})
		return length.string.strip()

	except AttributeError:
		available = "Not Available"	

	return available	

def extract_info(soups):
    links=soups.find_all('div',attrs={'class':"lister-item-image float-left"})
    links_list=[]
    for link in links:
        links_list.append(link.find('a').get('href'))
    links_list = [*set(links_list)]
    for i in links_list:      
        try:  
            req=requests.get(base_link+i,headers=headers)
            if req.status_code < 500:
                soup = BeautifulSoup(req.content, 'html.parser')
                title.append(get_title(soup))
                get_year_rated(soup)
                #rated.append(get_rated(soup))
                run_length.append(get_length(soup))
                genre.append(get_genre(soup))
                meta_rating.append(get_meta(soup))
                rating.append(get_rating(soup))
                rating_count_list.append(get_rating_count(soup))
                director.append(get_director(soup))
                global_box_office.append(get_box_office(soup))
                print('sucess')
                req.close()
            else:
                print("Link opening error : 404")
                
        
        except:
            print("Connection Error")
                

if __name__ == '__main__':
    global title
    global year
    global rated
    global run_length
    global genre
    global meta_rating
    global rating
    global rating_count_list
    global director
    global global_box_office
    
    global headers
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    
    title=list()
    year=list()
    rated=list()
    run_length=list()
    genre=list()
    meta_rating=list()
    rating=list()
    rating_count_list=list()
    director=list()
    global_box_office=list()

    movie_genre=['Action','Adventure','Animation','Biography','Comedy','Crime','Documentary','Drama','Family','Fantasy','film-noir','History','Horror','Music','Musical','Mystery','Romance','sci-fi','Short','Sport','Superhero','Thriller','War','Western']
    
    base_link='https://www.imdb.com'
    target_link='https://www.imdb.com/search/title/?title_type=feature&genres={}&start={}&explore=genres&ref_=adv_explore_rhs'
    for i in movie_genre:
        try:
            req=requests.get(target_link.format(i,1),headers=headers)
            soup = BeautifulSoup(req.content, 'html.parser')
            
            #of 250000 titles
            number=soup.find('div',attrs={'class':'desc'})
            number=number.find('span').string
            no_titles=int((number[number.find('of')+2:number.find('titles')].strip()).replace(',',''))

            for j in range(1,no_titles,50):
                reqs=requests.get(target_link.format(i,j),headers=headers)
                soup = BeautifulSoup(reqs.content, 'html.parser')
                extract_info(soup)
                reqs.close()
        except:
            print("Error connecting")
            quit()
	
    information_map={'Title':title,'Release Year':year,'Rated':rated,'Run Length':run_length,'Genre':genre,'Meta Rating':meta_rating,'IMDB Rating':rating,'Review Count':rating_count_list,'Director':director,'Global Box Office':global_box_office}
    store_data(information_map)


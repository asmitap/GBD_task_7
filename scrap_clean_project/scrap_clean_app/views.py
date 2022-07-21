from django.shortcuts import render
import pandas as pd
import json
from .models import *
from selenium import webdriver
from datetime import datetime


def json_content(json_files):
    scheme_name = json_files['name']
            #print(scheme_name)
    scheme = Scheme()
    
    scheme_exist = Scheme.objects.filter(schema_name=scheme_name).exists()
    
    if not scheme_exist:
        scheme.schema_name = scheme_name
        scheme.save()
    else:
        pass
        #print("already exist scheme name")
        
        
    #print(scheme_name)
    scheme_id = Scheme.objects.filter(schema_name=scheme_name).values_list('pk', flat=True)
    #print(scheme_id)
    category_content = json_files['parent_content']
    
    #print(category_content)
    for category_content in category_content:
        category_name = category_content['category']
        #print(category_name) # category name
        parent_xpath = category_content['parent_xpath']
        
        category_exist = Category.objects.filter(category_name=category_name).exists()
        #print(category_exist)
        if not category_exist:
            category = Category()
            category.category_name = category_name
            category.parent_xpath = parent_xpath
            category.scheme_id = scheme_id
            category.save()
        else:
            pass
            #print("already exist category name")
        category_id = Category.objects.filter(category_name=category_name).values_list('pk', flat=True)
        #print(category_id)
        content = category_content['content']
        #print(content)
        for i in content:
            content = Content()
            field_name = i['field']
            xpath = i['xpath']
            # print(field_name)
            #print(xpath)

            content_exist = Content.objects.filter(xpath=xpath).exists()
            if not content_exist:
                content.field_name = field_name
                content.xpath = xpath
                content.category_id = category_id
                content.save()
            else:
                pass
                #print("Already exist")


def indexing(final_dfs, url_number, category_number):
    indexx = []
    field = []
    value = []
    j=1
    for index,content in final_dfs.iterrows():
        for i in range(len(content)):
            indexx.append(f" {url_number}.{category_number+1}.{j}.{i+1}")
        j=j+1
    j=0        
    for index,content in final_dfs.iterrows():
        for i in range(len(content)):
            field.append(content.index[i])
            value.append(content[i])
            j = j+1
    # series
    s1 = pd.Series(indexx) 
    s2 = pd.Series(field)
    s3 = pd.Series(value)
    final_df =pd.concat([s1, s2, s3], axis=1)
    final_df.columns = ['index','field','value']
    final_df = final_df.sort_values(by=['field','index'])
    return(final_df)



def scrap(csv_data, json_files):
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(executable_path='/home/asmita/Desktop/webscrap/chromedriver')
    urls = csv_data.values.tolist()
    urls = [item for items in urls for item in items]

    final_json_to_csv_df = pd.DataFrame()
    url_number = 1
    for url in range(len(urls)):
        #print(urls[url])
        driver.get(urls[url])
        category_contents = json_files['parent_content']
        # print(category_contents)
        category_number = 0
        for category_content in category_contents:
            category_name = category_content['category']
            #print(category_name)
            parent_xpath = category_content['parent_xpath']
            #print(parent_xpath)
            elements = driver.find_element("xpath",parent_xpath)
           
            content = category_content['content']
            field_names = []
            child_xpaths = []
            for i in content:
                field_name = i['field']
                child_xpath = i['xpath']
                #print(field_name, child_xpath)
                field_names.append(field_name)
                child_xpaths.append(child_xpath)

            title = []
            rating = []
            rating_count = []
            price = []

            titles = elements.find_elements("xpath", child_xpaths[0])
            for title_name in titles:
                title.append(title_name.text)
            # print(title)

            ratings = elements.find_elements("xpath", child_xpaths[1])
            for rating_number in ratings:
                rating.append(rating_number.get_attribute('textContent'))
            
            rating_counts = elements.find_elements("xpath", child_xpaths[2])
            for rating_count_number in rating_counts:
                rating_count.append(rating_count_number.text)

            prices = elements.find_elements("xpath", child_xpaths[3])
            for price_number in prices:
                price.append(price_number.get_attribute('textContent'))


            s1 = pd.Series(title)
            s2 = pd.Series(rating)
            s3 = pd.Series(rating_count)
            s4 = pd.Series(price)
            final_df =pd.concat([s1, s2, s3, s4], axis=1)
            final_df.columns = [category_name + '_title',category_name + '_rating',category_name + '_rating_count',category_name + '_price']
            #print(category_number)
            final_df = indexing(final_df, url_number, category_number)
            final_json_to_csv_df = pd.concat([final_json_to_csv_df, final_df])
            #print(final_df)
            category_number = category_number + 1
        url_number = url_number + 1
    final_json_to_csv_df = final_json_to_csv_df.fillna("Na")
    currentDateTime = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    #final_json_to_csv_df.to_csv(r'/home/asmita/Downloads/'f"output {currentDateTime}.csv", index = False)
    print(final_json_to_csv_df)

    



                

            
                   
                
            
            


        








    




# Create your views here.
def index(request):
    if request.method == 'POST':
        if request.FILES['jsonfile']:
            json_file = request.FILES['jsonfile']
            json_files = json.load(json_file)
            json_content(json_files)
    return render(request, "index.html")

def schemename(request):
    schemes_name = Scheme.objects.all()
    category_name = Category.objects.all()
    contents = Content.objects.all()
    return render(request, "scheme_name.html", {'schemes_name': schemes_name, 'categorys_name':category_name, 'contents': contents})


def listconfig(request):
    schemes_name = Scheme.objects.all()
    return render(request, "list_config.html",{'schemes_name': schemes_name})

def editconfig(request):
    schemes_name = Scheme.objects.all()
    category_name = Category.objects.all()
    contents = Content.objects.all()

    if request.method == 'POST':
        c_id = request.POST.getlist('c_id')
        xpath = request.POST.getlist('xpath')
        new_dict = {c_id[i]: xpath[i] for i in range(len(c_id))}
        #print ("Created dictionary:",new_dict)
        for key in new_dict.keys():
            pk = key
            xpath = new_dict[key]
            Content.objects.filter(pk=pk).update(xpath=xpath, updated_at=datetime.datetime.now())
    return render(request, "edit_config.html", {'schemes_name': schemes_name, 'categorys_name':category_name, 'contents': contents})

def upload(request):
    if request.method == 'POST':
        if request.FILES['csvfile']:
            csv_file = request.FILES['csvfile']
            #csv_data = csv_file.read().decode("utf-8")	
            csv_data = pd.read_csv(csv_file, header=0)
            #print(csv_data)            
            json_file = request.FILES['jsonfiles']
            json_files = json.load(json_file)
            #print("hello")
            json_content(json_files)
            scrap(csv_data, json_files)
            
        
        
    return render(request, "upload.html")
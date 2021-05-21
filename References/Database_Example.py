import MySQLdb
import pandas as pd
import requests
def createConnection(db_name='crawler'):
    host = "localhost"
    passwd = "la12A$hong"
    user = "root"
    dbname = db_name
    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=dbname)
    cursor = db.cursor()
    return cursor, db

def fixdb(db_name):
    cursor, db = createConnection(db_name=db_name)
    cursor.execute("ALTER DATABASE `%s` CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci'" % dbname)

    sql = "SELECT DISTINCT(table_name) FROM information_schema.columns WHERE table_schema = '%s'" % dbname
    cursor.execute(sql)

    results = cursor.fetchall()
    for row in results:
        sql = "ALTER TABLE `%s` convert to character set DEFAULT COLLATE DEFAULT" % (row[0])
        print(sql)
        cursor.execute(sql)
    db.close()
#-----------------------------------------------------------------------------------------------
def select_attr(id):
    sql = "SELECT * FROM news_site_siteattributes" 
    cursor, db = createConnection()
    cursor.execute(sql)
    results = cursor.fetchall()
    list_id = []
    list_name = []
    list_type_selector = []
    list_selector = []
    for row in results:
        print(row[0], end = ' - ')
        list_id.append(row[0])
        print(row[1], end = ' - ')
        list_name.append(row[1])
        print(row[2], end = ' - ')
        list_type_selector.append(row[2])
        print(row[5])
        list_selector.append(row[5])
    db.close()
    d = {'id' : list_id, 'name' : list_name, 'name Selector' : list_type_selector, 'selector' : list_selector}
    data = pd.DataFrame(data=d)
    print(data)
    data.to_csv('attrs.csv', index=False)

def select_site(db_name):
    sql = "SELECT id, CONVERT(CAST(SiteName as BINARY) USING utf8), SiteLink, PageParam, ArticleLinkSelector FROM news_site_sites" 
    cursor, db = createConnection()
    cursor.execute(sql)
    results = cursor.fetchall()
    list_id = []
    list_name = []
    list_link = []
    list_pageparam = []
    list_selector = []
    for row in results:
        print('ID: ', end = '')
        print(row[0], end = ' - ')
        list_id.append(row[0])
        print('Name: ', end = '')
        print(row[1], end = ' - ')
        list_name.append(row[1])
        print('Link: ', end = '')
        print(row[2], end = ' - ')
        list_link.append(row[2])
        print('PageParam: ', end = '')
        print(row[3], end = ' - ')
        list_pageparam.append(row[3])
        print('Selector: ', end = '')
        print(row[4])
        list_selector.append(row[4])
    db.close()

    d = {'id' : list_id, 'name' : list_name, 'link' : list_link, 'pageParam' : list_pageparam, 'selector' : list_selector}
    data = pd.DataFrame(data=d)
    print(data)
    data.to_csv('sites.csv', index=False)

def select_category():
    cursor, db = createConnection()
    sql = "SELECT siteLink, siteName FROM DB1_SITE"
    cursor.execute(sql)
    results = cursor.fetchall()
    list_siteName = []
    list_category = []
    for row in results:
        #print(row[0], end = ' - ')
        #print(row[1])
        list_siteName.append(row[0])
        list_category.append(row[1])
    df = pd.DataFrame({'siteName' : list_siteName, 'category' : list_category})
    df.to_csv('map_cate.csv', index=False)
    print(df)

def insert_category():
    cursor, db = createConnection()
    df = pd.read_csv('map_cate.csv')
    count = 1
    for index, row in df.iterrows():
        try:
			#conn, cursor = connect_db()
            cursor, db = createConnection()
            cursor.execute("insert into MAP_CATEGORY values(%s,%s,%s)",(
                    row['siteName'],
                    row['categoryOrigin'],
                    row['categoryNew']
                ))
            print(count, end = ' - ')
            db.commit()
            cursor.close()
            db.close()
            count += 1
        except Exception as e:
            cursor.close()
            db.close()
            print(e)
    print(df)
def select_category():
    cursor, db = createConnection()
    sql = "SELECT DISTINCT categoryNew FROM MAP_CATEGORY"
    cursor.execute(sql)
    results = cursor.fetchall()
    list_ = []
    for row in results:
        list_.append(row[0])
        print(row)
    df = pd.DataFrame({'category' :  list_})
    df.to_csv('categoryNew.csv', index=False)
#select_category()
def export_link():
    cursor, db = createConnection()
    sql = "SELECT link FROM DB1_DATA"
    cursor.execute(sql)
    results = cursor.fetchall()
    list_ = []
    for row in results:
        list_.append(row[0])
    df = pd.DataFrame({'LINK' :  list_})
    df.to_csv('LINK_DATA.csv', index=False)
#export_link()

def export_db_crawler():
    cursor, db = createConnection()
    sql = "SELECT * FROM DB1_SITEATTRIBUTE;"
    cursor.execute(sql)
    results = cursor.fetchall()
    fN = []
    tS = []
    fJ = []
    selc = []
    root_id = []
    for row in results:
        fN.append(row[1])
        tS.append(row[2])
        fJ.append(row[3])
        selc.append(row[4])
        root_id.append(row[5])

    df = pd.DataFrame({'fieldName' :  fN, 'typeSelector' : tS, 'findJson' : fJ, 'selector' : selc, 'root_id' : root_id})
    df.to_csv('db_crawler_attributes.csv', index=False)

    sql = " SELECT * FROM MAP_CATEGORY;"
    cursor.execute(sql)
    results = cursor.fetchall()
    sitename = []
    cate_origin = []
    cate_new = []
    for row in results:
        sitename.append(row[0])
        cate_origin.append(row[1])
        cate_new.append(row[2])

    df = pd.DataFrame({'link_site' :  sitename, 'categoryOrigin' : cate_origin, 'categoryNew' : cate_new})
    df.to_csv('db_crawler_map_category.csv', index=False)
    

def export_db_news_sites():
    cursor, db = createConnection(db_name='news_crawler')
    id = []
    siteName = []
    siteLink = []
    article_link = []
    page_param = []
    page_param_rule = []
    sql = "SELECT id, SiteName, SiteLink, ArticleLinkSelector, PageParam, PageParam_rule FROM news_site_sites;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        id.append(row[0])
        siteName.append(row[1])
        siteLink.append(row[2])
        article_link.append(row[3])
        page_param.append(row[4])
        page_param_rule.append(row[5])

    df = pd.DataFrame({'id' :  id, 'siteName' : siteName, 'siteLink' : siteLink, 'page_param' : page_param, 'article_link' : article_link, 'page_param_rule' : page_param_rule})
    df.to_csv('db_news_crawler_site.csv', index=False)

    sql = "SELECT  id, root_site_name, FieldName, Selectors FROM news_site_siteattributes;"
    cursor.execute(sql)
    results = cursor.fetchall()
    id = []
    root_site_name = []
    fieldName = []
    selector = []
    for row in results:
        id.append(row[0])
        root_site_name.append(row[1])
        fieldName.append(row[2])
        selector.append(row[3])

    df = pd.DataFrame({'id' :  id, 'root_site_name' : root_site_name, 'fieldName' : fieldName, 'selector' : selector})
    df.to_csv('db_news_crawler_attribute.csv', index=False)


export_db_news_sites()

#export_db_crawler()
def update_mapCategory():
    cursor, db = createConnection()
    business = [
        {"nameCate" : "Tech", "link" : "https://www.businessinsider.com/sai"},
        {"nameCate" : "Finance", "link" : "https://www.businessinsider.com/clusterstock"},
        {"nameCate" : "Strategy", "link" : "https://www.businessinsider.com/warroom"},
        {"nameCate" : "Retail", "link" : "https://www.businessinsider.com/retail"},
        {"nameCate" : "Advertising", "link" : "https://www.businessinsider.com/advertising"},
        {"nameCate" : "HealthCare", "link" : "https://www.businessinsider.com/healthcare"}	
    ]

    life = [
        {"nameCate" : "Entertainment", "link" : "https://www.insider.com/entertainment"},
        {"nameCate" : "Culture", "link" : "https://www.insider.com/culture"},
        {"nameCate" : "Travel", "link" : "https://www.insider.com/travel"},
        {"nameCate" : "Food", "link" : "https://www.insider.com/food"},
        {"nameCate" : "Health", "link" : "https://www.insider.com/health"},
        {"nameCate" : "Parenting", "link" : "https://www.insider.com/parenting"},
        {"nameCate" : "Beauty", "link" : "https://www.insider.com/beauty"},
        {"nameCate" : "Style", "link" : "https://www.insider.com/style"},
        {"nameCate" : "Womens-clothing", "link" : "https://www.businessinsider.com/reviews/style/womens-clothing"},
        {"nameCate" : "Womens-shoes", "link" : "https://www.businessinsider.com/reviews/style/womens-shoes"},
        {"nameCate" : "Handbags-accessories", "link" : "https://www.businessinsider.com/reviews/style/handbags-accessories"},
        {"nameCate" : "Mens-clothing", "link" : "https://www.businessinsider.com/reviews/style/mens-clothing"},
        {"nameCate" : "Men-shoes", "link" : "https://www.businessinsider.com/reviews/style/mens-shoes"},
        {"nameCate" : "Men-accessories", "link" : "https://www.businessinsider.com/reviews/style/mens-accessories"},
        {"nameCate" : "Matress", "link" : "https://www.businessinsider.com/reviews/home/mattress"},
        {"nameCate" : "Bedroom", "link" : "https://www.businessinsider.com/reviews/home/bedroom"},
        {"nameCate" : "Bathroom", "link" : "https://www.businessinsider.com/reviews/home/bathroom"},
        {"nameCate" : "Cleaning", "link" : "https://www.businessinsider.com/reviews/home/cleaning"},
        {"nameCate" : "Closet-laundry", "link" : "https://www.businessinsider.com/reviews/home/closet-laundry"},
        {"nameCate" : "Garage", "link" : "https://www.businessinsider.com/reviews/home/garage"},
        {"nameCate" : "Entertaining", "link" : "https://www.businessinsider.com/reviews/home/entertaining"},
        {"nameCate" : "Furniture", "link" : "https://www.businessinsider.com/reviews/home/furniture"},
        {"nameCate" : "Home-decor", "link" : "https://www.businessinsider.com/reviews/home/home-decor"},
        {"nameCate" : "Holiday-decor", "link" : "https://www.businessinsider.com/reviews/home/holiday-decor"},
        {"nameCate" : "Gardening", "link" : "https://www.businessinsider.com/reviews/home/gardenin"},
        {"nameCate" : "Office", "link" : "https://www.businessinsider.com/reviews/home/office"},
        {"nameCate" : "Safety", "link" : "https://www.businessinsider.com/reviews/home/safety"},
        {"nameCate" : "Smart-home", "link" : "https://www.businessinsider.com/reviews/home/smart-home"},
        {"nameCate" : "Storage", "link" : "https://www.businessinsider.com/reviews/home/storage"},
        {"nameCate" : "Tools", "link" : "https://www.businessinsider.com/reviews/home/tools"},
        {"nameCate" : "Appliances", "link" : "https://www.businessinsider.com/reviews/kitchen/appliances"},
        {"nameCate" : "Barking", "link" : "https://www.businessinsider.com/reviews/kitchen/baking"},
        {"nameCate" : "Coffee-tea", "link" : "https://www.businessinsider.com/reviews/kitchen/coffee-tea"},
        {"nameCate" : "Cookware", "link" : "https://www.businessinsider.com/reviews/kitchen/cookware"},
        {"nameCate" : "Dining-entertaining", "link" : "https://www.businessinsider.com/reviews/kitchen/dining-entertaining"},
        {"nameCate" : "Food-drink", "link" : "https://www.businessinsider.com/reviews/kitchen/food-drink"},
        {"nameCate" : "Storage", "link" : "https://www.businessinsider.com/reviews/kitchen/storage"},
        {"nameCate" : "Tools", "link" : "https://www.businessinsider.com/reviews/kitchen/tools"},
        {"nameCate" : "Wine-bar", "link" : "https://www.businessinsider.com/reviews/kitchen/wine-bar"},
        {"nameCate" : "Skin-care", "link" : "https://www.businessinsider.com/reviews/beauty/skin-care"},
        {"nameCate" : "Hair-care", "link" : "https://www.businessinsider.com/reviews/beauty/hair-care"},
        {"nameCate" : "Makeup", "link" : "https://www.businessinsider.com/reviews/beauty/makeup"},
        {"nameCate" : "Bath-body", "link" : "https://www.businessinsider.com/reviews/beauty/bath-body"},
        {"nameCate" : "Shaving-grooming", "link" : "https://www.businessinsider.com/reviews/beauty/shaving-grooming"},
        {"nameCate" : "Teeth", "link" : "https://www.businessinsider.com/reviews/beauty/teeth"},
        {"nameCate" : "Fragrance", "link" : "https://www.businessinsider.com/reviews/beauty/fragrance"},
        {"nameCate" : "Hotels", "link" : "https://www.businessinsider.com/reviews/travel/hotels"},
        {"nameCate" : "Flights", "link" : "https://www.businessinsider.com/reviews/travel/flights"},
        {"nameCate" : "Experiences", "link" : "https://www.businessinsider.com/reviews/travel/experiences"},
        {"nameCate" : "Destinations", "link" : "https://www.businessinsider.com/reviews/travel/destinations"},
        {"nameCate" : "Luggage-travel-gear", "link" : "https://www.businessinsider.com/reviews/travel/luggage-travel-gear"},
        {"nameCate" : "Rewards", "link" : "https://www.businessinsider.com/reviews/travel/rewards"},
        {"nameCate" : "Transportation", "link" : "https://www.businessinsider.com/reviews/travel/transportation"},
        {"nameCate" : "Men", "link" : "https://www.businessinsider.com/reviews/gifts/men"},
        {"nameCate" : "Women", "link" : "https://www.businessinsider.com/reviews/gifts/women"},
        {"nameCate" : "Baby", "link" : "https://www.businessinsider.com/reviews/gifts/baby"},
        {"nameCate" : "Kids", "link" : "https://www.businessinsider.com/reviews/gifts/kids"},
        {"nameCate" : "Teens", "link" : "https://www.businessinsider.com/reviews/gifts/teens"},
        {"nameCate" : "Everyone", "link" : "https://www.businessinsider.com/reviews/gifts/everyone"},
        {"nameCate" : "Christmas", "link" : "https://www.businessinsider.com/reviews/gifts/christmas"},
        {"nameCate" : "Valentines-day", "link" : "https://www.businessinsider.com/reviews/gifts/valentines-day"},
        {"nameCate" : "Mothers-day", "link" : "https://www.businessinsider.com/reviews/gifts/mothers-day"},
        {"nameCate" : "Fathers-day", "link" : "https://www.businessinsider.com/reviews/gifts/fathers-day"},
        {"nameCate" : "Black-friday", "link" : "https://www.businessinsider.com/reviews/deals/black-friday"},
        {"nameCate" : "Cyber-monday", "link" : "https://www.businessinsider.com/reviews/deals/cyber-monday"}
    ]   

    polictic = [
	    {"nameCate" : "Politics", "link" : "https://www.insider.com/politics"},
	    {"nameCate" : "Defense", "link" : "https://www.businessinsider.com/defense"}
    ]

    opinion = [
	    {"nameCate" : "Opinion", "link" : "https://www.insider.com/opinion"}
    ]

    sport = [
	    {"nameCate" : "Sports", "link" : "https://www.insider.com/sports"}
    ]

    technogoly  = [
        {"nameCate" : "Audio", "link" : "https://www.businessinsider.com/reviews/electronics/audio"},
        {"nameCate" : "Tech-Accessories", "link" : "https://www.businessinsider.com/reviews/electronics/tech-accessories"},
        {"nameCate" : "Batteries-Charging", "link" : "https://www.businessinsider.com/reviews/electronics/batteries-charging"},
        {"nameCate" : "Cameras", "link" : "https://www.businessinsider.com/reviews/electronics/cameras"},
        {"nameCate" : "Computers", "link" : "https://www.businessinsider.com/reviews/electronics/computers"},
        {"nameCate" : "Gaming", "link" : "https://www.businessinsider.com/reviews/electronics/gaming"},
        {"nameCate" : "Fitness", "link" : "https://www.businessinsider.com/reviews/electronics/fitness"},
        {"nameCate" : "Headphones", "link" : "https://www.businessinsider.com/reviews/electronics/headphones"},
        {"nameCate" : "Home-theater", "link" : "https://www.businessinsider.com/reviews/electronics/home-theater"},
        {"nameCate" : "Laptops", "link" : "https://www.businessinsider.com/reviews/electronics/laptops"},
        {"nameCate" : "Printers-scanners", "link" : "https://www.businessinsider.com/reviews/electronics/printers-scanners"},
        {"nameCate" : "Smart-home", "link" : "https://www.businessinsider.com/reviews/electronics/smart-home"},
        {"nameCate" : "Smartphones", "link" : "https://www.businessinsider.com/reviews/electronics/smartphones"},
        {"nameCate" : "Storage", "link" : "https://www.businessinsider.com/reviews/electronics/storage"},
        {"nameCate" : "Tablets", "link" : "https://www.businessinsider.com/reviews/electronics/tablets"},
        {"nameCate" : "TV", "link" : "https://www.businessinsider.com/reviews/electronics/tvs"}
    ]

    d_category = {
        'business' : business,
        'politic' : polictic,
        'technology' : technogoly,
        'life' : life,
        'sports' : sport,
        'opinion' : opinion
    }
    count = 1
    for key in d_category:
        for site in d_category[key]:
            try:
                cursor, db = createConnection()
                cursor.execute("insert into MAP_CATEGORY values(%s,%s,%s)",(
                    site['link'],
                    site['nameCate'],
                    key
                ))
                print(count, end = ' - ')
                db.commit()
                cursor.close()
                db.close()
                count += 1
            except Exception as e:
                cursor.close()
                db.close()
                print(e)

#update_mapCategory()



#select_attr(1)
#select_site(db_name='news_crawler')

# DROP DATABASE domain1;
# DROP DATABASE domain2;
# DROP DATABASE crawler;

# USE crawler_1;DELETE FROM DB1_SITE_DATA WHERE True;DELETE FROM DB1_DATA WHERE True;DELETE FROM DB1_SITEATTRIBUTE WHERE True;DELETE FROM DB1_LOG_DETAIL WHERE True;DELETE FROM DB1_LOG WHERE True;DELETE FROM DB1_READYCRAWLED WHERE True;DELETE FROM DB1_DOWNLOADWARNING WHERE True;DELETE FROM DB1_SITE WHERE True;DELETE FROM DB1_SITECLUSTER WHERE True;DELETE FROM DB1_SITEMASTER WHERE True;
# USE domain1;DELETE FROM DB2_DOC_CATEGORY WHERE TRUE;DELETE FROM DB2_DOCUMENT WHERE TRUE;DELETE FROM DB2_CATEGORY WHERE TRUE;DELETE FROM DB2_ERRORLINK WHERE TRUE;
# USE domain2;DELETE FROM DB3_DOC_CATEGORY WHERE TRUE;DELETE FROM DB3_DOCUMENT WHERE TRUE;DELETE FROM DB3_CATEGORY WHERE TRUE;DELETE FROM DB3_ERRORLINK WHERE TRUE;
#cursor.execute("DELETE FROM DB2_DOC_CATEGORY WHERE True")
#cursor.execute("DELETE FROM DB2_DOCUMENT WHERE True")
# cursor.execute("DELETE FROM DB1_SITE_DATA WHERE True;")
# cursor.execute("DELETE FROM DB1_DATA WHERE True;")
# cursor.execute("DELETE FROM DB1_SITEATTRIBUTE WHERE True;")
# cursor.execute("DELETE FROM DB1_LOG_DETAIL WHERE True;")
# cursor.execute("DELETE FROM DB1_LOG WHERE True;")
# cursor.execute("DELETE FROM DB1_READYCRAWLED WHERE True;")
# cursor.execute("DELETE FROM DB1_DOWNLOADWARNING WHERE True;")
# cursor.execute("DELETE FROM DB1_SITE WHERE True;")
# cursor.execute("DELETE FROM DB1_SITECLUSTER WHERE True;")
# cursor.execute("DELETE FROM DB1_SITEMASTER WHERE True;")

# db.close()
# SHOW max_connections;
# SELECT * FROM pg_stat_activity;
#این برنامه داده های یک پایگاه داده را که از قبل 
#اطلاعات و قیمت مربوط به پر بازدید ترین لپ تاپ های 5 صفحه اول
#سایت دیجی کالا را روی آن ذخیره کرده ایم میگیرد و 
#با استفاده از یادگیری ماشین از طریق کاربر قیمتی
#را بر حسب تومان میگیرد و مشخصات لپ تاپی متناسب با 
#قیمت داده شده را نمایش می دهد 
from bs4 import BeautifulSoup
import mysql.connector
from sklearn import tree
from sklearn import preprocessing

cnx = mysql.connector.connect(user='*****', password='*****',
                              host='localhost',
                              database='laptops')
cursor = cnx.cursor()

cursor.execute("SELECT * FROM laptops_table")

result = cursor.fetchall()
brands = []
models = []
sizes = []
cpus = []
rams = []
gpus = []

#داده را به صورت ستونی ذخیره می کند
for record in result:
    brands.append(record[0])    
    models.append(record[1])
    sizes.append(record[2])
    cpus.append(record[3])
    rams.append(record[4])
    gpus.append(record[5])

#و سپس داده هایی را که ستونی ذخیره کرده بود
#کد گزاری می کند و آن ها ذخیره می کند
le_brands = preprocessing.LabelEncoder()
le_brands.fit(brands)
fit_brands = list(le_brands.classes_)
encode_brands = le_brands.transform(fit_brands)
decode_brands = list(le_brands.inverse_transform(tuple(encode_brands)))

le_models = preprocessing.LabelEncoder()
le_models.fit(models)
fit_models = list(le_models.classes_)
encode_models = le_models.transform(fit_models)
decode_models = list(le_models.inverse_transform(tuple(encode_models)))

le_sizes = preprocessing.LabelEncoder()
le_sizes.fit(sizes)
fit_sizes = list(le_sizes.classes_)
encode_sizes = le_sizes.transform(fit_sizes)
decode_sizes = list(le_sizes.inverse_transform(tuple(encode_sizes)))

le_cpus = preprocessing.LabelEncoder()
le_cpus.fit(cpus)
fit_cpus = list(le_cpus.classes_)
encode_cpus = le_cpus.transform(fit_cpus)
decode_cpus = list(le_cpus.inverse_transform(tuple(encode_cpus)))

le_rams = preprocessing.LabelEncoder()
le_rams.fit(rams)
fit_rams = list(le_rams.classes_)
encode_rams = le_rams.transform(fit_rams)
decode_rams = list(le_rams.inverse_transform(tuple(encode_rams)))

le_gpus = preprocessing.LabelEncoder()
le_gpus.fit(gpus)
fit_gpus = list(le_gpus.classes_)
encode_gpus = le_gpus.transform(fit_gpus)
decode_gpus = list(le_gpus.inverse_transform(tuple(encode_gpus)))

# print(encode_brands, encode_models, encode_sizes, encode_cpus, encode_rams, encode_gpus)
# print(decode_rams)

ltp_codes = list()

x = []
y = []
for row in result:
    # if row[0] in decode_brands and row[1] in decode_models and row[2] in decode_sizes and row[3] in decode_cpus and row[4] in decode_rams and row[5] in decode_gpus:
        #print(le_brands.transform([row[0]]), le_models.transform([row[1]]), le_sizes.transform([row[2]]), le_cpus.transform([row[3]]),le_rams.transform([row[4]]), le_gpus.transform([row[5]]))
    #بار دیگه در اینجا داده ها را می خواند
    #و دوباره آن ها را کد گزاری می کند
    ltps_tuple = tuple()
    ltps_tuple = (
                str(le_brands.transform([row[0]])[0]), 
                str(le_models.transform([row[1]])[0]),
                str(le_sizes.transform([row[2]])[0]),
                str(le_cpus.transform([row[3]])[0]),
                str(le_rams.transform([row[4]])[0]), 
                str(le_gpus.transform([row[5]])[0])
                 )
    ltp_codes.append(ltps_tuple)
    # else:
    #     print('No')

for case in result:
    x.append([case[6]])
for code in ltp_codes:
    y.append(code)


#داده ها برای مقایسه و فیت کردن در
#اختیار ماشین لرنینگ قرار می دهد
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)                             
new_data = [[int(input("Enter A Price Whit Toman (Example: 14300000): "))]]     #قیمت را از کاربر میگیرد
answer = clf.predict(new_data)
# print(answer)
nahaei = list(answer[0])
res = tuple()
res = (
        le_brands.inverse_transform([int(nahaei[0])])[0],
        le_models.inverse_transform([int(nahaei[1])])[0], 
        le_sizes.inverse_transform([int(nahaei[2])])[0],
        le_cpus.inverse_transform([int(nahaei[3])])[0], 
        le_rams.inverse_transform([int(nahaei[4])])[0], 
        le_gpus.inverse_transform([int(nahaei[5])])[0]
      )

# print(le_brands.inverse_transform([int(nahaei[0])]),
#         le_models.inverse_transform([int(nahaei[1])]),
#         le_sizes.inverse_transform([int(nahaei[2])]),
#         le_cpus.inverse_transform([int(nahaei[3])]),
#         le_rams.inverse_transform([int(nahaei[4])]),
#         le_gpus.inverse_transform([int(nahaei[5])]))

print('Brand: %s\nModel: %s\nScreen Size: %s\nCpu: %s\nRam: %s\nGpu: %s' %
      (res[0], res[1], res[2], res[3], res[4], res[5]))


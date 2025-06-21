from flask import Flask
from flask import jsonify, request
from flask_cors import CORS
import json  
import time  

"""
2025/06 自动营销演示
一行airtable 记录的生成，共4步骤


try:
    # 可能出错的代码
    result = 10 / 0
except Exception as e:
    # 打印错误信息
    print(f"发生错误: {e}")
    # 打印完整的错误堆栈
    import traceback
    traceback.print_exc() 

"""
app = Flask(__name__)

# r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
CORS(app, resources=r"/*")


import requests
import json

# 替换以下变量为实际的值
baseId = "appwcZdiU9CwICb9x"
tableIdOrName = "Lead_Enrichment"
recordId = "recYKMtbcWxLYpLKA"
api_token = "patSNai41M2pmpTLv.2182deccd9787acb57ca0e025f78bb2435920dc29bc9104cfa81b056ece51fbb"
 
proxies = {"https": "127.0.0.1:15236"}
url = f"https://api.airtable.com/v0/{baseId}/{tableIdOrName}/{recordId}"
tableUrl = f"https://api.airtable.com/v0/{baseId}/{tableIdOrName}"
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}
 

@app.route("/")
def home():
    return "hello，app project!"


@app.route("/getCompany", methods=["GET", "POST"])
def update_airtable_Company():

    data = {
    "fields": {
         "公司名称": "Adwards101 Drapery Systems",
         "公司网站": "https://www.adwardsrapery.com",
    }
}

    response = requests.patch(url, headers=headers, data=json.dumps(data),proxies=proxies)

    # Update a record 
    print("Updating company columns...")
 

    # if updated_record: 
    if response.status_code == 200:
        print("Company updated successfully!") 
        # print(f"Updated fields: {updated_record['fields']}")

    else:

        print("Failed to update company")
    return ("POST")

@app.route("/getManager", methods=["GET", "POST"])
def update_airtable_Manager():
 

    # Update a record 
    print("Updating manager columns...")

    updated_fields = {
        "采购主管姓名": "Josh Sweptian",
        "采购主管邮箱": "josh.sweptian@awardrapery.com",
        "联系电话": "1-347-4466758",
        "LinkedIn URL": "https://www.linkedin.com/in/joshsweptian/",
        "CEO姓名": "David Savyrah",
        "CEO邮箱": "david.Savyrah@awardrapery.com",
        "采购主管个人资料": "Sales for Adward Drapery Systems, Inc. A commercial Window Treatment company specializing in medical and commercial spaces. From Draperies in hotel rooms or high end board/conference rooms to Cubicle Curtains and Track for hospitals and clinics, we have over 40 years of experiences servicing our customers. We also have solutions for covering windows using mini blinds, vertical blinds, honeycomb shades and roller shades. We also have blackout options. Great for photo labs or any place you would need complete light tight conditions."
    }

    data = {
        "fields": updated_fields
    }

    response = requests.patch(url, headers=headers, data=json.dumps(data),proxies=proxies)
 
    if response.status_code == 200:
        print("Manager updated successfully!")   
    else:

        print("Failed to update manager")

    return ("POST")

@app.route("/researchCompany", methods=["GET", "POST"])
def update_airtable_profile():
 
    # Update a record 
    print("Updating manager columns...")

    updated_fields = {
        "国家": "美国",
        "员工数量": "300-500",
        "行业": "Home Decor", 
        "年营业额": "$128,747,000",
        "公司介绍": "Adward Drapery Systems is the Midwest’s premier provider of high-quality commercial blinds tailored to institutions. With a steadfast commitment to excellence, we specialize in delivering top-tier curtain and blind installation services that cater to the unique needs of educational, governmental, and corporate institutions. Backed by years of experience, our skilled team ensures flawless installations that combine functionality and aesthetics seamlessly. Elevate your institution’s environment with our superior commercial blinds that not only enhance privacy and light control but also add a touch of sophistication to every space.Design: Our experts provide solutions combining style, form and function. Let us improve your environment with our expert knowledge, quality products and superior service.Fabricate:With decades of experience to call upon, we will fabricate and provide our commercial curtain products for any business, from the biggest corporations and small & large hospitals to medical facilities and restaurants on the corner.",
        "业态":"Importer/distributor",
        "ICP匹配度指数":0.75,   # 如果78%，则返回status=422，但不报错！
    }

    data = {
        "fields": updated_fields
    }
    try:
         response = requests.patch(url, headers=headers, data=json.dumps(data),proxies=proxies) 
         if response.status_code == 200: 
            print("Profile updated successfully!")   
         else: 
            print("Failed to update profile ",response.status_code)
    except Exception as e: 
        print(f"发生错误: {e}") 

    return ("POST")

@app.route("/clearTable", methods=["GET"])
def clear_airtable(): 
    # 首先获取所有记录
    response = requests.get(tableUrl, headers=headers,proxies=proxies)
    # print("response: ", response.json())
    records = response.json().get('records', [])
    # print("records: ",records)

    # 为每条记录创建更新请求，清空所有字段
    for record in records:
        record_id = record['id']
        # fields = {key: None for key in record['fields'].keys()}
        fields = {key: None for key in record['fields'].keys() if key != "RECORD_ID"}

        update_data = {
            'fields': fields
        }
        # print(update_data)
        update_url = f'{tableUrl}/{record_id}'
        requests.patch(update_url, headers=headers, json=update_data,proxies=proxies) 
        time.sleep(0.2)  # 放慢速度，embeded table 才能够实时响应 
     
    print("已经清空表格了！")
    return ("POST")


@app.route("/writeEmail", methods=["GET", "POST"])
def update_airtable_email():

    # Update a record 
    print("Updating email column...")

    updated_fields = {
        "个性化邮件": "Sales for Adward Drapery Systems, Inc. A commercial Window Treatment company specializing in medical and commercial spaces. From Draperies in hotel rooms or high end board/conference rooms to Cubicle Curtains and Track for hospitals and clinics, we have over 40 years of experiences servicing our customers. We also have solutions for covering windows using mini blinds, vertical blinds, honeycomb shades and roller shades. We also have blackout options. Great for photo labs or any place you would need complete light tight conditions.", 
    }

    data = {
        "fields": updated_fields
    }

    response = requests.patch(url, headers=headers, data=json.dumps(data),proxies=proxies)

    if response.status_code == 200:
        print("Profile updated successfully!")  
    else:
        print("Failed to update email")
    return ("POST")
 

if __name__ == "__main__":
    app.run(debug=True)

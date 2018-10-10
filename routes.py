from flask import Flask, render_template, request
from forms import search_form
import requests
from bs4 import BeautifulSoup
import lxml.html
from fake_useragent import UserAgent

app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

@app.route("/home", methods=["GET", "POST"])
def search():

  form = search_form()

  if request.method == "POST":
    if form.validate() == False:
      return render_template("home.html", form=form)
    else:
      appurl = form.url.data

      try:
            # getting the application page via the url
            ua = UserAgent()
            headers = {"User-Agent":ua.random}
            page = requests.get(appurl, headers=headers, timeout=15, verify=False)

            # getting the html code to be parsed using Soup
            html = page.text
            soup = BeautifulSoup(html,features="html.parser")

            # retrieving app info using xpath  
            root = lxml.html.fromstring(page.content)
            app_name = root.xpath('//*[@id="mas-title"]/div/span/text()')[0]
            app_version = root.xpath('.//*[@id="masTechnicalDetails-btf"]/div[2]/span[2]/text()')[0]
            app_changelog = root.xpath('//*[@id="mas-latest-updates"]/ul/li/span/text()')[0]

            # retrieving release date info using soup
            info_table = soup.find('table',id='productDetailsTable')
            row = info_table.findAll("li")
            app_original_release_date=row[1].getText().strip(row[1].find("b").getText())

            # print(app_name)
            # print(app_version)
            # print(app_changelog)
            # print(app_original_release_date)


            return render_template("display_search_results.html",name = app_name, version=app_version, changelog=app_changelog, release_date=app_original_release_date )
      except Exception as e :
            print(e)
            return render_template('display_search_results.html',error=e)
            

  elif request.method == 'GET':
    return render_template('home.html', form=form)



if __name__ == "__main__":
  app.run(debug=True)
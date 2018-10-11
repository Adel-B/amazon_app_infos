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

      # getting the application page via the url
      ua = UserAgent()
      headers = {"User-Agent":ua.random}
      try:
        page = requests.get(appurl, headers=headers, timeout=15, verify=False)
      except requests.exceptions.HTTPError as errh:
        return render_template('display_search_results.html',error="Http Error: "+errh)
      except requests.exceptions.ConnectionError as errc:
        return render_template('display_search_results.html',error="Connection Error :"+errc)
      except requests.exceptions.Timeout as errt:
        return render_template('display_search_results.html',error="Timeout Error :"+errt)
      except requests.exceptions.RequestException as err:
        return render_template('display_search_results.html',error="OOps: ERROR :"+err)

      # getting the html code to be parsed using Soup
      html = page.text
      soup = BeautifulSoup(html,features="html.parser")

      # retrieving app info using xpath  
      try:
        root = lxml.html.fromstring(page.content)
        app_name = root.xpath('//*[@id="mas-title"]/div/span/text()')[0]
        app_version = root.xpath('.//*[@id="masTechnicalDetails-btf"]/div[2]/span[2]/text()')[0]
        app_changelog = root.xpath('//*[@id="mas-latest-updates"]/ul/li/span/text()')[0]
      except (IndexError, ValueError):
        err_msg= "No App info is found. please try with a different URL. Example: https://www.amazon.com/Instagram/dp/B00KZP2DTQ"
        return render_template('display_search_results.html',error=err_msg)

      # retrieving release date info using soup
      try:
        info_table = soup.find('table',id='productDetailsTable')
        row = info_table.findAll("li")
        app_original_release_date=row[1].getText().strip(row[1].find("b").getText())
      except Exception as e :
        err_msg= "No App info is found. please try with a different URL. Example: https://www.amazon.com/Instagram/dp/B00KZP2DTQ"
        return render_template('display_search_results.html',error=err_msg)


      return render_template("display_search_results.html",name = app_name, version=app_version, changelog=app_changelog, release_date=app_original_release_date )          

  elif request.method == 'GET':
    return render_template('home.html', form=form)



if __name__ == "__main__":
  app.run(debug=True)
from flask import Flask, render_template, request, redirect, send_file
from extractor import scrape_job
from file import save_to_file


app = Flask("JobScrapper")

db = {}  # memory db for caching

# @: decorator (syntactic sugar)
@app.route("/")  # 사용자가 해당 경로로 접근하면 특정 함수를 실행하도록 할 것
def home():
    return render_template("home.html", name="nico")


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    
    if keyword == None:
        return redirect("/")

    if keyword in db:
        jobs = db[keyword]
    else:
        jobs = scrape_job(keyword)
        db[keyword] = jobs

    return render_template("search.html", keyword=keyword, jobs=jobs)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    
    if keyword == None:
        return redirect("/")

    if keyword not in db: 
        return redirect(f"/search?keyword={keyword}")

    save_to_file(keyword, db[keyword])

    return send_file(f"{keyword}.csv", as_attachment=True) # as_attachment=True: 다운로드용

app.run()

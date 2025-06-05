from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form.to_dict(flat=False)
        # Extract repeated fields as lists
        education = []
        experiences = []
        projects = []

        # Helper to collect repeated fields
        def collect(prefix):
            # Collect items by looking for keys with prefix and indexes
            items = []
            i = 0
            while True:
                key_base = f"{prefix}[{i}]"
                keys = [k for k in data.keys() if k.startswith(key_base)]
                if not keys:
                    break
                item = {}
                for k in keys:
                    # k example: education[0][degree]
                    field = k[len(key_base)+1:-1]  # get 'degree' from k
                    item[field] = data[k][0]
                items.append(item)
                i += 1
            return items

        # Collect education entries
        i = 0
        while True:
            degree = request.form.get(f"education[{i}][degree]")
            if not degree:
                break
            education.append({
                "degree": degree,
                "institution": request.form.get(f"education[{i}][institution]"),
                "year": request.form.get(f"education[{i}][year]")
            })
            i += 1

        # Collect experiences
        i = 0
        while True:
            title = request.form.get(f"experience[{i}][title]")
            if not title:
                break
            experiences.append({
                "title": title,
                "company": request.form.get(f"experience[{i}][company]"),
                "duration": request.form.get(f"experience[{i}][duration]"),
                "description": request.form.get(f"experience[{i}][description]")
            })
            i += 1

        # Collect projects
        i = 0
        while True:
            name = request.form.get(f"project[{i}][name]")
            if not name:
                break
            projects.append({
                "name": name,
                "link": request.form.get(f"project[{i}][link]"),
                "description": request.form.get(f"project[{i}][description]")
            })
            i += 1

        # Basic personal info and skills
        personal = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "summary": request.form.get("summary")
        }
        skills = request.form.get("skills")

        return render_template("resume.html",
                               personal=personal,
                               education=education,
                               experiences=experiences,
                               projects=projects,
                               skills=skills.split(",") if skills else [])
    else:
        return render_template("index.html")
        

if __name__ == "__main__":
    app.run(debug=True)

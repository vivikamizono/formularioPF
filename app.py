from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@localhost/formulario"
db = SQLAlchemy(app)

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    rg = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(20), nullable=False)
    cargo_publico = db.Column(db.String(50), nullable=False)
    endereco_rua = db.Column(db.String(100), nullable=False)
    endereco_cep = db.Column(db.String(20), nullable=False)

@app.route("/")
def index():
    funcionarios = Funcionario.query.all()
    return render_template("index.html", funcionarios=funcionarios)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        funcionario = Funcionario(
            nome_completo=request.form["nome_completo"],
            rg=request.form["rg"],
            cpf=request.form["cpf"],
            cargo_publico=request.form["cargo_publico"],
            endereco_rua=request.form["endereco_rua"],
            endereco_cep=request.form["endereco_cep"]
        )
        db.session.add(funcionario)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("create.html")

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    funcionario = Funcionario.query.get(id)
    if request.method == "POST":
        funcionario.nome_completo = request.form["nome_completo"]
        funcionario.rg = request.form["rg"]
        funcionario.cpf = request.form["cpf"]
        funcionario.cargo_publico = request.form["cargo_publico"]
        funcionario.endereco_rua = request.form["endereco_rua"]
        funcionario.endereco_cep = request.form["endereco_cep"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("update.html", funcionario=funcionario)

@app.route("/delete/<int:id>")
def delete(id):
    funcionario = Funcionario.query.get(id)
    db.session.delete(funcionario)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aluno.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Aluno(db.Model):
    __tablename__='alunos'

    _cpf = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    data_nasc = db.Column(db.String(10))
    sexo = db.Column(db.String(9))
    idade = db.Column(db.String(10))
    av1 = db.Column(db.String(5))
    av2 = db.Column(db.String(5))
    media = db.Column(db.String(5))

    def __init__(self, _cpf, nome, data_nasc, sexo, idade, av1, av2, media):
        self._cpf=_cpf
        self.nome = nome
        self.data_nasc=data_nasc
        self.sexo=sexo
        self.idade=idade
        self.av1=av1
        self.av2=av2
        self.media=media
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        _cpf = request.form.get("cpf")
        nome = request.form.get("nome")
        data_nasc = request.form.get("data_nasc")
        sexo = request.form.get("nome")
        idade = request.form.get("nome")
        av1 = request.form.get("nome")
        av2 = request.form.get("nome")
        media = request.form.get("email")

        if (_cpf and nome and data_nasc and sexo and idade and av1 and av2 and media ):
            f = Aluno(_cpf, nome, data_nasc, sexo, idade, av1, av2, media)
            db.session.add(f)
            db.session.commit()

    return redirect(url_for("index"))

@app.route("/lista")
def lista():
    alunos = Aluno.query.all()
    return render_template("lista.html", alunos=alunos)

@app.route("/excluir/<int:id>")
def excluir(cpf):
    aluno = Aluno.query.filter_by(_cpf=cpf).first()

    db.session.delete(aluno)
    db.session.commit()

    alunos = Aluno.query.all()

    return render_template("lista.html", alunos=alunos)

@app.route("/atualizar/<int:cpf>", methods=['GET', 'POST'])
def atualizar(cpf):
    aluno = Aluno.query.filter_by(_cpf=cpf).first()

    if request.method == 'POST':
        _cpf = request.form.get("cpf")
        nome = request.form.get("nome")
        data_nasc = request.form.get("data_nasc")
        sexo = request.form.get("sexo")
        idade = request.form.get("idade")
        av1 = request.form.get("av1")
        av2 = request.form.get("av2")
        media = request.form.get("media")
        nome = request.form.get("nome")

        if (_cpf and nome and data_nasc and sexo and idade and av1 and av2 and media ):
            aluno._cpf = cpf
            aluno.nome = nome
            aluno.data_nasc = data_nasc
            aluno.sexo = sexo
            aluno.idade = idade
            aluno.av1 = av1
            aluno.av2 = av2
            aluno.media = media

            db.session.commit()

            return redirect(url_for("lista"))

    return render_template("atualizar.html", aluno=aluno)


if __name__ == "__main__":
    app.run(debug=True)
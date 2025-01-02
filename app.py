from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Assurez-vous que le dossier instance existe
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

# Configuration avec chemin absolu
db_path = os.path.join(instance_path, 'tickets.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    vendu = db.Column(db.Boolean, default=False)
    date_achat = db.Column(db.DateTime, nullable=True)

def init_db():
    with app.app_context():
        db.create_all()
        # Vérifier si la base de données est vide
        if not Ticket.query.first():
            ticket_default = Ticket(type='Ticket', price=300.0, vendu=False)
            db.session.add(ticket_default)
            db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tickets')
def get_tickets():
    tickets = Ticket.query.filter_by(vendu=False).all()
    return jsonify([{
        'id': ticket.id,
        'type': ticket.type,
        'price': ticket.price
    } for ticket in tickets])

@app.route('/api/purchase', methods=['POST'])
def purchase():
    try:
        ticket = Ticket.query.filter_by(vendu=False).first()
        if ticket:
            nouveau_ticket = Ticket(
                type=ticket.type,
                price=ticket.price,
                vendu=True,
                date_achat=datetime.now()
            )
            db.session.add(nouveau_ticket)
            db.session.commit()

            return jsonify({
                'success': True,
                'tickets': [{
                    'id': nouveau_ticket.id
                }],
                'total': ticket.price
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Aucun ticket disponible'
            }), 400
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Erreur lors de la vente du ticket'
        }), 500

@app.route('/statistiques')
def statistiques():
    total_tickets = Ticket.query.filter_by(vendu=True).count()
    total_ventes = db.session.query(db.func.sum(Ticket.price)).filter_by(vendu=True).scalar() or 0
    
    # Statistiques par jour
    from sqlalchemy import func
    ventes_par_jour = db.session.query(
        func.date(Ticket.date_achat).label('date'),
        func.count(Ticket.id).label('tickets'),
        func.sum(Ticket.price).label('total')
    ).filter_by(vendu=True).group_by(func.date(Ticket.date_achat)).all()

    # Formater les dates
    ventes_formatees = []
    for vente in ventes_par_jour:
        if isinstance(vente.date, str):
            date_str = vente.date
        else:
            date_str = vente.date.strftime('%d/%m/%Y') if vente.date else 'N/A'
        ventes_formatees.append({
            'date': date_str,
            'tickets': vente.tickets,
            'total': vente.total
        })

    return render_template('statistiques.html', 
                         total_tickets=total_tickets,
                         total_ventes=total_ventes,
                         ventes_par_jour=ventes_formatees)

# Initialiser la base de données avant de démarrer l'application
init_db()

if __name__ == '__main__':
    print(f"Base de données : {db_path}")
    print("Démarrage du serveur sur http://127.0.0.1:8080")
    app.run(host='127.0.0.1', port=8080, debug=True)

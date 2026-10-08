import os
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Identifiants de connexion à la base, surchargeables via variables d'environnement
# (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME). Par défaut : serveur MySQL local
# (ex: Laragon/XAMPP) avec l'utilisateur root sans mot de passe.
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "financement")

# Connexion à la base pour récupérer les échéances déjà calculées du prêt 3
try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    cursor = conn.cursor()
    query = "SELECT num_echeance, montant FROM echeance WHERE id_pret = 3 ORDER BY num_echeance ASC;"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    mois = [row[0] for row in results]

except mysql.connector.Error as err:
    print(f"Erreur base de données : {err}")
    # Valeurs de secours si la base est inaccessible
    mois = [1, 2, 3, 4, 5]


# Équation différentielle simulée : y' = 1 - y^2
def F(x, y):
    return 1.0 - (y * y)


def recalculer_courbe(y_depart, h_choisi):
    """Recalcule la suite des points par la méthode RK4, pour un y initial et un pas donnés."""
    y_points = [y_depart]
    x = 0.0
    y = y_depart
    for _ in range(len(mois) - 1):
        k1 = h_choisi * F(x, y)
        k2 = h_choisi * F(x + h_choisi / 2.0, y + 0.5 * k1)
        k3 = h_choisi * F(x + h_choisi / 2.0, y + 0.5 * k2)
        k4 = h_choisi * F(x + h_choisi, y + k3)
        y = y + (1.0 / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        x += h_choisi
        y_points.append(y)
    return y_points


# Fenêtre principale et espace réservé aux curseurs
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.3)

# Courbe initiale
y_actuel = recalculer_courbe(0.1, 0.1)
courbe, = ax.plot(mois, y_actuel, marker='o', color='blue', linewidth=2, label='Capital de Réserve')

ax.set_title("Simulateur Interactif : Évolution du Capital de Réserve", fontsize=14, fontweight='bold')
ax.set_xlabel("Temps (Mois / Échéances)", fontsize=12)
ax.set_ylabel("Niveau du Capital (Ratio y)", fontsize=12)
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_xticks(mois)
ax.set_ylim(0, 1.1)
ax.legend()

# Curseur pour le capital initial (y0)
ax_slider_y0 = plt.axes([0.2, 0.15, 0.6, 0.03])
slider_y0 = Slider(ax=ax_slider_y0, label='Capital Initial (y0) ', valmin=0.0, valmax=1.0,
                    valinit=0.1, valfmt='%1.2f', color='deepskyblue')

# Curseur pour le pas de temps (h)
ax_slider_h = plt.axes([0.2, 0.08, 0.6, 0.03])
slider_h = Slider(ax=ax_slider_h, label='Pas de temps (h) ', valmin=0.01, valmax=0.5,
                   valinit=0.1, valfmt='%1.2f', color='tomato')


def update(val):
    nouveaux_points = recalculer_courbe(slider_y0.val, slider_h.val)
    courbe.set_ydata(nouveaux_points)
    fig.canvas.draw_idle()


slider_y0.on_changed(update)
slider_h.on_changed(update)

print("Simulateur multi-paramètres prêt !")
plt.show()

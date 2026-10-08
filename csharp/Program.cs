using System;
using MySql.Data.MySqlClient;

class Program
{
    // La chaîne de connexion peut être surchargée via la variable d'environnement
    // DB_CONNECTION_STRING. Par défaut, elle suppose un serveur MySQL local (ex: Laragon/XAMPP)
    // avec l'utilisateur root sans mot de passe.
    static string connectionString =
        Environment.GetEnvironmentVariable("DB_CONNECTION_STRING")
        ?? "Server=localhost;Database=financement;Uid=root;Pwd=;";

    // Fonction f(x, y) de l'équation différentielle simulée : y' = 1 - y^2
    static double F(double x, double y)
    {
        return 1.0 - (y * y);
    }

    static void Main(string[] args)
    {
        string query = "INSERT INTO echeance (id_pret, num_echeance, date_limite, montant) " +
                       "VALUES (@id_pret, @num_echeance, @date_limite, @montant);";

        double x = 0.0;
        double y = 0.1;
        double h = 0.1;

        using (MySqlConnection conn = new MySqlConnection(connectionString))
        {
            conn.Open();
            using (MySqlCommand cmd = new MySqlCommand(query, conn))
            {
                // Résolution numérique par la méthode de Runge-Kutta 4 (RK4)
                for (int i = 1; i <= 5; i++)
                {
                    double k1 = h * F(x, y);
                    double k2 = h * F(x + h / 2.0, y + 0.5 * k1);
                    double k3 = h * F(x + h / 2.0, y + 0.5 * k2);
                    double k4 = h * F(x + h, y + k3);

                    y = y + (1.0 / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4);
                    x += h;

                    cmd.Parameters.Clear();
                    cmd.Parameters.AddWithValue("@id_pret", 3);
                    cmd.Parameters.AddWithValue("@num_echeance", i);
                    cmd.Parameters.AddWithValue("@montant", y);
                    cmd.Parameters.AddWithValue("@date_limite", DateTime.Now.AddMonths(i));

                    cmd.ExecuteNonQuery();

                    Console.WriteLine($"Étape {i} : x = {x:F1} | y = {y:F7}");
                }
            }
        }

        Console.WriteLine("Simulation enregistrée !");
    }
}

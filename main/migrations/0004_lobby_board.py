# Generated by Django 5.0.6 on 2024-05-18 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_player_buzzered_lobby_buzzered_player_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lobby',
            name='board',
            field=models.JSONField(blank=True, default='{"Categories": [{"name": "Welt der Werbung", "questions": [["\'Da wei\\u00df man, was man hat.\'", "IKEA", 100, false], ["\'Nichts ist unm\\u00f6glich.\'", "Toyota", 200, false], ["\'Geiz ist geil.\'", "Saturn", 300, false], ["\'Wir lieben Lebensmittel.\'", "Edeka", 400, false], ["\'Auf diese Steine k\\u00f6nnen Sie bauen.\'", "Ytong", 500, false]]}, {"name": "Brands", "questions": [["Wann wurde YouTube gegr\\u00fcndet?", "2005", 100, false], ["Welches Unternehmen ist f\\u00fcr die Spielekonsole PlayStation verantwortlich?", "Sony", 200, false], ["Wie hei\\u00dft die Fluggesellschaft mit dem K\\u00fcrzel \'DL\'?", "Delta Air Lines", 300, false], ["Welches Unternehmen hat das Smartphone-Betriebssystem Android entwickelt?", "Google", 400, false], ["Welches Unternehmen hat das Social-Media-Netzwerk Instagram gegr\\u00fcndet?", "Kevin Systrom und Mike Krieger", 500, false]]}, {"name": "Filme und Serien", "questions": [["In welcher Stadt spielt die Serie \'Friends\'?", "New York", 100, false], ["Wie hei\\u00dft die Hauptfigur im Film \'The Matrix\'?", "Neo", 200, false], ["Welche Serie zeigt das Leben einer Werwolf-, Hexen- und Vampirgemeinschaft in Mystic Falls?", "The Vampire Diaries", 300, false], ["Wer f\\u00fchrte Regie bei dem Film \'Schindlers Liste\'?", "Steven Spielberg", 400, false], ["Wer f\\u00fchrte Regie bei dem Film \'Inception\'?", "Christopher Nolan", 500, false]]}, {"name": "Gaming", "questions": [["Was ist die Haupteinheit von In-Game-W\\u00e4hrung in \'The Sims\'?", "Simoleons", 100, false], ["Welches Spiel wurde als \\u201eSchwierigkeitsgrad: unm\\u00f6glich\\u201c bekannt, weil es so herausfordernd ist?", "Dark Souls", 200, false], ["Wie hei\\u00dft das Rollenspiel, das von Bethesda Game Studios entwickelt wurde und in der postapokalyptischen Zukunft spielt?", "Fallout", 300, false], ["Welches Spiel wurde 1998 ver\\u00f6ffentlicht und gilt als ein Pionier des Stealth-Genres?", "Metal Gear Solid", 400, false], ["In welchem Spiel spielt man als ein Hacktivist in einer Stadt mit dem fiktiven Namen DedSec?", "Watch Dogs 2", 500, false]]}, {"name": "Da fragt man sich", "questions": [["Diese Pflanze wird verwendet, um Schokolade herzustellen.", "Was ist der Kakaobaum?", 100, false], ["Dieser Fluss ist der l\\u00e4ngste der Welt.", "Was ist der Nil?", 200, false], ["Dieser Musiker ist bekannt als der \'King of Pop\'.", "Wer ist Michael Jackson?", 300, false], ["Diese Struktur ist bekannt als das \'Hirn\' der Zelle.", "Was ist der Zellkern?", 400, false], ["Diese Komponistin und Pianistin war die Ehefrau von Robert Schumann.", "Wer ist Clara Schumann?", 500, false]]}]}', null=True),
        ),
    ]
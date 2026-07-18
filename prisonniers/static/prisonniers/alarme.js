document.addEventListener("DOMContentLoaded", function () {

    let texte = document.body.innerText;

    if (texte.includes("LIBÉRATION AUJOURD’HUI")) {

        // Sirène
        let audio = new Audio("/static/prisonniers/siren.mp3");
        audio.volume = 1.0;
        audio.loop = true;

        audio.play().catch(() => {});

        // Recherche du nom du prisonnier
        let lignes = texte.split("\n");
        let nom = "Un prisonnier";

        for (let i = 0; i < lignes.length; i++) {
            if (lignes[i].includes("LIBÉRATION AUJOURD’HUI")) {
                if (i > 0) {
                    nom = lignes[i - 1];
                }
                break;
            }
        }

        // Lecture vocale
        let message = new SpeechSynthesisUtterance(
            "Attention ! Le prisonnier " +
            nom +
            " doit être libéré aujourd'hui."
        );

        message.lang = "fr-FR";
        message.rate = 0.9;
        message.pitch = 1;
        message.volume = 1;

        speechSynthesis.speak(message);

        alert(
            "🚨 ALERTE DE LIBÉRATION\n\n" +
            nom +
            "\n\nDoit être libéré aujourd'hui."
        );
    }

});
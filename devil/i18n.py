"""UI translations. The model is told to answer in LANGUAGES[code]['name']."""

LANGUAGES = {
    "en": {"name": "English", "flag": "🇬🇧"},
    "de": {"name": "German", "flag": "🇩🇪"},
    "it": {"name": "Italian", "flag": "🇮🇹"},
    "fr": {"name": "French", "flag": "🇫🇷"},
    "es": {"name": "Spanish", "flag": "🇪🇸"},
}

T = {
    # ---- header / nav
    "tagline": {
        "en": "An AI that disagrees well. Not to win, but to make your reasoning stronger.",
        "de": "Eine KI, die gut widerspricht. Nicht um zu gewinnen, sondern um dein Denken zu stärken.",
        "it": "Un'IA che sa dissentire bene. Non per vincere, ma per rafforzare il tuo ragionamento.",
        "fr": "Une IA qui sait contredire. Non pour gagner, mais pour renforcer ton raisonnement.",
        "es": "Una IA que sabe discrepar. No para ganar, sino para fortalecer tu razonamiento.",
    },
    "nav_arena": {"en": "Arena", "de": "Arena", "it": "Arena", "fr": "Arène", "es": "Arena"},
    "nav_history": {"en": "History", "de": "Verlauf", "it": "Cronologia", "fr": "Historique", "es": "Historial"},
    "nav_method": {"en": "How it works", "de": "So funktioniert's", "it": "Come funziona",
                   "fr": "Comment ça marche", "es": "Cómo funciona"},
    # ---- sidebar
    "language": {"en": "Language", "de": "Sprache", "it": "Lingua", "fr": "Langue", "es": "Idioma"},
    "model": {"en": "Model", "de": "Modell", "it": "Modello", "fr": "Modèle", "es": "Modelo"},
    "temperature": {"en": "Temperature", "de": "Temperatur", "it": "Temperatura",
                    "fr": "Température", "es": "Temperatura"},
    "connection": {"en": "Connection", "de": "Verbindung", "it": "Connessione",
                   "fr": "Connexion", "es": "Conexión"},
    "ollama_ok": {"en": "Connected", "de": "Verbunden", "it": "Connesso",
                  "fr": "Connecté", "es": "Conectado"},
    "ollama_missing": {
        "en": "Ollama not found. Start it with `ollama serve`, or type a model name.",
        "de": "Ollama nicht gefunden. Starte es mit `ollama serve` oder gib einen Modellnamen ein.",
        "it": "Ollama non trovato. Avvialo con `ollama serve` oppure inserisci il nome di un modello.",
        "fr": "Ollama introuvable. Lance-le avec `ollama serve` ou saisis un nom de modèle.",
        "es": "No se encuentra Ollama. Inícialo con `ollama serve` o escribe un nombre de modelo.",
    },
    "new_debate": {"en": "New belief", "de": "Neue Überzeugung", "it": "Nuova convinzione",
                   "fr": "Nouvelle conviction", "es": "Nueva creencia"},
    # ---- home
    "what_believe": {"en": "What do you believe?", "de": "Wovon bist du überzeugt?",
                     "it": "Di cosa sei convinto?", "fr": "De quoi es-tu convaincu ?",
                     "es": "¿Qué crees?"},
    "placeholder": {"en": "I think…", "de": "Ich denke, dass…", "it": "Penso che…",
                    "fr": "Je pense que…", "es": "Creo que…"},
    "how_sure": {"en": "How sure are you?", "de": "Wie sicher bist du?", "it": "Quanto ne sei sicuro?",
                 "fr": "À quel point es-tu sûr ?", "es": "¿Qué tan seguro estás?"},
    "challenge_me": {"en": "Challenge me", "de": "Fordere mich heraus", "it": "Mettimi alla prova",
                     "fr": "Défie-moi", "es": "Desafíame"},
    "or_try": {"en": "Or try one of these", "de": "Oder probier eines davon",
               "it": "Oppure prova uno di questi", "fr": "Ou essaie l'un de ceux-ci",
               "es": "O prueba uno de estos"},
    "empty_belief": {"en": "Write a belief first.", "de": "Schreib zuerst eine Überzeugung.",
                     "it": "Scrivi prima una convinzione.", "fr": "Écris d'abord une conviction.",
                     "es": "Escribe primero una creencia."},
    # ---- stage names
    "s_understand": {"en": "Understand", "de": "Verstehen", "it": "Comprendere", "fr": "Comprendre",
                     "es": "Comprender"},
    "s_debate": {"en": "Debate", "de": "Debatte", "it": "Dibattito", "fr": "Débat", "es": "Debate"},
    "s_judge": {"en": "Judge", "de": "Urteil", "it": "Giudice", "fr": "Juge", "es": "Juez"},
    "s_question": {"en": "Question", "de": "Fragen", "it": "Domande", "fr": "Questions",
                   "es": "Preguntas"},
    "s_reassess": {"en": "Reassess", "de": "Neu bewerten", "it": "Rivalutare", "fr": "Réévaluer",
                   "es": "Reevaluar"},
    # ---- progress messages
    "p_understand": {"en": "Restating your belief neutrally…", "de": "Formuliere deine Überzeugung neutral…",
                     "it": "Riformulo la tua convinzione in modo neutrale…",
                     "fr": "Je reformule ta conviction de façon neutre…",
                     "es": "Reformulando tu creencia de forma neutral…"},
    "p_advocate": {"en": "Advocate is building your strongest case…",
                   "de": "Der Anwalt baut dein stärkstes Argument…",
                   "it": "L'Avvocato costruisce la tua tesi più forte…",
                   "fr": "L'Avocat construit ton meilleur argumentaire…",
                   "es": "El Abogado construye tu mejor argumento…"},
    "p_devil": {"en": "Devil is hunting for weak assumptions…",
                "de": "Der Teufel sucht nach schwachen Annahmen…",
                "it": "Il Diavolo cerca le ipotesi deboli…",
                "fr": "Le Diable traque les hypothèses fragiles…",
                "es": "El Diablo busca supuestos débiles…"},
    "p_rebuttal": {"en": "Both sides reply to each other…", "de": "Beide Seiten antworten einander…",
                   "it": "Le due parti si rispondono…", "fr": "Les deux camps se répondent…",
                   "es": "Ambos lados se responden…"},
    "p_judge": {"en": "Blinded Judge is mapping the reasoning…",
                "de": "Der verblindete Richter kartiert die Argumente…",
                "it": "Il Giudice in cieco mappa il ragionamento…",
                "fr": "Le Juge à l'aveugle cartographie le raisonnement…",
                "es": "El Juez a ciegas mapea el razonamiento…"},
    "p_reassess": {"en": "Reassessing with your answers…", "de": "Bewerte neu mit deinen Antworten…",
                   "it": "Rivaluto con le tue risposte…", "fr": "Réévaluation avec tes réponses…",
                   "es": "Reevaluando con tus respuestas…"},
    "p_done": {"en": "Done", "de": "Fertig", "it": "Fatto", "fr": "Terminé", "es": "Listo"},
    # ---- understand step
    "did_i_get": {"en": "Did I get your belief right?", "de": "Habe ich dich richtig verstanden?",
                  "it": "Ho capito bene la tua convinzione?", "fr": "Ai-je bien compris ta conviction ?",
                  "es": "¿Entendí bien tu creencia?"},
    "understand_hint": {
        "en": "This neutral version is what both sides argue about, and the only version the Judge ever sees.",
        "de": "Über diese neutrale Fassung streiten beide Seiten. Der Richter sieht nur sie.",
        "it": "Su questa versione neutrale discutono entrambe le parti; è l'unica che vede il Giudice.",
        "fr": "Les deux camps débattent de cette version neutre, la seule que voit le Juge.",
        "es": "Ambos lados debaten esta versión neutral, la única que ve el Juez.",
    },
    "yes_go": {"en": "Yes, start the debate", "de": "Ja, Debatte starten", "it": "Sì, inizia il dibattito",
               "fr": "Oui, lance le débat", "es": "Sí, empieza el debate"},
    "edit_it": {"en": "Correct it", "de": "Korrigieren", "it": "Correggi", "fr": "Corriger",
                "es": "Corregir"},
    "save_edit": {"en": "Use my version", "de": "Meine Fassung verwenden", "it": "Usa la mia versione",
                  "fr": "Utiliser ma version", "es": "Usar mi versión"},
    "type": {"en": "Type", "de": "Typ", "it": "Tipo", "fr": "Type", "es": "Tipo"},
    "flag_false_premise": {"en": "Possible false premise", "de": "Mögliche falsche Prämisse",
                           "it": "Possibile premessa falsa", "fr": "Prémisse possiblement fausse",
                           "es": "Posible premisa falsa"},
    "flag_consensus": {"en": "Near-consensus claim", "de": "Nahezu Konsens",
                       "it": "Tesi quasi consensuale", "fr": "Quasi-consensus",
                       "es": "Casi consenso"},
    "skills_loaded": {"en": "Skills loaded", "de": "Geladene Skills", "it": "Skill caricate",
                      "fr": "Skills chargées", "es": "Skills cargadas"},
    # ---- arena
    "your_case": {"en": "Your case", "de": "Deine Seite", "it": "La tua tesi", "fr": "Ta position",
                  "es": "Tu postura"},
    "other_side": {"en": "The other side", "de": "Die Gegenseite", "it": "L'altra parte",
                   "fr": "L'autre camp", "es": "El otro lado"},
    "advocate": {"en": "Advocate", "de": "Anwalt", "it": "Avvocato", "fr": "Avocat", "es": "Abogado"},
    "devil": {"en": "Devil", "de": "Teufel", "it": "Diavolo", "fr": "Diable", "es": "Diablo"},
    "judge": {"en": "Judge", "de": "Richter", "it": "Giudice", "fr": "Juge", "es": "Juez"},
    "arguments": {"en": "Arguments", "de": "Argumente", "it": "Argomenti", "fr": "Arguments",
                  "es": "Argumentos"},
    "unmentioned": {"en": "Reasons you didn't mention", "de": "Gründe, die du nicht genannt hast",
                    "it": "Ragioni che non hai citato", "fr": "Raisons que tu n'as pas citées",
                    "es": "Razones que no mencionaste"},
    "weak_assumptions": {"en": "Load-bearing assumptions", "de": "Tragende Annahmen",
                         "it": "Ipotesi portanti", "fr": "Hypothèses porteuses",
                         "es": "Supuestos clave"},
    "if_false": {"en": "If false", "de": "Falls falsch", "it": "Se falso", "fr": "Si faux",
                 "es": "Si es falso"},
    "claims_checked": {"en": "Claims checked", "de": "Geprüfte Behauptungen",
                       "it": "Affermazioni verificate", "fr": "Affirmations vérifiées",
                       "es": "Afirmaciones verificadas"},
    "steelman": {"en": "The strongest case against", "de": "Das stärkste Gegenargument",
                 "it": "La tesi contraria più forte", "fr": "Le meilleur argument contraire",
                 "es": "El argumento contrario más fuerte"},
    "rebuttals": {"en": "Rebuttal round", "de": "Erwiderungsrunde", "it": "Round di replica",
                  "fr": "Tour de réplique", "es": "Ronda de réplica"},
    "concedes": {"en": "Concedes", "de": "Räumt ein", "it": "Concede", "fr": "Concède", "es": "Concede"},
    # ---- judge
    "the_map": {"en": "The map", "de": "Die Landkarte", "it": "La mappa", "fr": "La carte",
                "es": "El mapa"},
    "no_winner": {"en": "No score. No winner. A diagnosis.", "de": "Keine Punkte. Kein Sieger. Eine Diagnose.",
                  "it": "Nessun punteggio. Nessun vincitore. Una diagnosi.",
                  "fr": "Pas de score. Pas de gagnant. Un diagnostic.",
                  "es": "Sin puntuación. Sin ganador. Un diagnóstico."},
    "survived": {"en": "Survived scrutiny", "de": "Hat der Prüfung standgehalten",
                 "it": "Ha retto alla verifica", "fr": "A résisté à l'examen", "es": "Resistió el examen"},
    "needs_evidence": {"en": "Needs evidence", "de": "Braucht Belege", "it": "Servono prove",
                       "fr": "Nécessite des preuves", "es": "Necesita pruebas"},
    "hidden": {"en": "Hidden assumptions", "de": "Versteckte Annahmen", "it": "Ipotesi nascoste",
               "fr": "Hypothèses cachées", "es": "Supuestos ocultos"},
    "takeaway": {"en": "Question to take away", "de": "Frage zum Mitnehmen", "it": "Domanda da portare via",
                 "fr": "Question à emporter", "es": "Pregunta para llevarte"},
    "claim_map": {"en": "Claim-by-claim", "de": "Behauptung für Behauptung", "it": "Affermazione per affermazione",
                  "fr": "Affirmation par affirmation", "es": "Afirmación por afirmación"},
    "v_well_supported": {"en": "well supported", "de": "gut belegt", "it": "ben supportata",
                         "fr": "bien étayée", "es": "bien respaldada"},
    "v_asserted": {"en": "asserted", "de": "nur behauptet", "it": "solo affermata", "fr": "simplement affirmée",
                   "es": "solo afirmada"},
    "v_untested_assumption": {"en": "untested assumption", "de": "ungeprüfte Annahme",
                              "it": "ipotesi non verificata", "fr": "hypothèse non testée",
                              "es": "supuesto no probado"},
    "e_supported": {"en": "supported", "de": "belegt", "it": "supportata", "fr": "étayée", "es": "respaldada"},
    "e_contested": {"en": "contested", "de": "umstritten", "it": "contestata", "fr": "contestée",
                    "es": "discutida"},
    "e_unsupported": {"en": "unsupported", "de": "unbelegt", "it": "non supportata", "fr": "non étayée",
                      "es": "sin respaldo"},
    # ---- questions / reassess
    "your_turn": {"en": "Your turn: answer the Devil", "de": "Du bist dran: Antworte dem Teufel",
                  "it": "Tocca a te: rispondi al Diavolo", "fr": "À toi : réponds au Diable",
                  "es": "Tu turno: responde al Diablo"},
    "answer_here": {"en": "Your answer…", "de": "Deine Antwort…", "it": "La tua risposta…",
                    "fr": "Ta réponse…", "es": "Tu respuesta…"},
    "submit_answers": {"en": "Reassess my reasoning", "de": "Mein Denken neu bewerten",
                       "it": "Rivaluta il mio ragionamento", "fr": "Réévaluer mon raisonnement",
                       "es": "Reevaluar mi razonamiento"},
    "reassessment": {"en": "Reassessment", "de": "Neubewertung", "it": "Rivalutazione",
                     "fr": "Réévaluation", "es": "Reevaluación"},
    "unexamined": {"en": "Still unexamined", "de": "Noch ungeprüft", "it": "Ancora da esaminare",
                   "fr": "Encore non examiné", "es": "Aún sin examinar"},
    "next_step": {"en": "Next step", "de": "Nächster Schritt", "it": "Prossimo passo",
                  "fr": "Prochaine étape", "es": "Siguiente paso"},
    "conf_now": {"en": "How sure are you now?", "de": "Wie sicher bist du jetzt?",
                 "it": "Quanto ne sei sicuro adesso?", "fr": "Et maintenant, à quel point es-tu sûr ?",
                 "es": "¿Qué tan seguro estás ahora?"},
    "before": {"en": "Before", "de": "Vorher", "it": "Prima", "fr": "Avant", "es": "Antes"},
    "after": {"en": "After", "de": "Nachher", "it": "Dopo", "fr": "Après", "es": "Después"},
    "change_mind": {"en": "What would change your mind?", "de": "Was würde deine Meinung ändern?",
                    "it": "Cosa ti farebbe cambiare idea?", "fr": "Qu'est-ce qui te ferait changer d'avis ?",
                    "es": "¿Qué te haría cambiar de opinión?"},
    "save_session": {"en": "Save to my history", "de": "In meinem Verlauf speichern",
                     "it": "Salva nella cronologia", "fr": "Enregistrer dans l'historique",
                     "es": "Guardar en mi historial"},
    "saved": {"en": "Saved to memory.md", "de": "In memory.md gespeichert", "it": "Salvato in memory.md",
              "fr": "Enregistré dans memory.md", "es": "Guardado en memory.md"},
    "download": {"en": "Download debate (.md)", "de": "Debatte herunterladen (.md)",
                 "it": "Scarica il dibattito (.md)", "fr": "Télécharger le débat (.md)",
                 "es": "Descargar el debate (.md)"},
    # ---- pushback
    "push_title": {"en": "Push back on the Devil", "de": "Widersprich dem Teufel",
                   "it": "Ribatti al Diavolo", "fr": "Réplique au Diable", "es": "Rebate al Diablo"},
    "push_hint": {
        "en": "It only gives ground to new arguments or evidence, never to insistence.",
        "de": "Er gibt nur bei neuen Argumenten oder Belegen nach, nie bei bloßem Beharren.",
        "it": "Cede solo a nuovi argomenti o prove, mai all'insistenza.",
        "fr": "Il ne cède qu'à de nouveaux arguments ou preuves, jamais à l'insistance.",
        "es": "Solo cede ante argumentos o pruebas nuevas, nunca ante la insistencia.",
    },
    "push_placeholder": {"en": "Argue back…", "de": "Widersprich…", "it": "Controbatti…",
                         "fr": "Contre-argumente…", "es": "Rebate…"},
    "moved": {"en": "Position updated", "de": "Position angepasst", "it": "Posizione aggiornata",
              "fr": "Position ajustée", "es": "Postura ajustada"},
    "held": {"en": "Held its ground", "de": "Bleibt standhaft", "it": "Mantiene la posizione",
             "fr": "Tient sa position", "es": "Mantiene su postura"},
    "new_arg": {"en": "new argument detected", "de": "neues Argument erkannt", "it": "nuovo argomento rilevato",
                "fr": "nouvel argument détecté", "es": "nuevo argumento detectado"},
    "no_new_arg": {"en": "no new argument", "de": "kein neues Argument", "it": "nessun nuovo argomento",
                   "fr": "aucun nouvel argument", "es": "ningún argumento nuevo"},
    # ---- history
    "history_empty": {"en": "No saved debates yet.", "de": "Noch keine gespeicherten Debatten.",
                      "it": "Ancora nessun dibattito salvato.", "fr": "Aucun débat enregistré pour l'instant.",
                      "es": "Aún no hay debates guardados."},
    "confidence": {"en": "Confidence", "de": "Sicherheit", "it": "Sicurezza", "fr": "Confiance",
                   "es": "Confianza"},
    "clear_history": {"en": "Clear history", "de": "Verlauf löschen", "it": "Cancella cronologia",
                      "fr": "Effacer l'historique", "es": "Borrar historial"},
    "web_search": {"en": "Web search (Tavily)", "de": "Websuche (Tavily)", "it": "Ricerca web (Tavily)",
                   "fr": "Recherche web (Tavily)", "es": "Búsqueda web (Tavily)"},
    "tavily_key": {"en": "Tavily API key", "de": "Tavily-API-Schlüssel", "it": "Chiave API Tavily",
                   "fr": "Clé API Tavily", "es": "Clave API de Tavily"},
    "tavily_help": {"en": "Free key at tavily.com", "de": "Kostenloser Schlüssel auf tavily.com",
                    "it": "Chiave gratuita su tavily.com", "fr": "Clé gratuite sur tavily.com",
                    "es": "Clave gratuita en tavily.com"},
    "need_key": {"en": "Paste your Tavily key to search the web.",
                 "de": "Füge deinen Tavily-Schlüssel ein, um im Web zu suchen.",
                 "it": "Incolla la tua chiave Tavily per cercare sul web.",
                 "fr": "Colle ta clé Tavily pour chercher sur le web.",
                 "es": "Pega tu clave de Tavily para buscar en la web."},
    "p_search": {"en": "Searching the web for evidence on both sides…",
                 "de": "Suche im Web nach Belegen für beide Seiten…",
                 "it": "Cerco sul web prove per entrambe le parti…",
                 "fr": "Recherche de preuves sur le web pour les deux camps…",
                 "es": "Buscando en la web pruebas para ambos lados…"},
    "sources": {"en": "Sources", "de": "Quellen", "it": "Fonti", "fr": "Sources", "es": "Fuentes"},
    "sources_hint": {"en": "Found on the web. Claims cite them as [1], [2]. Sources can be wrong or one-sided.",
                     "de": "Im Web gefunden. Behauptungen zitieren sie als [1], [2]. Quellen können falsch oder einseitig sein.",
                     "it": "Trovate sul web. Le affermazioni le citano come [1], [2]. Le fonti possono essere errate o di parte.",
                     "fr": "Trouvées sur le web. Les affirmations les citent comme [1], [2]. Les sources peuvent être fausses ou partiales.",
                     "es": "Encontradas en la web. Las afirmaciones las citan como [1], [2]. Las fuentes pueden ser erróneas o parciales."},
    "search_failed": {"en": "Web search failed, so the debate ran without sources",
                      "de": "Websuche fehlgeschlagen, die Debatte lief ohne Quellen",
                      "it": "Ricerca web non riuscita, il dibattito è andato avanti senza fonti",
                      "fr": "La recherche web a échoué, le débat s'est fait sans sources",
                      "es": "Falló la búsqueda web, el debate se hizo sin fuentes"},
    "nav_community": {"en": "Community", "de": "Community", "it": "Community", "fr": "Communauté",
                      "es": "Comunidad"},
    "storage_supabase": {"en": "Debates saved to the shared database", "de": "Debatten werden in der gemeinsamen Datenbank gespeichert",
                         "it": "Dibattiti salvati nel database condiviso", "fr": "Débats enregistrés dans la base partagée",
                         "es": "Debates guardados en la base de datos compartida"},
    "storage_local": {"en": "Debates saved on this computer", "de": "Debatten werden auf diesem Computer gespeichert",
                      "it": "Dibattiti salvati su questo computer", "fr": "Débats enregistrés sur cet ordinateur",
                      "es": "Debates guardados en este ordenador"},
    "consent": {"en": "Debates are stored anonymously to improve the tool. Don't enter personal data.",
                "de": "Debatten werden anonym gespeichert, um das Tool zu verbessern. Gib keine persönlichen Daten ein.",
                "it": "I dibattiti vengono salvati in forma anonima per migliorare lo strumento. Non inserire dati personali.",
                "fr": "Les débats sont enregistrés anonymement pour améliorer l'outil. N'entre pas de données personnelles.",
                "es": "Los debates se guardan de forma anónima para mejorar la herramienta. No introduzcas datos personales."},
    "learned_from": {"en": "Devil studies {n} top-rated past challenges",
                     "de": "Der Teufel lernt von {n} top-bewerteten früheren Einwänden",
                     "it": "Il Diavolo studia {n} sfide passate molto apprezzate",
                     "fr": "Le Diable s'inspire de {n} contestations passées très bien notées",
                     "es": "El Diablo estudia {n} desafíos anteriores muy valorados"},
    "rate_q": {"en": "Was this challenge useful?", "de": "War dieser Einwand hilfreich?",
               "it": "Questa sfida ti è stata utile?", "fr": "Cette contestation t'a-t-elle été utile ?",
               "es": "¿Te ha sido útil este desafío?"},
    "rate_hint": {"en": "👍 challenges become examples the Devil learns from.",
                  "de": "👍-Einwände werden zu Beispielen, von denen der Teufel lernt.",
                  "it": "Le sfide con 👍 diventano esempi da cui il Diavolo impara.",
                  "fr": "Les contestations 👍 deviennent des exemples dont le Diable s'inspire.",
                  "es": "Los desafíos con 👍 se convierten en ejemplos de los que aprende el Diablo."},
    "feedback_ph": {"en": "Optional: what was strong or weak?", "de": "Optional: Was war stark oder schwach?",
                    "it": "Facoltativo: cosa era forte o debole?", "fr": "Facultatif : qu'est-ce qui était fort ou faible ?",
                    "es": "Opcional: ¿qué fue fuerte o débil?"},
    "thanks": {"en": "Thanks, feedback saved", "de": "Danke, Feedback gespeichert", "it": "Grazie, feedback salvato",
               "fr": "Merci, avis enregistré", "es": "Gracias, opinión guardada"},
    "community_hint": {"en": "Every debate run by every user, newest first.",
                       "de": "Alle Debatten aller Nutzer, neueste zuerst.",
                       "it": "Tutti i dibattiti di tutti gli utenti, dal più recente.",
                       "fr": "Tous les débats de tous les utilisateurs, du plus récent au plus ancien.",
                       "es": "Todos los debates de todos los usuarios, del más reciente al más antiguo."},
    "no_debates": {"en": "No debates yet. Be the first!", "de": "Noch keine Debatten. Sei der Erste!",
                   "it": "Ancora nessun dibattito. Sii il primo!", "fr": "Aucun débat pour l'instant. Lance le premier !",
                   "es": "Aún no hay debates. ¡Sé el primero!"},
    "m_debates": {"en": "Debates", "de": "Debatten", "it": "Dibattiti", "fr": "Débats", "es": "Debates"},
    "m_useful": {"en": "Rated useful", "de": "Als hilfreich bewertet", "it": "Giudicati utili",
                 "fr": "Jugés utiles", "es": "Valorados útiles"},
    "m_shift": {"en": "Avg. confidence shift", "de": "Ø Änderung der Sicherheit", "it": "Variazione media sicurezza",
                "fr": "Variation moy. de confiance", "es": "Cambio medio de confianza"},
    "m_languages": {"en": "Languages", "de": "Sprachen", "it": "Lingue", "fr": "Langues", "es": "Idiomas"},
    "team_export": {"en": "Team export (all debates as CSV)", "de": "Team-Export (alle Debatten als CSV)",
                    "it": "Esportazione team (tutti i dibattiti in CSV)", "fr": "Export équipe (tous les débats en CSV)",
                    "es": "Exportación del equipo (todos los debates en CSV)"},
    "admin_pw": {"en": "Team password", "de": "Team-Passwort", "it": "Password del team", "fr": "Mot de passe de l'équipe",
                 "es": "Contraseña del equipo"},
    "speed": {"en": "Mode", "de": "Modus", "it": "Modalità", "fr": "Mode", "es": "Modo"},
    "speed_fast": {"en": "⚡ Fast", "de": "⚡ Schnell", "it": "⚡ Veloce", "fr": "⚡ Rapide", "es": "⚡ Rápido"},
    "speed_thorough": {"en": "⚖️ Thorough", "de": "⚖️ Gründlich", "it": "⚖️ Approfondita",
                       "fr": "⚖️ Approfondi", "es": "⚖️ A fondo"},
    "speed_hint_fast": {"en": "Devil in one pass, no rebuttal round. About 3x faster.",
                        "de": "Teufel in einem Durchgang, ohne Erwiderungsrunde. Etwa 3x schneller.",
                        "it": "Diavolo in un passaggio, senza replica. Circa 3 volte più veloce.",
                        "fr": "Diable en une passe, sans réplique. Environ 3x plus rapide.",
                        "es": "Diablo en una pasada, sin réplica. Unas 3 veces más rápido."},
    "speed_hint_thorough": {"en": "Every stage is a separate call, plus the rebuttal round (the full proposal pipeline).",
                            "de": "Jede Stufe ist ein eigener Aufruf, plus Erwiderungsrunde (die volle Pipeline).",
                            "it": "Ogni fase è una chiamata separata, più il round di replica (pipeline completa).",
                            "fr": "Chaque étape est un appel séparé, plus la réplique (pipeline complet).",
                            "es": "Cada etapa es una llamada aparte, más la réplica (pipeline completo)."},
    "deep_think": {"en": "Deep thinking (slow)", "de": "Tiefes Nachdenken (langsam)", "it": "Ragionamento profondo (lento)",
                   "fr": "Réflexion profonde (lent)", "es": "Razonamiento profundo (lento)"},
    "deep_think_help": {"en": "Lets reasoning models think before answering. Better, but often 3–5x slower.",
                        "de": "Lässt Reasoning-Modelle vor der Antwort nachdenken. Besser, aber oft 3–5x langsamer.",
                        "it": "Fa ragionare il modello prima di rispondere. Migliore, ma spesso 3–5 volte più lento.",
                        "fr": "Laisse le modèle réfléchir avant de répondre. Meilleur, mais souvent 3 à 5x plus lent.",
                        "es": "Deja que el modelo razone antes de responder. Mejor, pero a menudo 3–5 veces más lento."},
    # ---- errors
    "error": {
        "en": "The model call failed.",
        "de": "Der Modellaufruf ist fehlgeschlagen.",
        "it": "La chiamata al modello è fallita.",
        "fr": "L'appel au modèle a échoué.",
        "es": "Falló la llamada al modelo.",
    },
}

EXAMPLES = {
    "en": ["Doing a master's degree is better than starting work immediately.",
           "Remote work makes employees less productive.",
           "Nuclear energy is necessary for the energy transition.",
           "Since we only use 10% of our brains, brain-training apps are a smart investment."],
    "de": ["Ein Master ist besser, als direkt mit dem Arbeiten anzufangen.",
           "Homeoffice macht Mitarbeitende weniger produktiv.",
           "Kernenergie ist für die Energiewende notwendig.",
           "Da wir nur 10 % unseres Gehirns nutzen, sind Gehirntrainings-Apps eine kluge Investition."],
    "it": ["Fare una laurea magistrale è meglio che iniziare subito a lavorare.",
           "Lo smart working rende i dipendenti meno produttivi.",
           "L'energia nucleare è necessaria per la transizione energetica.",
           "Visto che usiamo solo il 10% del cervello, le app di brain training sono un buon investimento."],
    "fr": ["Faire un master vaut mieux que commencer à travailler tout de suite.",
           "Le télétravail rend les salariés moins productifs.",
           "Le nucléaire est indispensable à la transition énergétique.",
           "Comme on n'utilise que 10 % de notre cerveau, les applis d'entraînement cérébral sont un bon investissement."],
    "es": ["Hacer un máster es mejor que empezar a trabajar de inmediato.",
           "El teletrabajo hace que los empleados sean menos productivos.",
           "La energía nuclear es necesaria para la transición energética.",
           "Como solo usamos el 10 % del cerebro, las apps de entrenamiento mental son una buena inversión."],
}

METHOD = {
    "en": """
### Why this exists
Language models are trained to be liked, and being liked is not the same as being useful to think with.
Assistants drift toward agreeing with whoever is typing. **Devil's Advocate** is built to do the opposite,
constructively.

### The central idea
Telling an AI to *"be critical"* produces contrarianism. **Designing a process** produces reasoning.
So nothing here is a single "be critical" instruction. Every stage is its own prompt and model call.

### The pipeline
1. **Understand**: a neutral restatement of your belief, which you confirm or correct.
2. **Advocate ‖ Devil**: built independently. The Advocate makes your best case. The Devil names three
   load-bearing assumptions, labels every claim *supported / contested / unsupported*, and writes a steelman
   of the opposing case.
3. **Rebuttal round**: each side replies once to the other.
4. **Blinded Judge**: sees only the neutral restatement and the two cases, never your wording or your
   confidence. It produces a **map**, not a verdict.
5. **Question → Reassess**: you answer the Devil's questions and see what held up. You then re-rate your
   confidence.

### Two rules everywhere
- **Concession rule**: the Devil gives ground only for new arguments or evidence, never for insistence.
- **Proportionality rule**: no false balance against well-established facts.

### Skills, loaded only when needed
Stage 1 can flag a *false premise*, a *near-consensus* claim or a *personal decision*. The matching
guidance in `skills/` is then loaded into the later stages.
""",
    "de": """
### Warum es das gibt
Sprachmodelle sind darauf trainiert, gemocht zu werden. Gemocht zu werden ist aber nicht dasselbe, wie beim
Denken zu helfen. **Devil's Advocate** soll konstruktiv widersprechen.

### Die zentrale Idee
Die Anweisung *„sei kritisch“* erzeugt bloßen Widerspruch. **Ein durchdachter Prozess** erzeugt Argumente.
Jede Stufe ist deshalb ein eigener Prompt und ein eigener Modellaufruf.

### Die Pipeline
1. **Verstehen**: eine neutrale Fassung deiner Überzeugung, die du bestätigst oder korrigierst.
2. **Anwalt ‖ Teufel**: unabhängig voneinander erstellt. Der Teufel nennt drei tragende Annahmen,
   bewertet jede Behauptung und baut das stärkste Gegenargument.
3. **Erwiderung**: jede Seite antwortet einmal.
4. **Verblindeter Richter**: sieht nie deinen Wortlaut oder deine Sicherheit. Er liefert eine **Landkarte**,
   kein Urteil.
5. **Fragen → Neubewertung**: du antwortest und bewertest deine Sicherheit neu.

### Zwei Regeln
- **Zugeständnisregel**: nur neue Argumente oder Belege bewegen den Teufel.
- **Verhältnismäßigkeit**: keine künstliche Debatte gegen gesicherte Fakten.
""",
    "it": """
### Perché esiste
I modelli linguistici sono addestrati a piacere, e piacere non equivale a essere utili per pensare.
**Devil's Advocate** è costruito per dissentire in modo costruttivo.

### L'idea centrale
Dire a un'IA *"sii critica"* produce contrarianismo. **Progettare un processo** produce ragionamento.
Ogni fase è un prompt e una chiamata al modello separati.

### La pipeline
1. **Comprendere**: una riformulazione neutrale, che confermi o correggi.
2. **Avvocato ‖ Diavolo**: costruiti in modo indipendente. Il Diavolo individua tre ipotesi portanti,
   etichetta ogni affermazione e costruisce la tesi contraria più forte.
3. **Replica**: ogni parte risponde una volta.
4. **Giudice in cieco**: non vede mai le tue parole né la tua sicurezza. Produce una **mappa**, non un verdetto.
5. **Domande → Rivalutazione**: rispondi e rivaluti la tua sicurezza.

### Due regole
- **Regola della concessione**: solo nuovi argomenti o prove smuovono il Diavolo.
- **Proporzionalità**: nessun falso equilibrio contro fatti consolidati.
""",
    "fr": """
### Pourquoi
Les modèles de langage sont entraînés à plaire, et plaire n'est pas la même chose qu'aider à penser.
**Devil's Advocate** est conçu pour contredire de manière constructive.

### L'idée centrale
Demander à une IA d'*« être critique »* produit de la contradiction. **Concevoir un processus** produit
du raisonnement. Chaque étape est un prompt et un appel au modèle distincts.

### Le pipeline
1. **Comprendre** : une reformulation neutre, que tu confirmes ou corriges.
2. **Avocat ‖ Diable** : construits indépendamment. Le Diable identifie trois hypothèses porteuses,
   qualifie chaque affirmation et construit le meilleur argument contraire.
3. **Réplique** : chaque camp répond une fois.
4. **Juge à l'aveugle** : ne voit jamais tes mots ni ta confiance. Il produit une **carte**, pas un verdict.
5. **Questions → Réévaluation** : tu réponds et réévalues ta confiance.

### Deux règles
- **Règle de concession** : seuls des arguments ou des preuves nouvelles font bouger le Diable.
- **Proportionnalité** : pas de faux équilibre face aux faits établis.
""",
    "es": """
### Por qué existe
Los modelos de lenguaje se entrenan para agradar, y agradar no es lo mismo que ayudar a pensar.
**Devil's Advocate** está hecho para discrepar de forma constructiva.

### La idea central
Pedirle a una IA que *"sea crítica"* produce llevar la contraria. **Diseñar un proceso** produce
razonamiento. Cada etapa es un prompt y una llamada al modelo distintos.

### El pipeline
1. **Comprender**: una reformulación neutral, que confirmas o corriges.
2. **Abogado ‖ Diablo**: construidos de forma independiente. El Diablo nombra tres supuestos clave,
   etiqueta cada afirmación y construye el mejor argumento contrario.
3. **Réplica**: cada lado responde una vez.
4. **Juez a ciegas**: nunca ve tus palabras ni tu confianza. Produce un **mapa**, no un veredicto.
5. **Preguntas → Reevaluación**: respondes y reevalúas tu confianza.

### Dos reglas
- **Regla de concesión**: solo argumentos o pruebas nuevas mueven al Diablo.
- **Proporcionalidad**: nada de falso equilibrio frente a hechos establecidos.
""",
}


def t(key: str, lang: str) -> str:
    entry = T.get(key, {})
    return entry.get(lang) or entry.get("en") or key

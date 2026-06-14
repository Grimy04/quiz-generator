const BANK = [
    {
      "q": "Il protocollo HTTP utilizza la porta 80 di default per le comunicazioni non criptate.",
      "fmt": "vf",
      "correct": true,
      "opts": null,
      "explain": "Esatto. L'HTTP viaggia sulla porta 80, mentre la sua versione sicura (HTTPS) utilizza la porta 443.",
      "points": null,
      "ch": "reti_01",
      "id": "reti_01-a1b2c3d4"
    },
    {
      "q": "La memoria RAM è un tipo di memoria non volatile, ovvero mantiene i dati anche in assenza di alimentazione elettrica.",
      "fmt": "vf",
      "correct": false,
      "opts": null,
      "explain": "Falso. La RAM è volatile. Quando spegni il PC, tutto il contenuto della RAM viene cancellato. Le memorie non volatili sono gli Hard Disk o gli SSD.",
      "points": null,
      "ch": "arch_01",
      "id": "arch_01-e5f6g7h8"
    },
    {
      "q": "Quale tra i seguenti NON è un paradigma di programmazione comunemente riconosciuto?",
      "fmt": "mc",
      "correct": 2,
      "opts": [
        "Programmazione Orientata agli Oggetti (OOP)",
        "Programmazione Funzionale",
        "Programmazione Caotica (CP)",
        "Programmazione Procedurale"
      ],
      "explain": "La Programmazione Caotica non esiste come paradigma ufficiale (anche se a volte il codice dei colleghi suggerisce il contrario!).",
      "points": null,
      "ch": "prog_01",
      "id": "prog_01-i9j0k1l2"
    },
    {
      "q": "Qual è il ruolo principale del DNS (Domain Name System) all'interno di una rete?",
      "fmt": "mc",
      "correct": 0,
      "opts": [
        "Tradurre i nomi di dominio leggibili (es. google.com) negli indirizzi IP dei server",
        "Assegnare dinamicamente gli indirizzi IP ai computer che si collegano alla rete",
        "Criptare i dati in transito tra il client e il server web",
        "Bloccare gli accessi non autorizzati alla rete locale tramite firewall"
      ],
      "explain": "Il DNS funziona come la 'rubrica telefonica' di Internet, traducendo gli URL umani in indirizzi IP comprensibili dalle macchine.",
      "points": null,
      "ch": "reti_01",
      "id": "reti_01-m3n4o5p6"
    },
    {
      "q": "Descrivi brevemente il concetto di 'Polimorfismo' nella Programmazione Orientata agli Oggetti.",
      "fmt": "open",
      "correct": null,
      "opts": null,
      "explain": null,
      "points": [
        "Capacità di un oggetto di assumere più forme",
        "Metodi con lo stesso nome ma comportamenti diversi in base alla classe derivata",
        "Overriding (sovrascrittura) o Overloading (sovraccarico)"
      ],
      "ch": "prog_01",
      "id": "prog_01-q7r8s9t0"
    }
  ];
  
  const META = [
    {
      "ch": "reti_01",
      "num": "01",
      "nm": "Reti di Calcolatori",
      "sb": "",
      "tone": "#ff9f1c"
    },
    {
      "ch": "arch_01",
      "num": "02",
      "nm": "Architettura degli Elaboratori",
      "sb": "",
      "tone": "#2ec4b6"
    },
    {
      "ch": "prog_01",
      "num": "03",
      "nm": "Ingegneria del Software",
      "sb": "",
      "tone": "#e71d36"
    }
  ];
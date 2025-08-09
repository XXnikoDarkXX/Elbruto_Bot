class Brute:
    def __init__(self, bruto_data: dict):
        self.id = bruto_data.get('id')
        self.name = bruto_data.get('name')
        self.level = bruto_data.get('level')
        self.xp = bruto_data.get('xp')
        self.hp = bruto_data.get('hp')
        self.enduranceStat = bruto_data.get('enduranceStat')
        self.strengthStat = bruto_data.get('strengthStat')
        self.agilityStat = bruto_data.get('agilityStat')
        self.speedStat = bruto_data.get('speedStat')
        self.ranking = bruto_data.get('ranking')
        self.gender = bruto_data.get('gender')
        self.weapons = bruto_data.get('weapons', [])
        self.skills = bruto_data.get('skills', [])
        self.clan = bruto_data.get('clan', {}).get('name', 'No Clan') if isinstance(bruto_data.get('clan'), dict) else 'No Clan'
        self.victories = bruto_data.get('victories')
        self.losses = bruto_data.get('losses')
        self.lastFight = bruto_data.get('lastFight')
        self.fightsLeft = bruto_data.get('fightsLeft')
        self.registeredForTournament = bruto_data.get('registeredForTournament')
        self.currentTournamentDate = bruto_data.get('currentTournamentDate')
        self.tournaments = bruto_data.get('tournaments', [])
        self.inventory = bruto_data.get('inventory', [])

        # 🔹 Guardar paths de decisiones
        self.destinyPath = bruto_data.get('destinyPath', [])
        self.previousDestinyPath = bruto_data.get('previousDestinyPath', [])

    def __repr__(self):
        return f"Bruto(name={self.name}, level={self.level}, hp={self.hp}, ranking={self.ranking}, " \
               f"victories={self.victories}, losses={self.losses})"

    def get_summary(self):
        return {
            "ID": self.id,
            "Name": self.name,
            "Level": self.level,
            "XP": self.xp,
            "HP": self.hp,
            "Endurance": self.enduranceStat,
            "Strength": self.strengthStat,
            "Agility": self.agilityStat,
            "Speed": self.speedStat,
            "Ranking": self.ranking,
            "Gender": self.gender,
            "Clan": self.clan,
            "Victories": self.victories,
            "Losses": self.losses,
            "Last Fight": self.lastFight,
            "Fights Left": self.fightsLeft,
            "Tournament Date": self.currentTournamentDate,
            "Weapons": self.weapons,
            "Skills": self.skills,
            "Destiny Path": self.destinyPath,
            "Previous Destiny Path": self.previousDestinyPath
        }

    # 🔹 Devolver la elección pasada en el nivel actual
    def get_previous_choice_for_current_level(self):
        if not isinstance(self.previousDestinyPath, list):
            return None
        idx = len(self.destinyPath)
        return self.previousDestinyPath[idx] if idx < len(self.previousDestinyPath) else None

    # 🔹 Devolver todas las elecciones pasadas por nivel
    def get_previous_choices_history(self):
        return [
            {"level": i + 2, "choice": choice}
            for i, choice in enumerate(self.previousDestinyPath)
        ]
    def get_repeatable_previous_choice(self):
        """
        Devuelve LEFT/RIGHT únicamente si:
        - previousDestinyPath tiene al menos idx+1 elementos, y
        - el prefijo de previousDestinyPath hasta idx coincide EXACTAMENTE con destinyPath actual.
        Si cambiaste alguna decisión antes, devuelve None.
        """
        dp = self.destinyPath or []
        pp = self.previousDestinyPath or []
        idx = len(dp)  # próximo nivel

        # previous no llegó tan lejos
        if len(pp) <= idx:
            return None

        # prefijo debe coincidir
        if not all(a == b for a, b in zip(dp, pp[:idx])):
            return None

        return pp[idx]  # LEFT / RIGHT válido para repetir
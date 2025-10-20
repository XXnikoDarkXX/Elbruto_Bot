from .brute_manager import BrutoManager
from .brute import Brute
from core.utils import random_sleep
from .telegram_notifier import TelegramNotifier, escape_markdown_v2

async def procesar_bruto(auth, bruto_name, subir_nivel_data, torneo):
    bruto_manager = BrutoManager(auth)
    json_bruto = bruto_manager.get_for_hook_info(bruto_name)

    if not json_bruto:
        mensaje_error = f"⚠️ No se pudo obtener información del bruto *{escape_markdown_v2(bruto_name)}*. Se omite."
        print(mensaje_error)
        notifier = TelegramNotifier()
        await notifier.enviar_mensaje(mensaje_error)
        return

    bruto = Brute(json_bruto)
    bruto_manager.brute = bruto

    print(f"#------------------------#\nBrutoActual: {bruto_name}")
    print(f"Registrado en torneo?: {bruto.registeredForTournament}")
    notifier = TelegramNotifier()

    # --- Helper: refrescar datos del bruto tras cambios ---
    async def refrescar_bruto():
        nonlocal bruto, bruto_manager
        nuevo = bruto_manager.get_for_hook_info(bruto_name)
        if nuevo:
            bruto = Brute(nuevo)
            bruto_manager.brute = bruto

    # --- Helper: intenta resolver subida de nivel ---
    async def resolver_subida_nivel():
        json_subida_local = bruto_manager.SubidaNivel()
        if not json_subida_local or json_subida_local == 500:
            return False

        izquierda_local, derecha_local = bruto_manager.obtener_recompensas(json_subida_local)
        print(f"Recompensas: {izquierda_local}, {derecha_local}")

        prev_choice_local = bruto.get_repeatable_previous_choice()
        if prev_choice_local in ("LEFT", "RIGHT"):
            nivel_actual = bruto.level or (len(bruto.destinyPath) + 1)
            nivel_siguiente = nivel_actual + 1
            recompensa_elegida = izquierda_local if prev_choice_local == "LEFT" else derecha_local

            aviso = (
                f"🔁 Se repite la elección pasada para *{escape_markdown_v2(bruto.name)}* "
                f"\\(Nivel {escape_markdown_v2(str(nivel_siguiente))}\\):\n"
                f"• Lado: *{escape_markdown_v2(prev_choice_local)}*\n"
                f"• Recompensa: {escape_markdown_v2(recompensa_elegida)}"
            )
            print(aviso)
            await notifier.enviar_mensaje(aviso)
            bruto_manager.subir_nivel(prev_choice_local)
            await refrescar_bruto()
            return True

        # Si no hay elección previa → mensaje detallado
        bruto_info = bruto.get_summary()
        usuario_display_name = escape_markdown_v2(auth.username)
        mensaje_telegram = f"👤 **Usuario:** {usuario_display_name}\n"
        mensaje_telegram += r"🎉 **¡Subida de Nivel\!** 🎉" + "\n"

        for key, value in bruto_info.items():
            if key == "ID":
                continue
            if key == "Name":
                mensaje_telegram += f"**Nombre**: {escape_markdown_v2(str(value))}\n"
            elif key == "Level":
                mensaje_telegram += f"**Nivel**: {value}\n"
            elif key == "XP":
                mensaje_telegram += f"**XP**: {value}\n"
            elif key == "HP":
                mensaje_telegram += f"**HP**: {value}\n"
            elif key == "Endurance":
                mensaje_telegram += f"🛡️ Resistencia: {value}\n"
            elif key == "Strength":
                mensaje_telegram += f"💪 Fuerza: {value}\n"
            elif key == "Agility":
                mensaje_telegram += f"🏃 Agilidad: {value}\n"
            elif key == "Speed":
                mensaje_telegram += f"💨 Velocidad: {value}\n"
            elif key == "Ranking":
                mensaje_telegram += f"🏆 Ranking: {value}\n"
            elif key == "Gender":
                mensaje_telegram += f"Género: {escape_markdown_v2(str(value)).capitalize()}\n"
            elif key == "Clan":
                mensaje_telegram += f"Clan: {escape_markdown_v2(value) if value else 'Ninguno'}\n"
            elif key == "Victories":
                mensaje_telegram += f"✅ Victorias: {value}\n"
            elif key == "Losses":
                mensaje_telegram += f"❌ Derrotas: {value}\n"
            elif key == "Last Fight":
                mensaje_telegram += f"📅 Última Lucha: {escape_markdown_v2(value.split('T')[0]) if value else 'N/A'}\n"
            elif key == "Fights Left":
                mensaje_telegram += f"⏳ Combates Restantes: {value}\n"
            elif key == "Tournament Date":
                mensaje_telegram += f"🗓️ Fecha Torneo: {escape_markdown_v2(value.split('T')[0]) if value else 'No registrado'}\n"
            elif key == "Weapons":
                safe_weapons = [escape_markdown_v2(w) for w in value] if value else []
                mensaje_telegram += f"⚔️ Armas: {', '.join(safe_weapons) if safe_weapons else 'Ninguna'}\n"
            elif key == "Skills":
                safe_skills = [escape_markdown_v2(s) for s in value] if value else []
                mensaje_telegram += f"✨ Habilidades: {', '.join(safe_skills) if safe_skills else 'Ninguna'}\n"

        mensaje_telegram += "🎁 **Recompensas disponibles:**\n"
        mensaje_telegram += f"* **Opción 1:** {escape_markdown_v2(izquierda_local)}\n"
        mensaje_telegram += f"* **Opción 2:** {escape_markdown_v2(derecha_local)}\n"

        print(mensaje_telegram)
        recompensa = bruto_manager.elegir_recompensa(izquierda_local, derecha_local, subir_nivel_data)
        print(f"Recompensa final: {recompensa}")

        if recompensa == "Hay que revisar a mano":
            await notifier.enviar_mensaje(mensaje_telegram)
            return None  # ⬅ señal para parar todo

        direction = "LEFT" if recompensa == izquierda_local else "RIGHT"
        bruto_manager.subir_nivel(direction)
        await refrescar_bruto()
        return True

    # Registrar al torneo si aplica
    if not bruto.registeredForTournament and torneo == "True":
        random_sleep()
        bruto_manager.register_to_tournament()
    if bruto.canRankUpSince is not None:
        await notifier.enviar_mensaje("Puedes subir de rango para: "+bruto.name)

    # Subida inicial
    resolver_subida = await resolver_subida_nivel()
    if resolver_subida is None:  # revisión manual
        return
    if resolver_subida:
        await refrescar_bruto()

    # Fase de combates
    combates = 8 if "regeneration" in bruto.skills else 6
    contador_error = 0
    for i in range(combates):
        random_sleep()
        opponents = bruto_manager.get_opponents(bruto_name)
        oponente = opponents[0]["name"]
        print(f"El oponente es: {oponente}")
        random_sleep()
        respuesta_lucha = bruto_manager.fight(bruto.name, oponente)
        print(respuesta_lucha)

        if contador_error == 1:
            contador_error = 0
            break

        if respuesta_lucha == 500:
            subio = await resolver_subida_nivel()
            if subio is None:  # revisión manual
                return
            if subio:
                contador_error = 0
                continue
            else:
                contador_error += 1
        else:
            fights_left = respuesta_lucha.get('fightsLeft', 'No disponible')
            victories = respuesta_lucha.get('victories', 'No disponible')
            derrotas = respuesta_lucha.get('losses', 'No disponible')

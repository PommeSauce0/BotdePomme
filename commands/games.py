import asyncio
import random
from discord.ext import commands


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Les commandes de jeux sont connectées.")

    # Jeu du pendu
    @commands.command(name='pendu', help='Jouer au pendu')
    async def pendu(self, ctx):
        # Liste de mots pour le pendu
        # mots = ['chat', 'chien', 'voiture', 'ordinateur', 'maison']
        liste_mot = open("./config/liste_pendu.txt", "r")
        mots = liste_mot.read().split(',')
        # print(mots)
        mot_a_deviner = random.choice(mots)
        lettres_trouvees = []
        nombre_de_coups = 0
        max_coups = 6
        mot_masque = '-' * len(mot_a_deviner)
        await ctx.send("Bienvenue au jeu du pendu ! Devine le mot en entrant une lettre à la fois.")
        await ctx.send(f"Mot à deviner : {mot_masque}")

        while nombre_de_coups < max_coups:
            lettre = (await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)).content
            if lettre == mot_a_deviner:
                await ctx.send(f"Bien joué, le mot à trouvé était bien {mot_a_deviner}")
                return
            else:
                if lettre in lettres_trouvees:
                    await ctx.send("Vous avez déjà trouvé cette lettre.")
                elif lettre in mot_a_deviner:
                    lettres_trouvees.append(lettre)
                    mot_masque = ''.join([lettre if lettre in lettres_trouvees else '-' for lettre in mot_a_deviner])
                    await ctx.send(f"Bravo ! La lettre {lettre} est dans le mot. Mot à deviner : {mot_masque}")
                    if '-' not in mot_masque:
                        await ctx.send(
                            f"Félicitations ! Vous avez deviné le mot {mot_a_deviner} en {nombre_de_coups + 1} coups.")
                        return
                else:
                    nombre_de_coups += 1
                    await ctx.send(
                        f"Désolé, la lettre {lettre} n'est pas dans le mot. Il vous reste {max_coups - nombre_de_coups} coups.")
                    if nombre_de_coups == max_coups:
                        await ctx.send(f"Désolé, vous avez épuisé tous vos coups. Le mot était {mot_a_deviner}.")

    @commands.command(name='pof', help='Pile ou Face quoi')
    async def pof(self, ctx):
        cpof = ["face", "pile", "La pièce n'est pas tomber... Tu me dois 2€"]
        await ctx.send("*Jette la pièce en l'air*")
        await asyncio.sleep(3)
        await ctx.send("*Bruit d'une pièce qui tourne*")
        await asyncio.sleep(2)
        dpof = random.choice(cpof)
        if not dpof == "La pièce n'est pas tomber... Tu me dois 2€":
            await ctx.send("C'est {}".format(dpof))
        else:
            await ctx.send(dpof)


async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))

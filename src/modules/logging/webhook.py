from discord_webhook import DiscordEmbed

def webhook(webhook, title, desc, time, color, imagePath = None):
    if title:
        embed = DiscordEmbed(title="[{}] {}".format(time,title), description=desc, color=color)
    else:
        embed = DiscordEmbed(title="", description="[{}] {}".format(time,desc), color=color)
    #if to add image
    if imagePath:
        with open(imagePath, "rb") as f:
            webhook.add_file(file=f.read(), filename= "screenshot.png")
        f.close()
        embed.set_image(url='attachment://screenshot.png')
    # add embed object to webhook
    webhook.add_embed(embed)

    response = webhook.execute()
    
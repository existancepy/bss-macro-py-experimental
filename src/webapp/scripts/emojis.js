/*
=============================================
Emoji list
=============================================
*/


//utility function to convert them to an array
function toEmojiArray(emojiObj){
    out = []
    for (const [k,v] of Object.entries(emojiObj)) {
        out.push(`${v} ${toTitleCase(k.replaceAll("_"," "))}`)
    }
    return out
}
//https://emojidb.org/
const fieldEmojis = {
    sunflower: "🌻",
    dandelion: "🌼",
    mushroom: "🍄",
    blue_flower: "🔷",
    clover: "🍀",
    strawberry: "🍓",
    spider: "🕸️",
    bamboo: "🐼",
    pineapple: "🍍",
    stump: "🐌",
    cactus: "🌵",
    pumpkin: "🎃",
    pine_tree: "🌲",
    rose: "🌹",
    mountain_top: "⛰️",
    pepper: "🌶️",
    coconut: "🥥"
}